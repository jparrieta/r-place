import json,shutil,tempfile,unittest,uuid
from pathlib import Path
from unittest.mock import patch
from runtime import actors,archive,study,fleet,bridge
from runtime.common import *

class LegOrderTests(unittest.TestCase):
 def setUp(self):
  self.rows=study.load_module(study.INSTRUMENT/'tools/steps.py','order_steps').table()
  self.stages=list(dict.fromkeys(r['stage'] for r in self.rows))
 def state(self,stage,previous=None,status='verified'):
  legs={} if previous is None else {previous:{'leg':previous,'stage':study.descriptor(previous)['stage'],'status':status}}
  return {'legs':legs,'finished_stages':self.stages[:self.stages.index(stage)]}
 def test_each_stage_starts_at_first_repeat_without_continuation(self):
  for stage in self.stages:
   row=next(r for r in self.rows if r['stage']==stage)
   suffix={'no':'','yes':'-01','round':'-r1'}[row['repeat']];first=stage+'a'+suffix
   state=self.state(stage);study.check_order(state,first)
   bad=[first+'-p1',first+'-p2']
   if row['repeat']!='no':bad += [stage+'a-'+('r'+str(n) if row['repeat']=='round' else f'{n:02d}') for n in (0,2)]
   for leg in bad:
    with self.subTest(leg=leg),self.assertRaises(Error):study.check_order(state,leg)
 def test_entering_a_repeated_step_starts_at_one(self):
  for previous,first in [('A1a','A1b-01'),('B1a','B1b-01'),('B1c','B1d-01'),('C2c','C2d-01'),('C5b','C5c-01'),('E1a','E1b-01')]:
   state=self.state(study.descriptor(first)['stage'],previous);study.check_order(state,first)
   for leg in (first[:-2]+'00',first[:-2]+'02',first+'-p2'):
    with self.subTest(previous=previous,leg=leg),self.assertRaises(Error):study.check_order(state,leg)
 def test_repeats_advance_by_one_after_verified_or_completed_continuation(self):
  for row in self.rows:
   if row['repeat']!='yes':continue
   prefix=row['stage']+row['step']
   for previous in (prefix+'-02',prefix+'-02-p2'):
    state=self.state(row['stage'],previous);study.check_order(state,prefix+'-03')
    for leg in (prefix+'-01',prefix+'-02',prefix+'-04',prefix+'-03-p2'):
     with self.subTest(previous=previous,leg=leg),self.assertRaises(Error):study.check_order(state,leg)
 def test_pilot_build_check_and_next_round_keep_their_round(self):
  for previous,allowed,refused in [('B2a-r1','B2b-r1',['B2b-r2','B2a-r2','B2c']),('B2b-r1','B2a-r2',['B2a-r1','B2a-r3']),('B2a-r2','B2b-r2',['B2b-r1','B2b-r3'])]:
   state=self.state('B2',previous);study.check_order(state,allowed)
   for leg in refused:
    with self.subTest(previous=previous,leg=leg),self.assertRaises(Error):study.check_order(state,leg)
  study.check_order(self.state('B2','B2b-r2'),'B2c')
 def test_only_paused_legs_accept_the_exact_next_continuation(self):
  for previous,next_leg in [('A1a','A1a-p2'),('A1b-02','A1b-02-p2'),('A1b-02-p2','A1b-02-p3'),('B2b-r2','B2b-r2-p2')]:
   stage=study.descriptor(previous)['stage'];state=self.state(stage,previous,'paused')
   study.check_order(state,next_leg)
   for leg in (next_leg[:-1]+'1',next_leg[:-1]+'4'):
    with self.subTest(previous=previous,leg=leg),self.assertRaises(Error):study.check_order(state,leg)
   for status in ('verified','prepared','failed'):
    with self.subTest(previous=previous,status=status),self.assertRaises(Error):study.check_order(self.state(stage,previous,status),next_leg)
  with self.assertRaises(Error):study.check_order(self.state('A1','A1b-02','paused'),'A1b-03')
 def test_branch_targets_match_claudes_stricter_order(self):
  claude=study.load_module(CODEX.parent/'claude-adapter/branches.py','order_claude_branches')
  cases=[('A1a','A1b-01',False,True),('A1a','A1b-02',False,False),('A1a','A1c',False,False),('A1a','A1a-p2',False,False),
         ('A1b-01','A1b-02',False,True),('A1b-01','A1b-03',False,False),('A1b-02','A1c',False,True),
         ('B1e','B2a-r1',True,True),('B1e','B2a-r2',True,False),('B2a-r2','B2b-r2',False,True),
         ('B2a-r2','B2b-r3',False,False),('B2b-r2','B2a-r3',False,True),('B2b-r2','B2a-r4',False,False),
         ('B2b-r2','B2c',False,True),('B4c','C1a-01',True,True),('B4c','C1a-02',True,False),('B4c','C1a-01-p2',True,False)]
  with tempfile.TemporaryDirectory(prefix='order-parity-',dir=ROOT) as tmp:
   root=Path(tmp);atomic(root/'DROPS/ORDER.tsv','stage\n'+'\n'.join(self.stages)+'\n')
   for previous,leg,finished,allowed in cases:
    with self.subTest(previous=previous,leg=leg):
     stage=study.descriptor(previous)['stage'];label=stage+'.'+previous
     marker=root/'CONTROL/stage-state'/stage/'FINISHED'
     if finished:atomic(marker,label+'\n')
     else:marker.unlink(missing_ok=True)
     state=self.state(stage,previous)
     if finished:state['finished_stages'].append(stage)
     outcomes=[]
     for check,error in ((lambda:study.check_order(state,leg),Error),(lambda:claude.check_target(root,label,leg),claude.Error)):
      try:check();outcomes.append(True)
      except error:outcomes.append(False)
     self.assertEqual(outcomes,[allowed,allowed])

