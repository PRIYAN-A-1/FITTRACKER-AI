"""Held-out classification metrics; does not claim these validate portion mass."""
import argparse,json,math
from pathlib import Path
def evaluate(rows,labels):
    k=len(labels);matrix=[[0]*k for _ in labels];correct5=0;bins=[[] for _ in range(10)]
    if not rows or not k:raise ValueError('nonempty held-out test set required')
    for r in rows:
        p=r['probabilities'];truth=r['true']
        if len(p)!=k or not 0<=truth<k or any(not math.isfinite(x) or not 0<=x<=1 for x in p) or abs(sum(p)-1)>1e-4:raise ValueError('invalid probabilities')
        pred=max(range(k),key=lambda j:p[j]);matrix[truth][pred]+=1;correct5+=truth in sorted(range(k),key=lambda j:p[j],reverse=True)[:min(5,k)];bins[min(9,int(p[pred]*10))].append((p[pred],int(pred==truth)))
    per=[]
    for i,name in enumerate(labels):
        tp=matrix[i][i];support=sum(matrix[i]);predicted=sum(row[i] for row in matrix);precision=tp/predicted if predicted else 0;recall=tp/support if support else 0;f1=2*precision*recall/(precision+recall) if precision+recall else 0;per.append({'label':name,'support':support,'precision':precision,'recall':recall,'f1':f1})
    n=len(rows);accuracy=sum(matrix[i][i] for i in range(k))/n;z=1.96;center=(accuracy+z*z/(2*n))/(1+z*z/n);half=z*math.sqrt(accuracy*(1-accuracy)/n+z*z/(4*n*n))/(1+z*z/n)
    ece=sum(abs(sum(x[0] for x in b)/len(b)-sum(x[1] for x in b)/len(b))*len(b)/n for b in bins if b)
    return {'n':n,'top1':accuracy,'top5':correct5/n,'macro_f1':sum(r['f1'] for r in per)/k,'ece_10_bins':ece,'top1_wilson_95':[center-half,center+half],'confusion_matrix':matrix,'per_class':per,'limitations':'Unknown-food detection, latency, regional representativeness, and portion estimation not evaluated.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model_dir');a=p.parse_args();d=Path(a.model_dir);report=evaluate(json.loads((d/'test-predictions.json').read_text()),json.loads((d/'metadata.json').read_text())['labels']);(d/'evaluation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
