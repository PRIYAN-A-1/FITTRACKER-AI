"""Download a pinned Apache-2.0 pretrained Food-101 baseline; this is not FitTrack custom training."""
import argparse,hashlib,json,urllib.request,os
from pathlib import Path
REVISION='e5e50bfc6425aa546f3b4421ca8bd79d0dd610b8'
BASE='https://huggingface.co/onnx-community/swin-finetuned-food101-ONNX/resolve/'+REVISION+'/'
MODEL_SHA256='acfbf2d19eed6c5ede07c8d50c08f53efbaf2808ca74c144c154b6ba50db2881'
def download(output):
 root=Path(output);root.mkdir(parents=True,exist_ok=True)
 for remote,local in [('onnx/model_q4.onnx','model.onnx'),('config.json','config.json'),('preprocessor_config.json','preprocessor_config.json')]:
  target=root/local
  if target.exists() and (local!='model.onnx' or hashlib.sha256(target.read_bytes()).hexdigest()==MODEL_SHA256):continue
  temporary=target.with_suffix('.download')
  try:
   with urllib.request.urlopen(BASE+remote,timeout=180) as src,temporary.open('wb') as dst:
    while chunk:=src.read(1024*1024):dst.write(chunk)
   if local=='model.onnx' and hashlib.sha256(temporary.read_bytes()).hexdigest()!=MODEL_SHA256:raise ValueError('Model checksum mismatch')
   if local.endswith('.json'):json.loads(temporary.read_text())
   os.replace(temporary,target)
  finally:temporary.unlink(missing_ok=True)
 (root/'PROVENANCE.json').write_text(json.dumps({'source':'onnx-community/swin-finetuned-food101-ONNX','revision':REVISION,'license':'Apache-2.0','model_sha256':MODEL_SHA256,'kind':'pretrained Food-101 baseline','custom_fittrack_training':False,'regional_coverage':'Not evaluated. Food-101 does not cover all Indian dishes.'},indent=2))
 print('Pinned pretrained Food-101 baseline ready. Regional custom model remains separate.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',default='ml/models/food101');a=p.parse_args();download(a.output)
