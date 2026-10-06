"""Relocated native history must not depend on the old actor's files."""
import json, sqlite3, tempfile, unittest, shutil, uuid
from pathlib import Path
from runtime.archive import relocate_native_index
from runtime.common import ROOT, REPO, CODEX, DATA, Error, sha
from runtime import actors, archive, native

class NativeRelocationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=ROOT);self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.home=self.root/'native';(self.home/'sessions').mkdir(parents=True)
  self.rollout=self.home/'sessions/one.jsonl';self.rollout.write_text(json.dumps({'type':'session_meta','payload':{'id':'one'}})+'\n')
 def index(self,tid='one'):
  with sqlite3.connect(self.home/'state_5.sqlite') as c:
   c.execute('CREATE TABLE threads (id TEXT PRIMARY KEY, rollout_path TEXT, cwd TEXT, history_mode TEXT)')
   c.execute('INSERT INTO threads VALUES (?,?,?,?)',(tid,'/old/native/sessions/one.jsonl','/old/workspace/out','paginated'))
  with sqlite3.connect(self.home/'thread_history_1.sqlite') as c:
   c.execute('CREATE TABLE thread_turns (thread_id TEXT, rollout_byte_offset INTEGER)')
   c.execute('INSERT INTO thread_turns VALUES (?,?)',('one',123))
 def run_relocation(self):
  return relocate_native_index(self.home,self.root/'child/native','one','/old/workspace',self.root/'child/workspace')
 def test_paginated_metadata_moves_without_rewriting_history(self):
  self.index();before=sha(self.rollout);history=sha(self.home/'thread_history_1.sqlite')
  result=self.run_relocation();self.assertTrue(result['indexed'])
  with sqlite3.connect(self.home/'state_5.sqlite') as c:
   row=c.execute('SELECT rollout_path,cwd,history_mode FROM threads').fetchone()
  self.assertEqual(row,(str(self.root/'child/native/sessions/one.jsonl'),str(self.root/'child/workspace/out'),'paginated'))
  self.assertEqual(before,sha(self.rollout));self.assertEqual(history,sha(self.home/'thread_history_1.sqlite'))
 def test_legacy_transcript_without_index_retains_path_restore(self):
  result=self.run_relocation();self.assertFalse(result['indexed']);self.assertTrue(result['resume_path'].endswith('/child/native/sessions/one.jsonl'))
 def test_missing_indexed_thread_fails_closed(self):
  self.index('absent')
  with self.assertRaisesRegex(Error,'absent from the archive'):self.run_relocation()
 def test_duplicate_thread_fails_closed(self):
  (self.home/'sessions/two.jsonl').write_bytes(self.rollout.read_bytes())
  with self.assertRaisesRegex(Error,'Duplicate native thread'):self.run_relocation()
 def test_package_helpers_survive_archive_and_restore(self):
  package=self.root/'package';exe=package/'CodexCLI.app/Contents/MacOS/codex';exe.parent.mkdir(parents=True)
  shutil.copy2(CODEX/'runtime/tests/fake_codex.py',exe)
  (package/'codex-package.json').write_text('{"layoutVersion":1}')
  helper=package/'bin/codex-code-mode-host';helper.parent.mkdir();helper.write_text('fixture helper');helper.chmod(0o755)
  ws=self.root/'workspace';(ws/'out').mkdir(parents=True)
  aid='test-package-'+uuid.uuid4().hex[:10];child=aid+'-child'
  self.addCleanup(shutil.rmtree,DATA/'actors'/aid,True);self.addCleanup(shutil.rmtree,DATA/'actors'/child,True)
  actors.create(aid,ws,'gpt-6-sol','medium',executable=str(exe));a=actors.Actor(aid);self.addCleanup(a.release)
  a.message('remember package');a.wait(15);r=a.checkpoint();self.addCleanup(shutil.rmtree,DATA/'checkpoints'/r['checkpoint'],True)
  state=archive.restore(r['checkpoint'],child);restored=Path(state['runtime']['package_root'])
  self.assertEqual(sha(helper),sha(restored/'bin/codex-code-mode-host'))
  self.assertEqual(native.fingerprint(state['runtime']['executable'])['package_files'],state['runtime']['package_files'])
 def test_package_fingerprint_includes_helper_changes(self):
  package=self.root/'package';package.mkdir();exe=package/'codex';exe.write_text('cli');(package/'codex-package.json').write_text('{}')
  helper=package/'codex-code-mode-host';helper.write_text('version1');before=native.fingerprint(exe)
  helper.write_text('version2');after=native.fingerprint(exe)
  self.assertEqual(before['sha256'],after['sha256']);self.assertNotEqual(before['package_files'],after['package_files'])
