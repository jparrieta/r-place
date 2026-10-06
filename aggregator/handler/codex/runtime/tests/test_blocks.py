"""Native fixture transitions, finite authorization and failure boundaries."""
import contextlib
import threading
from subprocess import CompletedProcess
from unittest.mock import patch
from runtime import blocks,study,publication
from runtime.common import *
from runtime.tests import test_workflow


class BlockTests(test_workflow.WorkflowTests):
    def setUp(self):
        super().setUp()
        first=self.prepare('A1a');a=self.register(first['actor'])
        a.message('A1a ORIGINAL NATIVE CONTEXT');a.wait(10);receipt=a.checkpoint()
        s=study.run_state(self.run);s['active_actor']=None
        s['legs']['A1a'].update(status='verified',checkpoint=receipt['checkpoint'],probe={'ok':True})
        write(self.root/'state.json',s)
        test=self
        class Controller:
            stopping=threading.Event()
            def __init__(self):self.actors={}
            def actor(self,aid):
                if aid not in self.actors:self.actors[aid]=test.register(aid)
                return self.actors[aid]
            def control(self,aid):return contextlib.nullcontext()
            def mutable(self,a,op):pass
            def close_leg(self,run,aid):
                result=study.close(run,self.actor(aid));publication.after_close(run);return result
        self.controller=Controller()
        self.exe=patch('runtime.actors.shutil.which',return_value=self.fake);self.exe.start()
        original=study.trusted
        def trusted(run,tool,args,cwd):
            if tool=='validate.py':return CompletedProcess([],0,'fixture validated','')
            return original(run,tool,args,cwd)
        self.validator=patch('runtime.study.trusted',side_effect=trusted);self.validator.start()
    def tearDown(self):
        self.validator.stop();self.exe.stop();super().tearDown()
    def tick(self):blocks.advance(self.controller,self.run)
    def finish(self,marker=True):
        b=blocks.state(self.run);a=self.controller.actor(b['actor']);a.wait(10)
        if marker:
            leg=a.state['leg'];atomic(a.base/f'workspace/out/_closes/A1-{leg}.closed','now close\n')
            write(a.base/'workspace/RUN.json',{'legs':[{'stage':'A1','leg':leg,'session':a.state['thread_id'],'cut':None}]})
        return a
    def test_two_legs_restore_history_and_stop_before_a1c(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();a=self.finish()
        self.assertIn('A1a ORIGINAL NATIVE CONTEXT',a.final())
        self.tick();self.tick();self.tick();b=self.finish()
        self.assertNotEqual(a.state['id'],b.state['id'])
        self.assertEqual(b.state['parent_checkpoint'],study.run_state(self.run)['legs']['A1b-01']['checkpoint'])
        self.tick();self.tick();self.tick()
        s=study.run_state(self.run);self.assertEqual(blocks.state(self.run)['status'],'completed')
        self.assertEqual(list(s['legs']),['A1a','A1b-01','A1b-02'])
        self.assertTrue(all(s['legs'][leg].get('probe') for leg in ('A1b-01','A1b-02')))
    def test_cross_step_interview_reverse_and_skipped_ranges_refused(self):
        for first,last in [('A1b-01','A1c'),('A1b-03','A1b-01'),('A1a','A1a'),('A1b-01-p2','A1b-02'),('A1b-01','A1b-1001')]:
            with self.subTest(first=first,last=last),self.assertRaises((Error,ValueError)):blocks.start(self.run,first,last)
        blocks.start(self.run,'A1b-01','A1b-02')
        with self.assertRaisesRegex(Error,'saved block'):blocks.start(self.run,'A1b-01','A1b-03')
        with self.assertRaisesRegex(Error,'owns'):study.prepare(self.run,'A1b-01')
    def test_stop_before_first_admission_and_resume_does_not_expand_range(self):
        blocks.start(self.run,'A1b-01','A1b-02');blocks.stop(self.run);self.tick()
        self.assertEqual(list(study.run_state(self.run)['legs']),['A1a'])
        self.assertEqual(blocks.state(self.run)['status'],'stopped')
        blocks.resume(self.run);self.tick();self.finish()
        self.assertEqual(blocks.state(self.run)['legs'],['A1b-01','A1b-02'])
    def test_stop_during_preparation_leaves_idle_actor_without_turn(self):
        blocks.start(self.run,'A1b-01','A1b-02');real=study.prepare
        def prepare(*args,**kwargs):
            result=real(*args,**kwargs);blocks.stop(self.run);return result
        with patch('runtime.study.prepare',side_effect=prepare):self.tick()
        a=actor_state(study.run_state(self.run)['active_actor'])
        self.assertFalse(a.get('leg_started'));self.assertEqual(blocks.state(self.run)['status'],'stopped')
    def test_stop_while_active_does_not_interrupt_or_start_another(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();a=self.finish()
        blocks.stop(self.run);self.tick()
        self.assertEqual(blocks.state(self.run)['status'],'stopped')
        self.controller.close_leg(self.run,a.state['id']);self.tick()
        self.assertNotIn('A1b-02',study.run_state(self.run)['legs'])
    def test_unclosed_question_blocks_without_repeated_turn(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();a=self.finish(False);turn=a.state['last_turn_id']
        self.tick();self.tick()
        self.assertEqual(blocks.state(self.run)['status'],'blocked');self.assertEqual(a.state['last_turn_id'],turn)
        self.assertIn('without a leg close',blocks.state(self.run)['reason'])
    def test_judgment_request_holds_even_with_close_marker(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();a=self.finish()
        atomic(a.base/'workspace/out/NEEDS-JUDGMENT.md','Which evidence should be used?')
        self.tick();self.assertIn('judgment',blocks.state(self.run)['reason'])
        with self.assertRaisesRegex(Error,'NEEDS-JUDGMENT'):blocks.resume(self.run)
    def test_validation_failure_is_not_retried_and_preserves_actor(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();a=self.finish()
        with patch('runtime.study.trusted',return_value=CompletedProcess([],1,'','defect')):self.tick()
        self.tick();self.assertEqual(study.run_state(self.run)['active_actor'],a.state['id'])
        self.assertEqual(blocks.state(self.run)['status'],'blocked')
        self.assertTrue((a.base/'native').is_dir())
    def test_native_start_failure_is_uncertain_and_cannot_replay(self):
        blocks.start(self.run,'A1b-01','A1b-02')
        with patch('runtime.actors.Actor.message',side_effect=Error('transport')):self.tick()
        self.assertEqual(blocks.state(self.run)['phase'],'starting')
        with self.assertRaisesRegex(Error,'Uncertain'):blocks.resume(self.run)
        # Explicit manual recovery can resolve that leg without replaying its start.
        a=self.controller.actor(blocks.state(self.run)['actor'])
        a.message('Manually inspected and recovered');a.state['leg_started']=True;a.save();self.finish()
        self.controller.close_leg(self.run,a.state['id']);blocks.resume(self.run);self.tick()
        self.assertEqual(blocks.state(self.run)['cursor'],1)
    def test_adopt_prepared_but_not_an_already_attempted_leg(self):
        first=self.prepare('A1b-01');a=self.register(first['actor'])
        a.state['leg_started']=True;a.save()
        with self.assertRaisesRegex(Error,'already started'):blocks.start(self.run,'A1b-01','A1b-02')
        a.state['leg_started']=False;a.save();blocks.start(self.run,'A1b-01','A1b-02');self.tick()
        self.assertEqual(blocks.state(self.run)['actor'],a.state['id']);self.finish()
    def test_restart_does_not_replay_authorized_admission(self):
        blocks.start(self.run,'A1b-01','A1b-02');blocks.pause_restart();self.tick()
        self.assertEqual(blocks.state(self.run)['status'],'paused')
        self.assertEqual(list(study.run_state(self.run)['legs']),['A1a'])
        blocks.resume(self.run);self.tick();self.finish()
    def test_failed_publication_and_fleet_barriers_stop_advance(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();self.finish()
        with patch('runtime.publication.after_close',side_effect=Error('push failed')):self.tick()
        self.assertEqual(study.run_state(self.run)['legs']['A1b-01']['status'],'verified')
        self.assertEqual(blocks.state(self.run)['status'],'blocked')
        s=study.run_state(self.run);s['publication']={'status':'blocked'};write(self.root/'state.json',s)
        with self.assertRaisesRegex(Error,'Git'):blocks.resume(self.run)
        s.pop('publication');s['dispatch_blocked']='fixture';write(self.root/'state.json',s)
        with self.assertRaisesRegex(Error,'fleet'):blocks.resume(self.run)

    def test_b1_pi_gate_and_exhausted_order_override_block_authorization(self):
        for state,left in [('check-in',20),('report',10),('stopped',10),('reading',0)]:
            response=CompletedProcess([],0,json.dumps({'state':state,'left':{'rooms':left}}),'')
            with self.subTest(state=state),patch('runtime.study.trusted',return_value=response),self.assertRaises(Error):
                blocks.scientific_gate(self.run,'B1b-01',self.ws)
        with patch('runtime.study.trusted',return_value=CompletedProcess([],0,json.dumps({'state':'reading','left':{'rooms':10}}),'')):
            blocks.scientific_gate(self.run,'B1b-01',self.ws)
    def test_final_pass_interview_stops_range_but_not_each_pass(self):
        self.assertEqual(blocks.sequence('C1a-01','C1a-03'),['C1a-01','C1a-02','C1a-03'])
        blocks.start(self.run,'A1b-01','A1b-03');self.tick();self.finish();self.tick()
        s=study.run_state(self.run);s['legs']['A1b-01']['cut']='interview';write(self.root/'state.json',s)
        self.tick();self.assertEqual(blocks.state(self.run)['status'],'completed')
        self.assertNotIn('A1b-02',study.run_state(self.run)['legs'])
    def test_blocked_close_is_not_retried_by_normal_watcher(self):
        blocks.start(self.run,'A1b-01','A1b-02');self.tick();a=self.finish()
        atomic(a.base/'workspace/out/NEEDS-JUDGMENT.md','Question');self.tick()
        self.assertTrue(blocks.manages_close(self.run,a.state['id']))
        blocks.stop(self.run);self.tick();self.assertFalse(blocks.manages_close(self.run,a.state['id']))


for name in list(test_workflow.WorkflowTests.__dict__):
    if name.startswith('test_'):setattr(BlockTests,name,None)
