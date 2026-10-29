#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
export function checkTopicSize(root, paths) {
  root=fs.realpathSync(root);
  if (!Array.isArray(paths)||!paths.length) throw new Error('Supply changed Markdown paths; this tool does not scan the vault.');
  return paths.map(p=>{
    if (typeof p!=='string'||!p.endsWith('.md')||path.isAbsolute(p)) throw new Error('Expected relative Markdown path');
    const f=fs.realpathSync(path.resolve(root,p)), rel=path.relative(root,f);
    if (rel.startsWith('..'+path.sep)||rel==='..'||path.isAbsolute(rel)) throw new Error('Path outside vault');
    const data=fs.readFileSync(f),text=data.toString('utf8');
    const historical=/^(INBOX|ARCHIVE|SYSTEM)\//.test(p)||/history-|История/.test(p)||/kb\/history/.test(text.slice(0,300));
    return {path:p,bytes:data.length,status:historical?'source-or-history':data.length>40000?'split-required':data.length>=20000?'review-boundaries':'within-size-budget',semantic_subtopics:'curator reviews independently; headings are not a proxy'};
  });
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try {const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');const r=checkTopicSize(root,process.argv.slice(2));console.log(JSON.stringify(r,null,2));process.exitCode=r.some(x=>x.status==='split-required')?1:0;}
 catch(e){console.error(e.message);process.exitCode=2;}
}
