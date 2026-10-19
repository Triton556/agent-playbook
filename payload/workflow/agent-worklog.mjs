import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';

const EVENTS=new Set(['task-start','task-done','question','manual-nudge','blocker','reference','interruption','human-feedback']);
const safeId=v=>typeof v==='string'&&/^[a-zA-Z0-9:._-]{1,128}$/.test(v);
const secret=/(?:\b(?:sk-|gh[pousr]_)[a-zA-Z0-9_-]{20,}|\bgithub_pat_[a-zA-Z0-9_]{20,}|-----BEGIN.*PRIVATE KEY-----|\bBearer\s+[a-zA-Z0-9._-]{24,})/i;
const digest=v=>crypto.createHash('sha256').update(v).digest('hex');
const ensure=(ok,msg)=>{if(!ok)throw new Error(msg)};
const words=(v,label,max=2500)=>{ensure(typeof v==='string'&&v.length<=max,'Invalid '+label);return v};
const canonical=v=>Array.isArray(v)?v.map(canonical):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):v;
const stable=v=>JSON.stringify(canonical(v));
const TASK_STATUSES=['in_progress','blocked','ready','complete','paused','cancelled'];
const STAGE_STATUSES=['pending','in_progress','pass','partial','failed','blocked','not_applicable'];

function noLinks(p){for(let q=p;;q=path.dirname(q)){if(fs.existsSync(q))ensure(!fs.lstatSync(q).isSymbolicLink(),'Linked workflow path');if(path.dirname(q)===q)break}}
function dir(root){root=fs.realpathSync(root);const d=path.join(root,'.workflow');noLinks(d);fs.mkdirSync(d,{recursive:true});return d}
function file(d,name){const p=path.join(d,name);noLinks(p);return p}
function readState(root,id){ensure(safeId(id),'Invalid task_id');const p=path.join(fs.realpathSync(root),'.workflow','task-'+encodeURIComponent(id)+'.json');noLinks(p);return fs.existsSync(p)?JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')):null}
function writeJson(p,v){const tmp=p+'.'+crypto.randomUUID()+'.tmp';try{fs.writeFileSync(tmp,JSON.stringify(v,null,2)+'\n',{mode:0o600});fs.renameSync(tmp,p)}finally{if(fs.existsSync(tmp))fs.unlinkSync(tmp)}}
function relativeFile(root,rel){
 ensure(typeof rel==='string'&&rel.length>0&&rel.length<=600&&!rel.includes('\\')&&!rel.includes(':')&&!rel.startsWith('/')&&!rel.split('/').some(x=>!x||x==='.'||x==='..'),'Invalid relative artifact path');
 const base=fs.realpathSync(root),p=path.resolve(base,...rel.split('/'));ensure(p.startsWith(base+path.sep),'Artifact path escapes project');noLinks(p);return p;
}
function hashFile(root,rel){const p=relativeFile(root,rel);ensure(fs.existsSync(p)&&fs.statSync(p).isFile(),'Missing artifact: '+rel);ensure(fs.statSync(p).size<=128*1024*1024,'Artifact too large for inline check');return digest(fs.readFileSync(p))}
function bindings(root,rows,label){
 ensure(Array.isArray(rows)&&rows.length<=1024,'Invalid '+label);const names=new Set();
 return rows.map(r=>{ensure(r&&typeof r==='object'&&!Array.isArray(r),'Invalid binding');relativeFile(root,r.path);ensure(!names.has(r.path),'Duplicate binding');names.add(r.path);ensure(/^[a-f0-9]{64}$/.test(r.sha256),'Binding needs sha256');return {path:r.path,sha256:r.sha256}});
}
function fresh(root,rows){const faults=[];for(const r of rows){try{const current=hashFile(root,r.path);if(current!==r.sha256)faults.push('Changed: '+r.path+' ('+r.sha256.slice(0,8)+' -> '+current.slice(0,8)+')')}catch(e){faults.push(e.message)}}return faults}
function rowsUnique(rows,label,limit){ensure(Array.isArray(rows)&&rows.length<=limit,'Invalid '+label);const seen=new Set();for(const r of rows){ensure(r&&safeId(r.id)&&!seen.has(r.id),'Invalid/duplicate '+label+' id');seen.add(r.id)}return seen}
function baseState(input){
 ensure(safeId(input?.task_id)&&[1,2].includes(input.schema_version),'Invalid state identity');
 const state={schema_version:input.schema_version,task_id:input.task_id,updated_at:new Date().toISOString()};
 for(const k of ['result','scope','next','blocker'])state[k]=words(input[k],k);
 ensure(Array.isArray(input.decisions)&&input.decisions.length<=20&&input.decisions.every(s=>typeof s==='string'&&s.length<=1000),'Invalid decisions');state.decisions=input.decisions;return state;
}
function normalizedV2(root,input){
 const state=baseState(input);ensure(state.result.trim()&&state.scope.trim(),'Graph task needs result and scope');ensure(TASK_STATUSES.includes(input.status),'Invalid task status');state.status=input.status;
 if(input.session_id!==undefined){ensure(safeId(input.session_id),'Invalid session_id');state.session_id=input.session_id}
 state.dependency_policy=input.dependency_policy||'conservative';ensure(['conservative','declared'].includes(state.dependency_policy),'Invalid dependency policy');
 if(state.dependency_policy==='declared'){ensure(input.independence&&words(input.independence.observation,'independence').trim(),'Declared independence needs observation');state.independence={observation:input.independence.observation,files:bindings(root,input.independence.files,'independence files')};ensure(state.independence.files.length>0,'Independence needs checked evidence')}
 if(input.blocker_kind!==undefined){ensure(['timeout','access','validation','external','user'].includes(input.blocker_kind),'Invalid blocker kind');state.blocker_kind=input.blocker_kind}
 ensure(Array.isArray(input.approved_actions||[])&&(input.approved_actions||[]).length<=40,'Invalid scope records');
 state.approved_actions=(input.approved_actions||[]).map(a=>{ensure(a&&safeId(a.id)&&a.source?.kind==='user','Scope record needs actual user source');return {id:a.id,action:words(a.action,'action',1000),resource:words(a.resource,'resource',1000),conditions:words(a.conditions,'conditions',1000),source:{kind:'user',reference:words(a.source.reference,'user source',1000)}}});rowsUnique(state.approved_actions,'scope',40);
 const outputIds=rowsUnique(input.outputs,'output',2000);ensure(outputIds.size>0,'Graph state needs declared outputs');
 state.outputs=input.outputs.map(o=>{ensure(['pending','ready','not_applicable'].includes(o.status),'Invalid output status');const row={id:o.id,status:o.status,required:o.required!==false};if(o.path!==undefined){relativeFile(root,o.path);row.path=o.path}if(o.sha256!==undefined){ensure(/^[a-f0-9]{64}$/.test(o.sha256),'Invalid output hash');row.sha256=o.sha256}if(o.status==='ready')ensure(row.path&&row.sha256,'Ready output needs actual file and hash');if(o.status==='not_applicable'){row.rationale=words(o.rationale,'output rationale');ensure(row.rationale.trim(),'Nonapplicable output needs rationale')}return row});
 const stageIds=rowsUnique(input.stages,'stage',128);ensure(stageIds.size>0,'Graph state needs stages');
 state.stages=input.stages.map(s=>{
  ensure(STAGE_STATUSES.includes(s.status)&&Array.isArray(s.dependencies)&&Array.isArray(s.output_ids),'Invalid stage');
  ensure(new Set(s.dependencies).size===s.dependencies.length&&s.dependencies.every(id=>stageIds.has(id)&&id!==s.id),'Unknown/self/duplicate dependency');
  ensure(new Set(s.output_ids).size===s.output_ids.length&&s.output_ids.every(id=>outputIds.has(id)),'Unknown/duplicate stage output');
  const row={id:s.id,status:s.status,required:s.required!==false,dependencies:s.dependencies,output_ids:s.output_ids,inputs:bindings(root,s.inputs||[],'stage inputs'),evidence:bindings(root,s.evidence||[],'stage evidence')};
  if(s.skill!==undefined)row.skill=words(s.skill,'skill',200);if(s.observation!==undefined)row.observation=words(s.observation,'observation');
  if(s.status==='pass')ensure(row.inputs.length>0&&row.evidence.length>0&&row.observation?.trim(),'Passing stage needs bound inputs, evidence and observation');
  if(s.status==='not_applicable'){row.rationale=words(s.rationale,'stage rationale');ensure(row.rationale.trim(),'Nonapplicable stage needs rationale')}return row;
 });
 ensure(state.outputs.filter(o=>o.required).every(o=>state.stages.some(s=>s.output_ids.includes(o.id))),'Required output has no declared stage');
 const graph=new Map(state.stages.map(s=>[s.id,s]));const visiting=new Set(),visited=new Set();function visit(id){ensure(!visiting.has(id),'Cyclic stage dependencies');if(visited.has(id))return;visiting.add(id);for(const dep of graph.get(id).dependencies)visit(dep);visiting.delete(id);visited.add(id)}for(const id of graph.keys())visit(id);
 if(input.quality_ledger!==undefined){relativeFile(root,input.quality_ledger);state.quality_ledger=input.quality_ledger}
 if(input.manifest_change!==undefined){ensure(input.manifest_change.source?.kind==='user','Manifest change needs actual user source');state.manifest_change={reason:words(input.manifest_change.reason,'manifest reason'),source:{kind:'user',reference:words(input.manifest_change.source.reference,'manifest source')}};ensure(state.manifest_change.reason.trim()&&state.manifest_change.source.reference.trim(),'Empty manifest change')}
 ensure(!secret.test(stable(state)),'Possible secret in task state');return state;
}
function ledgerStatus(root,relative){
 const python=process.env.HARNESS_PYTHON||'python';
 const script=fileURLToPath(new URL('../skills/dev-flow/scripts/quality_ledger.py',import.meta.url));
 const args=['-B','-X','utf8',script,'validate',relativeFile(root,relative),'--root',fs.realpathSync(root),'--require-ready'];
 let output;try{output=execFileSync(python,args,{encoding:'utf8',timeout:4000,maxBuffer:2*1024*1024,windowsHide:true})}catch(e){if(e.stdout)output=e.stdout.toString();else return {ready:false,reason:'Ledger check unavailable or timed out'}}
 try{const r=JSON.parse(output.replace(/^\uFEFF/,''));return {ready:r.schema_valid===true&&r.ready_to_complete===true,reason:r.ready_to_complete?'':(r.errors||r.blocking||['Ledger incomplete']).slice(0,4).join('; ')||'Ledger incomplete'}}catch{return {ready:false,reason:'Invalid ledger diagnostic'}}
}
export function inspectState(root,state,{checkLedger=true}={}){
 if(!state)return {schema_version:1,found:false,ready_to_complete:false,next:[],limitations:['No task state']};
 if(state.schema_version===1)return {schema_version:1,found:true,task_id:state.task_id,legacy:true,ready_to_complete:false,next:[{id:'legacy',action:state.next}],limitations:['Legacy state has no verified stage/output manifest']};
 state=normalizedV2(root,state);const reasons=[],outputs=new Map();
 for(const o of state.outputs){const failures=o.status==='ready'?fresh(root,[o]):[];const ok=(o.status==='ready'&&failures.length===0)||o.status==='not_applicable';outputs.set(o.id,{...o,current:ok,failures});if(o.required&&!ok)reasons.push('Output '+o.id+': '+(failures.join('; ')||o.status))}
 const stages=new Map();let staleAny=false;
 for(const s of state.stages){const faults=s.status==='pass'?[...fresh(root,s.inputs),...fresh(root,s.evidence),...s.output_ids.filter(id=>!outputs.get(id).current).map(id=>'Output not current: '+id)]:[];staleAny ||= faults.length>0;stages.set(s.id,{...s,effective_status:faults.length?'stale':s.status,faults})}
 if(state.dependency_policy==='declared'&&fresh(root,state.independence.files).length){reasons.push('Independence evidence is stale');staleAny=true;state.dependency_policy='conservative'}
 if(staleAny&&state.dependency_policy==='conservative')for(const s of stages.values())if(s.effective_status==='pass')s.effective_status='stale';
 let changed=true;while(changed){changed=false;for(const s of stages.values()){if(s.effective_status==='pass'&&s.dependencies.some(id=>!['pass','not_applicable'].includes(stages.get(id).effective_status))){s.effective_status='stale';s.faults.push('Dependency incomplete');changed=true}}}
 for(const s of stages.values())if(s.required&&!['pass','not_applicable'].includes(s.effective_status))reasons.push('Stage '+s.id+': '+s.effective_status);
 if(state.blocker.trim())reasons.push('Declared blocker: '+state.blocker);
 const suspended=['paused','cancelled'].includes(state.status);
 let ledger;if(state.quality_ledger&&checkLedger){ledger=ledgerStatus(root,state.quality_ledger);if(!ledger.ready)reasons.push('Ledger: '+ledger.reason)}
 const next=suspended?[]:[...stages.values()].filter(s=>!['pass','not_applicable','blocked'].includes(s.effective_status)&&s.dependencies.every(id=>['pass','not_applicable'].includes(stages.get(id).effective_status))).map(s=>({id:s.id,skill:s.skill||null,status:s.effective_status,outputs:s.output_ids}));
 return {schema_version:2,found:true,task_id:state.task_id,session_id:state.session_id||null,status:state.status,ready_to_complete:reasons.length===0&&!suspended,reasons,next,outputs:[...outputs.values()],stages:[...stages.values()],ledger:ledger||null,limitations:['Declared bindings only; undeclared dependencies and actual inspection cannot be authenticated','Scope records do not grant permissions; self-review is not independent human acceptance']};
}
export function inspect(root,id){return inspectState(root,readState(root,id))}
export function snapshot(root,paths){ensure(Array.isArray(paths)&&paths.length>0&&paths.length<=1024,'Invalid snapshot paths');return {files:paths.map(p=>({path:p,sha256:hashFile(root,p)}))}}
export function setState(root,input){
 const state=input?.schema_version===2?normalizedV2(root,input):baseState(input);ensure(!secret.test(stable(state)),'Possible secret in task state');
 const previous=readState(root,state.task_id);
 if(previous?.schema_version===2){ensure(state.schema_version===2,'Cannot downgrade a graph task to legacy');if(previous.session_id)ensure(state.session_id===previous.session_id,'Task belongs to another session; use a unique task_id and actual handoff');const changed=['outputs','stages'].some(k=>previous[k].filter(r=>r.required!==false).some(r=>!state[k].some(n=>n.id===r.id&&n.required!==false)));if(changed)ensure(input.manifest_change,'Required manifest changed without recorded user basis')}
 if(state.schema_version===2&&['ready','complete'].includes(state.status))ensure(inspectState(root,state).ready_to_complete,'Completion rejected: stale or incomplete required results');
 const d=dir(root),p=file(d,'task-'+encodeURIComponent(state.task_id)+'.json');writeJson(p,state);
 if(state.session_id)writeJson(file(d,'active-'+encodeURIComponent(state.session_id)+'.json'),{schema_version:1,task_id:state.task_id,session_id:state.session_id});
 return state.schema_version===1?{path:path.relative(root,p)}:{path:path.relative(root,p),schema_version:2};
}
export function record(root,input){
 ensure(input&&EVENTS.has(input.event)&&safeId(input.task_id),'Invalid event or task_id');
 const allowed=new Set(['event','task_id','event_id','kind','stage','type','verified','duration_ms']);ensure(Object.keys(input).every(k=>allowed.has(k)),'Unexpected telemetry field');
 const e={event:input.event,task_id:input.task_id,event_id:input.event_id||crypto.randomUUID()};ensure(safeId(e.event_id),'Invalid event identity');
 if(e.event==='question'){ensure(['repeated','technical','new_scope','clarification'].includes(input.kind),'Question kind required');e.kind=input.kind}
 if(e.event==='blocker'){ensure(['timeout','access','validation','external'].includes(input.type),'Blocker type required');e.type=input.type}
 if(e.event==='interruption'){ensure(['connection','user','external'].includes(input.kind),'Interruption kind required');e.kind=input.kind}
 if(input.stage!==undefined){ensure(['context','implementation','review','memory','approval','tool','references','preflight','verification'].includes(input.stage),'Invalid stage');e.stage=input.stage}
 if(e.event==='task-done'){ensure(input.verified===true,'Completion needs verified=true');const current=readState(root,input.task_id);if(current?.schema_version===2)ensure(inspectState(root,current).ready_to_complete,'Completion rejected: current manifest not ready');e.verified=true}
 if(input.duration_ms!==undefined){ensure(Number.isFinite(input.duration_ms)&&input.duration_ms>=0&&input.duration_ms<=86400000,'Invalid duration');e.duration_ms=input.duration_ms}
 ensure(!secret.test(stable(e)),'Possible secret in telemetry');const d=dir(root),p=file(d,'events.jsonl');
 const rows=fs.existsSync(p)?fs.readFileSync(p,'utf8').trim().split(/\r?\n/).filter(Boolean).map(s=>JSON.parse(s)):[];
 const previous=rows.find(x=>x.event_id===e.event_id);if(previous){const {at,schema_version,...same}=previous;ensure(stable(same)===stable(e),'Event identity conflict');return {event_id:e.event_id,duplicate:true}}
 fs.appendFileSync(p,JSON.stringify({schema_version:1,at:new Date().toISOString(),...e})+'\n',{mode:0o600});return {event_id:e.event_id,duplicate:false};
}
export function metrics(root){
 const p=path.join(fs.realpathSync(root),'.workflow','events.jsonl');noLinks(p);const rows=fs.existsSync(p)?fs.readFileSync(p,'utf8').trim().split(/\r?\n/).filter(Boolean).map(s=>JSON.parse(s)):[];
 const questionCounts={repeated:0,technical:0,new_scope:0,clarification:0};const counts={};for(const r of rows){counts[r.event]=(counts[r.event]||0)+1;if(r.event==='question'&&Object.hasOwn(questionCounts,r.kind))questionCounts[r.kind]++}
 const denominator=questionCounts.repeated+questionCounts.new_scope+questionCounts.clarification;
 return {schema_version:1,source:'.workflow/events.jsonl',method:'Agent-labelled recorded events only',period:{from:rows[0]?.at||null,to:rows.at(-1)?.at||null},recorded_events:rows.length,counts,questions:questionCounts,repeated_questions:{numerator:questionCounts.repeated,denominator,rate:denominator?questionCounts.repeated/denominator:null},limitations:['Incomplete/unverified event coverage is unknown, not zero','No causal attribution, perceptual quality score or model benchmark inferred']};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 let input='';try{for await(const c of process.stdin){input+=c;ensure(input.length<=256*1024,'Input too large')}const p=JSON.parse(input.replace(/^\uFEFF/,''));
 const r=p.command==='record'?record(process.cwd(),p.event):p.command==='state'?setState(process.cwd(),p.state):p.command==='inspect'?inspect(process.cwd(),p.task_id):p.command==='snapshot'?snapshot(process.cwd(),p.paths):p.command==='metrics'?metrics(process.cwd()):(()=>{throw new Error('Commands: record, state, inspect, snapshot, metrics')})();process.stdout.write(JSON.stringify(r)+'\n')
 }catch(e){process.stderr.write(e.message+'\n');process.exitCode=1}
}
