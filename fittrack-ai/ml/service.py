"""Private image inference endpoint; never invents predictions when weights are absent."""
import io,json,os,hmac,hashlib,threading,time,warnings
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from PIL import Image,ImageOps
MAX_BYTES=8*1024*1024
Image.MAX_IMAGE_PIXELS=20_000_000

def decode_image(data):
    if not data or len(data)>MAX_BYTES:raise ValueError('image must be 1 byte to 8MiB')
    with warnings.catch_warnings():
        warnings.simplefilter('error',Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(data)) as image:
            if image.format not in ('JPEG','PNG') or image.width*image.height>20_000_000:raise ValueError('unsupported format or image dimensions')
            image.load();return ImageOps.exif_transpose(image).convert('RGB')

class Runtime:
    def __init__(self,path):
        self.model=None;self.metadata=None
        directory=Path(path)
        if (directory/'model.onnx').is_file():
            from ml.food101 import Food101
            self.baseline=Food101(directory);self.model=self.baseline.model;self.metadata={'model_version':'food101-swin-q4-e5e50bf'};return
        if not (directory/'metadata.json').is_file() or not (directory/'weights.pt').is_file():return
        metadata=json.loads((directory/'metadata.json').read_text())
        if metadata.get('serving_approved') is not True:return
        if metadata.get('architecture')!='mobilenet_v3_small' or not metadata.get('labels'):raise ValueError('incompatible metadata')
        if hashlib.sha256((directory/'weights.pt').read_bytes()).hexdigest()!=metadata.get('weights_sha256'):raise ValueError('weights checksum mismatch')
        import torch
        from torchvision import models,transforms
        self.torch=torch;self.model=models.mobilenet_v3_small(weights=None);self.model.classifier[-1]=torch.nn.Linear(self.model.classifier[-1].in_features,len(metadata['labels']));self.model.load_state_dict(torch.load(directory/'weights.pt',map_location='cpu',weights_only=True));self.model.eval();self.metadata=metadata
        self.transform=transforms.Compose([transforms.Resize(256),transforms.CenterCrop(224),transforms.ToTensor(),transforms.Normalize([.485,.456,.406],[.229,.224,.225])])
    def infer(self,image):
        if self.model is None:return None
        if hasattr(self,'baseline'):return self.baseline.infer(image)
        start=time.monotonic()
        with self.torch.inference_mode():scores=self.model(self.transform(image).unsqueeze(0)).softmax(1)[0].tolist()
        ranked=sorted(range(len(scores)),key=lambda i:scores[i],reverse=True)[:5]
        return {'modelVersion':self.metadata['model_version'],'candidates':[{'label':self.metadata['labels'][i],'score':scores[i]} for i in ranked],'processingMs':round((time.monotonic()-start)*1000),'portionMethod':'user-entered grams','scoreMeaning':'uncalibrated classifier score; not proof that image is in scope'}

def server(host,port,token,runtime):
    if len(token)<32:raise ValueError('MODEL_SERVICE_TOKEN needs at least 32 characters')
    lock=threading.BoundedSemaphore(1)
    class Handler(BaseHTTPRequestHandler):
        def setup(self):super().setup();self.connection.settimeout(15)
        def log_message(self,*args):pass
        def send_json(self,status,data):
            raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def authorized(self):return hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+token)
        def do_GET(self):
            if not self.authorized():return self.send_json(401,{'detail':'Unauthorized'})
            if self.path!='/health':return self.send_json(404,{'detail':'Not found'})
            self.send_json(200,{'ready':runtime.model is not None})
        def do_POST(self):
            if not self.authorized():return self.send_json(401,{'detail':'Unauthorized'})
            if self.path!='/v1/analyze':return self.send_json(404,{'detail':'Not found'})
            try:size=int(self.headers.get('Content-Length','0'))
            except ValueError:return self.send_json(400,{'detail':'Invalid length'})
            if size<=0 or size>MAX_BYTES:return self.send_json(413,{'detail':'Image size out of range'})
            if not lock.acquire(blocking=False):return self.send_json(429,{'detail':'Inference busy'})
            try:
                image=decode_image(self.rfile.read(size));result=runtime.infer(image)
                if result is None:return self.send_json(503,{'detail':'No approved trained model installed. Use manual logging.'})
                self.send_json(200,result)
            except (ValueError,OSError,Image.DecompressionBombError,Image.DecompressionBombWarning):self.send_json(400,{'detail':'Invalid image'})
            except Exception:self.send_json(503,{'detail':'Inference failed. Use manual logging.'})
            finally:lock.release()
    return ThreadingHTTPServer((host,port),Handler)
if __name__=='__main__':
    runtime=Runtime(os.getenv('MODEL_DIR','ml/models/food101'));http=server(os.getenv('MODEL_HOST','127.0.0.1'),int(os.getenv('MODEL_PORT','8090')),os.environ.get('MODEL_SERVICE_TOKEN',''),runtime);http.serve_forever()
