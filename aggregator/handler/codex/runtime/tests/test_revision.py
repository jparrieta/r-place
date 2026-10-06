"""Revision acceptance: continuity is native; local adequacy is not global fit."""
import contextlib,io,json,shutil,sys,tempfile,unittest,uuid
from pathlib import Path
from unittest.mock import patch
from runtime import actors,archive,study,leads,labelers
from runtime.common import *

class RevisionTests(unittest.TestCase):
 def setUp(self):
  self.tag='rev-'+uuid.uuid4().hex[:8];TMP.mkdir(parents=True,exist_ok=True)
  self.temp=tempfile.TemporaryDirectory(dir=TMP);self.base=Path(self.temp.name);self.instances=[]
  self.corpus=self.base/'corpus';self.room=self.corpus/'example';self.room.mkdir(parents=True)
  for name in leads.TRIPLET:atomic(self.room/name,'original '+name)
  (self.room/'out').mkdir();self.fake=str(CODEX/'runtime/tests/fake_codex.py')
  self.patches=[patch.object(leads,'CORPUS',self.corpus),patch.object(leads,'REGISTRY',self.base/'registry.json')]
  for p in self.patches:p.start()
 def tearDown(self):
  for a in self.instances:a.release()
  for base in ('actors','checkpoints','runs','dispatches'):
   for p in (DATA/base).glob(self.tag+'*'):shutil.rmtree(p)
  for p in self.patches:p.stop()
  self.temp.cleanup()
 def reg(self,aid):
  a=actors.Actor(aid);self.instances.append(a);return a
 def lead(self):
  aid=self.tag+'-lead';actors.create(aid,self.room,'gpt-5.6-sol','medium',role='case-lead',executable=self.fake)
  a=self.reg(aid);a.message('ORIGINAL-CASE-LEAD-CONTEXT');a.wait(10);r=a.checkpoint();return a,r
 def test_matching_archive_required_and_stale_triplet_rejected(self):
  a,r=self.lead();leads.bind('example',r['checkpoint']);self.assertEqual(leads.require('example')['thread_id'],a.state['thread_id'])
  atomic(self.room/'case.md','new recoding')
  with self.assertRaisesRegex(Error,'older corpus'):leads.require('example')
  with self.assertRaisesRegex(Error,'do not match'):leads.bind('example',r['checkpoint'])
 def test_wrong_actor_role_and_missing_lead_refused(self):
  with self.assertRaisesRegex(Error,'No native lead'):leads.require('example')
  aid=self.tag+'-analyst';actors.create(aid,self.room,'gpt-6-astra','high',executable=self.fake)
  a=self.reg(aid);a.message('not a case lead');a.wait(10);r=a.checkpoint()
  with self.assertRaisesRegex(Error,'not a case lead'):leads.bind('example',r['checkpoint'])
 def test_return_uses_lead_model_and_history_and_reuses_valid_result(self):
  a,r=self.lead();rec=leads.bind('example',r['checkpoint']);run=self.tag+'-study';rd=study.run_dir(run);rd.mkdir(parents=True)
  source=self.base/'source';copy_tree(self.room,source/'package/example');(source/'out').mkdir()
  task=source/'out/handoff-D/tasks/example';task.mkdir(parents=True);atomic(task/'TASK.md','return');atomic(task/'VERSION','model-v1')
  write(rd/'state.json',{'id':run,'latest_workspace':str(source),'active_actor':None,'fleet_parallel':1,'legs':{'D1a':{'stage':'D1','status':'verified','cut':'packets-out'}}})
  seen=[]
  def register(aid):
   b=self.reg(aid);original=b.message
   def message(text):
    result=original(text);b.wait(10);seen.append(b.final())
    out=b.base/'workspace/out/return-D2';out.mkdir(parents=True,exist_ok=True)
    atomic(out/'model-D.md','grade: composes\nlocal_status: validated\n## Local exceptions\nnone\n<!-- end -->')
    atomic(out/'adaptations.jsonl','{"end":true,"lines":0}\n');return result
   b.message=message;return b
  from subprocess import CompletedProcess
  def checked(run,tool,args,cwd):return CompletedProcess([],0,'fixture: schema validated','')
  with patch('runtime.study.trusted',side_effect=checked):result=labelers.dispatch(run,register)
  self.assertTrue(result['complete']);b=self.instances[-1]
  self.assertEqual(b.state['model'],'gpt-5.6-sol');self.assertIn('ORIGINAL-CASE-LEAD-CONTEXT',seen[-1])
  self.assertEqual((b.base/'workspace/case.md').read_text(),'original case.md')
  self.assertEqual(b.state['parent_checkpoint'],r['checkpoint'])
  root=DATA/'dispatches'/result['dispatch'];before=len(seen)
  with patch('runtime.study.trusted',side_effect=checked):labelers.execute(root,register)
  self.assertEqual(before,len(seen));self.assertTrue(study.run_state(run)['case_returns']['example'])
 def test_v39_local_account_required_separately_from_grade(self):
  module=study.load_module(study.INSTRUMENT/'tools/dreturn.py','revision_dreturn')
  model='[P07] [c0001]\ngrade: composes\n<!-- end -->'
  self.assertTrue(any('local_status' in e for e in module.model_problems(model,'example',{'P07'},{'c0001'},{'P07'},True)))
  valid=model.replace('<!-- end -->','local_status: validated\n## Local exceptions\nnone, the record supports the local account.\n<!-- end -->')
  self.assertEqual(module.model_problems(valid,'example',{'P07'},{'c0001'},{'P07'},True),[])
  self.assertTrue(module.model_problems(valid.replace('grade: composes','grade: does-not-compose'),'example',{'P07'},{'c0001'},{'P07'},True))
 def test_build_delivers_only_current_instructions_and_current_templates(self):
  src=self.base/'prepared';copy_tree(self.room,src/'00_GIVE-THE-AGENT/package/example')
  (src/'00_GIVE-THE-AGENT/out').mkdir();(src/'DROPS').mkdir()
  run=self.tag+'-build';study.build(run,src);root=study.run_dir(run)
  self.assertFalse((root/'baseline/STAGES-full.md').exists())
  self.assertFalse((root/'baseline/SCHEMA-adaptations.md').exists())
  self.assertFalse((root/'baseline/handoff').exists())
  self.assertIn('local_status:',(root/'drops/D1/handoff/RETURN-D.md').read_text())
  self.assertTrue((root/'drops/E2/handling/proposal.md').is_file())
 def test_v43_build_delivers_codex_platform_and_excludes_claude(self):
  src=self.base/'platform-source';ws=src/'00_GIVE-THE-AGENT'
  (ws/'out').mkdir(parents=True);(src/'DROPS').mkdir()
  for name in ('CLAUDE.md','PLATFORM-claude.md','PLATFORM-codex.md'):
   atomic(ws/name,'stale source platform instructions')
  atomic(ws/'WRITING.md','stale source writing guide')
  atomic(ws/'tools/prose_check.py','raise SystemExit(42)')
  before=inventory(src)
  run=self.tag+'-platform';state=study.build(run,src);root=study.run_dir(run)
  self.assertEqual(state['version'],'v43-openai-1')
  for stage in ('A1','B1','B4'):
   card=next((study.INSTRUMENT/'stages').glob('STAGE-'+stage+'-*.md'))
   self.assertEqual(sha(root/'drops'/stage/'stages'/card.name),sha(card))
  self.assertEqual(sha(root/'baseline/tools/mem.py'),sha(study.INSTRUMENT/'tools/mem.py'))
  self.assertEqual(sha(root/'trusted/mem.py'),sha(study.INSTRUMENT/'tools/mem.py'))
  for folder in (root/'baseline',):
   self.assertEqual(sha(folder/'PLATFORM-codex.md'),sha(study.INSTRUMENT/'PLATFORM-codex.md'))
   self.assertTrue((folder/'WRITING.md').is_file())
   self.assertEqual(sha(folder/'WRITING.md'),sha(study.INSTRUMENT/'WRITING.md'))
   self.assertEqual(sha(folder/'tools/prose_check.py'),sha(study.INSTRUMENT/'tools/prose_check.py'))
   self.assertFalse((folder/'CLAUDE.md').exists())
   self.assertFalse((folder/'PLATFORM-claude.md').exists())
  with patch('runtime.actors.shutil.which',return_value=self.fake):prepared=study.prepare(run,'A1a')
  actor=self.reg(prepared['actor']);delivered=actor.base/'workspace'
  self.assertEqual(sha(delivered/'PLATFORM-codex.md'),sha(study.INSTRUMENT/'PLATFORM-codex.md'))
  self.assertIn('PLATFORM-codex.md',(delivered/'AGENTS.md').read_text())
  self.assertIn('WRITING.md',(delivered/'AGENT.md').read_text())
  self.assertEqual(sha(delivered/'WRITING.md'),sha(study.INSTRUMENT/'WRITING.md'))
  self.assertEqual(sha(delivered/'tools/prose_check.py'),sha(study.INSTRUMENT/'tools/prose_check.py'))
  self.assertFalse((delivered/'CLAUDE.md').exists())
  self.assertFalse((delivered/'PLATFORM-claude.md').exists())
  self.assertEqual([p.name.split('-')[1] for p in (delivered/'stages').glob('STAGE-*.md')],['A1'])
  schedule=read(root/'arm.json')['A1'];configured={**schedule,**schedule.get('legs',{}).get('a',{})}
  self.assertEqual((actor.state['model'],actor.state['effort']),(configured['analyst'],configured['effort']))
  self.assertEqual(inventory(src),before)
 def test_build_refreshes_shelves_without_early_delivery_or_source_mutation(self):
  src=self.base/'shelf-source';ws=src/'00_GIVE-THE-AGENT'
  (ws/'out').mkdir(parents=True)
  old=src/'DROPS/A1/shelves/on-request';old.mkdir(parents=True)
  atomic(old/'retired-paper.md','Retired source shelf entry')
  paper='gunther-joshi-constantinides-2026.md'
  atomic(old/paper,'Outdated source shelf text')
  before=inventory(src);run=self.tag+'-shelves';study.build(run,src);root=study.run_dir(run)
  for stage in ('A1','B1','C3'):
   self.assertEqual(inventory(root/'drops'/stage/'shelves'),inventory(study.INSTRUMENT/'shelves'/stage))
  self.assertFalse(any((root/'baseline/shelves').rglob('*.md')))
  with patch('runtime.actors.shutil.which',return_value=self.fake):prepared=study.prepare(run,'A1a')
  actor=self.reg(prepared['actor']);delivered=actor.base/'workspace'
  self.assertEqual(sha(delivered/'shelves/on-request'/paper),sha(study.INSTRUMENT/'shelves/A1/on-request'/paper))
  self.assertFalse((delivered/'shelves/read/felin-zenger-2016.md').exists())
  self.assertFalse((delivered/'shelves/on-request/retired-paper.md').exists())
  self.assertEqual(inventory(src),before)
 def test_actual_d2_ingest_enforces_local_account(self):
  sys.path.insert(0,str(study.INSTRUMENT/'tools'))
  from checks import selftest,stage_D2
  import ingest
  root=self.base/'d2-fixture';root.mkdir();out=Path(selftest.write_fixture(str(root)))
  previous=Path.cwd()
  try:
   os.chdir(root)
   with contextlib.redirect_stdout(io.StringIO()):stage_D2.plant_base(str(out),str(root))
  finally:os.chdir(previous)
  handoff=out/'handoff-D';handoff.mkdir(exist_ok=True)
  shutil.copy2(study.INSTRUMENT/'handoff/RETURN-D.md',handoff/'RETURN-D.md')
  def run(*args):
   import subprocess
   return subprocess.run([sys.executable,'-B',str(study.INSTRUMENT/'tools/ingest.py'),'D','--root',str(root),'--out',str(out),*args],capture_output=True,text=True,env=env())
  fail=run('--check','denmark');self.assertNotEqual(fail.returncode,0,fail.stdout+fail.stderr)
  for p in (root/'DROPS/D').glob('*/model-D.md'):
   text=p.read_text().replace('<!-- end -->','local_status: unresolved\n## Local exceptions\nThe preserved case evidence still needs examination.\n<!-- end -->')
   p.write_text(text)
  for p in (root/'DROPS/D').glob('*/adaptations.jsonl'):
   rows=[json.loads(line) for line in p.read_text().splitlines() if line.strip()]
   for row in rows:
    if row.get('op')=='absent':row['observation']='unobserved'
   p.write_text(''.join(json.dumps(row)+'\n' for row in rows))
  ok=run('--check','denmark');self.assertEqual(ok.returncode,0,ok.stdout+ok.stderr)
  ok=run();self.assertEqual(ok.returncode,0,ok.stdout+ok.stderr)
  self.assertEqual(read(root/'RUN.json')['D2']['accepted'],2)
 def test_adaptation_dendrogram_preserves_crosslinks_and_flags_masking(self):
  sys.path.insert(0,str(study.INSTRUMENT/'tools'))
  from adaptation_tree import generate,read_matrix
  from distance import delta_score,newick
  out=self.base/'tree';(out/'_views').mkdir(parents=True)
  atomic(out/'_views/distance.tsv','room\ta\tb\tc\na\t0\t0\t0.5\nb\t0\t0\t0.5\nc\t0.5\t0.5\t0\n')
  rows=[{'id':s,'sub':s,'decision':'accept','element':'P01','op':'restrict','kind':'correction','lift':['t','T3-001','T4-01','D1']} for s in ('a','b')]
  rows.append({**rows[1],'id':'b-extra','op':'absent','observation':'observed-absent'})
  atomic(out/'adaptations.jsonl',''.join(json.dumps(r)+'\n' for r in rows))
  atomic(out/'branches.jsonl',json.dumps({'id':'F01','members':['a','b']})+'\n')
  atomic(out/'crosslinks.jsonl',json.dumps({'sub':'b','branches':['F01','F02'],'reason':'different targets'})+'\n')
  r=generate(out)
  self.assertEqual(r['root'],'global-model');self.assertEqual(set(r['rooms']),{'a','b','c'})
  self.assertTrue(r['sensitivity']['zero_distance_different_key_pairs']);self.assertEqual(r['crosslinks'][0]['sub'],'b')
  self.assertIn('Global model',(out/'_views/adaptation-tree.svg').read_text())
  self.assertEqual(newick([],[]),';')
  self.assertIsNone(delta_score(['a','b','c','d'],[[0 if i==j else 1 for j in range(4)] for i in range(4)],10,0))
  atomic(out/'_views/distance.tsv','room\ta\nb\t0\n')
  with self.assertRaises(ValueError):read_matrix(out/'_views/distance.tsv')
 def test_recheck_cannot_omit_an_affected_case(self):
  sys.path.insert(0,str(study.INSTRUMENT/'tools'))
  import vlib
  from checks import stage_D3
  root=self.base/'scope';out=root/'out';out.mkdir(parents=True)
  atomic(root/'handoff/RETURN-D.md','local_status: validated')
  atomic(root/'package/store/rooms.jsonl','{"sub":"a"}\n{"sub":"b"}\n')
  atomic(out/'dropped.jsonl','')
  atomic(out/'handoff-D/recheck/tasks/a/TASK.md','return')
  atomic(out/'rooms/a/model-D-recheck.md','local_status: validated')
  write(out/'recheck-scope.json',{'affected_rooms':['a','b'],'unaffected_rooms':{},'reason':'shared mechanism changed'})
  def errors():
   vlib.E.clear();vlib.W.clear()
   with contextlib.redirect_stdout(io.StringIO()):stage_D3.check_recheck(str(out),[],{},[],[{'id':'change1','leg':'D3a-01'}])
   return [x[0] for x in vlib.E]
  self.assertTrue(any('omit affected rooms' in x for x in errors()))
  atomic(out/'handoff-D/recheck/tasks/b/TASK.md','return')
  self.assertTrue(any('no checked local account' in x for x in errors()))
  atomic(out/'rooms/b/model-D-recheck.md','local_status: unresolved')
  self.assertFalse(any('omit affected rooms' in x or 'no checked local account' in x for x in errors()))
