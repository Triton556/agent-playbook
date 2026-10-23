"""Exercise the fixed one-release workflow with a fake API, without credentials."""
import json
import subprocess
import unittest
from test_install import ROOT

class ReleaseWorkflow(unittest.TestCase):
    def test_fixed_release_gate_and_safe_idempotence(self):
        for version in ['2.1.0','2.2.0']:
            with self.subTest(version=version):self.check_version(version)

    def check_version(self,version):
        text=(ROOT/('.github/workflows/release-'+version.rsplit('.',1)[0]+'.yml')).read_text()
        script='\n'.join(line[12:] for line in text.split('          script: |\n',1)[1].splitlines())
        runner=r'''
const source=JSON.parse(process.argv[1]);
(async()=>{
for(const scenario of ['absent','equal','conflict','stale','failure','nonsuccess','foreign','draft','version','apiFailure']){
 const sha='a'.repeat(40), calls=[];
 const run={head_repository:{full_name:'Triton556/agent-playbook'},head_branch:'main',event:'push',name:'Validate package',conclusion:'success',head_sha:sha};
 if(scenario==='failure')run.conclusion='failure';
 if(scenario==='nonsuccess')run.event='pull_request';
 if(scenario==='foreign')run.head_repository.full_name='other/repo';
 const missing=()=>{throw Object.assign(new Error('missing'),{status:404})};
 const github={rest:{git:{getRef:async p=>{
  if(scenario==='apiFailure')throw Object.assign(new Error('forbidden'),{status:403});
  if(p.ref==='heads/main')return {data:{object:{sha:scenario==='stale'?'b'.repeat(40):sha}}};
  if(['equal','conflict','draft'].includes(scenario))return {data:{object:{type:'commit',sha:scenario==='conflict'?'b'.repeat(40):sha}}};
  return missing();},createRef:async p=>{calls.push(['tag',p]);}},repos:{
  getContent:async()=>({data:{content:Buffer.from(JSON.stringify({version:scenario==='version'?'999.0.0':'2.1.0'})).toString('base64')}}),
  getReleaseByTag:async()=>['equal','draft'].includes(scenario)?{data:{tag_name:'v2.1.0',draft:scenario==='draft',prerelease:false,html_url:'url'}}:missing(),
  createRelease:async p=>{calls.push(['release',p]);}
 }}};
 let error=null;try{await new (Object.getPrototypeOf(async()=>{}).constructor)('github','context','core',source)(github,{repo:{owner:'Triton556',repo:'agent-playbook'},payload:{workflow_run:run}},{info:()=>{}});}catch(e){error=e.message;}
 if(scenario==='absent'){if(error||calls.length!==2)throw new Error(scenario+JSON.stringify({error,calls}));}
 else if(['equal','version'].includes(scenario)){if(error||calls.length)throw new Error(scenario);}
 else if(!error||calls.length)throw new Error(scenario+JSON.stringify({error,calls}));
}
console.log('10 fake-API scenarios passed');
})().catch(e=>{console.error(e);process.exit(1)});
'''
        runner=runner.replace('2.1.0',version)
        result=subprocess.run(['node','-e',runner,json.dumps(script)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('permissions: {}',text)
        self.assertNotIn('actions/checkout',text)
        self.assertNotIn('secrets.',text)
