"""Offline platform routing: no CLI, inference, controller server or research run."""
import json
import importlib.util
import os
import sys
import tarfile
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from runtime import actors, archive, backends, blocks, branches, bridge, claude_backend, common, questions, retention, server, study
from runtime.common import Error, ROOT, inventory, read, sha, write


class BackendDispatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='backend-offline-', dir=ROOT)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.data = self.root / 'data'
        self.data.mkdir()
        # Isolate every imported runtime module from real actors, jobs and studies.
        for name, module in list(sys.modules.items()):
            if name.startswith('runtime.') and hasattr(module, 'DATA'):
                p = patch.object(module, 'DATA', self.data); p.start(); self.addCleanup(p.stop)
        self.aid = 'claude-fixture'; self.run = 'study-fixture'
        self.base = self.data / 'actors' / self.aid
        self.rundir = self.root / 'claude-run'; self.ws = self.rundir / '00_GIVE-THE-AGENT'
        (self.ws / 'out/_closes').mkdir(parents=True)
        (self.ws / 'out/_closes/A1-A1a.closed').write_text('2026-10-05T12:00:00Z close\n')
        write(self.ws / 'RUN.json', {'legs': [{'stage': 'A1', 'leg': 'A1a', 'session': 'sid', 'cut': 'close'}]})
        self.state = {'id': self.aid, 'backend': 'claude', 'role': 'aggregator', 'run': self.run,
                      'claude_run': str(self.rundir), 'workspace': str(self.ws), 'label': 'A1.A1a', 'leg': 'A1a',
                      'session_id': 'sid', 'thread_id': 'sid', 'last_turn_id': 'turn1', 'active_turn_id': None,
                      'boundary': 'completed', 'status': 'idle', 'questions': [], 'undelivered': []}
        write(self.base / 'state.json', self.state)
        self.study = {'id': self.run, 'backend': 'claude', 'active_actor': self.aid,
                      'latest_workspace': str(self.ws), 'finished_stages': [],
                      'legs': {'A1a': {'actor': self.aid, 'stage': 'A1', 'leg': 'A1a', 'status': 'prepared'}}}
        write(study.run_dir(self.run) / 'state.json', self.study)

    def pack(self, root, dest, prefix, manifest):
        entries = {}
        for p in sorted(root.rglob('*')):
            rel = str(p.relative_to(root)); mode = oct(p.stat().st_mode & 0o7777)
            entries[rel] = ('directory', mode, '-', '-') if p.is_dir() else ('file', mode, sha(p), str(p.stat().st_size))
        manifest.write_text('# v2\n' + ''.join('\t'.join((v[0], v[1], v[2], n, v[3])) + '\n' for n, v in entries.items()))
        with tarfile.open(dest, 'w:gz') as tar:
            tar.add(root, arcname=prefix, recursive=False)
            for rel in entries: tar.add(root / rel, arcname=prefix + '/' + rel, recursive=False)

    def bundle(self, kind='capture', state=None):
        st = state or self.state
        if st['label'] != self.state['label']:
            stage, leg = st['label'].split('.', 1)
            (self.ws / f'out/_closes/{stage}-{leg}.closed').write_text('2026-10-05T12:00:00Z close\n')
            write(self.ws / 'RUN.json', {'legs': [{'stage': stage, 'leg': leg, 'session': 'sid', 'cut': 'close'}]})
        folder = self.base / 'captures' / 'one' if kind == 'capture' else self.rundir / 'CONTROL/snapshots' / st['label']
        folder.mkdir(parents=True)
        native = self.root / 'native'; (native / 'projects/run').mkdir(parents=True, exist_ok=True)
        transcript = native / 'projects/run/sid.jsonl'
        transcript.write_text('{"type":"assistant","message":{"stop_reason":"end_turn"}}\n')
        (folder / 'transcript.jsonl').write_bytes(transcript.read_bytes())
        self.pack(self.ws, folder / 'fs.tar.gz', '00_GIVE-THE-AGENT', folder / 'fs.sha256')
        self.pack(native, folder / 'agent.tar.gz', '.cc', folder / 'agent-files.sha256')
        ck = {'subject': 'aggregator', 'session': {'session_id': 'sid', 'transcript_sha256': sha(transcript)},
              'label': st['label'], 'actor': st['id'], 'last_turn': st['last_turn_id'], 'boundary': st['boundary'],
              'claude_run': str(self.rundir)}
        receipt = {'backend': 'claude', 'format': claude_backend.FORMAT, 'kind': kind, 'actor': st['id'],
                   'session': 'sid', 'last_turn': st['last_turn_id'], 'boundary': st['boundary'], 'verified': True}
        if kind == 'close':
            report = folder / 'validation-report.txt'; report.write_text('0 errors\n')
            validation = {'complete': True, 'completed_turn': True, 'launcher_exited': True,
                          'validator_exit_code': 0, 'report_sha256': sha(report)}
            write(folder / 'validation.json', validation); write(folder / 'cost.json', {})
            with tarfile.open(folder / 'instrument.tar.gz', 'w:gz'): pass
            ck.update(checkpoint_id='bound-checkpoint', kind='agent-and-files', validation=validation, forced=None)
            ck['session']['boundary_verified'] = True
            receipt.update(checkpoint_id=ck['checkpoint_id'], snapshot=str(folder.relative_to(self.rundir)),
                           publication={'status': 'not configured'}, forced=False, scientific=True, cut='close')
        else:
            ck.update(backend='claude', format=claude_backend.FORMAT, kind='capture')
            receipt['archive'] = str(folder)
        write(folder / 'checkpoint.json', ck)
        self.reseal(folder, receipt)
        return folder, receipt

    def reseal(self, folder, receipt):
        excluded = {'MANIFEST.sha256', 'COMMITTED', 'DIGESTS.json'}
        digests = {p.name: sha(p) for p in sorted(folder.iterdir()) if p.name not in excluded}
        receipt['digests'] = digests
        if receipt['kind'] == 'close':
            (folder / 'MANIFEST.sha256').write_text(''.join(v + '  ' + k + '\n' for k, v in digests.items()))
            (folder / 'COMMITTED').write_text(read(folder / 'checkpoint.json')['checkpoint_id'] + '\n')
        else: write(folder / 'DIGESTS.json', digests)

    def controller(self, actor=None):
        c = server.Controller.__new__(server.Controller)
        c.guard = threading.RLock(); c.controls = {}; c.closing = set(); c.stopping = threading.Event()
        c.actors = {self.aid: actor or actors.load(self.aid)}; c.jobs = {}; c.block_busy = set(); c.job = Mock()
        return c

    def fake_actor(self, receipt=None):
        a = SimpleNamespace(state=self.state, base=self.base, workspace=self.ws, guard=threading.RLock())
        a.save = lambda: write(self.base / 'state.json', a.state)
        a.message = Mock(return_value={'delivery': 'queued', 'new_turn_started': False})
        a.close = Mock(return_value=receipt)
        return a

    def test_load_uses_claude_without_opening_or_changing_store(self):
        before = inventory(self.root)
        a = actors.load(self.aid)
        self.assertIsInstance(a, claude_backend.Actor)
        self.assertEqual(backends.workspace(a), self.ws)
        self.assertFalse(a.capabilities['admitted'])
        with self.assertRaisesRegex(Error, 'admission is pending'): a.message('test')
        self.assertEqual(before, inventory(self.root))

    def test_unknown_backend_is_not_native(self):
        write(self.base / 'state.json', {**self.state, 'backend': 'unrecognized'})
        with self.assertRaisesRegex(Error, 'Unknown backend'): actors.load(self.aid)

    def test_unadmitted_actions_refuse_before_jobs_or_interventions(self):
        c = self.controller(); before = inventory(self.root)
        for op in ('message', 'card', 'open', 'save', 'close', 'answer', 'answer-ask', 'start', 'pause', 'stop'):
            with self.subTest(op=op), self.assertRaisesRegex(Error, 'admission is pending'):
                c.action({'action': op, 'actor': self.aid, 'run': self.run, 'text': 'test'})
        c.job.assert_not_called(); self.assertEqual(before, inventory(self.root))

    def test_capture_register_verify_and_restore_dispatch(self):
        folder, raw = self.bundle(); result = claude_backend.register(raw, self.state)
        with patch.object(archive, 'verify', side_effect=AssertionError('Wrong native parser')):
            manifest = archive.verify_checkpoint(result['checkpoint'])
            self.assertIn('workspace/RUN.json', manifest['files'])
            module = SimpleNamespace(restore=Mock(return_value={'id': 'interview', 'backend': 'claude', 'role': 'interview'}))
            with patch.object(backends, 'CLAUDE_ADMITTED', True), patch.object(backends, 'claude_module', return_value=module):
                st = archive.restore(result['checkpoint'], 'interview')
            module.restore.assert_called_once_with(str(folder), 'interview', mode='interview', data=self.data)
        self.assertEqual(st['parent_checkpoint'], result['checkpoint'])
        self.assertFalse(result['portable'])

    def test_reworked_adapter_close_registers_with_real_guard_and_fake_cli(self):
        # Cross the actual adapter/controller boundary; no model or real run.
        helper = common.CODEX.parent / 'claude-adapter/tests/test_adapter.py'
        spec = importlib.util.spec_from_file_location('claude_close_fixture', helper)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with patch.dict(os.environ, {'PATH': str(Path(sys.executable).parent) + os.pathsep + os.environ.get('PATH', '')}), patch.object(tempfile, 'tempdir', str(self.root)):
            run = module.Run([[{'done': {'stage': 'A1'}}, {'say': 'Synthetic leg complete.'}]])
            self.addCleanup(run.close)
            actor = run.actor(); self.addCleanup(actor.release)
            actor.message('Complete the synthetic fixture.'); actor.wait(30)
            # Claude's fake done event writes the marker only. Supply done.sh's
            # matching ledger too, which the controller has always required.
            write(run.run / '00_GIVE-THE-AGENT/RUN.json', {'legs': [
                {'stage': 'A1', 'leg': 'A1a', 'session': actor.state['session_id'], 'cut': None}]})
            raw = actor.close()
            result = claude_backend.register(raw, actor.state, scientific=True)
            verified = archive.verify_checkpoint(result['checkpoint'])
        self.assertTrue(raw['scientific']); self.assertEqual(raw['cut'], 'close')
        self.assertTrue(result['scientific'])
        self.assertEqual(verified['thread_id'], actor.state['session_id'])

    def test_restore_refuses_continuation_before_destination_or_parser(self):
        _, raw = self.bundle(); result = claude_backend.register(raw, self.state)
        before = inventory(self.root)
        with patch.object(backends, 'CLAUDE_ADMITTED', True), self.assertRaisesRegex(Error, 'continuation'):
            archive.restore(result['checkpoint'], 'new-analysis', mode='continuation')
        self.assertEqual(before, inventory(self.root))

    def test_capture_mutation_is_rejected_after_registration(self):
        folder, raw = self.bundle(); result = claude_backend.register(raw, self.state)
        (folder / 'transcript.jsonl').write_text('changed')
        with self.assertRaisesRegex(Error, 'archive set changed'): archive.verify_checkpoint(result['checkpoint'])

    def test_partial_close_manifest_and_false_verified_flag_do_not_pass(self):
        folder, raw = self.bundle('close')
        raw['digests'] = {'checkpoint.json': sha(folder / 'checkpoint.json')}
        (folder / 'MANIFEST.sha256').write_text(raw['digests']['checkpoint.json'] + '  checkpoint.json\n')
        with self.assertRaisesRegex(Error, 'incomplete'): claude_backend.register(raw, self.state, scientific=True)
        self.assertFalse((self.data / 'checkpoints').exists())

    def test_wrong_commit_label_actor_session_and_turn_are_rejected(self):
        folder, raw = self.bundle('close')
        for key, value in [('actor', 'other'), ('session', 'other'), ('last_turn', 'other'), ('checkpoint_id', 'other')]:
            with self.subTest(key=key), self.assertRaises(Error):
                claude_backend.register({**raw, key: value}, self.state, scientific=True)
        (folder / 'COMMITTED').write_text('unbound\n')
        with self.assertRaises(Error): claude_backend.register(raw, self.state, scientific=True)

    def test_forced_or_incomplete_close_cannot_advance(self):
        folder, raw = self.bundle('close')
        with self.assertRaisesRegex(Error, 'forced'): claude_backend.register({**raw, 'forced': True}, self.state, scientific=True)
        ck = read(folder / 'checkpoint.json'); ck['validation']['complete'] = False
        write(folder / 'checkpoint.json', ck); self.reseal(folder, raw)
        with self.assertRaisesRegex(Error, 'incomplete'): claude_backend.register(raw, self.state, scientific=True)

    def test_adapter_non_scientific_receipt_cannot_advance(self):
        _, raw = self.bundle('close')
        for flag in (False, None, 'true'):
            with self.subTest(flag=flag), self.assertRaisesRegex(Error, 'scientific'):
                claude_backend.register({**raw, 'scientific': flag}, self.state, scientific=True)
        self.assertFalse((self.data / 'checkpoints').exists())

    def test_close_cut_must_match_the_saved_marker(self):
        _, raw = self.bundle('close')
        for cut in (None, 'pause', 'interview'):
            with self.subTest(cut=cut), self.assertRaisesRegex(Error, 'cut'):
                claude_backend.register({**raw, 'cut': cut}, self.state, scientific=True)
        self.assertFalse((self.data / 'checkpoints').exists())

    def test_saved_pause_cannot_advance_even_with_complete_validation(self):
        (self.ws / 'out/_closes/A1-A1a.closed').write_text('2026-10-05T12:00:00Z pause\n')
        write(self.ws / 'RUN.json', {'legs': [{'stage': 'A1', 'leg': 'A1a', 'session': 'sid', 'cut': 'pause'}]})
        _, raw = self.bundle('close'); raw['cut'] = 'pause'
        with self.assertRaisesRegex(Error, 'cut'):
            claude_backend.register(raw, self.state, scientific=True)

    def test_saved_leg_record_must_bind_session_and_cut(self):
        write(self.ws / 'RUN.json', {'legs': [{'stage': 'A1', 'leg': 'A1a', 'session': 'other', 'cut': 'close'}]})
        _, raw = self.bundle('close')
        with self.assertRaisesRegex(Error, 'leg record'):
            claude_backend.register(raw, self.state, scientific=True)

    def test_standalone_handler_ownership_blocks_actions_before_side_effects(self):
        # Even an idle or stopped standalone handler owns its prepared run.
        write(self.rundir / 'CONTROL/legs/job.json', {'status': 'paused'})
        c = self.controller(self.fake_actor()); before = inventory(self.root)
        with patch.object(backends, 'CLAUDE_ADMITTED', True):
            for op in ('message', 'card', 'open', 'save', 'close', 'answer', 'answer-ask', 'start', 'pause', 'stop'):
                with self.subTest(op=op), self.assertRaisesRegex(Error, 'standalone handler'):
                    c.action({'action': op, 'actor': self.aid, 'run': self.run, 'text': 'test'})
            self.assertFalse(backends.allowed(self.state, 'close'))
        c.job.assert_not_called(); self.assertEqual(before, inventory(self.root))

    def test_standalone_handler_blocks_restore_before_adapter_or_destination(self):
        _, raw = self.bundle(); receipt = claude_backend.register(raw, self.state)
        (self.rundir / 'CONTROL/legs').mkdir(parents=True)
        module = SimpleNamespace(restore=Mock())
        before = inventory(self.root)
        with patch.object(backends, 'CLAUDE_ADMITTED', True), patch.object(backends, 'claude_module', return_value=module):
            with self.assertRaisesRegex(Error, 'standalone handler'):
                archive.restore(receipt['checkpoint'], 'new-interview')
        module.restore.assert_not_called(); self.assertEqual(before, inventory(self.root))

    def test_bridge_does_not_claim_a_standalone_handler_run(self):
        (self.rundir / 'CONTROL/legs').mkdir(parents=True)
        c = self.controller(self.fake_actor())
        with patch.object(backends, 'CLAUDE_ADMITTED', True), patch.object(blocks, 'tick'):
            before = inventory(self.root); bridge.tick(c)
        c.job.assert_not_called(); self.assertEqual(before, inventory(self.root))

    def test_native_transcript_must_match_export(self):
        folder, raw = self.bundle()
        (folder / 'transcript.jsonl').write_text('other transcript')
        self.reseal(folder, raw)
        with self.assertRaisesRegex(Error, 'disagree'): claude_backend.register(raw, self.state)

    def test_archive_links_refused_without_extracting(self):
        folder, raw = self.bundle()
        with tarfile.open(folder / 'fs.tar.gz', 'w:gz') as tar:
            m = tarfile.TarInfo('00_GIVE-THE-AGENT/escape'); m.type = tarfile.SYMTYPE; m.linkname = '/tmp'
            tar.addfile(m)
        self.reseal(folder, raw)
        with self.assertRaisesRegex(Error, 'Unsafe'): claude_backend.register(raw, self.state)

    def test_scientific_close_dispatches_once_and_skips_native_publication(self):
        _, raw = self.bundle('close'); receipt = claude_backend.register(raw, self.state, scientific=True)
        a = self.fake_actor(receipt); c = self.controller(a)
        with patch.object(backends, 'CLAUDE_ADMITTED', True), patch.object(study, 'trusted', side_effect=AssertionError('Native validator')), patch.object(server.publication, 'after_close', side_effect=AssertionError('Second publication')):
            result = c._close_leg(self.run, self.aid)
            with self.assertRaisesRegex(Error, 'does not own'): c._close_leg(self.run, self.aid)
        a.close.assert_called_once()
        s = study.run_state(self.run)
        self.assertEqual(s['legs']['A1a']['status'], 'verified'); self.assertIsNone(s['active_actor'])
        self.assertNotIn('dispatch_plan', s); self.assertEqual(result['backend'], 'claude')

    def test_changed_leg_record_after_snapshot_blocks_advance(self):
        _, raw = self.bundle('close'); receipt = claude_backend.register(raw, self.state, scientific=True)
        # Valid live record for the same leg, but not the archived file.
        data = read(self.ws / 'RUN.json'); data['extra'] = True; write(self.ws / 'RUN.json', data)
        with patch.object(backends, 'CLAUDE_ADMITTED', True), self.assertRaisesRegex(Error, 'differs from the leg record'):
            study.close(self.run, self.fake_actor(receipt))
        self.assertEqual(study.run_state(self.run)['active_actor'], self.aid)

    def test_pause_and_undelivered_messages_do_not_close(self):
        a = self.fake_actor()
        with patch.object(backends, 'CLAUDE_ADMITTED', True):
            self.state['undelivered'] = ['queued']
            with self.assertRaisesRegex(Error, 'undelivered'): study.close(self.run, a)
            self.state['undelivered'] = []
            with self.assertRaisesRegex(Error, 'paused-leg'): study.close_claude(self.run, a, self.study, self.ws, 'A1', 'A1a', 'pause')
        a.close.assert_not_called()

    def test_cards_use_adapter_delivery_and_platform_pause_marker(self):
        a = self.fake_actor(); c = self.controller(a)
        (self.ws / '.pause').write_text('pause')
        with patch.object(backends, 'CLAUDE_ADMITTED', True):
            result = c.action({'action': 'card', 'actor': self.aid, 'text': 'Consider this evidence'})
        a.message.assert_called_once_with('Investigator card: Consider this evidence')
        self.assertEqual(result['delivery']['delivery'], 'queued')
        self.assertIsNone(result['card']); self.assertFalse((self.base / 'workspace').exists())
        self.assertFalse((self.ws / '.pause').exists())

    def test_retention_preserves_shared_store_and_does_not_flag_or_lock(self):
        self.state.update(status='saved', retention_ready=True, checkpoint='anything')
        write(self.base / 'state.json', self.state); before = inventory(self.root)
        self.assertTrue(retention.ready(self.aid)['retained'])
        self.assertFalse(retention.evict(self.aid)['evicted'])
        self.assertEqual(before, inventory(self.root))

    def test_bridge_waits_for_admission_and_uses_real_workspace_after(self):
        a = self.fake_actor(); c = self.controller(a)
        c.list = lambda: {'actors': [], 'runs': [], 'jobs': {}}
        with patch.object(blocks, 'tick'):
            before = inventory(self.root); bridge.tick(c)
            self.assertEqual(before, inventory(self.root)); c.job.assert_not_called()
            with patch.object(backends, 'CLAUDE_ADMITTED', True):
                bridge.tick(c); bridge.tick(c)
        self.assertEqual(c.job.call_count, 1)
        self.assertEqual(c.job.call_args.args[1:], (self.run, self.aid))

    def test_unsupported_routes_refuse_before_writes_even_when_admitted(self):
        before = inventory(self.root)
        with patch.object(backends, 'CLAUDE_ADMITTED', True):
            for fn, args in [(study.prepare, (self.run, 'A1b-01')), (blocks.start, (self.run, 'A1b-01', 'A1b-02')),
                             (blocks.resume, (self.run,)), (branches.create, (self.run, 'fake', 'new', 'A1b-01')),
                             (questions.answer_study, (self.run, 'QA1-001', 'yes', self.aid))]:
                with self.subTest(fn=fn.__name__), self.assertRaises(Error): fn(*args)
        self.assertEqual(before, inventory(self.root))

    def test_freeze_uses_claude_inventory_and_detects_changed_model(self):
        (self.ws / 'out/model').mkdir()
        (self.ws / 'out/model/elements.jsonl').write_text('model\n')
        for name in ('branches.jsonl', 'subforms.jsonl', 'crosslinks.jsonl'):
            (self.ws / 'out' / name).write_text('tree\n')
        frozen = {'legs': {}}
        for stage in ('D3', 'D4'):
            st = {**self.state, 'label': stage + '.' + stage + 'a', 'leg': stage + 'a'}
            _, raw = self.bundle('close', st); receipt = claude_backend.register(raw, st, scientific=True)
            frozen['legs'][st['leg']] = {'stage': stage, 'leg': st['leg'], 'status': 'verified', 'checkpoint': receipt['checkpoint']}
        trust = study.run_dir(self.run) / 'trusted'; trust.mkdir()
        write(study.run_dir(self.run) / 'trusted-hashes.json', {})
        with patch.object(study, 'load_module', return_value=SimpleNamespace(MODEL_FILES=('model/elements.jsonl',))), patch.object(archive, 'verify', side_effect=AssertionError('Wrong archive parser')):
            study.frozen_inputs(self.run, frozen, self.ws)
            (self.ws / 'out/model/elements.jsonl').write_text('changed\n')
            with self.assertRaisesRegex(Error, 'Frozen D3 inputs changed'): study.frozen_inputs(self.run, frozen, self.ws)

    def test_idle_claude_questions_are_exposed_as_durable_not_native(self):
        self.state['questions'] = [{'requestKey': 'QA1-001', 'questions': [{'id': 'answer', 'question': 'Which scope?'}]}]
        write(self.base / 'state.json', self.state)
        # asks.jsonl is one compact JSON object per line.
        (self.ws / 'out/asks.jsonl').write_text(json.dumps({'id': 'QA1-001', 'question': 'Which scope?', 'assumption': 'Wait'}) + '\n')
        c = self.controller()
        with patch.object(backends, 'CLAUDE_ADMITTED', True):
            result = c.list()['actors'][0]
        self.assertFalse(result['questions_live']); self.assertEqual(len(result['questions']), 1)
        q = result['questions'][0]
        self.assertEqual(q['source'], 'file'); self.assertTrue(q['answerable']); self.assertEqual(q['run'], self.run)

    def test_idle_answer_routes_through_adapter_without_message(self):
        a = self.fake_actor(); a.answer = Mock(return_value={'new_turn_started': False})
        c = self.controller(a)
        with patch.object(backends, 'CLAUDE_ADMITTED', True), patch.object(questions, 'answer_study', side_effect=AssertionError('Wrong file writer')):
            result = c.action({'action': 'answer-ask', 'actor': self.aid, 'run': self.run, 'request': 'QA1-001', 'text': 'yes'})
        a.answer.assert_called_once_with('QA1-001', {'answer': 'yes'}); a.message.assert_not_called()
        self.assertFalse(result['new_turn_started'])

    def test_other_study_cannot_close_or_answer_this_actor(self):
        other = {**self.study, 'id': 'other', 'active_actor': 'different'}
        write(study.run_dir('other') / 'state.json', other)
        a = self.fake_actor(); a.answer = Mock()
        with patch.object(backends, 'CLAUDE_ADMITTED', True):
            with self.assertRaises(Error): study.close('other', a)
            with self.assertRaisesRegex(Error, 'another study'):
                self.controller(a).action({'action': 'answer-ask', 'actor': self.aid, 'run': 'other', 'request': 'QA1-001', 'text': 'yes'})
        a.close.assert_not_called(); a.answer.assert_not_called()

    def test_failed_scientific_close_preserves_current_leg(self):
        a = self.fake_actor(); a.close.side_effect = Error('Platform close failed')
        before = read(study.run_dir(self.run) / 'state.json')
        with patch.object(backends, 'CLAUDE_ADMITTED', True), self.assertRaisesRegex(Error, 'Platform close failed'):
            study.close(self.run, a)
        self.assertEqual(before, read(study.run_dir(self.run) / 'state.json'))

    def test_controller_restart_keeps_idle_claude_questions(self):
        self.state['questions'] = [{'requestKey': 'QA1-001'}]
        write(self.base / 'state.json', self.state)
        with patch.object(bridge, 'watch'):
            c = server.Controller()
            c.stopping.set(); c.watcher.join()
            c.pool.shutdown(); c.control_pool.shutdown()
        self.assertEqual(read(self.base / 'state.json'), self.state)

    def test_registered_reference_cannot_change_backend_or_folder(self):
        _, raw = self.bundle(); receipt = claude_backend.register(raw, self.state)
        root = self.data / 'checkpoints' / receipt['checkpoint']
        write(root / 'receipt.json', {**receipt, 'backend': 'codex'})
        with patch.object(archive, 'verify', side_effect=AssertionError('Wrong parser')), self.assertRaises(Error):
            archive.verify_checkpoint(receipt['checkpoint'])
        write(root / 'receipt.json', receipt)
        record = read(root / 'backend.json'); record['folder'] = str(self.root / 'elsewhere')
        write(root / 'backend.json', record)
        with self.assertRaisesRegex(Error, 'reference changed'): archive.verify_checkpoint(receipt['checkpoint'])
