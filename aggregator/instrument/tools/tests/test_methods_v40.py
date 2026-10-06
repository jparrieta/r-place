"""Regression tests for evidential state, local composition and typed process claims. Offline only."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import dreturn
import vlib
from checks import selftest, stage_C2, stage_D2, stage_D5, stage_D6, stage_E1
import ingest
from adaptation_ledger import effective_lines


def rows(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row) + '\n' for row in data))


class MethodsV40(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='methods-v40-')
        self.root = Path(self.temp.name)
        self.out = Path(selftest.write_fixture(str(self.root)))
        self.ctx = {'root': str(self.root), 'package': str(self.root/'package'), 'outdir': str(self.out)}
        self.old_cwd = os.getcwd()
        os.chdir(self.root)
        vlib.E.clear(); vlib.W.clear()

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.temp.cleanup()

    def fixture(self, module):
        with contextlib.redirect_stdout(io.StringIO()):
            module.base(str(self.out), str(self.root))
        vlib.E.clear(); vlib.W.clear()

    def ledger(self, decision='particular', op='contradict', observation=None):
        rows(self.out/'model/elements.jsonl', [{'id':'P01','kind':'process','statement':'Call precedes collective work.','dimension':None}])
        rows(self.out/'model/arrows.jsonl', [])
        rows(self.out/'dimensions.jsonl', [])
        version=vlib.model_hash(str(self.out))
        line={'id':'denmark-001','sub':'denmark','op':op,'element':'P01','statement':'Private coordination precedes public invitation.',
              'how':'Explains early joint work.', 'evidence':{'codes':['c0117']},'model_version':version,'decision':'pending'}
        if observation: line['observation']=observation
        rows(self.out/'adaptations.jsonl',[line])
        rows(self.out/'adjudications.jsonl',[{'adaptation':line['id'],'decision':decision,'reason':'Supported locally, shared scope unresolved.'}])
        rows(self.out/'adaptation-returns.jsonl',[{'sub':'denmark','phase':'initial','status':'accepted','model_version':version,
             'ids':[line['id']],'local_status':'validated' if decision!='pending' else 'unresolved','local_grade':'composes'}])
        return version, line

    def rebuild(self, json_output=True):
        args=[sys.executable,'-B',str(TOOLS/'rebuild.py'),'denmark','--out',str(self.out)]
        if json_output: args.append('--json')
        result=subprocess.run(args, capture_output=True,text=True,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        return json.loads(result.stdout) if json_output else result.stdout

    def test_supported_particular_survives_both_exports(self):
        self.ledger()
        result=self.rebuild()
        self.assertEqual(result['elements'][0]['ops'][0]['decision'],'particular')
        self.assertIn('Private coordination',self.rebuild(False))
        self.assertIn('Adapted-local status: validated',self.rebuild(False))

    def test_unknown_absence_never_becomes_no(self):
        for state in ('unobserved','not-testable','not-needed','observed-absent'):
            with self.subTest(state=state):
                self.ledger('accept','absent',state)
                got=self.rebuild()['elements'][0]['applies']
                self.assertEqual(got, 'no' if state=='observed-absent' else state)
        self.assertTrue(dreturn.absence_problems({'op':'absent','observation':'observed-absent','evidence':{'codes':[]}}))
        self.assertFalse(dreturn.absence_problems({'op':'absent','observation':'unobserved','evidence':{'codes':[]}}))
        self.assertTrue(dreturn.absence_problems({'op':'absent'}))

    def test_pending_is_visible_but_not_asserted(self):
        self.ledger('pending')
        result=self.rebuild()
        self.assertEqual(result['elements'][0]['ops'],[])
        self.assertEqual(len(result['unresolved_adaptations']),1)
        self.assertIn('Unresolved adaptations: 1 (not asserted support)',self.rebuild(False))
        self.assertIn('Private coordination',self.rebuild(False))

    def test_empty_recheck_replaces_original(self):
        version,_=self.ledger()
        records=json.loads((self.out/'adaptation-returns.jsonl').read_text())
        rows(self.out/'adaptations-recheck.jsonl',[])
        rows(self.out/'adaptation-returns.jsonl',[records,dict(records,phase='recheck',ids=[])])
        self.assertEqual(self.rebuild()['elements'][0]['ops'],[])
        self.assertEqual(self.rebuild()['ledger'],'recheck')

    def test_modified_text_is_the_effective_text(self):
        _,line=self.ledger('modify')
        rows(self.out/'adjudications.jsonl',[{'adaptation':line['id'],'decision':'modify','revised':{'statement':'A narrower supported local claim.'}}])
        self.assertEqual(self.rebuild()['elements'][0]['ops'][0]['text'],'A narrower supported local claim.')

    def test_stale_return_never_claims_current_validation(self):
        self.ledger()
        rows(self.out/'model/elements.jsonl',[{'id':'P01','statement':'An amended mechanism.'}])
        result=self.rebuild()
        self.assertEqual(result['local_account']['local_status'],'unresolved')
        self.assertEqual(result['elements'][0]['applies'],'unverified-current')
        self.assertIn('stale or its version is unknown',self.rebuild(False))

    def test_explicit_unaffected_carryforward(self):
        self.ledger()
        rows(self.out/'model/elements.jsonl',[{'id':'P01','statement':'A typographic amendment.'}])
        current=vlib.model_hash(str(self.out))
        (self.out/'_closes').mkdir(exist_ok=True)
        (self.out/'_closes/model-D3.sha256').write_text(current)
        (self.out/'recheck-scope.json').write_text(json.dumps({'unaffected_rooms':{'denmark':'Only punctuation changed.'}}))
        result=self.rebuild()
        self.assertEqual(result['local_account']['version_status'],'unaffected-carry-forward')
        self.assertEqual(result['local_account']['local_status'],'validated')

    def test_cannot_tell_can_name_decisive_missing_evidence(self):
        row={'verdict':'cannot-tell','cannot_tell_under':'missing-decisive-evidence','sentence':'The decisive allocation event is missing.',
             'themes':[],'concepts':[],'residue':None}
        self.assertFalse(dreturn.verdict_problems(row,'denmark'))
        self.assertTrue(dreturn.verdict_problems(dict(row,cannot_tell_under=None),'denmark'))
        self.assertTrue(dreturn.verdict_problems(dict(row,sentence=''),'denmark'))

    def test_historical_global_failure_can_have_valid_local_accounts(self):
        self.fixture(stage_D5)
        version=vlib.model_hash(str(self.out))
        manifest=[dict(row,local_status='validated',local_grade='composes') for row in vlib.jsonl(str(self.out/'adaptation-returns.jsonl'))]
        rows(self.out/'adaptation-returns.jsonl',manifest)
        line=copy.deepcopy(stage_D5.LINE_F01)
        line.update(verdicts={'does-not-compose':2},local_statuses={'denmark':'validated','asoiaf':'validated'},unresolved_members=[],
                    binds=[],leaves_free=[],construct_bindings=['P07'],binding_account='Evidence supports the emergent relation.')
        branches={row['id']:row for row in vlib.jsonl(str(self.out/'branches.jsonl'))}
        args=(1,str(self.out),self.ctx,branches,{'denmark','asoiaf','sweden'}, {'denmark':'does-not-compose','asoiaf':'does-not-compose'},stage_D5.arrow_subs(str(self.out)),stage_D5.propositions(str(self.out)),{'T4-003'})
        stage_D5.check_line(line,*args)
        self.assertEqual(vlib.E,[])
        vlib.E.clear()
        stage_D5.check_line(dict(line,unresolved_members=['denmark','asoiaf']),*args)
        self.assertTrue(any('unresolved_members disagree' in error[0] for error in vlib.E))
        vlib.E.clear()
        stage_D5.check_line(dict(line,construct_bindings=['invented']),*args)
        self.assertTrue(any('construct_bindings' in error[0] for error in vlib.E))

    def test_d6_model_or_tree_change_fails_even_with_amendment(self):
        self.fixture(stage_D6)
        rows(self.out/'model/elements.jsonl',[{'id':'P99','statement':'Changed without a case return.'}])
        rows(self.out/'amendments-D6.jsonl',[{'what':'element','id':'P99','change':'changed','why':'retelling','evidence':{'codes':['denmark:c0117']}}])
        with contextlib.redirect_stdout(io.StringIO()): stage_D6.check(str(self.root),str(self.out),self.ctx)
        self.assertTrue(any(error[1]=='model:moved' for error in vlib.E))
        vlib.E.clear()
        self.fixture(stage_D6)
        rows(self.out/'crosslinks.jsonl',[{'branches':['F01','F02']}])
        with contextlib.redirect_stdout(io.StringIO()): stage_D6.check(str(self.root),str(self.out),self.ctx)
        self.assertTrue(any(error[1]=='tree:moved' for error in vlib.E))

    def test_zero_dimensions_are_valid(self):
        rows(self.out/'dimensions.jsonl',[])
        got=stage_C2.check_dimensions(str(self.out),[{'id':'T4-001','dimension':[]}],'C2')
        self.assertEqual(got,(set(),[]))
        self.assertFalse(vlib.E)
        self.assertFalse(vlib.W)

    def test_typed_inter_room_loop_and_negative_controls(self):
        rows(self.out/'model/arrows.jsonl',[{'id':'A01','from':'P01','to':'P02','in_model':True},{'id':'A02','from':'P02','to':'P01','in_model':True}])
        row={'id':'L01','level':'inter-room','arrows':['A01','A02'], 'mechanism':'Reciprocal defense links the two actions.',
             'alternative':'Both actions followed an outside attack.','why_not_alternative':'Dated requests and replies show reciprocal dependence.',
             'events':[{'arrow':'A01','sub':'denmark','code':'c0117','item':'thread:1','hour':2,'clock':'forest-hours-since-open'},
                       {'arrow':'A02','sub':'asoiaf','code':'c0011','item':'thread:2','hour':4,'clock':'forest-hours-since-open'}]}
        rows(self.out/'model/loops.jsonl',[row]);stage_C2.check_loops(str(self.out),self.ctx)
        self.assertFalse(vlib.E)
        rows(self.out/'model/loops.jsonl',[dict(row,level='within-room')]);stage_C2.check_loops(str(self.out),self.ctx)
        self.assertTrue(any(error[1]=='loops:scope' for error in vlib.E));vlib.E.clear()
        wrong=copy.deepcopy(row);wrong['events'][1]['hour']=1
        rows(self.out/'model/loops.jsonl',[wrong]);stage_C2.check_loops(str(self.out),self.ctx)
        self.assertTrue(any(error[1]=='loops:order' for error in vlib.E));vlib.E.clear()
        wrong=copy.deepcopy(row);wrong['events'][1]['code']='c9999'
        rows(self.out/'model/loops.jsonl',[wrong]);stage_C2.check_loops(str(self.out),self.ctx)
        self.assertTrue(any(error[1]=='loops:provenance' for error in vlib.E))

    def test_negative_or_unresolved_composition_passes_e1(self):
        self.fixture(stage_E1)
        branches={r['id']:r for r in vlib.jsonl(str(self.out/'branches.jsonl'))}
        for status in ('unsupported','unresolved'):
            vlib.E.clear()
            (self.out/'audit-E1.md').write_text(stage_E1.AUDIT.replace('composition_status: supported','composition_status: '+status))
            with contextlib.redirect_stdout(io.StringIO()): stage_E1.check_audit(str(self.out),str(self.root),self.ctx,branches)
            self.assertFalse(vlib.E,vlib.E)

    def test_recheck_ids_bind_version_and_preserve_prior_work(self):
        with contextlib.redirect_stdout(io.StringIO()): stage_D2.plant_base(str(self.out),str(self.root))
        hand=self.out/'handoff-D'
        shutil.copytree(hand,hand/'recheck',ignore=shutil.ignore_patterns('recheck','tasks'))
        drop=self.root/'DROPS/D/recheck/denmark'
        shutil.copytree(self.root/'DROPS/D/denmark',drop)
        def compile_return():
            obj=ingest.Ingest(str(self.root),str(self.out),str(drop.parent),True)
            with contextlib.redirect_stdout(io.StringIO()): obj.compile()
            return [r for r in effective_lines(str(self.out),include_pending=True,include_particular=True) if r['sub']=='denmark']
        first=compile_return(); first_ids={r['id'] for r in first}
        rows(self.out/'adjudications.jsonl',[{'adaptation':i,'decision':'accept','reason':'Supported.'} for i in first_ids])
        self.assertEqual(first_ids,{r['id'] for r in compile_return()})
        old_account=(self.out/'rooms/denmark/model-D-recheck.md').read_text()
        new_version='f'*64
        (hand/'recheck/VERSION').write_text(new_version)
        objects=vlib.jsonl(str(drop/'adaptations.jsonl'))
        for obj in objects:
            if 'op' in obj: obj['model_version']=new_version
        rows(drop/'adaptations.jsonl',objects)
        (drop/'model-D.md').write_text(old_account.replace('<!-- end -->','New local reading [c0117].\n<!-- end -->'))
        second=compile_return(); second_ids={r['id'] for r in second}
        self.assertTrue(first_ids.isdisjoint(second_ids))
        self.assertTrue(all(r['decision']=='pending' for r in second))
        preserved={r['id'] for r in vlib.jsonl(str(self.out/'adaptations-recheck.jsonl'))}
        self.assertTrue(first_ids <= preserved)
        archives=list((self.out/'return-history/accounts/denmark').rglob('model-D-recheck.md'))
        self.assertTrue(any(p.read_text()==old_account for p in archives))
        rows(drop/'adaptations.jsonl',[{'end':True,'lines':0}])
        self.assertEqual(compile_return(),[])


suite=unittest.defaultTestLoader.loadTestsFromTestCase(MethodsV40)
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
