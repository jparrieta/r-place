"""Generated views must use current adjudicated returns, including empty rechecks."""
import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
BASE=None
def jl(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
class Views(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=BASE);self.root=Path(self.temp.name);self.out=self.root/'out';self.out.mkdir()
        jl(self.root/'package/store/codes.jsonl',[])
        jl(self.root/'package/store/themes.jsonl',[{'sub':'room','theme_id':'t01','second_order':'theme'}])
        jl(self.out/'adaptations.jsonl',[{'id':'old','sub':'room','op':'restrict','element':'P01','decision':'accept','condition':'OLD STATEMENT'}])
    def tearDown(self): self.temp.cleanup()
    def run_views(self):
        subprocess.run([sys.executable,'-B',str(TOOLS/'gen_views.py'),'D2','--root',str(self.root)],check=True,capture_output=True,text=True)
    def test_current_adjudication_replaces_original_kind_and_text(self):
        jl(self.out/'adjudications.jsonl',[{'adaptation':'old','decision':'particular','kind':'correction','revised':'CURRENT STATEMENT'}])
        self.run_views();wiki=(self.out/'_wiki/rooms/room.md').read_text()
        self.assertIn('CURRENT STATEMENT',wiki);self.assertIn('particular;correction',wiki);self.assertNotIn('OLD STATEMENT',wiki)
        matrix=(self.out/'_views/rooms-x-elements.tsv').read_text().splitlines()
        self.assertEqual(matrix[-1],'room\trestrict')
        detail=(self.out/'_views/adaptations-current.tsv').read_text().splitlines()
        record=list(csv.DictReader(detail[1:],delimiter='\t'))[0]
        self.assertEqual(record['decision'],'particular');self.assertEqual(record['kind'],'correction')
        self.assertEqual(record['condition'],'CURRENT STATEMENT')
    def test_unknown_absence_keeps_observation_explicit(self):
        jl(self.out/'adaptations.jsonl',[{'id':'unknown','sub':'room','op':'absent','element':'P01'}])
        self.run_views()
        detail=(self.out/'_views/adaptations-current.tsv').read_text().splitlines()
        record=list(csv.DictReader(detail[1:],delimiter='\t'))[0]
        self.assertEqual(record['observation'],'unobserved')
        self.assertEqual(record['decision'],'pending')
    def test_empty_recheck_removes_old_view_and_exposes_missing_version(self):
        self.run_views();self.assertIn('restrict',(self.out/'_views/rooms-x-elements.tsv').read_text())
        jl(self.out/'adaptation-returns.jsonl',[{'sub':'room','phase':'recheck','status':'accepted','ids':[],'model_version':'new','local_status':'validated'}])
        self.run_views();self.assertNotIn('restrict',(self.out/'_views/rooms-x-elements.tsv').read_text())
        self.assertNotIn('OLD STATEMENT',(self.out/'_wiki/rooms/room.md').read_text())
        self.assertEqual(len((self.out/'_views/adaptations-current.tsv').read_text().splitlines()),2)
        self.assertIn('stale-or-unknown',(self.out/'_views/local-accounts.tsv').read_text())
unittest.main()
