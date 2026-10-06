import shutil, subprocess, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from runtime import publication, study, actors
from runtime.common import *
from runtime.tests import test_branches


class PublicationTests(test_branches.BranchTests):
    # Reuse only the fixture, not its test methods.
    def setUp(self):
        super().setUp()
        self.temp=tempfile.TemporaryDirectory(dir=TMP);self.repo=Path(self.temp.name)/'repo';self.remote=Path(self.temp.name)/'remote.git'
        subprocess.run(['git','init','--bare',str(self.remote)],check=True,capture_output=True)
        subprocess.run(['git','init','-b','main',str(self.repo)],check=True,capture_output=True)
        self.g('config','user.name','Offline Test');self.g('config','user.email','test@example.invalid')
        (self.repo/'unrelated.txt').write_text('main');self.g('add','unrelated.txt');self.g('commit','-m','fixture')
        self.g('remote','add','origin',str(self.remote));self.g('push','origin','main')
        self.patch=patch('runtime.publication.REPO',self.repo);self.patch.start()
        self.reg_patch=patch('runtime.publication.REGISTRY',Path(self.temp.name)/'registry.json');self.reg_patch.start()
    def tearDown(self):
        self.reg_patch.stop()
        self.patch.stop();self.temp.cleanup();super().tearDown()
    def g(self,*args):
        r=subprocess.run(['git',*args],cwd=self.repo,capture_output=True,check=True)
        return r.stdout.decode().strip()
    def test_siblings_share_exact_checkpoint_parent_without_touching_checkout(self):
        self.fork();self.put('stages/STAGE-B1-test.md','variant card','B1')
        (self.repo/'unrelated.txt').write_text('uncommitted unrelated work')
        before=self.g('status','--porcelain');head=self.g('rev-parse','HEAD')
        one=publication.publish(self.child)['publication']
        pub=read(study.run_dir(self.child)/'publication.json')
        self.assertEqual(self.g('rev-parse',pub['setup_commit']+'^'),pub['base_commit'])
        self.assertEqual(self.g('status','--porcelain'),before);self.assertEqual(self.g('rev-parse','HEAD'),head)
        original_child=self.child;self.child=self.tag+'-sibling';self.fork()
        two=publication.publish(self.child)['publication'];self.child=original_child
        self.assertEqual(one['base_commit'],two['base_commit']);self.assertNotEqual(one['commit'],two['commit'])
        self.assertEqual(self.g('merge-base',one['commit'],two['commit']),one['base_commit'])
        self.assertIn('variant card',self.g('show',one['commit']+':'+pub['prefix']+'/stage-deliveries/B1/stages/STAGE-B1-test.md'))
        self.assertEqual(publication.remote_ref(one['ref']),one['commit'])
    def test_verified_child_leg_extends_setup_and_retry_does_not_duplicate(self):
        self.fork();first=publication.publish(self.child)['publication']
        p=study.prepare(self.child,'B1a');a=actors.Actor(p['actor']);self.instances.append(a)
        a.message('NEW BRANCH ANALYSIS');a.wait(10);receipt=a.checkpoint()
        s=study.run_state(self.child);s['active_actor']=None;s['legs']['B1a'].update(status='verified',checkpoint=receipt['checkpoint']);write(study.run_dir(self.child)/'state.json',s)
        second=publication.after_close(self.child)['publication']
        self.assertEqual(self.g('rev-parse',second['commit']+'^'),first['commit'])
        self.assertEqual(publication.publish(self.child)['publication']['commit'],second['commit'])
        self.assertEqual(self.g('rev-parse',publication.checkpoint_ref(receipt['checkpoint'])),second['commit'])
    def test_push_failure_keeps_commit_and_retry_preserves_ancestry(self):
        self.fork();real=publication.git
        def fail(*args,**kw):
            if args[0]=='push':raise Error('simulated transport outage')
            return real(*args,**kw)
        with patch('runtime.publication.git',side_effect=fail),self.assertRaisesRegex(Error,'transport'):
            publication.publish(self.child)
        pub=read(study.run_dir(self.child)/'publication.json');self.assertIsNone(pub['pushed_commit'])
        result=publication.publish(self.child)['publication']
        self.assertEqual(result['commit'],pub['pending_commit'])
    def test_interview_and_native_files_never_enter_snapshot(self):
        self.fork();base=study.run_dir(self.child)
        # Exercise filtering independently without changing the sealed input record.
        temp=Path(self.temp.name)/'filter';temp.mkdir()
        atomic(temp/'out/interview-workspaces/private/transcript.md','private')
        atomic(temp/'native/session.json','private');atomic(temp/'auth.json','secret');atomic(temp/'out/research.md','research')
        self.assertEqual([str(rel) for rel,p in publication.safe_files(temp)],['out/research.md'])
    def test_nested_branch_begins_at_the_actual_parent_branch_checkpoint(self):
        self.fork();publication.publish(self.child)
        p=study.prepare(self.child,'B1a');a=actors.Actor(p['actor']);self.instances.append(a)
        a.message('FIRST VARIANT');a.wait(10);receipt=a.checkpoint()
        s=study.run_state(self.child);s['active_actor']=None;s['legs']['B1a'].update(status='verified',checkpoint=receipt['checkpoint']);write(study.run_dir(self.child)/'state.json',s)
        parent=publication.after_close(self.child)['publication']
        grandchild=self.tag+'-grandchild'
        from runtime import branches
        branches.create(self.child,receipt['checkpoint'],grandchild,'B1b-01')
        result=publication.publish(grandchild)['publication']
        self.assertEqual(result['base_commit'],parent['commit'])
        self.assertEqual(self.g('rev-parse',result['commit']+'^'),parent['commit'])
    def test_failed_post_close_push_blocks_progress_without_losing_verified_leg(self):
        self.fork();publication.publish(self.child)
        p=study.prepare(self.child,'B1a');a=actors.Actor(p['actor']);self.instances.append(a)
        a.message('FINISHED');a.wait(10);receipt=a.checkpoint()
        s=study.run_state(self.child);s['active_actor']=None;s['legs']['B1a'].update(status='verified',checkpoint=receipt['checkpoint']);write(study.run_dir(self.child)/'state.json',s)
        real=publication.git
        def fail(*args,**kw):
            if args[0]=='push':raise Error('offline')
            return real(*args,**kw)
        with patch('runtime.publication.git',side_effect=fail),self.assertRaisesRegex(Error,'do not rerun'):
            publication.after_close(self.child)
        self.assertEqual(study.run_state(self.child)['legs']['B1a']['status'],'verified')
        with self.assertRaisesRegex(Error,'publication is blocked'):study.prepare(self.child,'B1b-01')
        published=publication.publish(self.child)
        self.assertEqual(published['publication']['status'],'pushed')
        self.assertTrue(study.prepare(self.child,'B1b-01')['actor'])


# Only the publication tests use this class; inherited branch tests run once in
# test_branches, with their own isolated fixture.
for name in list(test_branches.BranchTests.__dict__):
    if name.startswith('test_'):setattr(PublicationTests,name,None)
