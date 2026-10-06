"""The real close script must not mark a leg closed after its record writer fails."""
import os, shutil, subprocess, tempfile, unittest
from pathlib import Path
from runtime.common import ROOT, REPO, CODEX, write, read

class CloseRecordTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=ROOT);self.addCleanup(self.tmp.cleanup);self.ws=Path(self.tmp.name)
  tools=self.ws/'tools';tools.mkdir();(self.ws/'out').mkdir()
  shutil.copy2(REPO/'aggregator/instrument/tools/done.sh',tools/'done.sh')
  for n in ['validate.py','links.py','gen_views.py']:(tools/n).write_text('raise SystemExit(0)\n')
  (self.ws/'.leg').write_text('A1a\n');(self.ws/'.session').write_text('native-thread\n')
 def close(self,*args):
  return subprocess.run(['/bin/bash','tools/done.sh','A1',*args],cwd=self.ws,env={**os.environ,'TMPDIR':str(self.ws/'does-not-exist')},capture_output=True,text=True)
 def test_record_and_marker_written_without_shell_temp_file(self):
  r=self.close();self.assertEqual(r.returncode,0,r.stdout+r.stderr)
  self.assertEqual(read(self.ws/'RUN.json')['legs'][-1]['session'],'native-thread')
  self.assertTrue((self.ws/'out/_closes/A1-A1a.closed').is_file())
 def test_invalid_record_blocks_close_marker(self):
  (self.ws/'RUN.json').write_text('broken json');r=self.close()
  self.assertNotEqual(r.returncode,0);self.assertIn('leg record FAILED',r.stdout)
  self.assertFalse((self.ws/'out/_closes/A1-A1a.closed').exists())
 def test_pause_without_shell_temp_file_requires_matching_diary(self):
  r=self.close('--pause');self.assertNotEqual(r.returncode,0)
  (self.ws/'out/diary').mkdir();(self.ws/'out/diary/A1-test.jsonl').write_text('{"kind":"pause","leg":"A1a"}\n')
  r=self.close('--pause');self.assertEqual(r.returncode,0,r.stdout+r.stderr)
  self.assertEqual(read(self.ws/'RUN.json')['legs'][-1]['cut'],'pause')
