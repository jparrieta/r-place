"""Scientific regression counterexamples, synthetic and offline."""
import contextlib, io, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
import adaptation_ledger as ledger
import distance, adaptation_tree, vlib
from checks import stage_D4,selftest
import chunk_compare
BASE=None

def writejl(p,rows):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
def line(sub='a',op='add-condition',kind='elaboration',**kw):
    return dict(id=sub+'-1',sub=sub,op=op,kind=kind,element='P07',lift=[sub+':t01','T3-014','T4-003','D2'],decision='accept',**kw)
class Statistics(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=BASE);self.root=Path(self.tmp.name);self.out=self.root/'out';self.out.mkdir()
        (self.out/'prior.md').write_text('w = 4, 2, 1, 0.5\ng = 1, 0.5, 0, -1\n')
    def tearDown(self):self.tmp.cleanup()
    def run_distance(self,rooms):
        writejl(self.root/'package/store/rooms.jsonl',[{'sub':s} for s in rooms])
        argv=sys.argv
        try:
            sys.argv=['distance','--out',str(self.out),'--quartets','50']
            with contextlib.redirect_stdout(io.StringIO()):distance.main()
        finally:sys.argv=argv
        return adaptation_tree.read_matrix(self.out/'_views/distance.tsv')
    def test_final_kind_and_revision(self):
        writejl(self.out/'adaptations.jsonl',[line(),line('b',op='restrict',kind='correction')])
        writejl(self.out/'adjudications.jsonl',[{'adaptation':'a-1','decision':'modify','kind':'correction','revised':'fixed condition'}])
        rows=ledger.effective_lines(self.out);self.assertEqual(len(rows),2);self.assertEqual(rows[0]['statement'],'fixed condition')
        self.assertEqual(self.run_distance(['a','b'])[1][0][1],.25)
    def test_empty_recheck_replaces_all_old_lines(self):
        writejl(self.out/'adaptations.jsonl',[line(),dict(line(),id='a-2')])
        self.assertEqual(len(ledger.effective_lines(self.out)),2)
        writejl(self.out/'adaptation-returns.jsonl',[{'sub':'a','phase':'recheck','status':'accepted','model_version':'v2','ids':[]}])
        self.assertEqual(ledger.effective_lines(self.out,True,True,True),[])
        self.assertEqual(ledger.effective_rooms(self.out)['a']['model_version'],'v2')
    def test_absence_observation_and_no_none_key(self):
        rows=[line(s,op='absent',kind='specification',observation='observed-absent') for s in ['a','b']]
        for r in rows:r['lift']=None
        writejl(self.out/'adaptations.jsonl',rows)
        self.assertEqual(self.run_distance(['a','b'])[1][0][1],0)
        report=json.loads((self.out/'_views/adaptation-tree.json').read_text())
        self.assertFalse(report['nodes'][0]['shared_keys'])
        rows[0].pop('observation');writejl(self.out/'adaptations.jsonl',rows)
        self.assertEqual(len(ledger.shared_lines(self.out)),1)
    def test_missing_frame(self):
        writejl(self.out/'adaptations.jsonl',[line()]);(self.out/'dropped.jsonl').write_text('')
        d=self.root/'DROPS/D';d.mkdir(parents=True);(d/'UNRETURNED.tsv').write_text('sub\treason\nb\tmissing\n')
        names,D=self.run_distance(['a','b']);self.assertEqual(names,['a'])
        ctx={'root':str(self.root),'package':str(self.root/'package'),'outdir':str(self.out),'stage':'D4'}
        vlib.E.clear()
        with contextlib.redirect_stdout(io.StringIO()):stage_D4.check_views(str(self.out),ctx)
        self.assertFalse(vlib.E,vlib.E)
    def test_invalid_weights(self):
        (self.out/'prior.md').write_text('w = 0, 2, 1, 0.5\ng = 1, 0.5, 0, -1')
        with self.assertRaises(ValueError):distance.read_prior(self.out/'prior.md')
    def test_full_precision_tree(self):
        names=list('abc');D=[[0,.10004,.10003],[.10004,0,.5],[.10003,.5,0]]
        v=self.out/'_views';v.mkdir();distance.write_tsv(v/'distance.tsv',[[n]+[format(x,'.17g') for x in row] for n,row in zip(names,D)],['room']+names)
        writejl(self.out/'adaptations.jsonl',[line(n) for n in names])
        r=adaptation_tree.generate(self.out);self.assertEqual(set(r['nodes'][3]['members']),{'a','c'})
    def branch_fixture(self):
        selftest.write_fixture(str(self.root));stage_D4.base(str(self.out),str(self.root))
        return {'root':str(self.root),'package':str(self.root/'package'),'outdir':str(self.out),'stage':'D4'}
    def branch_errors(self,ctx):
        vlib.E.clear()
        with contextlib.redirect_stdout(io.StringIO()):ids=stage_D4.check_branches(str(self.out),str(self.root),ctx);stage_D4.check_crosslinks(str(self.out),ctx,ids)
        return [e[0] for e in vlib.E]
    def test_cycle_and_typed_overlap(self):
        ctx=self.branch_fixture();b=dict(stage_D4.BRANCH_F01,parent='F01');writejl(self.out/'branches.jsonl',[b])
        self.assertTrue(any('cycle' in x for x in self.branch_errors(ctx)))
        b['parent']=None;c=dict(b,id='F02',name='specific condition');writejl(self.out/'branches.jsonl',[b,c]);(self.out/'forms/F02.md').write_text((self.out/'forms/F01.md').read_text())
        writejl(self.out/'crosslinks.jsonl',[{'note':'denmark asoiaf'}]);self.assertTrue(self.branch_errors(ctx))
        writejl(self.out/'crosslinks.jsonl',[{'sub':s,'branches':['F01','F02'],'reason':'different targets'} for s in ['denmark','asoiaf']]);self.assertFalse(self.branch_errors(ctx))
    def test_cross_tier_and_negative_result(self):
        ctx=self.branch_fixture();b=dict(stage_D4.BRANCH_F01,level='fourth',keys=['add-condition:P07:T4-003']);c=dict(stage_D4.BRANCH_F01,id='F02',parent='F01',name='specific condition')
        writejl(self.out/'branches.jsonl',[b,c]);(self.out/'forms/F01.md').write_text('denmark asoiaf add-condition:P07:T4-003');(self.out/'forms/F02.md').write_text('denmark asoiaf add-condition:P07:T3-014')
        self.assertFalse(self.branch_errors(ctx))
        writejl(self.out/'branches.jsonl',[]);self.assertTrue(self.branch_errors(ctx))
        (self.out/'taxonomy-status.json').write_text(json.dumps({'status':'no-supported-forms','reason':'no common supported change','reviewed_rooms':['denmark','asoiaf','sweden']}));self.assertFalse(self.branch_errors(ctx))
    def test_literal_unadapted(self):
        ctx=self.branch_fixture();b=dict(stage_D4.BRANCH_F01,type='unadapted',keys=[],members=['sweden'],name='unadapted cases');writejl(self.out/'branches.jsonl',[b]);(self.out/'forms/F01.md').write_text('sweden');self.assertFalse(self.branch_errors(ctx))
    def comparison_fixture(self):
        store=self.root/'package/store';themes=[];codes=[];assign=[]
        writejl(store/'rooms.jsonl',[{'sub':str(i)} for i in range(8)])
        for i in range(8):
            for t in range(6):
                sub=str(i);tid='t'+str(t);themes.append({'sub':sub,'theme_id':tid})
                for c in range(1+(i+t)%3):codes.append({'sub':sub,'theme_id':tid,'code_id':tid+'c'+str(c)})
                assign.append({'sub':sub,'theme_id':tid,'third_order':['T3-%03d'%((t+(i//4)*2)%4)]})
        writejl(store/'themes.jsonl',themes);writejl(store/'codes.jsonl',codes);writejl(self.out/'assignments_final.jsonl',assign)
        writejl(self.out/'fourth/fourth.jsonl',[{'id':'T4-%03d'%j,'members':['T3-%03d'%j]} for j in range(4)])
        writejl(self.out/'dimensions.jsonl',[{'id':'D1','members':['T4-000','T4-001']},{'id':'D2','members':['T4-002','T4-003']}])
        return store
    def test_comparison_numeric_replay_tamper_and_isolation(self):
        store=self.comparison_fixture();r=chunk_compare.generate(self.out,store)
        self.assertEqual(len(r['all_cases']['tables']),6)
        self.assertFalse(chunk_compare.verify_report(self.out,store))
        env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
        proc=subprocess.run([sys.executable,'-I',str(TOOLS/'chunk_compare.py'),'--verify','--out',str(self.out),'--store',str(store)],env=env,capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
        r['all_cases']['tables'][0]['real']['mean']=.123456
        (self.out/'chunk-share-D4.result.json').write_text(json.dumps(r))
        self.assertTrue(chunk_compare.verify_report(self.out,store))
    def test_zero_two_three_cases_and_no_dimension(self):
        store=self.comparison_fixture()
        writejl(self.out/'dimensions.jsonl',[])
        r=chunk_compare.generate(self.out,store)
        self.assertEqual(r['dimension_status'],'unavailable: absent or single dimension')
        for n in (0,2,3):
            writejl(self.out/'dropped.jsonl',[{'sub':str(i)} for i in range(n,8)])
            r=chunk_compare.generate(self.out,store)
            self.assertEqual(r['all_cases']['status'],'no-supported-partition')
            self.assertEqual(r['clusters'],[])
            self.assertFalse(chunk_compare.verify_report(self.out,store))
    def test_all_none_distance_is_not_forced_form(self):
        writejl(self.out/'adaptations.jsonl',[{'id':s,'sub':s,'op':'none'} for s in ['a','b','c']])
        names,D=self.run_distance(['a','b','c'])
        self.assertEqual(sum(map(sum,D)),0)
        report=json.loads((self.out/'_views/adaptation-tree.json').read_text())
        self.assertTrue(all(not n.get('declared_branches') for n in report['nodes']))
    def test_all_placements_sensitivity(self):
        writejl(self.out/'adaptations.jsonl',[line(),line('b')])
        writejl(self.out/'assignments_final.jsonl',[{'sub':'a','theme_id':'t01','third_order':['T3-014','T3-015']}])
        self.run_distance(['a','b'])
        report=json.loads((self.out/'_views/adaptation-tree.json').read_text())
        self.assertEqual(report['sensitivity']['multiply_placed_lines'],['a-1'])

    def test_stub_and_bad_control_rejected(self):
        self.assertTrue(chunk_compare.verify_report(self.out,self.root/'store'))
        with self.assertRaises(ValueError):chunk_compare.compute(self.out,self.root/'store',{'concentration':float('nan'),'seeds':[0,1],'resamples':200,'permutations':100})
        with self.assertRaises(ValueError):chunk_compare.compute(self.out,self.root/'store',{'concentration':1.,'seeds':[0,1],'resamples':2,'permutations':100})

if __name__=='__main__':unittest.main()
