import * as SecureStore from 'expo-secure-store';
import {createClient} from './client';
export {ApiError} from './client';export type {Session} from './client';
const BASE=(process.env.EXPO_PUBLIC_API_URL??'http://10.0.2.2:8080').replace(/\/$/,'');
if(!__DEV__&&!BASE.startsWith('https://'))throw new Error('Release builds require an HTTPS API');
const client=createClient(BASE,{read:()=>SecureStore.getItemAsync('session'),write:async value=>{if(value===null)await SecureStore.deleteItemAsync('session');else await SecureStore.setItemAsync('session',value);}});
export const {api,restore,setSession,owner}=client;
