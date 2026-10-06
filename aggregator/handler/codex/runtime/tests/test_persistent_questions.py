"""Question delivery across idle turns, closures, restored workspaces and failures."""
import json, shutil, unittest, uuid
from types import SimpleNamespace
from unittest.mock import patch
from runtime import questions, study, actors, native, common
from runtime.common import *


class PersistentQuestionTests(unittest.TestCase):
    def setUp(self):
        self.run='questions-'+uuid.uuid4().hex[:10];self.aid=self.run+'-actor'
        self.base=actor_dir(self.aid);self.ws=self.base/'workspace'
        (self.ws/'out').mkdir(parents=True)
        self.state={'id':self.run,'active_actor':self.aid,'latest_workspace':str(self.ws),'legs':{'A1a':{'actor':self.aid,'status':'prepared'}}}
        write(study.run_dir(self.run)/'state.json',self.state)
        write(self.base/'state.json',{'id':self.aid,'run':self.run,'role':'aggregator','leg':'A1a','questions':[]})
        event(self.ws/'out/asks.jsonl',id='QA1-001',stage='A1',leg='A1a',question='Treat the aftermath separately?',assumption='Read independent rooms meanwhile.')
        self.addCleanup(lambda:shutil.rmtree(self.base,ignore_errors=True))
        self.addCleanup(lambda:shutil.rmtree(study.run_dir(self.run),ignore_errors=True))

    def answer(self,text='Yes'):
        return questions.answer_study(self.run,'QA1-001',text,self.aid)

    def test_idle_answer_records_intervention_without_starting_model(self):
        with patch.object(actors.Actor,'message',side_effect=AssertionError('must not start')):
            result=self.answer()
        self.assertFalse(result['new_turn_started'])
        self.assertEqual((self.ws/'out/_answers/QA1-001.md').read_text(),'Yes\n')
        self.assertTrue(questions.listing(self.ws,self.run)[0]['answered'])
        self.assertEqual(len((study.run_dir(self.run)/'interventions.jsonl').read_text().splitlines()),1)
        self.answer()
        self.assertEqual(len((study.run_dir(self.run)/'interventions.jsonl').read_text().splitlines()),1)
        with self.assertRaises(Error):self.answer('No')

    def test_closed_answer_leaves_parent_immutable_and_is_delivered_to_next_leg(self):
        self.state['active_actor']=None;self.state['legs']['A1a']['status']='verified'
        write(study.run_dir(self.run)/'state.json',self.state);before=inventory(self.ws)
        self.answer()
        self.assertEqual(before,inventory(self.ws))
        restored=self.base/'next-workspace';copy_tree(self.ws,restored)
        questions.deliver(self.run,restored)
        self.assertEqual((restored/'out/_answers/QA1-001.md').read_text(),'Yes\n')
        self.assertEqual(before,inventory(self.ws))

    def test_stale_actor_and_unknown_question_are_rejected(self):
        with self.assertRaises(Error):questions.answer_study(self.run,'QA1-001','Yes','old-actor')
        with self.assertRaises(Error):questions.answer_study(self.run,'QA1-002','Yes',self.aid)
        with self.assertRaises(Error):questions.answer_study(self.run,'../../escape','Yes',self.aid)

    def test_symlink_cannot_write_outside_answers(self):
        (self.ws/'out/_answers').symlink_to(self.base,target_is_directory=True)
        with self.assertRaises(Error):self.answer()
        self.assertFalse((self.base/'QA1-001.md').exists())

    def test_native_request_is_mirrored_but_live_answer_cannot_use_file_route(self):
        actor=SimpleNamespace(base=self.base,state=actor_state(self.aid))
        req={'requestKey':'thread-turn-request','questions':[{'id':'judgment','question':'Required choice?'}]}
        questions.mirror_native(actor,req);qid=req['persistedAsks']['judgment']
        actor.state['questions']=[req];write(self.base/'state.json',actor.state)
        with self.assertRaisesRegex(Error,'live request'):questions.answer_study(self.run,qid,'A',self.aid)
        questions.record_native_answer(actor,req,{'judgment':'A'})
        self.assertEqual(next(r for r in questions.listing(self.ws) if r['id']==qid)['answer'],'A')

    def test_interrupted_native_question_can_receive_a_durable_answer(self):
        actor=SimpleNamespace(base=self.base,state=actor_state(self.aid))
        req={'requestKey':'lost-request','questions':[{'id':'judgment','question':'Required choice?'}]}
        questions.mirror_native(actor,req);qid=req['persistedAsks']['judgment']
        result=questions.answer_study(self.run,qid,'Wait until review',self.aid)
        self.assertFalse(result['new_turn_started'])

    def test_partial_append_waits_but_bad_completed_line_reports_error(self):
        with (self.ws/'out/asks.jsonl').open('a') as f:f.write('{"id":')
        self.assertEqual(len(questions.rows(self.ws)),1)
        with (self.ws/'out/asks.jsonl').open('a') as f:f.write('\n')
        with self.assertRaises(Error):questions.rows(self.ws)

    def test_analyst_can_read_but_not_write_investigator_answers(self):
        native.configure(self.base/'native','gpt-6-sol','medium',self.ws)
        import tomllib
        config=tomllib.loads((self.base/'native/config.toml').read_text())
        self.assertEqual(config['permissions']['rplace']['filesystem'][str(self.ws/'out/_answers')],'read')

    def test_draft_adapter_is_not_silently_loaded_as_codex(self):
        state=actor_state(self.aid);state.update(backend='claude',claude_run=str(self.base),workspace=str(self.ws));write(self.base/'state.json',state)
        actor=actors.load(self.aid)
        self.assertFalse(actor.capabilities['admitted'])
        self.assertEqual(actor.workspace,self.ws)
        with self.assertRaisesRegex(Error,'admission is pending'):actor.message('No turn may start')

    def test_v43_runtime_cannot_adopt_v42_data(self):
        self.assertEqual(common.DATA.name,'.rplace-runtime-v43')
        self.assertNotEqual(common.DATA,common.ROOT/'.rplace-runtime')

    def test_changed_question_cannot_inherit_an_old_answer(self):
        self.answer()
        row=questions.rows(self.ws)[0];row['question']='A different decision?'
        atomic(self.ws/'out/asks.jsonl',json.dumps(row)+'\n')
        with self.assertRaises(Error):questions.listing(self.ws,self.run)
        with self.assertRaises(Error):questions.deliver(self.run,self.ws)

    def test_status_exposes_idle_questions_without_sending_native_transcript(self):
        from runtime import server
        state=actor_state(self.aid);state['effective']={'thread':{'turns':['private bulk history']},'model':'gpt-6-sol'}
        write(self.base/'state.json',state)
        controller=server.Controller.__new__(server.Controller);controller.actors={};controller.jobs={}
        with patch.object(server.branches,'summary',return_value={}):status=controller.list()
        row=next(a for a in status['actors'] if a['id']==self.aid)
        self.assertEqual(row['questions'][0]['source'],'file')
        self.assertTrue(row['questions'][0]['answerable'])
        self.assertNotIn('thread',row['effective'])
        self.assertEqual(actor_state(self.aid)['effective']['thread']['turns'],['private bulk history'])
