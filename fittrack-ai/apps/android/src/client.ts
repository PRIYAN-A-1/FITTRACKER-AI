export type Session={accessToken:string;refreshToken:string;userId:string};
export class ApiError extends Error {constructor(public status:number,message:string){super(message);this.name='ApiError';}get retryable(){return this.status===0||this.status===429||this.status>=500;}}
type Store={read():Promise<string|null>;write(value:string|null):Promise<void>};
export function createClient(base:string,storage:Store,fetcher:typeof fetch=fetch,timeoutMs=20000){
 let current:Session|null=null,epoch=0;let refreshFlight:Promise<void>|null=null;let writes=Promise.resolve();
 function valid(s:unknown):s is Session{return !!s&&typeof s==='object'&&['accessToken','refreshToken','userId'].every(k=>typeof (s as Record<string,unknown>)[k]==='string');}
 async function setSession(s:Session|null){if(s!==null&&!valid(s))throw new Error('Invalid session response');const old=current;const generation=++epoch;current=s;const serialized=s?JSON.stringify(s):null;const task=writes.catch(()=>{}).then(()=>storage.write(serialized));writes=task;try{await task;}catch(e){if(epoch===generation){current=old;epoch++;}throw e;}}
 async function restore(){const raw=await storage.read();if(!raw)return null;try{const s:unknown=JSON.parse(raw);if(!valid(s))throw new Error('Corrupt session');current=s;epoch++;return current;}catch{await setSession(null);return null;}}
 async function send(path:string,method:string,body:unknown,token?:string){const abort=new AbortController();const timer=setTimeout(()=>abort.abort(),timeoutMs);try{const multipart=typeof FormData!=='undefined'&&body instanceof FormData;const response=await fetcher(base+path,{method,headers:{...(multipart?{}:{'Content-Type':'application/json'}),...(token?{Authorization:`Bearer ${token}`}:{})},body:body===undefined?undefined:multipart?body as FormData:JSON.stringify(body),signal:abort.signal});const text=await response.text();let data:any;try{data=text?JSON.parse(text):undefined;}catch{data=undefined;}return {status:response.status,ok:response.ok,data};}catch(e){throw new ApiError(0,e instanceof Error&&e.name==='AbortError'?'Connection timed out. Your drafts are safe.':'Cannot reach server. Check your connection.');}finally{clearTimeout(timer);}}
 async function api<T=any>(path:string,method='GET',body?:unknown):Promise<T>{
  const starting=current,startingEpoch=epoch;let result=await send(path,method,body,starting?.accessToken);
  const authOnly=['/api/v1/auth/login','/api/v1/auth/register','/api/v1/auth/refresh'].includes(path);
  if(starting&&current?.userId!==starting.userId)throw new ApiError(409,'Account changed; request stopped');
  if(result.status===401&&starting&&!authOnly){
   if(current?.accessToken===starting.accessToken){
    if(!refreshFlight){const refreshSession=current;const refreshEpoch=epoch;
     const flight=(async()=>{const r=await send('/api/v1/auth/refresh','POST',{refreshToken:refreshSession!.refreshToken});if(epoch!==refreshEpoch)throw new ApiError(409,'Session changed during refresh');if(!r.ok){if(r.status===401||r.status===400)await setSession(null);throw new ApiError(r.status,r.status>=500?'Session service temporarily unavailable. Try again.':'Session expired. Sign in again.');}await setSession(r.data);})();
     refreshFlight=flight;void flight.finally(()=>{if(refreshFlight===flight)refreshFlight=null;}).catch(()=>{});
    }
    await refreshFlight;
   }
   if(current?.userId!==starting.userId)throw new ApiError(401,'Sign in again');
   result=await send(path,method,body,current?.accessToken);
  }
  if(starting&&current?.userId!==starting.userId)throw new ApiError(409,'Account changed; response ignored');
  if(!result.ok)throw new ApiError(result.status,result.data?.detail??`Request failed (${result.status})`);
  if(!starting&&startingEpoch!==epoch&&authOnly)throw new ApiError(409,'Session changed; retry sign-in');
  return result.data as T;
 }
 return {api,restore,setSession,owner:()=>current?.userId??null};
}
