import copy, io, json, shutil, tempfile, threading, unittest, uuid
from pathlib import Path
from unittest.mock import patch
from runtime import actors, archive, arms, fleet, openrouter, openrouter_http, study
from runtime.common import *

class FakeTransport:
    calls=[]; failures=0; invalid=0; fail_second=0; guard=threading.Lock()
    def __init__(self,record=None): self.cancelled=threading.Event()
    def cancel(self): self.cancelled.set()
    def call(self,path,body=None,timeout=900):
        if path.startswith('generation'): return {'data':{'model':'test/reader','provider_name':'Fixture','total_cost':0}}
        with self.guard:
            self.calls.append(copy.deepcopy(body))
            if 'PART TWO' in body['messages'][-1]['content'] and type(self).fail_second:
                type(self).fail_second-=1; raise Error('fixture interrupted second part')
            if body['model']!='@preset/cheap' and type(self).failures:
                type(self).failures-=1; raise Error('fixture 429')
            bad=body['model']!='@preset/cheap' and type(self).invalid
            if bad: type(self).invalid-=1
        last=body['messages'][-1]['content']
        text='READY' if body['model']=='@preset/cheap' else ('bad' if bad else '{"position":'+('2' if 'PART TWO' in last else '1')+'}\nEND')
        return {'id':'gen-'+uuid.uuid4().hex,'model':'test/reader','provider':'Fixture',
                'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':text,'reasoning_details':[{'type':'reasoning.encrypted','data':'opaque-fixture'}]}}],
                'usage':{'prompt_tokens':10,'completion_tokens':4,'total_tokens':14,'cost':0}}

class ArmTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True,exist_ok=True)
        self.tag='arms-'+uuid.uuid4().hex[:8]; self.base=study.run_dir(self.tag); self.base.mkdir(parents=True)
        self.temp=tempfile.TemporaryDirectory(dir=TMP); self.ws=Path(self.temp.name)/'ws'; (self.ws/'out').mkdir(parents=True)
        self.instances=[]; FakeTransport.calls=[]; FakeTransport.failures=0; FakeTransport.invalid=0; FakeTransport.fail_second=0
        self.stub=patch('runtime.openrouter.Transport',FakeTransport); self.stub.start()
        config,selection=arms.resolve('openrouter'); write(self.base/'arm.json',config); write(self.base/'fleet-arm.json',{**selection,'arm_sha256':sha(self.base/'arm.json')})
        copy_tree(study.INSTRUMENT/'tools',self.base/'trusted'); write(self.base/'trusted-hashes.json',inventory(self.base/'trusted'))
        write(self.base/'state.json',{'id':self.tag,'active_actor':None,'dispatch_active':None,'latest_workspace':str(self.ws),
            'fleet_arm':'openrouter','fleet_parallel':2,'legs':{'B3a':{'status':'verified','cut':'packets-out','stage':'B3'}},'finished_stages':[]})
        pk=self.ws/'out/_packets-B3'; pk.mkdir(); atomic(pk/'p1.md','PART ONE'); atomic(pk/'p2.md','PART TWO')
        write(pk/'MANIFEST.json',{'p1':{'group':'G1','part':1,'parts':2,'items':1},'p2':{'group':'G1','part':2,'parts':2,'items':1}})
        atomic(self.ws/'out/RETURN-B3.md','```json\n{}\nEND\n```'); write(self.ws/'out/RETURN-B3.schema.json',{'required':['position']})
    def tearDown(self):
        for instance in self.instances: instance.interrupt(); instance.release()
        self.stub.stop()
        for name in ('runs','actors','checkpoints','dispatches'):
            for p in (DATA/name).glob(self.tag+'*'): shutil.rmtree(p)
        self.temp.cleanup()
    def register(self,aid):
        result=actors.load(aid); self.instances.append(result); return result
    def test_profiles_preserve_science_and_keep_other_roles_native(self):
        a,_=arms.resolve('codex'); b,_=arms.resolve('openrouter')
        for stage in ('B2','B3','B4','D2','E1'):
            self.assertEqual(a[stage]['readers']['n'],b[stage]['readers']['n'])
            self.assertEqual(a[stage]['readers']['shared'],b[stage]['readers']['shared'])
            self.assertEqual(a[stage]['analyst'],b[stage]['analyst'])
        self.assertEqual(a['C2'],b['C2']); self.assertEqual(a['D2']['labelers'],b['D2']['labelers'])
        with self.assertRaises(Error): arms.resolve('typo')
        cfg=read(self.base/'arm.json'); cfg['B3']['readers']['model']='changed'; write(self.base/'arm.json',cfg)
        with self.assertRaisesRegex(Error,'changed'): fleet.dispatch(self.tag,'B3',self.register,dry_run=True)
    def test_dry_run_never_contacts_provider(self):
        result=fleet.dispatch(self.tag,'B3',self.register,dry_run=True)
        self.assertEqual(result['route'],'openrouter'); self.assertEqual(result['jobs'],2); self.assertFalse(FakeTransport.calls)
    def test_parallel_multipart_history_archives_and_two_interviews(self):
        result=fleet.dispatch(self.tag,'B3',self.register); self.assertTrue(result['complete'])
        calls=FakeTransport.calls
        self.assertEqual(sum(c['model']=='@preset/cheap' for c in calls),1)
        multi=[c for c in calls if len(c['messages'])==4]; self.assertEqual(len(multi),2)
        for call in multi:
            self.assertEqual(call['messages'][2]['reasoning_details'][0]['data'],'opaque-fixture')
            self.assertEqual(call['provider']['only'],['Fixture']); self.assertFalse(call['provider']['allow_fallbacks'])
            self.assertEqual(call['tool_choice'],'none')
        r1,r2=result['results']; self.assertNotEqual(r1['actor'],r2['actor'])
        first=r1['checkpoints'][-1]; original=sha(DATA/'checkpoints'/first/'agent.tar.gz')
        restored=archive.restore(first,self.tag+'-interview'); self.assertNotIn('study_run',restored); self.assertNotIn('dispatch_id',restored); self.assertEqual(restored['origin_study_run'],self.tag); agent=self.register(restored['id']); agent.message('Interview'); agent.wait()
        self.assertEqual(agent.state['boundary'],'completed'); second=agent.checkpoint()['checkpoint']
        again=archive.restore(second,self.tag+'-interview2'); agent2=self.register(again['id']); agent2.message('Follow-up'); agent2.wait()
        third=agent2.checkpoint(); self.assertEqual(third['parent'],second)
        self.assertEqual(sha(DATA/'checkpoints'/first/'agent.tar.gz'),original)
        manifest=archive.verify(DATA/'checkpoints'/third['checkpoint']/'agent.tar.gz')
        self.assertIn('workspace/packet.json',manifest['files']); self.assertIn('thread.json',manifest['files'])
        self.assertFalse(any('auth.json' in x for x in manifest['files']))
        raw=Path(study.run_state(self.tag)['latest_workspace'])/'out/_fleet_raw/B3'
        self.assertEqual(read(raw/'arm.json')['served'],'test/reader')
        self.assertEqual(read(raw/'G1/r1.meta.json')[0]['provider'],'Fixture')
    def test_interruption_preserves_other_returns_and_recovery(self):
        FakeTransport.failures=1
        with self.assertRaisesRegex(Error,'unresolved'): fleet.dispatch(self.tag,'B3',self.register)
        did=study.run_state(self.tag)['dispatch_blocked']; root=DATA/'dispatches'/did
        results=read(root/'RESULT.json')['results']; good=next(x for x in results if x['status']=='valid'); failed=next(x for x in results if x['status']=='interrupted')
        self.assertFalse(failed['coding_failure']); before=sha(root/'returns/G1'/(good['reader']+'.jsonl'))
        result=fleet.recover(did,self.register); self.assertTrue(result['complete'])
        self.assertEqual(sha(root/'returns/G1'/(good['reader']+'.jsonl')),before)
        self.assertEqual(sum(c['model']=='@preset/cheap' for c in FakeTransport.calls),1)
    def test_bad_returns_reissued_without_reusing_identity(self):
        FakeTransport.invalid=1
        result=fleet.dispatch(self.tag,'B3',self.register); root=DATA/'dispatches'/result['dispatch']
        self.assertTrue(result['complete']); self.assertEqual(len(list((root/'returns/G1').glob('*.failed.txt'))),1)
        records=[read(p) for p in (root/'jobs').glob('*.json') if not p.name.endswith('-parts.json')]
        self.assertEqual(sorted(r['status'] for r in records),['invalid','valid','valid'])
        self.assertEqual(len({r['actor'] for r in records}),3)
    def test_recovery_replays_only_the_unfinished_part(self):
        FakeTransport.fail_second=1
        with self.assertRaises(Error): fleet.dispatch(self.tag,'B3',self.register)
        did=study.run_state(self.tag)['dispatch_blocked']
        self.assertTrue(fleet.recover(did,self.register)['complete'])
        first=[c for c in FakeTransport.calls if 'PART ONE' in c['messages'][-1]['content']]
        self.assertEqual(len(first),2)
        retries=[c for c in FakeTransport.calls if 'PART TWO' in c['messages'][-1]['content']]
        self.assertEqual(len(retries),3)
        self.assertTrue(all(len(c['messages'])==4 for c in retries))
    def test_cancel_saves_interrupted_request_without_accepting_it(self):
        entered=threading.Event()
        class WaitingTransport(FakeTransport):
            def call(self,path,body=None,timeout=900):
                entered.set(); self.cancelled.wait(5); raise Error('fixture local cancellation')
        aid=self.tag+'-stop'; openrouter.create(aid,self.ws,{'model':'@preset/cheap','effort':'medium'},{'model':'test/reader','provider':'Fixture'})
        agent=self.register(aid)
        with patch('runtime.openrouter.Transport',WaitingTransport):
            agent.message('pending'); self.assertTrue(entered.wait(2)); receipt=agent.checkpoint(interrupt=True)
        self.assertEqual(receipt['boundary'],'interrupted')
        self.assertEqual(len(read(agent.base/'thread.json')['messages']),1)
        self.assertTrue((agent.base/'workspace/out/PAUSE').exists())
        self.assertTrue(list((agent.base/'turns').glob('*/request.json')))
    def test_tampered_api_archive_cannot_resume(self):
        result=fleet.dispatch(self.tag,'B3',self.register); checkpoint=result['results'][0]['checkpoints'][0]
        with (DATA/'checkpoints'/checkpoint/'agent.tar.gz').open('ab') as f: f.write(b'bad')
        with self.assertRaisesRegex(Error,'hash'): archive.restore(checkpoint,self.tag+'-bad-restore')
    def test_served_model_drift_is_mechanical_and_keeps_response(self):
        binding={'model':'expected/reader','provider':'Fixture','alias':'@preset/cheap'}; aid=self.tag+'-drift'
        openrouter.create(aid,self.ws,{'model':'@preset/cheap','effort':'medium'},binding)
        agent=self.register(aid); agent.message('Code'); agent.wait()
        self.assertEqual(agent.state['boundary'],'interrupted'); self.assertIn('differs',agent.state['error'])
        self.assertTrue(list((agent.base/'turns').glob('*/response.json')))
        receipt=agent.checkpoint(); self.assertEqual(receipt['boundary'],'interrupted')
    def test_actor_owner_and_inflight_message_rejected(self):
        aid=self.tag+'-owner'; openrouter.create(aid,self.ws,{'model':'@preset/cheap','effort':'medium'},{'model':'test/reader','provider':'Fixture'})
        agent=self.register(aid); agent.open(); other=actors.load(aid)
        with self.assertRaises(Error): other.open()
        agent.state['active_turn_id']='working'
        with self.assertRaisesRegex(Error,'in flight'): agent.message('Do not overlap')
        agent.state['active_turn_id']=None; agent.save()
    def test_metadata_non_object_does_not_crash(self):
        transport=FakeTransport()
        with patch.object(transport,'call',return_value={'data':'not-an-object'}):
            with self.assertRaisesRegex(Error,'could not be verified'): openrouter.evidence({'id':'gen-1'},transport)
    def test_build_freezes_selection_from_tiny_source(self):
        source=Path(self.temp.name)/'source'; (source/'00_GIVE-THE-AGENT/out').mkdir(parents=True); (source/'DROPS').mkdir()
        (source/'CONTROL').mkdir(); write(source/'CONTROL/sessions.json',{})
        run=self.tag+'-built'; result=study.build(run,source,'openrouter')
        self.assertEqual(result['fleet_arm'],'openrouter'); self.assertEqual(arms.frozen(study.run_dir(run))['name'],'openrouter')
        self.assertEqual(read(study.run_dir(run)/'arm.json')['B3']['readers']['route'],'openrouter')

