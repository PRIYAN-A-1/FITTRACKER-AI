"""Disposable local PostgreSQL API regression suite. No synthetic records enter the shipped catalog."""
import os,json,urllib.request,urllib.error,uuid,time,io
from PIL import Image
from pathlib import Path
BASE=os.getenv('TEST_API_URL','http://localhost:8080')
if not BASE.startswith(('http://localhost:','http://127.0.0.1:')):raise SystemExit('Use a disposable loopback API')
http=urllib.request.build_opener(urllib.request.ProxyHandler({}))
checks=0
def passed(name):
 global checks
 checks+=1;print('PASS:',name,flush=True)
def call(path,method='GET',body=None,token=None,expect=200,raw=None,content_type='application/json'):
 headers={'Content-Type':content_type}
 if token:headers['Authorization']='Bearer '+token
 data=raw if raw is not None else (None if body is None else json.dumps(body).encode())
 req=urllib.request.Request(BASE+path,data=data,headers=headers,method=method)
 try:
  with http.open(req,timeout=30) as r:status=r.status;payload=r.read()
 except urllib.error.HTTPError as e:status=e.code;payload=e.read()
 assert status==expect,(path,status,payload[:300]);return json.loads(payload) if payload else None
accounts=[]
try:
 for _ in range(2):accounts.append(call('/api/v1/auth/register','POST',{'email':str(uuid.uuid4())+'@example.test','password':'Integration-test-password','displayName':'Integration test'},expect=201))
 a,b=accounts;token=a['accessToken'];foods=call('/api/v1/food/search?q=rice',token=token)['items'];assert foods,'Catalog not ready';food=foods[0];passed('real catalog imported and searchable')
 body={'foodId':food['id'],'grams':150,'mealType':'breakfast','eatenAt':'2026-10-13T20:00:00.123456789Z','idempotencyKey':str(uuid.uuid4()),'confirmed':True}
 meal=call('/api/v1/meals','POST',body,token,201);retry=call('/api/v1/meals','POST',body,token,201);assert meal['id']==retry['id'];passed('nanosecond timestamp and duplicate replay')
 call('/api/v1/meals','POST',{**body,'grams':151},token,409);passed('conflicting request key rejected')
 call('/api/v1/meals/'+meal['id'],token=b['accessToken'],expect=404);call('/api/v1/meals/'+meal['id'],'DELETE',token=b['accessToken'],expect=404);passed('foreign user cannot read or delete meals')
 diary=call('/api/v1/meals/daily?date=2026-10-14&zone=Asia%2FKolkata',token=token);assert any(x['id']==meal['id'] for x in diary['items']);passed('local midnight diary grouping')
 edit={**body,'grams':200,'version':meal['version']};call('/api/v1/meals/'+meal['id'],'PATCH',edit,token);edited=call('/api/v1/meals/'+meal['id'],token=token);assert float(edited['grams'])==200;passed('versioned meal edit')
 call('/api/v1/meals/'+meal['id'],'PATCH',edit,token,409);passed('stale edit rejected')
 replay=call('/api/v1/meals','POST',body,token,201);assert replay['id']==meal['id'];assert float(call('/api/v1/meals/'+meal['id'],token=token)['grams'])==200;passed('creation retry does not undo a later edit')
 call('/api/v1/meals/daily?date=2026-10-13&zone=invalid-zone',token=token,expect=400);passed('invalid timezone yields 400')
 call('/api/v1/users/me','PATCH',{'displayName':'Updated test','timeZone':'Asia/Kolkata'},token);assert call('/api/v1/users/me',token=token)['display_name']=='Updated test';passed('profile update persists')
 goals={'calories':2100,'protein':None,'carbs':250,'fat':60};call('/api/v1/nutrition/goals','PUT',goals,token);assert call('/api/v1/nutrition/goals',token=token)['protein'] is None;passed('goals preserve unknown values')
 assert call('/api/v1/nutrition/goals',token=b['accessToken'])['calories'] is None;passed('goals are owner scoped')
 report=call('/api/v1/reports/weekly?start=2026-10-13&zone=Asia%2FKolkata',token=token);assert len(report['days'])==7;passed('seven-day report')
 recipe=call('/api/v1/recipes/calculate','POST',{'ingredients':[{'foodId':food['id'],'grams':100}],'servings':2},token);assert abs(float(recipe['perServing']['calories'])-float(food['calories'])/2)<1e-8;passed('recipe calculation uses source data')
 stream=io.BytesIO();Image.new('RGB',(10,10),'red').save(stream,format='PNG');boundary='FitTrackTestBoundary';raw=b'--'+boundary.encode()+b'\r\nContent-Disposition: form-data; name="image"; filename="test.png"\r\nContent-Type: image/png\r\n\r\n'+stream.getvalue()+b'\r\n--'+boundary.encode()+b'--\r\n'
 vision_ready=os.getenv('EXPECT_VISION_READY','1')=='1'
 result=call('/api/v1/food/analyze','POST',token=token,expect=200 if vision_ready else 503,raw=raw,content_type='multipart/form-data; boundary='+boundary)
 if vision_ready:
  assert result['unknown'] is True;passed('blank image is rejected as uncertain by real pretrained baseline')
  pizza=(Path(__file__).resolve().parents[1]/'tests/fixtures/supreme-pizza.jpg').read_bytes();pizza_request=raw.replace(stream.getvalue(),pizza)
  predictions=call('/api/v1/food/analyze','POST',token=token,raw=pizza_request,content_type='multipart/form-data; boundary='+boundary);assert predictions['candidates'][0]['label']=='pizza';passed('actual food photo recognized through Java and private ONNX service')
 else:passed('missing approved model is explicit')
 invalid=raw.replace(stream.getvalue(),b'invalid-image');call('/api/v1/food/analyze','POST',token=token,expect=400,raw=invalid,content_type='multipart/form-data; boundary='+boundary);passed('corrupt image rejected')
 exported=call('/api/v1/users/me/export',token=token);assert exported['goals'] and exported['requestHistory'];passed('export includes stored goals and replay history')
 call('/api/v1/meals/'+meal['id'],'DELETE',token=token,expect=204);call('/api/v1/meals/'+meal['id'],token=token,expect=404);call('/api/v1/meals','POST',body,token,410);passed('delete clears replay data and prevents resurrection')
finally:
 for a in accounts:
  try:call('/api/v1/users/me','DELETE',token=a['accessToken'],expect=204)
  except Exception as e:print('Cleanup needed:',type(e).__name__)
print('TOTAL PASSED:',checks)
