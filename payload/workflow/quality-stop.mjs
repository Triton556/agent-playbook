import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {inspect} from './agent-worklog.mjs';
const safe=v=>typeof v==='string'&&/^[a-zA-Z0-9:._-]{1,128}$/.test(v);
function checkPath(p){for(let q=p;;q=path.dirname(q)){if(fs.existsSync(q)&&fs.lstatSync(q).isSymbolicLink())throw new Error('Linked diagnostic path');if(path.dirname(q)===q)break}}
export function diagnose(payload){
 if(payload?.hook_event_name!=='Stop'||!safe(payload.session_id)||typeof payload.cwd!=='string')return {};
 const root=fs.realpathSync(payload.cwd),d=path.join(root,'.workflow');checkPath(d);if(!fs.existsSync(d))return {};
 const active=path.join(d,'active-'+encodeURIComponent(payload.session_id)+'.json');checkPath(active);if(!fs.existsSync(active))return {};
 const pointer=JSON.parse(fs.readFileSync(active,'utf8'));if(pointer.session_id!==payload.session_id||!safe(pointer.task_id))return {};
 const result=inspect(root,pointer.task_id);if(!result.found||result.legacy||result.session_id!==payload.session_id||result.ready_to_complete||['paused','cancelled'].includes(result.status))return {};
 const cache=path.join(d,'quality-warning-'+encodeURIComponent(payload.session_id)+'.json');checkPath(cache);
 const fingerprint=crypto.createHash('sha256').update(JSON.stringify({task:result.task_id,reasons:result.reasons})).digest('hex');
 if(fs.existsSync(cache)){const previous=JSON.parse(fs.readFileSync(cache,'utf8'));if(previous.fingerprint===fingerprint)return {}}
 const tmp=cache+'.'+crypto.randomUUID()+'.tmp';try{fs.writeFileSync(tmp,JSON.stringify({schema_version:1,fingerprint,task_id:result.task_id})+'\n');fs.renameSync(tmp,cache)}finally{if(fs.existsSync(tmp))fs.unlinkSync(tmp)}
 return {systemMessage:'Workflow '+result.task_id+': '+result.reasons.slice(0,4).join('; ')+'. Diagnostic only: ordinary authorized work continues; a real blocker remains explicit.'};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 let input='';try{for await(const c of process.stdin){input+=c;if(input.length>256*1024)throw new Error('Diagnostic input too large')}process.stdout.write(JSON.stringify(diagnose(JSON.parse(input.replace(/^\uFEFF/,''))))+'\n')}
 catch{process.stdout.write(JSON.stringify({systemMessage:'Workflow diagnostic unavailable; use the ordinary task-state/ledger check. This hook does not block or restart work.'})+'\n')}
}
