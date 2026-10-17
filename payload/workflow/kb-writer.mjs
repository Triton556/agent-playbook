import {capture,checkpoint} from '../runtime/memory/SYSTEM/scripts/kb.mjs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const VAULT=process.env.HARNESS_KB_ROOT;if(!VAULT)throw new Error('Set HARNESS_KB_ROOT to the authorized fixed vault before starting this writer');
const obj=(properties,required=Object.keys(properties))=>({type:'object',properties,required,additionalProperties:false});
const str={type:'string',minLength:1,maxLength:12000},short=maxLength=>({...str,maxLength}),identity={...short(256),pattern:'^[a-zA-Z0-9:._-]+$'},source=obj({kind:{enum:['codex','rumi','cloud','manual']},session_id:identity,turn_id:identity,label:short(256)},['kind','session_id','turn_id']);
const item=obj({type:{enum:['fact','preference','decision','task','project-update','idea','research','hypothesis']},text:str,evidence:short(2000),status:short(64),topics:{type:'array',maxItems:10,items:short(100)},links:{type:'array',items:{...short(2000),pattern:'^https?://',description:'Web source URLs only. Put local file paths in text or evidence.'}}},['type','text','evidence']);
const payload=obj({schema_version:{const:1},title:short(160),source,batch_key:short(128),final:{type:'boolean'},items:{type:'array',minItems:1,maxItems:40,items:item}},['schema_version','title','source','items']);
const tools=[{name:'kb_capture',description:'Save structured non-secret knowledge in the fixed authorized INBOX. Uses original session/turn IDs and idempotent batch identity. No arbitrary path, shell, deletion, sync or publication.',inputSchema:obj({payload}),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:true,openWorldHint:false}},{name:'kb_checkpoint',description:'Mark a turn in the fixed authorized vault when there is no new memory. Does not edit knowledge notes or arbitrary files.',inputSchema:obj({session_id:identity,turn_id:identity}),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:true,openWorldHint:false}}];
const secret=/(?:\b(?:sk-|gh[pousr]_)[a-zA-Z0-9_-]{20,}|\bgithub_pat_[a-zA-Z0-9_]{20,}|-----BEGIN.*PRIVATE KEY-----|\bBearer\s+[a-zA-Z0-9._-]{24,})/i;
function validate(schema,value){
 if(schema.const!==undefined&&value!==schema.const)throw new Error('Invalid constant');if(schema.enum&&!schema.enum.includes(value))throw new Error('Invalid choice');
 if(schema.type==='object'){if(!value||typeof value!=='object'||Array.isArray(value))throw new Error('Object required');if(schema.additionalProperties===false&&Object.keys(value).some(k=>!Object.hasOwn(schema.properties,k)))throw new Error('Unexpected field');for(const k of schema.required||[])if(!Object.hasOwn(value,k))throw new Error('Required field missing');for(const [k,v] of Object.entries(value))validate(schema.properties[k],v)}
 if(schema.type==='string'&&(typeof value!=='string'||!value.trim()||value.length>(schema.maxLength||12000)||value.length<(schema.minLength||0)))throw new Error('Invalid string length');if(schema.pattern&&!new RegExp(schema.pattern).test(value))throw new Error('Invalid string format; source links must be web URLs and identities must be plain IDs');if(schema.type==='boolean'&&typeof value!=='boolean')throw new Error('Boolean required');
 if(schema.type==='array'){if(!Array.isArray(value)||value.length>(schema.maxItems||50)||value.length<(schema.minItems||0))throw new Error('Invalid array');for(const x of value)validate(schema.items,x)}
}
export function makeHandler(adapter){
 return request=>{if(!request||request.jsonrpc!=='2.0'||Array.isArray(request))return {jsonrpc:'2.0',id:null,error:{code:-32600,message:'Invalid request'}};
 if(request.id===undefined)return null;
 const reply=result=>({jsonrpc:'2.0',id:request.id,result});
 if(request.method==='initialize')return reply({protocolVersion:['2025-11-25','2025-06-18','2025-03-26','2024-11-05'].includes(request.params?.protocolVersion)?request.params.protocolVersion:'2025-11-25',capabilities:{tools:{listChanged:false}},serverInfo:{name:'danil-kb-writer',version:'1.1.0'}});
 if(request.method==='ping')return reply({});if(request.method==='tools/list')return reply({tools});
 if(request.method==='tools/call'){
 const tool=tools.find(t=>t.name===request.params?.name);if(!tool)return {jsonrpc:'2.0',id:request.id,error:{code:-32602,message:'Unknown tool'}};
 try{validate(tool.inputSchema,request.params.arguments);if(secret.test(JSON.stringify(request.params.arguments)))throw new Error('Possible credential detected');const r=tool.name==='kb_capture'?adapter.capture(request.params.arguments.payload):adapter.checkpoint(request.params.arguments);return reply({content:[{type:'text',text:JSON.stringify(r)}],structuredContent:r,isError:false})}catch(e){const safe=['Invalid constant','Invalid choice','Object required','Unexpected field','Required field missing','Invalid string length','Invalid string format; source links must be web URLs and identities must be plain IDs','Boolean required','Invalid array','Possible credential detected'].includes(e.message)?'Input rejected: '+e.message:e.code&&/^[A-Z0-9_]+$/.test(e.code)?'Memory operation failed: '+e.code:'Memory input or local operation rejected. Check the published schema, source identity and local permissions.';return reply({content:[{type:'text',text:safe}],isError:true})}
 }
 return {jsonrpc:'2.0',id:request.id,error:{code:-32601,message:'Method not supported'}};
 };
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const handle=makeHandler({capture:p=>capture(VAULT,p),checkpoint:p=>checkpoint(VAULT,p)});let buffer='',discard=false;process.stdin.setEncoding('utf8');
 function processLine(line){if(!line.trim())return;let r;try{r=handle(JSON.parse(line))}catch{r={jsonrpc:'2.0',id:null,error:{code:-32700,message:'Invalid JSON'}}}if(r)process.stdout.write(JSON.stringify(r)+'\n')}
 for await(const chunk of process.stdin){for(const piece of chunk.toString('utf8').split(/(?<=\n)/)){if(discard){if(piece.endsWith('\n'))discard=false;continue}buffer+=piece;if(buffer.length>1024*1024){buffer='';discard=!piece.endsWith('\n');process.stdout.write(JSON.stringify({jsonrpc:'2.0',id:null,error:{code:-32600,message:'Input exceeds limit'}})+'\n');continue}if(piece.endsWith('\n')){processLine(buffer);buffer=''}}}if(buffer&&!discard)processLine(buffer);
}
