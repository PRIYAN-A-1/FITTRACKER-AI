"""MobileNet V3 small baseline. Requires approved manifest and local images; never creates fake labels."""
import argparse,json,random,hashlib
from pathlib import Path
import numpy as np
import torch
from PIL import Image,ImageOps
from torchvision import models,transforms
from torch.utils.data import Dataset,DataLoader
class Foods(Dataset):
    def __init__(self,rows,root,labels,training):
        self.rows=rows;self.root=Path(root).resolve();self.labels=labels
        self.transform=transforms.Compose(([transforms.RandomResizedCrop(224),transforms.RandomHorizontalFlip()] if training else [transforms.Resize(256),transforms.CenterCrop(224)])+[transforms.ToTensor(),transforms.Normalize([.485,.456,.406],[.229,.224,.225])])
    def __len__(self):return len(self.rows)
    def __getitem__(self,i):
        row=self.rows[i];path=(self.root/row['path']).resolve()
        if not path.is_relative_to(self.root):raise ValueError('path outside dataset')
        with Image.open(path) as im:image=self.transform(ImageOps.exif_transpose(im).convert('RGB'))
        return image,self.labels.index(row['label'])
def main(a):
    random.seed(a.seed);np.random.seed(a.seed);torch.manual_seed(a.seed)
    rows=[json.loads(line) for line in Path(a.manifest).read_text().splitlines()];labels=sorted({r['label'] for r in rows})
    for label in labels:
        for split in ['train','val','test']:
            if not any(r['label']==label and r['split']==split for r in rows):raise ValueError(f'{label} missing {split} images; collect more independent groups')
    device='cuda' if torch.cuda.is_available() else 'cpu'
    net=models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT if a.pretrained else None);net.classifier[-1]=torch.nn.Linear(net.classifier[-1].in_features,len(labels));net.to(device)
    loaders={s:DataLoader(Foods([r for r in rows if r['split']==s],a.root,labels,s=='train'),batch_size=a.batch,shuffle=s=='train',num_workers=0) for s in ['train','val','test']}
    opt=torch.optim.AdamW(net.parameters(),lr=0.0003);criterion=torch.nn.CrossEntropyLoss();best=-1;out=Path(a.output);out.mkdir(parents=True,exist_ok=True);history=[]
    for epoch in range(a.epochs):
        net.train();loss_sum=0
        for images,targets in loaders['train']:
            images,targets=images.to(device),targets.to(device);opt.zero_grad();loss=criterion(net(images),targets);loss.backward();opt.step();loss_sum+=loss.item()*len(targets)
        net.eval();correct=0;count=0
        with torch.no_grad():
            for images,targets in loaders['val']:
                pred=net(images.to(device)).argmax(1).cpu();correct+=int((pred==targets).sum());count+=len(targets)
        accuracy=correct/count;history.append({'epoch':epoch+1,'train_loss':loss_sum/len(loaders['train'].dataset),'val_accuracy':accuracy})
        if accuracy>best:
            best=accuracy;torch.save(net.state_dict(),out/'weights.pt')
    net.load_state_dict(torch.load(out/'weights.pt',weights_only=True,map_location=device));net.eval();predictions=[]
    with torch.no_grad():
        for images,targets in loaders['test']:
            probabilities=net(images.to(device)).softmax(1).cpu().tolist()
            predictions.extend({'true':int(t),'probabilities':p} for t,p in zip(targets,probabilities))
    metadata={'model_version':a.version,'architecture':'mobilenet_v3_small','labels':labels,'seed':a.seed,'pretrained':a.pretrained,'manifest_sha256':hashlib.sha256(Path(a.manifest).read_bytes()).hexdigest(),'weights_sha256':hashlib.sha256((out/'weights.pt').read_bytes()).hexdigest(),'serving_approved':False,'note':'Requires evaluation and unknown-food validation before serving.'}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2));(out/'history.json').write_text(json.dumps(history,indent=2));(out/'test-predictions.json').write_text(json.dumps(predictions))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--root',required=True);p.add_argument('--output',default='ml/models/baseline');p.add_argument('--version',required=True);p.add_argument('--epochs',type=int,default=10);p.add_argument('--batch',type=int,default=16);p.add_argument('--seed',type=int,default=42);p.add_argument('--pretrained',action='store_true');a=p.parse_args()
    if a.epochs<1 or a.batch<1:p.error('epochs and batch must be positive')
    main(a)