class HTTPBoundaryTests(unittest.TestCase):
    def test_http_worker_hides_key_and_uses_fixed_https_route(self):
        secret='fixture-secret-not-a-real-key'
        reply=io.StringIO(json.dumps({'model':'test/reader','test':secret}))
        class Opener:
            def open(self,request,timeout):
                assert request.full_url=='https://openrouter.ai/api/v1/chat/completions'
                assert request.get_header('Authorization')=='Bearer '+secret
                assert json.loads(request.data)['model']=='test/reader'
                return reply
        out=io.StringIO()
        with patch('runtime.openrouter_http.urllib.request.build_opener',return_value=Opener()),patch('sys.stdin',io.StringIO(json.dumps({'key':secret,'path':'chat/completions','timeout':10,'body':{'model':'test/reader'}}))),patch('sys.stdout',out):
            openrouter_http.main()
        self.assertNotIn(secret,out.getvalue()); self.assertEqual(json.loads(out.getvalue())['data']['model'],'test/reader')
    def test_live_orphan_transport_blocks_second_owner(self):
        TMP.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TMP) as directory:
            path=Path(directory)/'process.json'; write(path,{'pid':1234,'identity':'fixture-running'})
            with patch('runtime.native.process_identity',return_value='fixture-running'):
                with self.assertRaisesRegex(Error,'second owner'): openrouter.check_process(path)
            with patch('runtime.native.process_identity',return_value=None): openrouter.check_process(path)
