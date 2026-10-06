#!/usr/bin/env python3
"""The adapter's offline tests: a stand-in CLI (fake_stream_claude.py) and a small run that carries the
real harness's protocol_guard.py, so the session bookkeeping (prepare, confirm, preclose) is the
harness's own. No model is called and nothing outside a temporary folder is written.
    python3 aggregator/handler/claude-adapter/tests/test_adapter.py
"""
import fcntl
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ADAPTER = HERE.parent
HARNESS = Path(os.environ.get('ADAPTER_TEST_HARNESS') or ADAPTER.parent / 'claude')   # the harness beside it
FAKE = HERE / 'fake_stream_claude.py'


def load(name):
    spec = importlib.util.spec_from_file_location('adapter_test_' + name, ADAPTER / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load('stream')
A = load('actor')

# the run's step.sh and close.sh: harness_stub.py, which builds what a real close builds (a complete snapshot)
STEP = '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/harness_stub.py" step "$@"\n'
CLOSE = '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/harness_stub.py" close "$@"\n'


class Run:
    """A temporary repository with one run in aggregator/runs, and the controller's data folder."""
    def __init__(self, turns):
        self.t = Path(tempfile.mkdtemp(prefix='adapter-test-')).resolve()   # macOS reaches its temporary folder through a link
        self.run = self.t / 'repo/aggregator/runs/test-run'
        c = self.run / 'CONTROL'
        (c / 'harness/validation_tools').mkdir(parents=True)
        (c / '.cc').mkdir()
        (self.run / '00_GIVE-THE-AGENT/out').mkdir(parents=True)
        shutil.copy(HARNESS / 'protocol_guard.py', c / 'harness/protocol_guard.py')
        shutil.copy(HERE / 'harness_stub.py', c / 'harness/harness_stub.py')
        shutil.copy(HARNESS / 'settings.template.json', c / 'settings.template.json')
        (c / 'harness/step.sh').write_text(STEP)
        (c / 'harness/close.sh').write_text(CLOSE)
        (c / 'harness/validation_tools/validate.py').write_text('import sys\nsys.exit(0)\n')
        (c / 'arm.json').write_text(json.dumps({'A1': {'analyst': 'claude-test-model', 'effort': 'medium'}}))
        (c / 'RUN.json').write_text('{}\n')
        (c / '.cc/.claude.json').write_text('{}\n')
        self.data = self.t / 'data'
        os.environ['RPLACE_ADAPTER_DATA'] = str(self.data)
        self.scenario = self.t / 'scenario.json'
        self.scenario.write_text(json.dumps({'turns': turns}))
        os.environ['FAKE_SCENARIO'] = str(self.scenario)
        # the stand-in runs through a launcher of its own: the test folder may not allow executing it
        self.exe = self.t / 'bin/claude'
        self.exe.parent.mkdir()
        self.exe.write_text('#!/bin/sh\nexec "%s" "%s" "$@"\n' % (sys.executable, FAKE))
        self.exe.chmod(0o755)

    def actor(self, name='claude-test-1', leg='A1a'):
        A.create(name, self.run, leg, executable=str(self.exe))
        return A.ClaudeActor(name)

    def events(self, name='claude-test-1'):
        p = self.data / 'actors' / name / 'events.jsonl'
        return [json.loads(x)['native'] for x in p.read_text().splitlines()] if p.exists() else []

    def calls(self):
        p = self.run / 'CONTROL/.cc/stream_calls.jsonl'
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

    def close(self):
        shutil.rmtree(self.t, ignore_errors=True)


def until(fn, timeout=15):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        v = fn()
        if v:
            return v
        time.sleep(0.05)
    raise AssertionError('condition not met in %ss' % timeout)


class TranslatorTest(unittest.TestCase):
    def test_streamed_and_whole_text_share_one_item(self):
        t = S.Translator('sid', 'turn')
        out = []
        for m in ({'type': 'stream_event', 'event': {'type': 'message_start', 'message': {'id': 'm1'}}},
                  {'type': 'stream_event', 'event': {'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'thinking'}}},
                  {'type': 'stream_event', 'event': {'type': 'content_block_start', 'index': 1, 'content_block': {'type': 'text'}}},
                  {'type': 'stream_event', 'event': {'type': 'content_block_delta', 'index': 1, 'delta': {'type': 'text_delta', 'text': 'Hel'}}},
                  {'type': 'stream_event', 'event': {'type': 'content_block_delta', 'index': 1, 'delta': {'type': 'text_delta', 'text': 'lo'}}},
                  {'type': 'assistant', 'message': {'id': 'm1', 'content': [{'type': 'thinking', 'thinking': 'secret'}]}},
                  {'type': 'assistant', 'message': {'id': 'm1', 'content': [{'type': 'text', 'text': 'Hello'}]}}):
            out += t.feed(m)
        deltas = [p for m, p in out if m == 'item/agentMessage/delta']
        whole = [p['item'] for m, p in out if m == 'item/completed']
        self.assertEqual([d['delta'] for d in deltas], ['Hel', 'lo'])
        self.assertEqual(len(whole), 1)
        self.assertEqual(whole[0]['id'], deltas[0]['itemId'])
        self.assertNotIn('secret', json.dumps(out))

    def test_tools_helpers_and_notes(self):
        t = S.Translator('sid', 'turn')
        out = t.feed({'type': 'assistant', 'message': {'id': 'm', 'content': [
            {'type': 'tool_use', 'id': 'b1', 'name': 'Bash', 'input': {'command': 'ls out'}},
            {'type': 'tool_use', 'id': 'h1', 'name': 'Agent', 'input': {'description': 'count rooms', 'prompt': 'Count the rooms in store/rooms.jsonl.', 'subagent_type': 'general-purpose'}}]}})
        self.assertEqual(out[0][1]['item']['command'], 'Bash: ls out')
        self.assertEqual(out[0][1]['item']['type'], 'commandExecution')
        self.assertIn('Count the rooms', out[1][1]['item']['aggregatedOutput'])
        out = t.feed({'type': 'user', 'message': {'content': [{'type': 'text', 'text': 'Count the rooms in store/rooms.jsonl.'}]}, 'parent_tool_use_id': 'h1'})
        self.assertEqual(out, [])   # the same prompt is already on the helper's row
        out = t.feed({'type': 'assistant', 'message': {'id': 'x', 'content': [{'type': 'tool_use', 'id': 'r1', 'name': 'Read', 'input': {'file_path': 'store/rooms.jsonl'}}]}, 'parent_tool_use_id': 'h1'})
        self.assertTrue(out[0][1]['item']['command'].startswith('Helper "count rooms"'))
        out = t.feed({'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': 'b1', 'content': [{'type': 'text', 'text': 'a\nb'}], 'is_error': True}]}})
        self.assertEqual(out[0][1]['item']['status'], 'failed')
        self.assertEqual(out[0][1]['item']['aggregatedOutput'], 'a\nb')
        out = t.feed({'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': 'h1', 'content': '705 rooms'}]}})
        self.assertIn('705 rooms', out[0][1]['item']['aggregatedOutput'])
        self.assertIn('Count the rooms', out[0][1]['item']['aggregatedOutput'])
        self.assertEqual(t.feed({'type': 'system', 'subtype': 'compact_boundary'})[0][1]['item']['command'], 'Context compacted')
        self.assertEqual(t.feed({'type': 'system', 'subtype': 'permission_denied', 'tool_name': 'Write'})[0][1]['item']['status'], 'failed')
        self.assertEqual(t.feed({'type': 'tool_progress'}), [])
        self.assertEqual(t.feed({'type': 'result', 'subtype': 'success'}), [])
        self.assertEqual(t.result['subtype'], 'success')


