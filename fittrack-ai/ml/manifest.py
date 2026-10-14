"""Validate explicitly licensed, consented local meal images; split leakage groups together."""
import argparse,csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageOps
ALLOWED={"CC0-1.0","CC-BY-4.0","CC-BY-SA-4.0","OWN-CONSENT"}
def validate(manifest,root):
    root=Path(root).resolve();records=[];seen={};groups={};aliases={}
    with open(manifest,newline="",encoding="utf-8") as f:
        for index,row in enumerate(csv.DictReader(f),2):
            if row.get("license") not in ALLOWED:raise ValueError(f"row {index}: verify license")
            if not all(row.get(k) for k in ("path","label","source_url","group_id","consent_reference")):raise ValueError(f"row {index}: missing provenance")
            if row.get("license")=="OWN-CONSENT" and not row['consent_reference'].startswith("consent:"):raise ValueError("explicit training consent reference required")
            path=(root/row['path']).resolve()
            if not path.is_relative_to(root):raise ValueError("image escapes dataset root")
            if path.stat().st_size>8_000_000:raise ValueError("image too large")
            with Image.open(path) as im:
                if im.width*im.height>20_000_000:raise ValueError("pixel limit")
                im.verify()
            with Image.open(path) as im:
                im=ImageOps.exif_transpose(im).convert('RGB')
                digest=hashlib.sha256(im.tobytes()+str(im.size).encode()).hexdigest()
                small_image=im.convert('L').resize((9,8));small=[small_image.getpixel((x,y)) for y in range(8) for x in range(9)];bits=[small[y*9+x]>small[y*9+x+1] for y in range(8) for x in range(8)];phash=sum(int(v)<<i for i,v in enumerate(bits))
            if digest in seen:
                if records[seen[digest]]['label']!=row['label']:raise ValueError("same image has conflicting labels")
                aliases[seen[digest]].add(row['group_id'])
                continue
            seen[digest]=len(records);aliases[len(records)]={row['group_id']};records.append({**row,"sha256":digest,"dhash":phash})
    # Connected components tie both meal sessions and near duplicates together.
    parents=list(range(len(records)))
    def find(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    def union(a,b):parents[find(b)]=find(a)
    for i,a in enumerate(records):
        for group in aliases[i]:
            if group in groups:union(i,groups[group])
            groups[group]=i
        for j in range(i):
            if (a['dhash']^records[j]['dhash']).bit_count()<=4:union(i,j)
    components={}
    for i,row in enumerate(records):components.setdefault(find(i),[]).append(row)
    for members in components.values():
        # Stable for the versioned manifest, not guaranteed stable when its group composition changes.
        key=min(x['sha256'] for x in members);n=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)%100
        split='train' if n<70 else ('val' if n<85 else 'test')
        for row in members:row['split']=split
    return records
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--root',required=True);p.add_argument('--output',default='ml/manifest.jsonl');a=p.parse_args();rows=validate(a.manifest,a.root);Path(a.output).write_text(''.join(json.dumps(r)+'\n' for r in rows));print(json.dumps({'images':len(rows),'splits':{s:sum(r['split']==s for r in rows) for s in ['train','val','test']}}))
