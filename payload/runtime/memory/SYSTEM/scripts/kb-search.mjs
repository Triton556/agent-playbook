#!/usr/bin/env node
// Read-only lexical search. Does not mutate the vault or the pinned sync core.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const excluded=new Set(['.git','.kb','.obsidian','SYSTEM','node_modules']);
const stop=new Set('как кто что где какой какая какие сейчас текущий актуальный состояние статус ли и в на по для с из о об это уже'.split(' '));
const normalize=s=>s.toLocaleLowerCase('ru').replaceAll('ё','е').normalize('NFKC');
const plainLine=s=>s.replace(/!?\[[^\]]*\]\([^)]*\)/g,'').replace(/<https?:[^>]+>/g,'').replace(/https?:\/\/\S+/g,'');
function stem(s){
  if(/^[а-я]{6,}$/.test(s)) return s.replace(/(?:иями|ями|ами|ого|его|ому|ему|ыми|ими|ая|яя|ое|ее|ые|ие|ый|ий|ой|ую|юю|ов|ев|ам|ям|ах|ях|ом|ем|ы|и|а|я|у|ю|е|о)$/,'');
  return s;
}
function tokens(s){return [...new Set((normalize(s).match(/[\p{L}\p{N}]+(?:[./-][\p{L}\p{N}]+)*/gu)||[]).filter(x=>!stop.has(x)&&x.length>1).map(stem))];}
function words(s){return tokens(s).map(x=>x.startsWith('воксел')||x==='voxel'?'voxel':x==='харнесс'?'harness':x);}
function scan(folder,relative=''){
  return fs.readdirSync(folder,{withFileTypes:true}).flatMap(e=>{
    if(e.isSymbolicLink()||excluded.has(e.name))return [];
    const rel=relative?relative+'/'+e.name:e.name;
    if(e.isDirectory())return scan(path.join(folder,e.name),rel);
    return /\.md$/i.test(e.name)&&!['README.md','AGENTS.md','STATUS.md','PLAN.md'].includes(e.name)?[rel]:[];
  });
}
const kind=p=>p.startsWith('INBOX/')?'inbox':p.startsWith('ARCHIVE/')?'original':p.startsWith('HYPOTHESES/')?'hypothesis':/history-|История/.test(p)?'history':p==='INDEX.md'||p.includes('Навигация —')||p==='Главная.md'||p==='START-HERE.md'?'index':'topic';
export function searchVault(root,query,{mode='current',limit=8}={}){
  if(!['current','history'].includes(mode))throw new Error('mode must be current or history');
  if(typeof query!=='string'||!query.trim()||query.length>300)throw new Error('query must contain 1–300 characters');
  root=path.resolve(root);if(!fs.existsSync(path.join(root,'SYSTEM/connection.json')))throw new Error('Not a knowledge vault');
  const terms=words(query);if(!terms.length)return {mode,query,results:[],inbox:[]};
  const docs=scan(root).map(p=>{
    const content=fs.readFileSync(path.join(root,p),'utf8');
    const front=content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1]||'';
    const body=content.replace(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/,'');
    const title=body.match(/^#\s+(.+)$/m)?.[1]||p;
    return {path:p,title,body,kind:kind(p),front,terms:new Set(words(content+' '+p)),titleTerms:new Set(words(title+' '+p)),metaTerms:new Set(words(front))};
  });
  const idf=new Map(terms.map(t=>[t,Math.log(1+(docs.length+1)/(1+docs.filter(d=>d.terms.has(t)).length))]));
  const rank=d=>{
    let score=0,hits=0;
    for(const t of terms){if(d.terms.has(t)){hits++;score+=idf.get(t)*(1+(d.titleTerms.has(t)?2.6:0)+(d.metaTerms.has(t)?0.6:0));}}
    if(!hits)return null;
    score*=0.45+0.55*hits/terms.length;
    const factor=mode==='history'?({original:1.5,history:1.2,inbox:1.1,topic:1,index:0.5,hypothesis:0.9}[d.kind]):({original:0.55,history:0.22,inbox:1,topic:1.5,index:0.6,hypothesis:0.72}[d.kind]);
    score*=factor;
    if(/перенаправ|redirect/i.test(d.body.slice(0,500)))score*=0.4;
    const current=d.body.split(/^## .*?(?:Исторические|Исторический|Предыдущие|Прежний)/im)[0];
    let excerptScope='current';
    let lines=current.split(/\r?\n/).map((text,i)=>({text,line:i+1,score:words(plainLine(text)).filter(t=>terms.includes(t)).reduce((s,t)=>s+idf.get(t),0)})).filter(x=>x.score>0&&!/^#/.test(x.text));
    if(!lines.length&&terms.some(t=>d.titleTerms.has(t)))lines=current.split(/\r?\n/).map((text,i)=>({text,line:i+1,score:0})).filter(x=>!/^#/.test(x.text)&&plainLine(x.text).trim().length>60).slice(0,1);
    if(!lines.length){excerptScope='historical';lines=d.body.split(/\r?\n/).map((text,i)=>({text,line:i+1,score:words(plainLine(text)).filter(t=>terms.includes(t)).reduce((s,t)=>s+idf.get(t),0)})).filter(x=>x.score>0&&!/^#/.test(x.text));}
    lines.sort((a,b)=>b.score-a.score||a.line-b.line);
    const line=lines[0];
    const date=d.front.match(/"created_at"\s*:\s*"([^"]+)"/)?.[1]||null;
    return {path:d.path,title:d.title,kind:d.kind,score:+score.toFixed(3),matched_terms:hits,query_terms:terms.length,captured_at:date,excerpt_scope:excerptScope,excerpt:line?.text.slice(0,450)||d.title,contains_hypotheses:d.kind==='hypothesis'||/hypothesis · unconfirmed/.test(d.body)};
  };
  const ranked=docs.map(rank).filter(Boolean).sort((a,b)=>b.score-a.score||a.path.localeCompare(b.path));
  const n=Math.min(20,Math.max(1,Number(limit)||8));
  return {mode,query,results:ranked.filter(x=>x.kind!=='inbox').slice(0,n),inbox:ranked.filter(x=>x.kind==='inbox').slice(0,n),notice:'Рейтинг — поиск кандидатов. Проверь дату события, источник, заменённые решения и свежие INBOX.'};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  try{
    const args=process.argv.slice(2),opts={},query=[];let root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
    for(let i=0;i<args.length;i++){
      if(args[i]==='--root')root=args[++i];
      else if(args[i]==='--mode')opts.mode=args[++i];
      else if(args[i]==='--limit')opts.limit=args[++i];
      else if(args[i].startsWith('--'))throw new Error('Unknown option '+args[i]);
      else query.push(args[i]);
    }
    console.log(JSON.stringify(searchVault(root,query.join(' '),opts),null,2));
  }catch(e){console.error(e.message);process.exitCode=1;}
}