class HookTest(unittest.TestCase):
    def setUp(self):
        self.inbox = Path(tempfile.mkdtemp(prefix='adapter-inbox-'))

    def tearDown(self):
        shutil.rmtree(self.inbox, ignore_errors=True)

    def hook(self, payload):
        r = subprocess.run([sys.executable, str(ADAPTER / 'inbox_hook.py'), str(self.inbox)], input=payload,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(r.returncode, 0)
        return r.stdout

    def test_delivers_once_and_never_to_a_helper(self):
        self.assertEqual(self.hook('{}'), '')
        for i, kind in enumerate(('message', 'answer')):
            (self.inbox / ('2026100%d-x.json' % i)).write_text(json.dumps({'id': str(i), 'kind': kind, 'text': 'text %d' % i, 'utc': 'now'}))
        self.assertEqual(self.hook(json.dumps({'agent_id': 'a1', 'tool_name': 'Read'})), '')
        out = json.loads(self.hook(json.dumps({'tool_name': 'Bash', 'tool_use_id': 't1', 'session_id': 's'})))
        ctx = out['hookSpecificOutput']['additionalContext']
        self.assertEqual(out['hookSpecificOutput']['hookEventName'], 'PostToolUse')
        self.assertIn('Message from the principal investigator', ctx)
        self.assertIn('text 0', ctx)
        self.assertIn('text 1', ctx)
        self.assertEqual(len(list((self.inbox / 'delivered').glob('*.json'))), 2)
        self.assertEqual(self.hook(json.dumps({'tool_name': 'Bash'})), '')
        self.assertEqual(self.hook('not json'), '')


class LifecycleTest(unittest.TestCase):
    def tearDown(self):
        self.r.close()

    def test_a_turn_end_to_end_and_the_harness_close(self):
        self.r = Run([[{'say': 'Reading the head.'}, {'tool': 'Bash', 'input': {'command': 'cat out/_head.md'}, 'output': 'head'},
                       {'thinking': 'private'}, {'done': {'stage': 'A1'}}, {'say': 'Leg done.'}],
                      [{'say': 'Second turn.'}]])
        a = self.r.actor()
        cap = a.capabilities()
        self.assertEqual((cap['backend'], cap['queued_messages_start_turns'], cap['restore_modes']), ('claude', False, ['interview']))
        self.assertEqual(cap['workspace'], str(self.r.run / '00_GIVE-THE-AGENT'))
        st = json.loads((self.r.data / 'actors/claude-test-1/state.json').read_text())
        self.assertEqual((st['backend'], st['label'], st['model'], st['effort'], st['mode']),
                         ('claude', 'A1.A1a', 'claude-test-model', 'medium', 'fresh'))
        self.assertEqual(st['runtime']['flags'], list(A.OPTIONAL))
        first = (self.r.data / 'actors/claude-test-1/first-message.txt').read_text()
        a.message(first)
        c = self.r.run / 'CONTROL'
        self.assertTrue((c / 'active_launch.json').exists())
        with (c / '.protocol.lock').open('a') as f:
            with self.assertRaises(BlockingIOError):
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        a.wait(30)
        self.assertEqual((a.state['status'], a.state['boundary']), ('idle', 'completed'))
        self.assertFalse((c / 'active_launch.json').exists())
        self.assertEqual(json.loads((c / 'last_launch_exit.json').read_text())['exit_code'], 0)
        self.assertEqual(json.loads((c / 'sessions.json').read_text())['A1.A1a']['session_id'], a.state['session_id'])
        self.assertTrue(a.state['confirmed'])
        call = self.r.calls()[0]
        argv = call['argv']
        for k, v in (('--output-format', 'stream-json'), ('--permission-mode', 'dontAsk'), ('--session-id', a.state['session_id']),
                     ('--model', 'claude-test-model'), ('--effort', 'medium'), ('--permission-prompts', 'none')):
            self.assertEqual(argv[argv.index(k) + 1], v)
        for f in ('-p', '--verbose', '--include-partial-messages', '--forward-subagent-text', '--strict-mcp-config', '--settings'):
            self.assertIn(f, argv)
        self.assertEqual(argv[-1], first)
        self.assertEqual(call['env']['CLAUDE_CODE_PROJECT_DIR_NAME'], 'run')
        self.assertEqual(call['env']['CLAUDE_CODE_DISABLE_AUTO_MEMORY'], '1')
        self.assertTrue(call['cwd'].endswith('00_GIVE-THE-AGENT'))
        methods = [e['method'] for e in self.r.events()]
        for m in ('item/completed', 'turn/started', 'item/agentMessage/delta', 'item/started', 'turn/completed'):
            self.assertIn(m, methods)
        texts = [e['params']['item'].get('text') for e in self.r.events() if e['method'] == 'item/completed'
                 and e['params']['item']['type'] == 'agentMessage']
        self.assertEqual(texts, ['Reading the head.', 'Leg done.'])
        self.assertNotIn('private', json.dumps(self.r.events()))
        self.assertEqual(a.final(), 'Leg done.')
        cmd = json.loads(next((self.r.data / 'actors/claude-test-1/turns').glob('*/command.json')).read_text())
        self.assertNotIn(first, json.dumps(cmd))
        # the next message resumes the leg's own session
        a.message('One more thing.')
        a.wait(30)
        argv = self.r.calls()[1]['argv']
        self.assertEqual(argv[argv.index('--resume') + 1], a.state['session_id'])
        # saving is not closing: the folder and the session, verified, and close.sh does not run
        saved = a.checkpoint()
        self.assertEqual((saved['backend'], saved['kind'], saved['verified']), ('claude', 'capture', True))
        for name in ('fs.tar.gz', 'agent.tar.gz', 'transcript.jsonl', 'checkpoint.json'):
            self.assertIn(name, saved['digests'])
            self.assertTrue((Path(saved['archive']) / name).exists())
        self.assertFalse((c / 'close-calls.log').exists())
        self.assertFalse(a.state.get('closed'))
        # the harness's own preclose accepts what the adapter left: a finished turn and an exited launcher
        receipt = a.close()
        committed = (c / 'snapshots/A1.A1a/COMMITTED').read_text().strip()
        self.assertEqual((receipt['kind'], receipt['label'], receipt['checkpoint_id']), ('close', 'A1.A1a', committed))
        self.assertTrue(receipt['verified'] and receipt['scientific'])
        self.assertEqual((receipt['cut'], receipt['forced']), ('close', False))
        self.assertEqual(set(receipt['digests']) & A.CLOSE_FILES, A.CLOSE_FILES)
        self.assertEqual(receipt['publication']['status'], 'no repository')
        status = json.loads((c / 'close-status-A1.A1a.json').read_text())
        self.assertTrue(status['completed_turn'] and status['launcher_exited'] and status['complete'])
        self.assertEqual(a.state['status'], 'closed')
        # once: a second close returns the same receipt and runs nothing
        again = a.close()
        self.assertTrue(again['repeated'])
        self.assertEqual(again['checkpoint_id'], receipt['checkpoint_id'])
        self.assertEqual(len((c / 'close-calls.log').read_text().splitlines()), 1)
        with self.assertRaises(A.Error):
            a.message('After the close.')

    def test_a_message_mid_turn_reaches_the_analyst_beside_a_tool_result(self):
        self.r = Run([[{'tool': 'Bash', 'input': {'command': 'sleep 1'}, 'output': '', 'sleep': 1.0},
                       {'wait_context': 15}, {'say': 'Back to the leg.'}]])
        a = self.r.actor()
        a.message('Start.')
        r = a.message('Use the h73 cut, not h78.')
        self.assertIn('queued', r)
        a.wait(30)
        heard = [e['params']['item']['text'] for e in self.r.events() if e['method'] == 'item/completed'
                 and e['params']['item']['type'] == 'agentMessage' and e['params']['item']['text'].startswith('heard:')]
        self.assertTrue(heard and 'Use the h73 cut, not h78.' in heard[0])
        self.assertIn('Message from the principal investigator', heard[0])
        receipts = [json.loads(p.read_text()) for p in (self.r.data / 'actors/claude-test-1/inbox/delivered').glob('*.json')]
        self.assertEqual([x['via'] for x in receipts], ['hook'])
        self.assertTrue(any(e['params'].get('item', {}).get('command', '').startswith('Message delivered')
                            for e in self.r.events() if e['method'] == 'item/completed'))
        users = [e['params']['item'] for e in self.r.events() if e['method'] == 'item/completed'
                 and e['params']['item']['type'] == 'userMessage']
        self.assertEqual([u['content'][0]['text'] for u in users], ['Start.', 'Use the h73 cut, not h78.'])

    def test_a_message_no_tool_call_picks_up_waits_for_j(self):
        self.r = Run([[{'tool': 'Bash', 'input': {'command': 'true'}, 'output': ''}, {'pause': 1.5}, {'say': 'Done.'}],
                      [{'say': 'Answering J.'}]])
        a = self.r.actor()
        a.message('Start.')
        until(lambda: len([e for e in self.r.events() if e['method'] == 'item/completed'
                           and e['params']['item']['type'] == 'commandExecution']) >= 1)
        r = a.message('Did you check the frame?')
        self.assertEqual((r['delivery'], r['new_turn_started']), ('pending', False))
        a.wait(30)
        time.sleep(1.0)
        self.assertEqual(len(self.r.calls()), 1)   # no turn opened by itself
        self.assertEqual(a.state['undelivered'], [r['queued']])
        self.assertIsNone(a.receipt(r['queued']))
        self.assertTrue(any(e['params'].get('item', {}).get('command', '').startswith('1 message(s) not delivered')
                            for e in self.r.events() if e['method'] == 'item/completed'))
        s = a.continue_queued()   # J's explicit word
        self.assertEqual(s['delivered_with_prompt'], [r['queued']])
        a.wait(30)
        argv = self.r.calls()[1]['argv']
        self.assertIn('Did you check the frame?', argv[-1])
        self.assertEqual(argv[argv.index('--resume') + 1], a.state['session_id'])
        self.assertEqual(a.receipt(r['queued'])['via'], 'prompt')
        self.assertEqual(a.state['undelivered'], [])
        self.assertIn('rplace/messageDelivered', [e['method'] for e in self.r.events()])
        with self.assertRaises(A.Error):
            a.continue_queued()

    def test_a_failed_start_keeps_the_message_and_a_retry_sends_it(self):
        self.r = Run([[{'say_context': True}]])
        a = self.r.actor()
        good = a.state['runtime']['executable']
        a.state['runtime']['executable'] = str(self.r.t / 'bin/missing-claude')
        a.save()
        with self.assertRaises(OSError):   # the missing executable
            a.message('Read the head first.')
        self.assertEqual(len(a.state['undelivered']), 1)
        self.assertIn('could not start', a.state['error'])
        self.assertFalse((self.r.run / 'CONTROL/active_launch.json').exists())
        time.sleep(0.5)
        self.assertEqual(self.r.calls(), [])
        a.state['runtime']['executable'] = good
        a.save()
        s = a.continue_queued()
        self.assertEqual(len(s['delivered_with_prompt']), 1)
        a.wait(30)
        self.assertIn('Read the head first.', self.r.calls()[0]['argv'][-1])
        self.assertEqual(a.state['boundary'], 'completed')

    def test_an_unconfirmed_session_fails_the_boundary(self):
        self.r = Run([[{'foreign_session': True}, {'say': 'Done.'}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        self.assertEqual((a.state['status'], a.state['boundary']), ('failed', 'failed'))
        self.assertIn('Session not confirmed', a.state['error']['message'])
        self.assertFalse(a.state['confirmed'])

    def test_a_later_turn_under_another_session_fails_its_boundary(self):
        # every turn's transcript is checked, not only the first (OpenAI recheck 2026-10-05, blocker 2)
        self.r = Run([[{'say': 'One.'}], [{'foreign_session': True}, {'say': 'Two.'}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        self.assertEqual((a.state['boundary'], a.state['confirmed']), ('completed', True))
        a.message('Again.')
        a.wait(30)
        self.assertEqual(a.state['boundary'], 'failed')
        self.assertIn('the turn added is under session', a.state['error']['message'])

    def test_a_turn_held_from_its_run_files_is_finished_first_and_never_over_a_later_turn(self):
        # independent review of the recheck round: a held turn is finished under the lock before the next launch,
        # and never written over a later turn's boundary
        self.r = Run([[{'say': 'One.'}, {'pause': 2}, {'say': 'One done.'}], [{'say': 'Two.'}, {'exit': 3}]])
        a = self.r.actor()
        c = self.r.run / 'CONTROL'
        a.message('Start.')
        with a.guard:   # another owner (close.sh from Terminal, say) takes the run's lock while the turn runs
            A.unlock(a.runlock)
            a.runlock = None
            a.lock_wait = 0.5
            other = (c / '.protocol.lock').open('a')
            fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
        a.wait(30)
        first = a.state['last_turn_id']
        self.assertEqual(a.state['boundary'], 'uncertain')
        self.assertEqual(a.state['pending_finalize']['turn'], first)
        self.assertFalse((c / 'last_launch_exit.json').exists())
        with self.assertRaisesRegex(A.Error, 'nothing saved'):
            a.checkpoint()
        A.unlock(other)
        a.lock_wait = None
        a.message('Again.')   # the held turn is finished under the lock this start takes, then the turn runs
        a.wait(30)
        self.assertNotIn('pending_finalize', a.state)
        self.assertEqual(a.state['boundary'], 'failed')
        self.assertTrue(a.state['confirmed'])
        self.assertEqual(json.loads((c / 'last_launch_exit.json').read_text())['adapter_turn'], a.state['last_turn_id'])
        a.release()
        b = A.ClaudeActor('claude-test-1')
        b.open()
        self.assertEqual((b.state['boundary'], b.state['last_turn_id']), ('failed', a.state['last_turn_id']))
        self.assertNotEqual(first, a.state['last_turn_id'])
        b.release()

    def test_a_turn_settled_while_the_lock_is_held_waits_for_no_one(self):
        # independent review of the recheck round: open() settles without waiting for the run's lock
        self.r = Run([[{'say': 'One.'}, {'pause': 1}, {'say': 'One done.'}]])
        self.r.actor()
        c = self.r.run / 'CONTROL'
        code = ('import sys, os, time; sys.path.insert(0, %r); import test_adapter as T; '
                'a = T.A.ClaudeActor("claude-test-1"); a.message("Start."); time.sleep(0.5); os._exit(9)') % str(HERE)
        subprocess.run([sys.executable, '-c', code], env=dict(os.environ, RPLACE_ADAPTER_LOCK_WAIT='30'), check=False)
        until(lambda: not A.group_alive(json.loads((self.r.data / 'actors/claude-test-1/state.json').read_text())
                                       .get('last_pid')), timeout=20)
        other = (c / '.protocol.lock').open('a')
        fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
        b = A.ClaudeActor('claude-test-1')
        t0 = time.monotonic()
        os.environ['RPLACE_ADAPTER_LOCK_WAIT'] = '30'
        try:
            b.open()
        finally:
            os.environ.pop('RPLACE_ADAPTER_LOCK_WAIT', None)
        self.assertLess(time.monotonic() - t0, 5)
        self.assertEqual(b.state['boundary'], 'uncertain')
        A.unlock(other)
        b.release()
        d = A.ClaudeActor('claude-test-1')
        d.open()   # the lock is free: the held turn is finished now
        self.assertEqual(d.state['boundary'], 'completed')
        self.assertNotIn('pending_finalize', d.state)
        self.assertEqual(json.loads((c / 'last_launch_exit.json').read_text())['adapter_turn'], d.state['last_turn_id'])
        d.release()

    def test_an_old_leg_never_saves_or_closes_the_next_legs_folder(self):
        # OpenAI recheck 2026-10-05, blocker 1
        self.r = Run([[{'say': 'A1a done.'}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        self.r.actor('claude-test-2', 'A1b-01')   # step.sh prepares the next leg: the run moves on
        (self.r.run / '00_GIVE-THE-AGENT/later-leg.txt').write_text('A1b-01 was here\n')
        with self.assertRaisesRegex(A.Error, 'moved on to A1.A1b-01'):
            a.checkpoint()
        with self.assertRaisesRegex(A.Error, 'moved on to A1.A1b-01'):
            a.close(force=True)
        self.assertFalse((self.r.data / 'actors/claude-test-1/captures').exists())

    def test_an_idle_question_is_answered_without_a_turn(self):
        ask = {'id': 'QA1-002', 'question': 'Which frame?', 'assumption': 'I use the 705.'}
        self.r = Run([[{'tool': 'Bash', 'input': {'command': 'python3 tools/mem.py ask ...'}, 'output': 'asked', 'ask': ask},
                       {'say': 'Done.'}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        q = until(lambda: json.loads((self.r.data / 'actors/claude-test-1/state.json').read_text()).get('questions'))
        self.assertEqual(q[0]['requestKey'], 'QA1-002')
        r = a.answer('QA1-002', {'answer': 'The 705.'})
        self.assertFalse(r['new_turn_started'])
        f = self.r.run / '00_GIVE-THE-AGENT/out/_answers/QA1-002.md'
        self.assertEqual(f.read_text(), 'The 705.\n')
        self.assertEqual(oct(f.stat().st_mode & 0o777), oct(0o444))
        time.sleep(0.5)
        self.assertEqual(len(self.r.calls()), 1)
        self.assertEqual(a.state['undelivered'], [r['message']])
        # one owner at a time; a fresh owner after a controller restart shows nothing open and starts nothing
        with self.assertRaises(A.Error):
            A.ClaudeActor('claude-test-1').open()
        a.release()
        b = A.ClaudeActor('claude-test-1')
        b.open()
        self.assertEqual(b.state['open_asks'], [])
        self.assertEqual(len(self.r.calls()), 1)

    def test_restore_opens_an_interview_and_refuses_a_continuation(self):
        # two turns before the save: the parent's lines without ids then outnumber the interview's new rows, so
        # a fork's history is told by message ids, never by a line count (J's Mac, claude 2.1.289, 5 October)
        self.r = Run([[{'say': 'Leg done.'}], [{'say': 'More.'}], [{'say_context': True}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        a.message('Go on.')
        a.wait(30)
        saved = a.checkpoint()
        with self.assertRaises(A.Error):
            A.restore(saved, 'claude-continue-1', mode='continuation', executable=str(self.r.exe))
        self.assertFalse((self.r.data / 'actors/claude-continue-1').exists())
        self.assertFalse((self.r.run / 'interview-workspaces').exists())
        st = A.restore(saved, 'claude-iv-1', executable=str(self.r.exe))
        self.assertEqual((st['role'], st['mode'], st['parent_session']), ('interview', 'fork', a.state['session_id']))
        b = A.ClaudeActor('claude-iv-1')
        self.assertTrue(str(b.workspace).endswith('00_GIVE-THE-AGENT'))
        self.assertIn('interview-workspaces', str(b.workspace))
        self.assertIsNone(b.capabilities()['close'])
        b.message('What did you find?')
        b.wait(30)
        call = self.r.calls()[-1]
        argv = call['argv']
        self.assertEqual(argv[argv.index('--resume') + 1], a.state['session_id'])
        self.assertIn('--fork-session', argv)
        self.assertEqual(argv[argv.index('--session-id') + 1], st['session_id'])
        self.assertTrue(argv[-1].startswith('This is an interview, not a leg.'))
        self.assertEqual(call['env']['CLAUDE_CODE_PROJECT_DIR_NAME'], st['project'])
        self.assertEqual(call['cwd'], str(b.workspace))
        self.assertEqual(b.state['boundary'], 'completed')
        self.assertFalse((self.r.run / 'CONTROL/active_launch.json').exists())
        # the saved folder is untouched
        self.assertTrue(A.verify_saved(A.harness(self.r.run), saved['archive']))
        with self.assertRaises(A.Error):
            b.close()

    def test_a_question_is_answered_from_the_panel(self):
        ask = {'id': 'QA1-001', 'question': 'Which cut counts?', 'assumption': 'I use h73 meanwhile.'}
        self.r = Run([[{'tool': 'Bash', 'input': {'command': 'python3 tools/mem.py ask ...'}, 'output': 'asked', 'ask': ask},
                       {'wait_context': 20}, {'say': 'Done.'}]])
        a = self.r.actor()
        a.message('Start.')
        q = until(lambda: json.loads((self.r.data / 'actors/claude-test-1/state.json').read_text()).get('questions'))
        self.assertEqual((q[0]['requestKey'], q[0]['isBlocking']), ('QA1-001', False))
        self.assertIn('Which cut counts?', q[0]['questions'][0]['question'])
        self.assertIn('I use h73 meanwhile.', q[0]['questions'][0]['question'])
        with self.assertRaises(A.Error):
            a.answer('QA1-001', {'answer': '  '})
        r = a.answer('QA1-001', {'answer': 'h73 counts.'})
        self.assertEqual(r['answered'], 'QA1-001')
        a.wait(30)
        ag = self.r.run / '00_GIVE-THE-AGENT'
        self.assertEqual((ag / 'out/_answers/QA1-001.md').read_text(), 'h73 counts.\n')
        heard = [e['params']['item']['text'] for e in self.r.events() if e['method'] == 'item/completed'
                 and e['params']['item']['type'] == 'agentMessage' and e['params']['item']['text'].startswith('heard:')]
        self.assertTrue(heard and 'answered QA1-001' in heard[0] and 'h73 counts.' in heard[0])
        methods = [e['method'] for e in self.r.events()]
        self.assertIn('item/tool/requestUserInput', methods)
        self.assertIn('rplace/questionAnswered', methods)
        self.assertEqual(a.state['questions'], [])
        with self.assertRaises(A.Error):
            a.answer('QA1-001', {'answer': 'again'})

    def test_stop_interrupts_and_close_needs_force(self):
        self.r = Run([[{'tool': 'Bash', 'input': {'command': 'sleep 20'}, 'output': '', 'sleep': 20}]])
        a = self.r.actor()
        a.message('Start.')
        until(self.r.calls)
        time.sleep(0.5)
        a.interrupt()
        self.assertEqual((a.state['status'], a.state['boundary']), ('interrupted', 'interrupted'))
        self.assertNotEqual(json.loads((self.r.run / 'CONTROL/last_launch_exit.json').read_text())['exit_code'], 0)
        saved = a.checkpoint()   # an interrupted session can be saved; that is not a close
        self.assertEqual((saved['boundary'], saved['verified']), ('interrupted', True))
        self.assertFalse((self.r.run / 'CONTROL/close-calls.log').exists())
        with self.assertRaises(A.Error):
            a.close()
        receipt = a.close(force=True)
        self.assertTrue(receipt['forced'] and receipt['verified'])
        self.assertFalse(receipt['scientific'])   # a forced close never advances the run
        self.assertIn('--force', (self.r.run / 'CONTROL/close-calls.log').read_text())

    def test_close_verifies_the_snapshot_whole(self):
        self.r = Run([[{'done': {'stage': 'A1'}}, {'say': 'Closed.'}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        receipt = a.close()
        d = self.r.run / 'CONTROL/snapshots/A1.A1a'
        # a file changed after the close: the repeat is checked from the files and refused
        with (d / 'validation-report.txt').open('a') as f:
            f.write('changed\n')
        with self.assertRaises(A.Error):
            a.close()
        (d / 'validation-report.txt').write_text((d / 'validation-report.txt').read_text()[:-len('changed\n')])
        self.assertEqual(a.close()['checkpoint_id'], receipt['checkpoint_id'])
        # a file the manifest does not list, a missing manifest, a COMMITTED that names another checkpoint
        (d / 'extra.txt').write_text('x')
        with self.assertRaises(A.Error):
            a.close_receipt(d, None, None, None)
        (d / 'extra.txt').unlink()
        (d / 'MANIFEST.sha256').rename(d / 'MANIFEST.keep')
        with self.assertRaises(A.Error):
            a.close_receipt(d, None, None, None)
        (d / 'MANIFEST.keep').rename(d / 'MANIFEST.sha256')
        good = (d / 'COMMITTED').read_text()
        (d / 'COMMITTED').write_text('another\n')
        with self.assertRaises(A.Error):
            a.close_receipt(d, None, None, None)
        (d / 'COMMITTED').write_text(good)
        self.assertTrue(a.close_receipt(d, None, None, None)['verified'])


class PublicationTest(unittest.TestCase):
    def test_publication_lines(self):
        for text, status in (('  git: pushed "close A1.A1a"', 'pushed'),
                             ('  git: committed "close A1.A1a"\n  git: no remote set; committed locally', 'committed, no remote'),
                             ('  git: committed\n  git: push failed', 'committed, push failed'),
                             ('  git: the run is not in a repository; nothing committed', 'no repository'),
                             ('checkpoint A1.A1a', 'not reported')):
            self.assertEqual(A.publication(text)['status'], status)

    def test_helpers_prompts_and_pause(self):
        self.r = Run([[{'helper': {'description': 'count rooms', 'prompt': 'Count the rooms. Report the number only.',
                                   'subagent_type': 'general-purpose'}, 'reply': '705'}, {'say': 'Done.'}]])
        a = self.r.actor()
        a.message('Start.')
        a.wait(30)
        rows = [e['params']['item'] for e in self.r.events() if e['method'] in ('item/started', 'item/completed')]
        helper = [x for x in rows if x.get('command', '').startswith('Helper (general-purpose): count rooms')]
        self.assertTrue(helper and 'Count the rooms. Report the number only.' in helper[0]['aggregatedOutput'])
        self.assertIn('705', helper[-1]['aggregatedOutput'])
        self.assertTrue(any(x.get('command', '').startswith('Helper "count rooms" · Read') for x in rows))
        self.assertTrue(any(x.get('command', '') == 'Helper "count rooms" says' for x in rows))
        r = a.pause()
        self.assertFalse(r['new_turn_started'])
        self.assertTrue((self.r.run / '00_GIVE-THE-AGENT/.pause').read_text().startswith('pause requested '))
        self.assertIn('pause-requested', (self.r.run / 'CONTROL/handover-events.log').read_text())


class PathsTest(unittest.TestCase):
    def test_no_full_path_in_the_adapter(self):
        # verify.sh's pattern, built from parts so that this line does not match it
        roots = '|'.join('/%s/' % r for r in ('Users', 'home', 'sessions', 'mnt', 'private', 'root', 'tmp', 'var/folders'))
        pat = re.compile(r'(^|[\s"\'(=`])(' + roots + '|~/mnt/|~/Jail/|[A-Z]:\\\\)')
        for p in list(ADAPTER.glob('*.py')) + list(ADAPTER.glob('*.md')) + list(HERE.glob('*.py')):
            for i, line in enumerate(p.read_text().splitlines(), 1):
                self.assertIsNone(pat.search(line), '%s:%d' % (p.name, i))


if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')   # the harness's own files leave ResourceWarnings
