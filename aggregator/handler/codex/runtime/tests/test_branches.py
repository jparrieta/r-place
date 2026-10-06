import base64, hashlib, json, shutil, tempfile, unittest, uuid
from pathlib import Path
from unittest.mock import patch
from runtime import actors, archive, study, branches
from runtime.common import *


class BranchTests(unittest.TestCase):
    def setUp(self):
        self.tag='branch-test-'+uuid.uuid4().hex[:8]
        self.source=self.tag+'-parent';self.child=self.tag+'-child'
        self.base=study.run_dir(self.source);self.base.mkdir(parents=True)
        self.ws=self.base/'baseline';(self.ws/'out').mkdir(parents=True)
        atomic(self.ws/'out/evidence.md','original evidence')
        atomic(self.ws/'package/data.txt','original data')
        copy_tree(study.INSTRUMENT/'tools',self.base/'trusted')
        write(self.base/'trusted-hashes.json',inventory(self.base/'trusted'))
        shutil.copy2(study.HARNESS/'arm.codex.json',self.base/'arm.json')
        for stage in ('A1','B1'):
            atomic(self.base/'drops'/stage/'stages'/('STAGE-'+stage+'-test.md'),'original '+stage)
        self.instances=[]
        self.aid=self.tag+'-actor'
        actors.create(self.aid,self.ws,'gpt-6-sol','medium',run=self.source,leg='A1c',executable=str(CODEX/'runtime/tests/fake_codex.py'))
        self.a=actors.Actor(self.aid);self.instances.append(self.a)
        self.a.message('SAVED NATIVE CONTEXT');self.a.wait(10);self.receipt=self.a.checkpoint()
        self.cp=self.receipt['checkpoint']
        state={'id':self.source,'active_actor':None,'latest_workspace':str(self.a.base/'workspace'),
               'legs':{'A1c':{'actor':self.aid,'leg':'A1c','stage':'A1','status':'verified','checkpoint':self.cp}},
               'finished_stages':['A1'],'auto_dispatch':False,'fleet_parallel':1,'fleet_arm':'codex'}
        write(self.base/'state.json',state)
    def tearDown(self):
        for a in self.instances:a.release()
        for group in ('runs','actors','checkpoints'):
            for p in (DATA/group).glob(self.tag+'*'):shutil.rmtree(p)
    def fork(self):return branches.create(self.source,self.cp,self.child,'B1a')
    def put(self,path,content,stage=None):
        content=content.encode()
        return branches.upload(self.child,path,base64.b64encode(content).decode(),0,len(content),hashlib.sha256(content).hexdigest(),stage)
    def test_idle_fork_upload_prepare_continuity_and_parent_unchanged(self):
        before=inventory(self.base);parent_hash=sha(DATA/'checkpoints'/self.cp/'agent.tar.gz')
        with patch.object(actors.Actor,'message',side_effect=AssertionError('No model turn during setup')):
            result=self.fork();self.assertFalse(result['new_turn_started'])
            self.put('stages/STAGE-B1-test.md','revised B1','B1')
            self.put('package/data.txt','revised data')
            self.assertEqual(branches.inspect(self.child)['branch']['status'],'draft')
            prepared=study.prepare(self.child,'B1a')
        a=actors.Actor(prepared['actor']);self.instances.append(a)
        self.assertEqual((a.base/'workspace/package/data.txt').read_text(),'revised data')
        self.assertEqual((a.base/'workspace/stages/STAGE-B1-test.md').read_text(),'revised B1')
        self.assertIn('supersede remembered',prepared['prompt'])
        a.message(prepared['prompt']);a.wait(10);self.assertIn('SAVED NATIVE CONTEXT',a.final())
        self.assertNotEqual(a.state['thread_id'],self.a.state['thread_id'])
        self.assertEqual(before,inventory(self.base));self.assertEqual(parent_hash,sha(DATA/'checkpoints'/self.cp/'agent.tar.gz'))
        with self.assertRaisesRegex(Error,'sealed'):self.put('package/data.txt','too late')
    def test_future_cards_delivered_only_at_their_stage(self):
        self.fork();self.put('stages/STAGE-B1-test.md','branch B1','B1')
        atomic(study.run_dir(self.child)/'drops/C1/stages/STAGE-C1-test.md','unrecorded')
        with self.assertRaisesRegex(Error,'outside recorded'):study.prepare(self.child,'B1a')
    def test_c1_then_c2_keep_new_cards_data_history_and_parent(self):
        self.a.state['leg']='B4c';self.a.save();self.a.message('BEFORE C1');self.a.wait(10)
        self.cp=self.a.checkpoint()['checkpoint']
        s=study.run_state(self.source);s['legs']={'B4c':{'actor':self.aid,'leg':'B4c','stage':'B4','status':'verified','checkpoint':self.cp}};s['finished_stages']=['B4'];write(self.base/'state.json',s)
        for stage in ('C1','C2'):
            atomic(self.base/'drops'/stage/'stages'/('STAGE-'+stage+'-test.md'),'original '+stage)
        original=inventory(self.base)
        with self.assertRaisesRegex(Error,'first|count'):branches.create(self.source,self.cp,self.child,'C1a-02')
        self.assertFalse(study.run_dir(self.child).exists());self.assertEqual(original,inventory(self.base))
        branches.create(self.source,self.cp,self.child,'C1a-01')
        self.put('stages/STAGE-C1-test.md','new C1 card','C1');self.put('stages/STAGE-C2-test.md','new C2 card','C2')
        self.put('package/data.txt','branch data')
        p=study.prepare(self.child,'C1a-01');c1=actors.Actor(p['actor']);self.instances.append(c1)
        self.assertEqual((c1.base/'workspace/stages/STAGE-C1-test.md').read_text(),'new C1 card')
        self.assertFalse((c1.base/'workspace/stages/STAGE-C2-test.md').exists())
        c1.message('NEW C1 FINDING');c1.wait(10);receipt=c1.checkpoint()
        manifest=archive.verify(DATA/'checkpoints'/receipt['checkpoint']/'agent.tar.gz')
        self.assertIn('study/drops/C2/stages/STAGE-C2-test.md',manifest['files'])
        state=study.run_state(self.child);state['active_actor']=None;state['finished_stages'].append('C1');state['legs']['C1a-01'].update(status='verified',checkpoint=receipt['checkpoint']);write(study.run_dir(self.child)/'state.json',state)
        p=study.prepare(self.child,'C2a-01');c2=actors.Actor(p['actor']);self.instances.append(c2)
        self.assertEqual((c2.base/'workspace/stages/STAGE-C2-test.md').read_text(),'new C2 card')
        self.assertEqual((c2.base/'workspace/package/data.txt').read_text(),'branch data')
        self.assertFalse(c2.state['leg_started'])
        c2.message('Continue with new C2');c2.wait(10);self.assertIn('NEW C1 FINDING',c2.final())
        self.assertEqual(original,inventory(self.base))
    def test_cannot_select_an_interview_or_reverse_completed_stage(self):
        with self.assertRaisesRegex(Error,'finished'):branches.create(self.source,self.cp,self.child,'A1a')
        self.assertFalse(study.run_dir(self.child).exists())
        s=study.run_state(self.source);s['legs']['A1c']['status']='paused';write(self.base/'state.json',s)
        with self.assertRaisesRegex(Error,'verified'):self.fork()
    def test_upload_traversal_control_and_past_stage_rejected(self):
        self.fork()
        for path,stage in (('../x',None),('out/_closes/fake',None),('tools/validate.py',None),('package/auth.json',None),('stages/STAGE-A1-test.md','A1'),('stages/WRONG.md','B1')):
            with self.subTest(path=path),self.assertRaises(Error):self.put(path,'bad',stage)
        self.assertEqual(branches.inspect(self.child)['pending_uploads'],[])
    def test_chunked_upload_blocks_preparation_and_rejects_duplicate_chunk(self):
        self.fork();body=b'x'*(branches.CHUNK+7);digest=hashlib.sha256(body).hexdigest()
        first=base64.b64encode(body[:branches.CHUNK]).decode()
        branches.upload(self.child,'package/large.txt',first,0,len(body),digest)
        with self.assertRaisesRegex(Error,'pending upload'):study.prepare(self.child,'B1a')
        with self.assertRaisesRegex(Error,'pending'):branches.upload(self.child,'package/large.txt',first,0,len(body),digest)
        branches.upload(self.child,'package/large.txt',base64.b64encode(body[branches.CHUNK:]).decode(),branches.CHUNK,len(body),digest)
        self.assertEqual((study.run_dir(self.child)/'baseline/package/large.txt').read_bytes(),body)
        self.assertEqual(branches.inspect(self.child)['pending_uploads'],[])
    def test_bad_upload_can_be_set_aside_without_changing_data(self):
        self.fork()
        with self.assertRaisesRegex(Error,'hash mismatch'):
            branches.upload(self.child,'package/data.txt',base64.b64encode(b'wrong').decode(),0,5,'0'*64)
        preserved=branches.cancel_upload(self.child,'package/data.txt')
        self.assertTrue(Path(preserved['preserved']).is_dir())
        self.assertEqual(branches.inspect(self.child)['pending_uploads'],[])
        self.put('package/data.txt','good')
        self.assertEqual((study.run_dir(self.child)/'baseline/package/data.txt').read_text(),'good')
    def test_future_history_and_probe_files_not_inherited(self):
        s=study.run_state(self.source);s['legs']['B1a']={'leg':'B1a','stage':'B1','status':'verified','checkpoint':'future'};s['finished_stages'].append('B1');write(self.base/'state.json',s)
        atomic(self.base/'sealed/_transcripts/A1c.json','earlier');atomic(self.base/'sealed/_transcripts/B1a.json','future')
        atomic(self.base/'sealed/_probe/A1-A1c.questions.md','earlier');atomic(self.base/'sealed/_probe/B1-B1a.questions.md','future')
        self.fork();child=study.run_state(self.child)
        self.assertEqual(list(child['legs']),['A1c']);self.assertEqual(child['finished_stages'],['A1'])
        self.assertFalse((study.run_dir(self.child)/'sealed/_transcripts/B1a.json').exists())
        self.assertFalse((study.run_dir(self.child)/'sealed/_probe/B1-B1a.questions.md').exists())
