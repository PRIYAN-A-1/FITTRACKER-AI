"""Traceable, resumable OFF catalog collector. No third-party dependencies."""
import argparse, datetime, hashlib, json, math, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
FIELDS="code,product_name,brands,nutriments,nutrition_data_per,quantity,last_modified_t,categories_tags"
KEYS={"calories":"energy-kcal", "protein":"proteins", "carbs":"carbohydrates", "fat":"fat", "fiber":"fiber"}
def normalize(p):
    code=str(p.get("code", "")); name=p.get("product_name", "").strip()
    if not code.isdigit() or not name: raise ValueError("missing barcode or name")
    # OFF suffix is per 100 g OR per 100 ml. Liquids require density and must not enter a grams-only catalog.
    quantity=str(p.get("quantity", "")).lower()
    if any(x in quantity for x in ("ml", "cl", "litre", "liter")) or quantity.endswith(" l"):
        raise ValueError("liquid requires density or volume support")
    tags=p.get("categories_tags", [])
    if any(t in tags for t in ("en:beverages", "en:milks", "en:oils", "en:sauces")):
        raise ValueError("ambiguous volume basis")
    n=p.get("nutriments", {}); out={}
    for k,v in KEYS.items():
        value=n.get(v+"_100g")
        if value is None: out[k]=None; continue
        if isinstance(value,bool): raise ValueError("boolean nutrient")
        value=float(value)
        if not math.isfinite(value) or value<0 or value>(1000 if k=="calories" else 100):
            raise ValueError("invalid nutrient range")
        out[k]=value
    if all(v is None for v in out.values()): raise ValueError("no measured nutrients")
    return {"id":"off:"+code,"name":name,"brand":p.get("brands", ""),"basis":"100g",
        **out,"source":"Open Food Facts","source_url":"https://world.openfoodfacts.org/product/"+code,
        "license":"ODbL-1.0","verification":"community_unverified","source_version":str(p.get("last_modified_t", "unknown"))}
def fetch(url,agent):
    for attempt in range(4):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":agent,"Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=45) as response:
                raw=response.read(10_000_001)
                if len(raw)>10_000_000: raise ValueError("response exceeds 10MB")
                return raw
        except urllib.error.HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt==3: raise
            time.sleep(min(60,max(7,int(e.headers.get("Retry-After",7)))))
        except urllib.error.URLError:
            if attempt==3: raise
            time.sleep(7*(attempt+1))
def run(root,pages,agent,country,query="",legacy=False):
    root=Path(root); rawdir=root/"raw";rawdir.mkdir(parents=True,exist_ok=True)
    foods={}; rejected=[]; errors=[]; evidence=[]
    for page in range(1,pages+1):
        scope=hashlib.sha256((country+query+str(legacy)).encode()).hexdigest()[:12]
        cache=rawdir/f"off-{scope}-{page}.json"
        params=urllib.parse.urlencode({"countries_tags_en":country,"page":page,"page_size":100,"fields":FIELDS})
        url="https://world.openfoodfacts.org/api/v2/search?"+params
        if legacy:
            params=urllib.parse.urlencode({"action":"process","json":1,"search_simple":1,"search_terms":query,"tagtype_0":"countries","tag_contains_0":"contains","tag_0":country,"page":page,"page_size":100,"fields":FIELDS})
            url="https://world.openfoodfacts.org/cgi/search.pl?"+params
        try:
            if cache.exists(): raw=cache.read_bytes()
            else:
                raw=fetch(url,agent); json.loads(raw)
                tmp=cache.with_suffix(".tmp");tmp.write_bytes(raw);tmp.replace(cache)
                time.sleep(7)
            payload=json.loads(raw)
            if "products" not in payload: raise ValueError("missing products array")
            evidence.append({"file":cache.name,"url":url,"sha256":hashlib.sha256(raw).hexdigest()})
            for product in payload["products"]:
                try:
                    item=normalize(product);foods[item["id"]]=item
                except (ValueError,TypeError) as e: rejected.append({"id":product.get("code"),"reason":str(e)})
            if not payload["products"]: break
        except Exception as e:
            errors.append({"page":page,"error":type(e).__name__,"detail":str(e)});break
    target=root/"catalog.jsonl"
    # Do not erase an earlier good catalog on a failed run. Rebuild from all cached pages on each run.
    if foods:
        tmp=target.with_suffix(".tmp");tmp.write_text("".join(json.dumps(v,ensure_ascii=False)+"\n" for v in foods.values()));tmp.replace(target)
    report={"collected_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"accepted_unique":len(foods),"rejected":len(rejected),"errors":errors,"evidence":evidence,"training_images":0}
    (root/"collection-report.json").write_text(json.dumps(report,indent=2))
    (root/"rejections.json").write_text(json.dumps(rejected,indent=2))
    print(json.dumps(report,indent=2));return 1 if errors else 0
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",default="data");p.add_argument("--pages",type=int,default=10);p.add_argument("--country",default="india");p.add_argument("--user-agent",required=True,help="App/version (contact URL or email)")
    p.add_argument("--query",default="");p.add_argument("--legacy",action="store_true");a=p.parse_args()
    if not 1<=a.pages<=10000:p.error("pages must be 1..10000")
    raise SystemExit(run(a.output,a.pages,a.user_agent,a.country,a.query,a.legacy))
