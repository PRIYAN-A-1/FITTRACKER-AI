"""Actual CPU ONNX inference for the published Food-101 baseline, with user review mandatory."""
import hashlib,json,time,math
from pathlib import Path
import numpy as np
from PIL import Image
class Food101:
 def __init__(self,root):
  from .download_baseline import MODEL_SHA256
  import onnxruntime as ort
  root=Path(root)
  if hashlib.sha256((root/'model.onnx').read_bytes()).hexdigest()!=MODEL_SHA256:raise ValueError('Model checksum mismatch')
  config=json.loads((root/'config.json').read_text());processor=json.loads((root/'preprocessor_config.json').read_text());self.labels=config['id2label'];self.mean=np.array(processor['image_mean'],dtype=np.float32);self.std=np.array(processor['image_std'],dtype=np.float32)
  size=processor['size'];self.size=(size['width'],size['height']);options=ort.SessionOptions();options.intra_op_num_threads=2
  self.model=ort.InferenceSession(str(root/'model.onnx'),sess_options=options,providers=['CPUExecutionProvider']);self.input=self.model.get_inputs()[0].name
 def infer(self,image):
  start=time.monotonic();array=np.asarray(image.resize(self.size,Image.Resampling.BICUBIC).convert('RGB'),dtype=np.float32)/255.0;array=((array-self.mean)/self.std).transpose(2,0,1)[None,...]
  logits=self.model.run(None,{self.input:array})[0][0];prob=np.exp(logits-np.max(logits));prob=prob/np.sum(prob);ranked=np.argsort(prob)[::-1][:5];entropy=float(-np.sum(prob*np.log(np.maximum(prob,1e-12))))
  uncertain=float(prob[ranked[0]])<.4 or entropy>3.0
  return {'modelVersion':'food101-swin-q4-e5e50bf','modelKind':'pretrained-baseline','candidates':[] if uncertain else [{'label':self.labels[str(int(i))],'score':float(prob[i])} for i in ranked], 'unknown':uncertain,'processingMs':round((time.monotonic()-start)*1000),'portionMethod':'user-entered measured grams','scoreMeaning':'Suggestions require review. Scores are not calibrated confidence; portions and hidden ingredients are not inferred.','coverage':'Food-101 classes; broad Indian meal recognition is not established.'}
