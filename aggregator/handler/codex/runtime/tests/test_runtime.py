import concurrent.futures, io, json, os, shutil, tarfile, tempfile, time, unittest, uuid
from pathlib import Path
from runtime import actors, archive, study
from runtime.common import DATA, ROOT, REPO, CODEX, Error, inside, inventory, lock, read, write, sha

class RuntimeTests(unittest.TestCase):
 def setUp(self):
  (ROOT/'_codex_migration/scratch').mkdir(parents=True,exist_ok=True)
  self.aids=[];self.checkpoints=[];self.temporary=tempfile.TemporaryDirectory(dir=ROOT/'_codex_migration/scratch');self.ws=Path(self.temporary.name)/'workspace';(self.ws/'out').mkdir(parents=True);(self.ws/'out/sentinel.txt').write_text('fixed file');self.live=[]
 def tearDown(self):
  for a in self.live:a.release()
  for aid in self.aids:shutil.rmtree(DATA/'actors'/aid,ignore_errors=True)
  for ck in self.checkpoints:shutil.rmtree(DATA/'checkpoints'/ck,ignore_errors=True)
  self.temporary.cleanup()
 def actor(self):
  aid='test-'+uuid.uuid4().hex[:14];self.aids.append(aid)
  actors.create(aid,self.ws,'gpt-6-sol','medium',executable=str(CODEX/'runtime/tests/fake_codex.py'))
  a=actors.Actor(aid);self.live.append(a);return a
 def save(self,a):
  r=a.checkpoint();self.checkpoints.append(r['checkpoint']);return r
 def test_escape_rejected(self):
  with self.assertRaises(Error):inside(ROOT.parent/'outside')
 def test_symlink_rejected(self):
  (self.ws/'outside').symlink_to(ROOT.parent)
  with self.assertRaises(Error):inventory(self.ws)
 def test_atomic_actor_ownership(self):
  a=self.actor();a.open();other=actors.Actor(a.state['id'])
  with self.assertRaises(Error):other.open()
 def test_native_roundtrip_and_interview_of_interview(self):
  a=self.actor();a.message('Remember BLUE-OTTER');a.wait(15);first_tid=a.state['thread_id'];r=self.save(a)
  self.assertEqual(sha(DATA/'checkpoints'/r['checkpoint']/'agent.tar.gz'),r['sha256'])
  for n in range(2):
   aid='test-restore-'+uuid.uuid4().hex[:10];self.aids.append(aid);state=archive.restore(r['checkpoint'],aid);b=actors.Actor(aid);self.live.append(b)
   self.assertEqual((b.base/'workspace/out/sentinel.txt').read_text(),'fixed file');b.message('Which sentinel?');b.wait(15)
   self.assertNotEqual(first_tid,b.state['thread_id']);self.assertIn('BLUE-OTTER',b.final());first_tid=b.state['thread_id'];r=self.save(b)
 def test_secret_not_archived(self):
  a=self.actor();a.message('Hello');a.wait(15);a.release();(a.base/'native/auth.json').write_text('never archive me');r=self.save(a)
  m=archive.verify(DATA/'checkpoints'/r['checkpoint']/'agent.tar.gz');self.assertFalse(any(p.endswith('auth.json') for p in m['files']))
 def test_parent_immutable(self):
  a=self.actor();a.message('hello');a.wait(15);r=self.save(a);arc=DATA/'checkpoints'/r['checkpoint']/'agent.tar.gz';old=sha(arc)
  aid='test-child-'+uuid.uuid4().hex[:10];self.aids.append(aid);archive.restore(r['checkpoint'],aid);(DATA/'actors'/aid/'workspace/out/sentinel.txt').write_text('changed');self.assertEqual(sha(arc),old)
 def test_archive_tamper(self):
  a=self.actor();a.message('hello');a.wait(15);r=self.save(a);arc=DATA/'checkpoints'/r['checkpoint']/'agent.tar.gz'
  with arc.open('ab') as f:f.write(b'bad')
  aid='test-bad-'+uuid.uuid4().hex[:10]
  with self.assertRaises(Error):archive.restore(r['checkpoint'],aid)
 def test_archive_path_traversal(self):
  bad=Path(self.temporary.name)/'evil.tar.gz'
  with tarfile.open(bad,'w:gz') as tf:
   info=tarfile.TarInfo('../bad');info.size=1;tf.addfile(info,io.BytesIO(b'x'))
  with self.assertRaises(Error):archive.verify(bad)
 def test_independent_agents_concurrent(self):
  a,b=self.actor(),self.actor()
  def run(actor,text):actor.message(text);actor.wait(15);return actor.final()
  with concurrent.futures.ThreadPoolExecutor(2) as pool:
   fa=pool.submit(run,a,'ALPHA');fb=pool.submit(run,b,'BETA');ra,rb=fa.result(),fb.result()
  self.assertNotIn('BETA',ra);self.assertNotIn('ALPHA',rb)
 def test_stage_identifiers(self):
  self.assertEqual(study.descriptor('B2a-r1')['round'],'1')
  with self.assertRaises(ValueError):study.descriptor('B1b')
 def question(self,a):
  a.message('ASK_PI');deadline=time.monotonic()+10
  while not a.state.get('questions') and time.monotonic()<deadline:time.sleep(.01)
  self.assertTrue(a.state.get('questions'));return a.state['questions'][0]
 def test_live_question_waits_and_answer_completes_same_turn(self):
  a=self.actor();q=self.question(a);turn=a.state['active_turn_id'];time.sleep(.1)
  self.assertEqual(read(a.base/'state.json')['questions'][0]['requestKey'],q['requestKey'])
  self.assertEqual(a.state['active_turn_id'],turn)
  result=a.answer(q['requestKey'],{'choice':'Use the second, with this qualification.'})
  self.assertFalse(result['new_turn_started']);a.wait(10)
  self.assertEqual(a.state['last_turn_id'],turn);self.assertIn('qualification',a.final());self.assertEqual(a.state['questions'],[])
  with self.assertRaises(Error):a.answer(q['requestKey'],{'choice':'A'})
 def test_questions_reject_empty_wrong_actor_and_unscoped_answers(self):
  a,b=self.actor(),self.actor();q=self.question(a);self.question(b)
  for bad in ({},{'wrong':'A'},{'choice':''}):
   with self.assertRaises(Error):a.answer(q['requestKey'],bad)
  with self.assertRaises(Error):b.answer(q['requestKey'],{'choice':'A'})
  with self.assertRaises(Error):a.message('Pretend this answered it')
  a.interrupt();b.interrupt()
 def test_interrupt_preserves_question_log_and_rejects_late_reply(self):
  a=self.actor();q=self.question(a);a.interrupt()
  self.assertEqual(a.state['boundary'],'interrupted');self.assertEqual(a.state['questions'],[])
  self.assertIn('Which interpretation?',(a.base/'events.jsonl').read_text())
  with self.assertRaises(Error):a.answer(q['requestKey'],{'choice':'A'})
 def test_question_route_does_not_accept_permissions_or_credentials(self):
  a=self.actor();a.open()
  self.assertFalse(a.server.question_request({'id':1,'method':'item/permissions/requestApproval','params':{}}))
  self.assertFalse(a.server.question_request({'id':2,'method':'item/tool/requestUserInput','params':{'questions':[{'id':'secret','isSecret':True}]}}))
 def test_dispatch_marker_validation(self):
  validator=study.load_module(REPO/'aggregator/instrument/tools/fleet.py','test_fleet')
  rows,why=validator.validate('{"position":1}\nEND','END',{'required':['position']},2,{'count_key':'position'})
  self.assertIsNone(rows);self.assertIn('expected',why)
