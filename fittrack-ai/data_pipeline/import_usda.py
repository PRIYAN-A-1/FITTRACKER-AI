"""Convert official USDA SR Legacy CSV ZIP to provenance-preserving 100g JSONL."""
import argparse,csv,io,json,zipfile,hashlib,datetime
from pathlib import Path
NUTRIENTS={"1008":"calories","1003":"protein","1005":"carbs","1004":"fat","1079":"fiber"}
def convert(source,target):
    source=Path(source);target=Path(target);foods={}
    with zipfile.ZipFile(source) as z:
        def rows(name):
            matches=[n for n in z.namelist() if n.rsplit("/",1)[-1]==name]
            if len(matches)!=1: raise ValueError("missing/ambiguous "+name)
            return csv.DictReader(io.TextIOWrapper(z.open(matches[0]),encoding="utf-8-sig"))
        for row in rows("food.csv"):
            fid=row["fdc_id"]
            foods[fid]={"id":"usda:"+fid,"name":row["description"],"brand":"","basis":"100g",**{k:None for k in NUTRIENTS.values()},"source":"USDA FoodData Central SR Legacy","source_url":"https://fdc.nal.usda.gov/food-details/"+fid+"/nutrients","license":"CC0-1.0","verification":"source_published","source_version":"SR Legacy 2018-04"}
        for row in rows("food_nutrient.csv"):
            food=foods.get(row["fdc_id"]);key=NUTRIENTS.get(row["nutrient_id"])
            if food is not None and key and row.get("amount"):
                value=float(row["amount"])
                if not 0<=value<=(1000 if key=="calories" else 100): raise ValueError("invalid nutrient")
                food[key]=value
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("".join(json.dumps(v,ensure_ascii=False)+"\n" for v in foods.values()),encoding="utf-8")
    report={"source":"USDA FoodData Central","source_archive":source.name,"archive_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"license":"CC0-1.0","records":len(foods),"training_images":0,"imported_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"note":"Source publication is not independent clinical verification. Regional Indian coverage is incomplete."}
    target.with_suffix(".report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("archive");p.add_argument("--output",default="data/catalog.jsonl");a=p.parse_args();convert(a.archive,a.output)
