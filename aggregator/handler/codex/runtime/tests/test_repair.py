"""Regressions for independently found control, continuation and retention defects."""
import concurrent.futures, json, shutil, subprocess, sys, tempfile, threading, unittest, uuid
from pathlib import Path
from unittest.mock import patch, Mock
from runtime import actors,archive,study,fleet,labelers,server,plans,cancellation,retention,native,acceptance,bridge
from runtime.common import *

class RepairTests(unittest.TestCase):
 def setUp(self):
  TMP.mkdir(parents=True,exist_ok=True);self.tag='repair-'+uuid.uuid4().hex[:8]
  self.temp=tempfile.TemporaryDirectory(dir=TMP);self.ws=Path(self.temp.name)/'ws';(self.ws/'out').mkdir(parents=True)
  atomic(self.ws/'out/sentinel.txt','preserved scientific data');self.live=[];self.controllers=[]
  self.fake=str(CODEX/'runtime/tests/fake_codex.py')
 def tearDown(self):
  for a in self.live:a.release()
  for c in self.controllers:
   c.pool.shutdown(wait=True,cancel_futures=True);c.control_pool.shutdown(wait=True,cancel_futures=True)
   for jid in c.jobs:(DATA/'jobs'/(jid+'.json')).unlink(missing_ok=True)
  for name in ('actors','checkpoints','runs','dispatches'):
   for path in (DATA/name).glob(self.tag+'*'):shutil.rmtree(path)
  self.temp.cleanup()
 def actor(self,suffix='a',role='aggregator',run=None):
  aid=self.tag+'-'+suffix;actors.create(aid,self.ws,'gpt-6-sol','medium',role=role,run=run,leg='A1a',executable=self.fake)
  a=actors.Actor(aid);self.live.append(a);return a
 def controller(self,*instances):
  c=server.Controller.__new__(server.Controller);c.guard=threading.RLock();c.controls={};c.closing=set();c.stopping=threading.Event();c.jobs={};c.actors={a.state['id']:a for a in instances};c.pool=concurrent.futures.ThreadPoolExecutor(max_workers=2);c.control_pool=concurrent.futures.ThreadPoolExecutor(max_workers=2);self.controllers.append(c);return c
 def state(self,**extra):
  s={'id':self.tag,'active_actor':None,'dispatch_active':None,'latest_workspace':str(self.ws),'legs':{},'fleet_parallel':1,'finished_stages':[]}
  s.update(extra);write(study.run_dir(self.tag)/'state.json',s);return s
 def test_rejected_question_reply_does_not_stop_block(self):
  a=self.actor(run=self.tag);self.state(active_actor=a.state['id']);c=self.controller(a)
  with patch.object(a,'answer',side_effect=Error('Question expired')),patch.object(server.blocks,'stop') as stop:
   with self.assertRaisesRegex(Error,'expired'):c.action({'action':'answer','actor':a.state['id'],'request':'stale','answers':{'choice':'A'}})
   stop.assert_not_called()
 def test_restart_keeps_question_history_but_removes_dead_request(self):
  root=Path(self.temp.name)/'isolated';p=root/'actors/old/state.json'
  write(p,{'id':'old','questions':[{'requestKey':'gone','questions':[{'question':'Which scope?'}]}],'active_turn_id':'old-turn','boundary':'completed'})
  with patch.object(server,'DATA',root),patch.object(server.blocks,'pause_restart'),patch.object(server.bridge,'watch'):
   c=server.Controller();self.controllers.append(c);c.stopping.set();c.watcher.join(2)
  state=read(p);self.assertEqual(state['questions'],[]);self.assertIsNone(state['active_turn_id']);self.assertEqual(state['status'],'interrupted');self.assertEqual(state['boundary'],'interrupted')
  self.assertIn('Which scope?',(p.parent/'events.jsonl').read_text());self.assertIn('Send a message',state['error'])
 def saved(self,**kwargs):
  a=self.actor(**kwargs);a.message('original conversation');a.wait(10);r=a.checkpoint();return a,r
 def test_saved_and_closing_pause_refused_without_parent_mutation(self):
  a=self.actor(run=self.tag);self.state();c=self.controller(a)
  with patch.object(a,'message') as message:
   with self.assertRaisesRegex(Error,'saved'):c.action({'action':'pause','actor':a.state['id']})
   self.assertFalse((a.base/'workspace/out/PAUSE').exists());message.assert_not_called()
   self.state(active_actor=a.state['id']);c.closing.add(a.state['id'])
   with self.assertRaisesRegex(Error,'closure'):c.action({'action':'pause','actor':a.state['id']})
   message.assert_not_called()
 def test_reader_pause_never_changes_scientific_prompt(self):
  a=self.actor(role='reader');c=self.controller(a)
  with patch.object(a,'message') as message:
   c.action({'action':'pause','actor':a.state['id']});message.assert_not_called()
  self.assertTrue((a.base/'workspace/out/PAUSE').is_file())
 def test_actor_controls_are_atomic_between_threads(self):
  a=self.actor();c=self.controller(a);entered=threading.Event();release=threading.Event()
  def hold():
   with c.control(a.state['id']):entered.set();release.wait(10)
  thread=threading.Thread(target=hold);thread.start();entered.wait(10)
  try:
   with self.assertRaisesRegex(Error,'in progress'):c.action({'action':'pause','actor':a.state['id']})
  finally:release.set();thread.join()
 def test_blocked_and_planned_studies_refuse_fresh_dispatch(self):
  self.state(dispatch_blocked='existing')
  with self.assertRaises(Error):fleet.dispatch(self.tag,'B3',lambda _:None)
  self.state(dispatch_plan=plans.new('D1','D1a'))
  with self.assertRaisesRegex(Error,'plan owns'):fleet.dispatch(self.tag,'D2',lambda _:None)
  with self.assertRaisesRegex(Error,'plan owns'):labelers.dispatch(self.tag,lambda _:None)
 def test_durable_plan_recovers_labelers_then_verdicts_without_replay(self):
  self.state(dispatch_plan=plans.new('D1','D1a'));did=self.tag+'-labels';called=[]
  def initial(run,register,recheck=False,phase=None):
   s=study.run_state(run);plans.claim(s,'labelers','D2',did,phase);s['dispatch_blocked']=did;write(study.run_dir(run)/'state.json',s)
   write(DATA/'dispatches'/did/'input.json',{'run':run,'room_names':['example']});called.append('labels-start');raise Error('mechanical stop')
  with patch.object(labelers,'dispatch',side_effect=initial):
   with self.assertRaisesRegex(Error,'mechanical'):plans.resume(self.tag,lambda _:None)
  def recover(dispatch,register,reset_stop=False):
   self.assertEqual(dispatch,did);s=study.run_state(self.tag);s.pop('dispatch_blocked');plans.complete(s,did);write(study.run_dir(self.tag)/'state.json',s);called.append('labels-recovered')
  def verdicts(run,stage,register,round=None,phase=None):
   s=study.run_state(run);plans.claim(s,'fleet','D2',self.tag+'-verdicts',phase);plans.complete(s,self.tag+'-verdicts');write(study.run_dir(run)/'state.json',s);called.append('verdicts')
  with patch.object(fleet,'recover',side_effect=recover),patch.object(fleet,'dispatch',side_effect=verdicts):plans.recover(did,lambda _:None)
  self.assertEqual(called,['labels-start','labels-recovered','verdicts']);self.assertFalse(plans.pending(study.run_state(self.tag)))
 def test_b2_plan_remembers_three_rounds(self):
  self.assertEqual([p['round'] for p in plans.new('B2','B2c')['phases']],['gold','stab-1','stab-2'])
 def test_cancelled_cohort_never_admits_pending_workers(self):
  root=DATA/'dispatches'/(self.tag+'-cancel');root.mkdir(parents=True);token=cancellation.gate(root);seen=[]
  def work(i):seen.append(i);token.cancel('test stop');return i
  with self.assertRaisesRegex(Error,'stopped'):cancellation.bounded(range(20),work,1,token)
  self.assertEqual(seen,[0])
  with self.assertRaises(Error):token.call(lambda:seen.append('late'))
  self.assertEqual(seen,[0]);cancellation.reset(root).check()
 def test_actor_stop_latches_before_checkpoint_job_is_queued(self):
  a=self.actor(run=self.tag);self.state(active_actor=a.state['id']);c=self.controller(a)
  with patch.object(c,'job',return_value={'job':'delayed'}) as job:
   result=c.action({'action':'stop','actor':a.state['id']})
  self.assertEqual(result,{'job':'delayed'});job.assert_called_once()
  with self.assertRaisesRegex(Error,'stopped'):cancellation.run_stopped(self.tag)
 def test_urgent_stop_job_runs_when_study_pool_is_full(self):
  c=self.controller();release=threading.Event();entered=[threading.Event(),threading.Event()];stopped=threading.Event()
  def busy(index):entered[index].set();release.wait(10)
  for index in range(2):c.job(busy,index)
  try:
   self.assertTrue(all(event.wait(5) for event in entered));c.job(stopped.set,urgent=True)
   self.assertTrue(stopped.wait(3),'Stop must not queue behind long-running studies')
  finally:release.set()
 def test_shutdown_refuses_late_actor_registration(self):
  c=self.controller();c.stopping.set()
  with self.assertRaisesRegex(Error,'stopping'):c.actor(self.tag+'-late')
  with self.assertRaisesRegex(Error,'stopping'):c.job(lambda:None)
 def test_verified_eviction_restores_history_and_files(self):
  a,r=self.saved();retention.ready(a.state['id']);result=retention.evict(a.state['id'])
  self.assertTrue(result['evicted']);self.assertFalse((a.base/'workspace').exists());self.assertTrue((DATA/'checkpoints'/r['checkpoint']/'COMMITTED').exists())
  with self.assertRaisesRegex(Error,'archived'):a.open()
  st=archive.restore(r['checkpoint'],self.tag+'-restored');b=actors.Actor(st['id']);self.live.append(b)
  self.assertEqual((b.base/'workspace/out/sentinel.txt').read_text(),'preserved scientific data')
  b.message('Continue');b.wait(10);self.assertIn('original conversation',b.final())
 def test_eviction_refuses_changed_current_interrupted_and_lead_stores(self):
  a,r=self.saved();retention.ready(a.state['id']);self.state(latest_workspace=str(a.base/'workspace'))
  self.assertFalse(retention.evict(a.state['id'])['evicted'])
  self.state();atomic(a.base/'workspace/out/new.txt','not archived')
  with self.assertRaisesRegex(Error,'differ'):retention.evict(a.state['id'])
  (a.base/'workspace/out/new.txt').unlink();s=actor_state(a.state['id']);s['boundary']='interrupted';write(a.base/'state.json',s)
  self.assertFalse(retention.evict(a.state['id'])['evicted']);s.update(boundary='completed',role='case-lead');write(a.base/'state.json',s)
  self.assertFalse(retention.evict(a.state['id'])['evicted'])
 def test_eviction_rejects_tampered_checkpoint_without_deleting_store(self):
  a,r=self.saved();retention.ready(a.state['id']);atomic(DATA/'checkpoints'/r['checkpoint']/'COMMITTED','bad')
  with self.assertRaisesRegex(Error,'hash'):retention.evict(a.state['id'])
  self.assertTrue((a.base/'workspace/out/sentinel.txt').is_file())
 def test_handler_continuation_is_operational_and_does_not_replay_requests(self):
  a=self.actor(role='handler');write(a.base/'workspace/out/requests/old.json',{'action':'build','run':'never-replay'})
  a.message('handler history');a.wait(10);r=a.checkpoint();c=self.controller(a)
  state=c.continue_handler(r['checkpoint'],self.tag+'-handler2');self.assertEqual(state['role'],'handler')
  self.assertTrue((actor_dir(state['id'])/'mailbox/old.json').exists());self.assertTrue(actor_state(a.state['id'])['handler_retired'])
  with self.assertRaisesRegex(Error,'continued elsewhere'):a.open()
  h=actors.Actor(state['id']);self.live.append(h);c.actors[h.state['id']]=h
  with patch.object(c,'action') as action:bridge.tick(c);action.assert_not_called()
  with self.assertRaisesRegex(Error,'already has'):c.continue_handler(r['checkpoint'],self.tag+'-handler3')
 def test_handler_continuation_rejects_nonhandler_checkpoint(self):
  a,r=self.saved();c=self.controller(a)
  with self.assertRaisesRegex(Error,'not a native handler'):c.continue_handler(r['checkpoint'])
 def test_callback_errors_are_visible_in_status(self):
  a=self.actor();write(a.base/'callback-error.json',{'error':'disk failure'});c=self.controller(a)
  self.assertTrue(any(e.get('error')=='disk failure' for e in c.list()['errors']))
 def test_native_acceptance_secrets_are_independent_before_any_model_call(self):
  # Fail deliberately before transport; capture the two independently created values.
  seen={}
  def create(aid,ws,*args,**kwargs):seen['file']=(ws/'out/payload.txt').read_text();seen['aid']=aid
  class NoHistory:
   state={'boundary':'completed'}
   def __init__(self,aid):pass
   def message(self,text):seen['prompt']=text;raise Error('no model called')
   def release(self):pass
  with patch.object(acceptance.actors,'create',side_effect=create),patch.object(acceptance.actors,'Actor',NoHistory),patch.object(Path,'is_file',return_value=True):
   result=acceptance.live()
  self.assertFalse(result['passed']);self.assertNotIn(seen['file'].removeprefix('filesystem-'),seen['prompt'])
  (DATA/'acceptance'/(seen['aid']+'.json')).unlink()
 def test_rehashed_analyst_receipt_cannot_change_trusted_d3_d4_freeze(self):
  atomic(self.ws/'out/model/elements.jsonl','original model\n');atomic(self.ws/'out/branches.jsonl','original branches\n')
  a,r=self.saved();state=self.state(legs={'D3c':{'stage':'D3','status':'verified','checkpoint':r['checkpoint']},'D4a-01':{'stage':'D4','status':'verified','checkpoint':r['checkpoint']}})
  trust=study.run_dir(self.tag)/'trusted';copy_tree(study.INSTRUMENT/'tools',trust);write(study.run_dir(self.tag)/'trusted-hashes.json',inventory(trust))
  study.frozen_inputs(self.tag,state,a.base/'workspace')
  atomic(a.base/'workspace/out/branches.jsonl','different branches\n');atomic(a.base/'workspace/out/_closes/tree-D4.sha256','rehashed by analyst\n')
  with self.assertRaisesRegex(Error,'Frozen D4'):study.frozen_inputs(self.tag,state,a.base/'workspace')
  atomic(a.base/'workspace/out/branches.jsonl','original branches\n');atomic(a.base/'workspace/out/model/new-elements.jsonl','undeclared addition\n')
  with self.assertRaisesRegex(Error,'Frozen D3'):study.frozen_inputs(self.tag,state,a.base/'workspace')

 def test_api_acceptance_secrets_are_independent_before_any_model_call(self):
  from runtime import arms,openrouter
  seen={}
  def create(aid,ws,*args,**kwargs):seen['file']=(ws/'out/payload.txt').read_text();seen['aid']=aid
  class NoHistory:
   state={'boundary':'completed'}
   def message(self,text):seen['prompt']=text;raise Error('no model called')
   def release(self):pass
  config={'B3':{'readers':{'model':'test/model','effort':'low'}}}
  with patch.object(openrouter,'key'),patch.object(arms,'resolve',return_value=[config]),patch.object(openrouter,'bind',return_value={}),patch.object(openrouter,'create',side_effect=create),patch.object(actors,'load',return_value=NoHistory()):
   result=acceptance.live_openrouter()
  self.assertFalse(result['passed']);self.assertNotIn(seen['file'].removeprefix('filesystem-'),seen['prompt'])
  shutil.rmtree(DATA/'acceptance'/seen['aid'])

 def test_idle_pause_never_starts_native_turn(self):
  a=self.actor();c=self.controller(a)
  with patch.object(a,'message') as message,patch.object(a,'open') as opened:
   result=c.action({'action':'pause','actor':a.state['id']})
   self.assertFalse(result['new_turn_started']);message.assert_not_called();opened.assert_not_called()
  self.assertTrue((a.base/'workspace/out/PAUSE').exists())
 def test_start_is_once_and_failed_delivery_is_not_replayed(self):
  a=self.actor(run=self.tag);self.state(active_actor=a.state['id'],legs={'A1a':{'status':'prepared'}});c=self.controller(a)
  atomic(a.base/'first-message.txt','First prompt')
  with patch.object(a,'message',side_effect=Error('transport outcome unknown')) as message:
   with self.assertRaisesRegex(Error,'transport'):c.action({'action':'start','actor':a.state['id']})
   with self.assertRaisesRegex(Error,'already started'):c.action({'action':'start','actor':a.state['id']})
   message.assert_called_once_with('First prompt')
  self.assertTrue(actor_state(a.state['id'])['leg_started'])
 def test_restored_unstarted_leg_can_start_but_not_twice(self):
  a=self.actor(run=self.tag);a.state.update(last_turn_id='inherited',leg_started=False);a.save()
  self.state(active_actor=a.state['id'],legs={'A1a':{'status':'prepared'}});c=self.controller(a);atomic(a.base/'first-message.txt','Restored prompt')
  with patch.object(a,'message',return_value={'turn':{'id':'new'}}) as message:
   c.action({'action':'start','actor':a.state['id']})
   with self.assertRaisesRegex(Error,'already started'):c.action({'action':'start','actor':a.state['id']})
   message.assert_called_once_with('Restored prompt')
 def test_stopped_study_refuses_first_start_without_claim(self):
  a=self.actor(run=self.tag);self.state(active_actor=a.state['id'],legs={'A1a':{'status':'prepared'}});c=self.controller(a)
  atomic(a.base/'first-message.txt','First prompt');c.cancel_run(self.tag)
  with patch.object(a,'message') as message:
   with self.assertRaisesRegex(Error,'stopped'):c.action({'action':'start','actor':a.state['id']})
   message.assert_not_called()
  self.assertFalse(a.state.get('leg_started'));self.assertTrue(next(r for r in c.list()['runs'] if r['id']==self.tag)['stop'])
 def test_pending_restore_is_shared_across_repeated_requests(self):
  c=self.controller();entered=threading.Event();release=threading.Event()
  def restore(*args):entered.set();release.wait(5);return {'id':self.tag+'-restored'}
  with patch.object(archive,'restore',side_effect=restore) as called:
   try:
    one=c.action({'action':'restore','checkpoint':self.tag+'-cp'});self.assertTrue(entered.wait(3))
    two=c.action({'action':'restore','checkpoint':self.tag+'-cp'});self.assertEqual(one,two);called.assert_called_once()
    record=c.jobs[one['job']];self.assertEqual(record['request']['checkpoint'],self.tag+'-cp')
   finally:release.set();c.pool.shutdown(wait=True)
  self.assertEqual(c.jobs[one['job']]['status'],'completed');self.assertIn('started_utc',c.jobs[one['job']]);self.assertIn('finished_utc',c.jobs[one['job']])

 def test_interview_controls_never_touch_inherited_live_study(self):
  a=self.actor(role='interview');a.state.update(study_run=self.tag,dispatch_id=self.tag+'-dispatch');a.save()
  self.state();c=self.controller(a)
  with patch.object(c,'cancel_run') as cancel,patch.object(a,'checkpoint',return_value={'checkpoint':'saved'}) as capture,patch.object(a,'pause',return_value={'new_turn_started':False}):
   c.lifecycle(a.state['id'],'pause');c.action({'action':'stop','actor':a.state['id']});c.pool.shutdown(wait=True);c.control_pool.shutdown(wait=True)
   cancel.assert_not_called();capture.assert_called_once_with(interrupt=True)
  with patch.object(a,'checkpoint') as capture:c.stop_run(self.tag);capture.assert_not_called()
 def test_native_interview_restore_preserves_origin_but_not_fleet_ownership(self):
  a=self.actor(role='reader');a.state.update(study_run=self.tag,dispatch_id=self.tag+'-dispatch');a.save()
  a.message('Reader context');a.wait(10);receipt=a.checkpoint();st=archive.restore(receipt['checkpoint'],self.tag+'-interview')
  self.assertEqual(st['origin_study_run'],self.tag);self.assertEqual(st['origin_dispatch_id'],self.tag+'-dispatch')
  self.assertFalse(st.get('run'));self.assertNotIn('study_run',st);self.assertNotIn('dispatch_id',st)
 def test_pending_actor_stop_blocks_clearing_study_stop(self):
  a=self.actor(run=self.tag);self.state(active_actor=a.state['id']);c=self.controller(a);release=threading.Event();entered=threading.Event()
  def checkpoint(**kwargs):entered.set();release.wait(5);return {'checkpoint':'saved'}
  with patch.object(a,'checkpoint',side_effect=checkpoint):
   try:
    result=c.action({'action':'stop','actor':a.state['id']});self.assertTrue(entered.wait(3))
    self.assertEqual(c.jobs[result['job']]['request']['run'],self.tag)
    with self.assertRaisesRegex(Error,'still working'):c.action({'action':'continue-run','run':self.tag})
   finally:release.set();c.control_pool.shutdown(wait=True)