class WorkflowTests(unittest.TestCase):
 def setUp(self):
  self.tag='wf-'+uuid.uuid4().hex[:8];self.run=self.tag;self.root=DATA/'runs'/self.tag;self.root.mkdir(parents=True);self.temp=tempfile.TemporaryDirectory(dir=TMP);self.ws=Path(self.temp.name)/'ws';(self.ws/'out').mkdir(parents=True);self.instances=[]
  copy_tree(study.INSTRUMENT/'tools',self.root/'trusted');write(self.root/'trusted-hashes.json',inventory(self.root/'trusted'))
  shutil.copy2(study.HARNESS/'arm.codex.json',self.root/'arm.json')
  (self.root/'drops/A1/stages').mkdir(parents=True);atomic(self.root/'drops/A1/stages/STAGE-A1-test.md','Test stage')
  write(self.root/'state.json',{'id':self.tag,'active_actor':None,'latest_workspace':str(self.ws),'legs':{},'finished_stages':[],'auto_dispatch':False,'fleet_parallel':2})
  self.fake=str(CODEX/'runtime/tests/fake_codex.py')
 def tearDown(self):
  for a in self.instances:a.release()
  for base in ('actors','checkpoints','dispatches'):
   for p in (DATA/base).glob(self.tag+'*'):shutil.rmtree(p)
  for p in (DATA/'actors').glob('probe-*'):
   s=read(p/'state.json',{})
   if str(s.get('parent_checkpoint','')).startswith(self.tag):shutil.rmtree(p)
  for p in (DATA/'checkpoints').glob('probe-*'):
   s=read(p/'receipt.json',{})
   if str(s.get('parent','')).startswith(self.tag):shutil.rmtree(p)
  shutil.rmtree(self.root);self.temp.cleanup()
 def register(self,aid):
  a=actors.Actor(aid);self.instances.append(a);return a
 def prepare(self,leg):
  with patch('runtime.actors.shutil.which',return_value=self.fake):return study.prepare(self.run,leg)
 def test_stage_order_and_single_owner(self):
  with self.assertRaises(Error):self.prepare('B1a')
  with self.assertRaises(Error):self.prepare('A1b-01')
  p=self.prepare('A1a')
  with self.assertRaises(Error):self.prepare('A1a')
  with self.assertRaises(Error):self.prepare('A1b-01')
 def test_round_mismatch_refused(self):
  s=study.run_state(self.run);s['finished_stages']=['A1','B1'];s['legs']={'B2a-r1':{'leg':'B2a-r1','stage':'B2','status':'verified'}};write(self.root/'state.json',s)
  with self.assertRaisesRegex(Error,'round'):self.prepare('B2b-r2')
 def test_skipped_first_repeat_refused_before_prepare_side_effects(self):
  s=study.run_state(self.run);s['legs']={'A1a':{'leg':'A1a','stage':'A1','status':'verified'}};write(self.root/'state.json',s)
  before=inventory(self.root)
  with patch('runtime.branches.seal') as seal,patch('runtime.archive.restore') as restore,patch('runtime.actors.create') as create:
   with self.assertRaises(Error):self.prepare('A1b-02')
   seal.assert_not_called();restore.assert_not_called();create.assert_not_called()
  self.assertEqual(before,inventory(self.root))
 def test_trusted_validator_is_not_actor_copy(self):
  p=self.prepare('A1a');a=self.register(p['actor']);atomic(a.base/'workspace/tools/validate.py','raise SystemExit(0)')
  r=study.trusted(self.run,'validate.py',['A1',str(a.base/'workspace'),str(a.base/'workspace/out')],a.base/'workspace')
  self.assertNotEqual(r.returncode,0)
  atomic(self.root/'trusted/validate.py','raise SystemExit(0)')
  with self.assertRaises(Error):study.trusted(self.run,'validate.py',[],a.base/'workspace')
 def test_pause_requires_matching_continuation(self):
  s=study.run_state(self.run);s['legs']={'A1a':{'leg':'A1a','stage':'A1','status':'paused'}};write(self.root/'state.json',s)
  with self.assertRaisesRegex(Error,'paused'):self.prepare('A1b-01')
  with self.assertRaisesRegex(Error,'native checkpoint'):self.prepare('A1a-p2')
  aid=self.tag+'-paused';actors.create(aid,self.ws,'gpt-6-sol','medium',executable=self.fake)
  a=self.register(aid);a.message('PAUSED-NATIVE-HISTORY');a.wait(10);receipt=a.checkpoint()
  s['legs']['A1a']['checkpoint']=receipt['checkpoint'];write(self.root/'state.json',s)
  p=self.prepare('A1a-p2');b=self.register(p['actor']);b.message('Continue');b.wait(10)
  self.assertIn('PAUSED-NATIVE-HISTORY',b.final());self.assertIn('A1a-p2',p['actor'])
 def test_native_archive_preserves_empty_directories(self):
  aid=self.tag+'-empty';actors.create(aid,self.ws,'gpt-6-sol','medium',executable=self.fake);a=self.register(aid);a.message('hello');a.wait(10);r=a.checkpoint()
  restored=archive.restore(r['checkpoint'],self.tag+'-restored');self.assertTrue((actor_dir(restored['id'])/'workspace/out').is_dir())
 def test_completed_close_has_probe_transcript_and_archive(self):
  p=self.prepare('A1a');a=self.register(p['actor']);a.message('fixture close');a.wait(10)
  atomic(a.base/'workspace/out/_closes/A1-A1a.closed','now close\n')
  write(a.base/'workspace/RUN.json',{'legs':[{'stage':'A1','leg':'A1a','session':a.state['thread_id'],'cut':None}]})
  # The control integration uses a clean validation result. Scientific validators have
  # their own 135 planted/clean cases; they are not weakened for this test.
  original=study.trusted
  def trusted(run,tool,args,cwd):
   if tool=='validate.py':
    from subprocess import CompletedProcess
    return CompletedProcess([],0,'fixture validated','')
   return original(run,tool,args,cwd)
  with patch('runtime.study.trusted',side_effect=trusted):r=study.close(self.run,a)
  s=study.run_state(self.run);self.assertIsNone(s['active_actor']);self.assertEqual(s['legs']['A1a']['status'],'verified');self.assertTrue(s['legs']['A1a']['probe']);self.assertTrue((self.root/'sealed/_transcripts/INDEX.md').exists());self.assertTrue((DATA/'checkpoints'/r['receipt']['checkpoint']/'COMMITTED').exists())
 def test_close_requires_record_for_current_session_and_cut(self):
  p=self.prepare('A1a');a=self.register(p['actor']);a.message('fixture close');a.wait(10)
  atomic(a.base/'workspace/out/_closes/A1-A1a.closed','now close\n')
  for record in ({},{'legs':[{'stage':'A1','leg':'A1a','session':'another','cut':None}]},{'legs':[{'stage':'A1','leg':'A1a','session':a.state['thread_id'],'cut':'pause'}]}):
   with self.subTest(record=record):
    write(a.base/'workspace/RUN.json',record)
    with patch('runtime.study.trusted') as validate,patch.object(a,'checkpoint') as capture:
     with self.assertRaisesRegex(Error,'Leg record'):study.close(self.run,a)
     validate.assert_not_called();capture.assert_not_called()
 def test_independent_multipart_reader_and_recovery(self):
  pk=self.ws/'out/_packets-B3';pk.mkdir();atomic(pk/'p1.md','FIXTURE_RETURN {"position":1}\n');atomic(pk/'p2.md','FIXTURE_RETURN {"position":2}\n')
  write(pk/'MANIFEST.json',{'p1':{'group':'G1','part':1,'parts':2,'items':1},'p2':{'group':'G1','part':2,'parts':2,'items':1}})
  atomic(self.ws/'out/RETURN-B3.md','```json\n{}\nEND\n```\n');write(self.ws/'out/RETURN-B3.schema.json',{'required':['position']})
  s=study.run_state(self.run);s['legs']={'B3a':{'leg':'B3a','stage':'B3','status':'verified','cut':'packets-out'}};write(self.root/'state.json',s)
  original=fleet.one
  def fail_second(job,replica,*args):
   if replica==2:return {'status':'interrupted','error':'fixture transport interruption','coding_failure':False}
   return original(job,replica,*args)
  with patch('runtime.actors.shutil.which',return_value=self.fake),patch('runtime.fleet.one',side_effect=fail_second):
   with self.assertRaisesRegex(Error,'unresolved'):fleet.dispatch(self.run,'B3',self.register)
  blocked=study.run_state(self.run)['dispatch_blocked']
  first_before=read(DATA/'dispatches'/blocked/'jobs/G1-r1.json')
  with patch('runtime.actors.shutil.which',return_value=self.fake):r=fleet.recover(blocked,self.register)
  self.assertEqual(first_before,read(DATA/'dispatches'/blocked/'jobs/G1-r1.json'))
  self.assertTrue(r['complete']);self.assertEqual(len(r['results']),2)
  rows=[read(p) for p in (DATA/'dispatches'/r['dispatch']/'returns/G1').glob('*.meta.json')]
  self.assertEqual(len(rows),2)
  for parts in rows:self.assertEqual(parts[0]['thread_id'],parts[1]['thread_id'])
  self.assertNotEqual(rows[0][0]['thread_id'],rows[1][0]['thread_id'])
  self.assertTrue(read(Path(study.run_state(self.run)['latest_workspace'])/'out/_fleet_raw/B3/DONE')['complete'])
 def test_duplicate_handler_request_is_not_replayed(self):
  aid=self.tag+'-handler';actors.create(aid,self.ws,'gpt-6-sol','medium',role='handler',executable=self.fake);a=self.register(aid)
  import threading
  class Control:
   guard=threading.RLock();actors={aid:a};count=0
   def list(self):return {'runs':[],'actors':[],'jobs':{}}
   def action(self,data):self.count+=1;return {'ok':True}
  c=Control();write(a.base/'workspace/out/requests/one.json',{'action':'build','run':'safe'})
  bridge.tick(c);bridge.tick(c);self.assertEqual(c.count,1);self.assertEqual(read(a.base/'workspace/out/responses/one.json')['status'],'accepted')

 def test_case_cli_capture_is_resumable(self):
  from runtime.imports import capture_cli
  aid=self.tag+'-cli';actors.create(aid,self.ws,'gpt-6-sol','medium',executable=self.fake);a=self.register(aid);a.message('CLI-TEST');a.wait(10);a.release()
  receipt=capture_cli(a.base/'native',a.base/'workspace',self.fake,'gpt-6-sol','medium',a.state['thread_id'])
  captured=receipt['actor']
  try:
   restored=archive.restore(receipt['checkpoint'],self.tag+'-cli-interview');b=self.register(restored['id']);b.message('Recall');b.wait(10);self.assertIn('CLI-TEST',b.final())
  finally:
   shutil.rmtree(DATA/'actors'/captured);shutil.rmtree(DATA/'checkpoints'/receipt['checkpoint'])

 def test_next_leg_retains_native_history_and_delivery(self):
  p=self.prepare('A1a');a=self.register(p['actor']);a.message('PRIOR-LEG-NATIVE-CONTEXT');a.wait(10)
  atomic(a.base/'workspace/out/evidence.txt','saved evidence');receipt=a.checkpoint()
  s=study.run_state(self.run);s['active_actor']=None;s['legs']['A1a'].update(status='verified',checkpoint=receipt['checkpoint'])
  delivered=self.root/'delivery';copy_tree(a.base/'workspace',delivered);atomic(delivered/'out/returned.txt','controller delivery')
  s['latest_workspace']=str(delivered);write(self.root/'state.json',s)
  parent_hash=sha(DATA/'checkpoints'/receipt['checkpoint']/'agent.tar.gz')
  p2=self.prepare('A1b-01');b=self.register(p2['actor']);b.message('Continue');b.wait(10)
  self.assertIn('PRIOR-LEG-NATIVE-CONTEXT',b.final());self.assertNotEqual(a.state['thread_id'],b.state['thread_id'])
  self.assertEqual((b.base/'workspace/out/evidence.txt').read_text(),'saved evidence')
  self.assertEqual((b.base/'workspace/out/returned.txt').read_text(),'controller delivery')
  self.assertEqual(parent_hash,sha(DATA/'checkpoints'/receipt['checkpoint']/'agent.tar.gz'))
  self.assertEqual(b.state['parent_checkpoint'],receipt['checkpoint'])
  self.assertTrue((b.base/'continuation.json').is_file())
