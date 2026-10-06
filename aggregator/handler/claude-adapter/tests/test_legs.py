#!/usr/bin/env python3
"""The leg handler's offline tests: legs.py serve as its own process, the commands as separate processes
(the way Claude Code or Cowork calls them), the stand-in CLI (fake_stream_claude.py), and a synthetic run
with the real protocol_guard.py and steps.py and the faithful harness_stub.py for step.sh and close.sh.
No model is called and nothing outside a temporary folder is written.
    python3 aggregator/handler/claude-adapter/tests/test_legs.py
"""
import hashlib
import hmac
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ADAPTER = HERE.parent
HARNESS = Path(os.environ.get('ADAPTER_TEST_HARNESS') or ADAPTER.parent / 'claude')
INSTRUMENT = ADAPTER.parents[1] / 'instrument/tools'
LEGS = ADAPTER / 'legs.py'
FAKE = HERE / 'fake_stream_claude.py'
STEP = '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/harness_stub.py" step "$@"\n'
CLOSE = '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/harness_stub.py" close "$@"\n'
PAUSE = '#!/usr/bin/env bash\nprintf "pause requested\\n" > "$(dirname "$0")/../../00_GIVE-THE-AGENT/.pause"\necho "Pause requested."\n'
# the parent's publish.sh in a repository: what the run's publish.sh does to main at every close, without the Manual
PUBLISH = ('#!/usr/bin/env bash\nRUN="$(cd "$(dirname "$0")/../.." && pwd -P)"\ncd "$(git -C "$RUN" rev-parse --show-toplevel)" || exit 0\n'
           'git add -A && git commit -q -m "$2 $1" && echo "  git: committed \\"$2 $1\\""\necho "  git: no remote set; committed locally"\n')


def done(cut=None):
    return {'done': {'stage': 'A1', 'cut': cut}}


class World:
    """A temporary run, the handler's folder, and legs.py serve running beside them."""
    def __init__(self, turns, git=False, exec_delay=0):
        self.t = Path(tempfile.mkdtemp(prefix='legs-test-')).resolve()   # macOS reaches its temporary folder through a link
        self.repo = self.t / 'repo'
        self.runs = self.repo / 'aggregator/runs' if git else self.t / 'runs'
        self.run = self.runs / 'test-run'
        c = self.run / 'CONTROL'
        (c / 'harness/validation_tools').mkdir(parents=True)
        (c / '.cc').mkdir()
        (self.run / '00_GIVE-THE-AGENT/out').mkdir(parents=True)
        for f in ('protocol_guard.py',):
            shutil.copy(HARNESS / f, c / 'harness' / f)
        for f in ('steps.py', 'steps.tsv'):
            shutil.copy(INSTRUMENT / f, c / 'harness' / f)
        shutil.copy(HERE / 'harness_stub.py', c / 'harness/harness_stub.py')
        shutil.copy(HARNESS / 'settings.template.json', c / 'settings.template.json')
        (c / 'harness/step.sh').write_text(STEP)
        (c / 'harness/close.sh').write_text(CLOSE)
        (c / 'harness/pause.sh').write_text(PAUSE)
        (c / 'harness/validation_tools/validate.py').write_text('import sys\nsys.exit(0)\n')
        (c / 'arm.json').write_text(json.dumps({'A1': {'analyst': 'claude-test-model', 'effort': 'medium'}}))
        (c / 'RUN.json').write_text('{}\n')
        (c / '.cc/.claude.json').write_text('{}\n')
        self.data = self.t / 'legs'
        self.scenario = self.t / 'scenario.json'
        self.scenario.write_text(json.dumps({'turns': turns}))
        exe = self.t / 'bin/claude'
        exe.parent.mkdir()
        # exec_delay: the launcher lives a moment before it becomes the CLI, as a shell script, env or node does
        exe.write_text('#!/bin/sh\n%sexec "%s" "%s" "$@"\n' % ('sleep %s\n' % exec_delay if exec_delay else '', sys.executable, FAKE))
        exe.chmod(0o755)
        self.env = dict(os.environ, RPLACE_LEGS_DATA=str(self.data), RPLACE_LEGS_RUNS=str(self.runs),
                        RPLACE_CLAUDE_BIN=str(exe), FAKE_SCENARIO=str(self.scenario))
        self.env.pop('ANTHROPIC_API_KEY', None)
        if git:
            self.in_repository()
        self.log = (self.t / 'serve.log').open('a')
        self.start()

    def in_repository(self):
        """The run in a repository with the real .gitignore, a stage drop, a publish.sh that commits to main, and
        the branches' publisher named for the branch's own publish.sh."""
        d = self.run / 'DROPS'
        (d / 'A1/stages').mkdir(parents=True)
        (d / 'ORDER.tsv').write_text('stage\tfile\nA1\tstages/STAGE-A1-reading.md\nB1\tstages/STAGE-B1-coding.md\n')
        (d / 'A1/stages/STAGE-A1-reading.md').write_text('# A1, the parent\'s card\n')
        (self.run / '00_GIVE-THE-AGENT/RUN.json').write_text(json.dumps({'legs': [{'stage': 'A1', 'leg': 'A1a'},
                                                                                {'stage': 'A1', 'leg': 'A1b-01'}]}))
        (self.run / 'CONTROL/harness/publish.sh').write_text(PUBLISH)
        shutil.copy(ADAPTER.parents[2] / '.gitignore', self.repo / '.gitignore')
        os.chmod(self.repo / '.gitignore', 0o644)
        self.env.update(GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@example.org', GIT_COMMITTER_NAME='t',
                        GIT_COMMITTER_EMAIL='t@example.org', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
                        RPLACE_BRANCHES_PY=str(ADAPTER / 'branches.py'))
        self.git('init', '-q', '-b', 'main')
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'the run before its first leg')

    def git(self, *args):
        return subprocess.run(['git'] + list(args), cwd=str(self.repo), env=self.env, capture_output=True, text=True,
                              check=True).stdout.strip()

    def start(self):
        (self.data / 'server.json').unlink(missing_ok=True)
        self.server = subprocess.Popen([sys.executable, str(LEGS), 'serve'], env=self.env, stdout=self.log,
                                       stderr=subprocess.STDOUT, start_new_session=True)
        end = time.time() + 20
        while not (self.data / 'server.json').exists():
            if time.time() > end or self.server.poll() is not None:
                raise AssertionError('the handler did not start: ' + (self.t / 'serve.log').read_text())
            time.sleep(0.1)

    def kill(self):
        """The handler dies at once (no clean stop); the analyst's turn runs on in its own process group."""
        os.killpg(self.server.pid, signal.SIGKILL)
        self.server.wait(10)

    def legs(self, *args, ok=True, timeout=120):
        r = subprocess.run([sys.executable, str(LEGS)] + list(args), env=self.env, capture_output=True, text=True,
                           timeout=timeout)
        if ok and r.returncode:
            raise AssertionError('legs.py %s failed: %s %s\nserver: %s' % (' '.join(args), r.stdout, r.stderr,
                                                                          (self.t / 'serve.log').read_text()[-3000:]))
        return r.stdout + r.stderr

    def calls(self, run=None):
        p = (run or self.run) / 'CONTROL/.cc/stream_calls.jsonl'
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

    def job(self, run=None):
        return json.loads(((run or self.run) / 'CONTROL/legs/job.json').read_text())

    def until_job_ends(self, timeout=60, run=None):
        end = time.time() + timeout
        while time.time() < end:
            j = self.job(run)
            if j['status'] != 'running':
                return j
            time.sleep(0.2)
        raise AssertionError('the list did not end: %s' % self.job(run))

    def committed(self, label):
        return (self.run / 'CONTROL/snapshots' / label / 'COMMITTED').exists()

    def close(self):
        try:
            os.killpg(self.server.pid, signal.SIGTERM)
            self.server.wait(10)
        except Exception:
            pass
        self.log.close()
        shutil.rmtree(self.t, ignore_errors=True)


class LegsTest(unittest.TestCase):
    def tearDown(self):
        self.w.close()

    def test_a_whole_stage_then_talking_to_a_closed_leg(self):
        self.w = World([
            [{'write': {'path': 'out/order-A1.txt', 'text': '01\troom-a\n01\troom-b\n02\troom-c\n'}}, done(), {'say': 'A1a done.'}],
            [done(), {'say': 'Block 1 read.'}],
            [done(), {'say': 'Block 2 read.'}],
            [{'write': {'path': 'out/handback-A1.md', 'text': 'handback'}}, {'write': {'path': 'out/interview/A1c.md', 'text': 'brief'}},
             done('interview'), {'say': 'A1c done.'}],
            [{'say': 'I declared two blocks.'}],
            [{'say': 'Then I read them.'}]])
        (self.w.run / 'CONTROL/legs').mkdir(parents=True)
        follow = subprocess.Popen([sys.executable, str(LEGS), 'watch', 'test-run', '--follow', '--full'], env=self.w.env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out = self.w.legs('run', 'test-run', 'A1')
        self.assertIn('A1b, one leg per declared block', out)
        j = self.w.until_job_ends()
        time.sleep(1.5)
        follow.send_signal(signal.SIGINT)
        live = follow.communicate(timeout=10)[0]
        # one window shows the whole list as it runs, leg after leg, each tool call with its output
        for x in ('=== A1.A1a', '=== A1.A1b-01', '=== A1.A1b-02', '=== A1.A1c', 'analyst: A1c done.',
                  'Bash: bash tools/done.sh A1', 'output of Bash: bash tools/done.sh A1', 'leg A1c closed. Stop now.'):
            self.assertIn(x, live)
        self.assertEqual(j['status'], 'completed')
        self.assertIn('interview point', j['reason'])
        for label in ('A1.A1a', 'A1.A1b-01', 'A1.A1b-02', 'A1.A1c'):
            self.assertTrue(self.w.committed(label), label)
        self.assertEqual([d['label'] for d in j['done']], ['A1.A1a', 'A1.A1b-01', 'A1.A1b-02', 'A1.A1c'])
        self.assertTrue(all(d['advances'] for d in j['done']))
        # every leg after the first continues the last close's conversation
        sessions = json.loads((self.w.run / 'CONTROL/sessions.json').read_text())
        self.assertEqual([sessions[x]['mode'] for x in ('A1.A1a', 'A1.A1b-01', 'A1.A1b-02', 'A1.A1c')],
                         ['fresh', 'fork', 'fork', 'fork'])
        self.assertTrue((self.w.run / 'CONTROL/stage-state/A1/FINISHED').exists())
        # a notice you have not seen through wait shows at once, then only newer ones
        seen = self.w.legs('wait', 'test-run', '--timeout', '3')
        self.assertGreater(seen.count('needs you'), 1)   # every notice not yet shown, not only the latest (v43.2)
        self.assertIn('Nothing new', self.w.legs('wait', 'test-run', '--timeout', '3'))
        # the last close's conversation goes on in the next leg: your words wait for its first message
        out = self.w.legs('say', 'test-run', 'A1c', 'Good', 'work.')
        self.assertIn('first message', out)
        self.assertEqual(len(list((self.w.run / 'CONTROL/legs/next-leg').glob('*.json'))), 1)
        # an older close is talked to only in an interview: you open it, as it was at its close
        self.assertIn('legs.py interview test-run A1a', self.w.legs('say', 'test-run', 'A1a', 'Hello.', ok=False))
        self.assertFalse((self.w.run / 'CONTROL/interviews.tsv').exists())
        reply = self.w.legs('interview', 'test-run', 'A1a', 'What', 'did', 'you', 'declare?')
        self.assertIn('an interview of its checkpoint answers', reply)
        self.assertIn('I declared two blocks.', reply)
        self.assertEqual(len((self.w.run / 'CONTROL/interviews.tsv').read_text().splitlines()), 1)
        again = self.w.legs('interview', 'test-run', 'A1.A1a', 'And', 'then?')
        self.assertIn('Then I read them.', again)
        first, second = self.w.calls()[-2]['argv'], self.w.calls()[-1]['argv']
        self.assertIn('--fork-session', first)
        self.assertEqual(second[second.index('--resume') + 1], first[first.index('--session-id') + 1])
        self.assertTrue(self.w.calls()[-1]['cwd'].endswith('00_GIVE-THE-AGENT'))
        self.assertIn('interview-workspaces', self.w.calls()[-1]['cwd'])
        legs = self.w.legs('legs', 'test-run')
        self.assertIn('A1.A1a', legs)
        self.assertIn('closed (close); 1 interview', legs)
        self.assertIn('closed (interview)', legs)
        self.assertIn('Then I read them.', self.w.legs('reply', 'test-run', 'A1a', '--interview'))
        self.assertIn('A1a done.', self.w.legs('reply', 'test-run', 'A1a'))   # the leg's own session
        self.assertIn('A1a done.', self.w.legs('reply', 'test-run', 'A1a', '--leg'))
        # a closed list is skipped when it is named again
        self.w.legs('run', 'test-run', 'A1')
        j = self.w.until_job_ends()
        self.assertEqual(j['status'], 'completed')
        self.assertEqual(j['skipped'], ['A1a', 'A1b-01', 'A1b-02', 'A1c'])

    def test_gates_a_turn_without_a_close_talk_close_and_a_pause(self):
        self.w = World([
            [{'say': 'I stopped early.'}],
            [done(), {'say': 'Closed now.'}],
            [done('pause'), {'say': 'Paused.'}],
            [done(), {'say': 'Block finished after the pause.'}]])
        self.w.legs('run', 'test-run', 'A1a')
        j = self.w.until_job_ends()
        self.assertEqual(j['status'], 'stopped')
        self.assertIn('without closing the leg', j['reason'])
        self.assertIn('without closing the leg', self.w.legs('status', 'test-run'))
        self.assertIn('I stopped early.', self.w.legs('reply', 'test-run', 'A1a'))
        # the leg is open and idle: words to it start a new turn in its own session
        out = self.w.legs('say', 'test-run', 'A1a', 'Please', 'close', 'the', 'leg.')
        self.assertIn('a new turn in its session answers', out)
        self.assertIn('Closed now.', out)
        argv = self.w.calls()[-1]['argv']
        sid = json.loads((self.w.run / 'CONTROL/sessions.json').read_text())['A1.A1a']['session_id']
        self.assertEqual(argv[argv.index('--resume') + 1], sid)
        out = self.w.legs('close', 'test-run', 'A1a')
        self.assertIn('advances: True', out)
        self.assertIn('publication: no repository', out)
        self.assertIn('git no repository', (self.w.run / 'CONTROL/legs/events.log').read_text())
        self.assertIn('not on GitHub', (self.w.run / 'CONTROL/legs/needs-you.json').read_text())
        self.assertTrue(self.w.committed('A1.A1a'))
        self.assertIn('Refused', self.w.legs('close', 'test-run', 'A1a', ok=False) + 'Refused')
        # a pause stops the list; naming the leg again continues it as -p2
        self.w.legs('run', 'test-run', 'A1b-01..A1b-02')
        j = self.w.until_job_ends()
        self.assertIn('paused at a safe stop', j['reason'])
        self.assertTrue(self.w.committed('A1.A1b-01'))
        self.assertFalse((self.w.run / 'CONTROL/snapshots/A1.A1b-02').exists())
        self.w.legs('run', 'test-run', 'A1b-01')
        j = self.w.until_job_ends()
        self.assertEqual(j['status'], 'completed')
        self.assertEqual([d['label'] for d in j['done']], ['A1.A1b-01-p2'])

    def test_live_words_an_answer_a_stop_and_a_refusal(self):
        self.w = World([
            [{'tool': 'Bash', 'input': {'command': 'python3 tools/mem.py ask'}, 'output': 'asked',
              'ask': {'id': 'QA1-001', 'question': 'Keep the room?', 'assumption': 'kept'}},
             {'wait_context': 20}, {'wait_context': 20}, done(), {'say': 'Done.'}],
            [{'tool': 'Bash', 'input': {'command': 'sleep 2'}, 'output': '', 'sleep': 2}, done(), {'say': 'Block 1.'}]])
        self.w.legs('open', 'test-run', 'A1a')
        end = time.time() + 20
        while 'QA1-001' not in self.w.legs('status', 'test-run'):
            self.assertLess(time.time(), end)
            time.sleep(0.3)
        out = self.w.legs('say', 'test-run', 'A1a', 'The', 'code', 'word', 'is', 'ZEBRA.', '--wait', '20')
        self.assertIn('Your words reach it beside its next tool result', out)
        self.assertIn('Delivered', out)
        out = self.w.legs('answer', 'test-run', 'QA1-001', 'Keep', 'it.')
        self.assertIn('answered: QA1-001', out)
        p = self.w.run / '00_GIVE-THE-AGENT/out/_answers/QA1-001.md'
        self.assertEqual(p.read_text().strip(), 'Keep it.')
        self.assertEqual(os.stat(p).st_mode & 0o222, 0)
        end = time.time() + 30
        while '--- turn ends' not in self.w.legs('watch', 'test-run', 'A1a'):
            self.assertLess(time.time(), end)
            time.sleep(0.3)
        watch = self.w.legs('watch', 'test-run', 'A1a', '-n', '100')
        self.assertIn('message: The code word is ZEBRA.', watch)
        self.assertNotIn('output of', watch)
        full = self.w.legs('watch', 'test-run', 'A1a', '-n', '200', '--full')
        self.assertIn('output of Bash: python3 tools/mem.py ask:\n      asked', full)
        self.assertIn('analyst: heard: The principal investigator answered QA1-001.', full)
        self.assertIn('ZEBRA', [x for x in watch.splitlines() if 'analyst: heard' in x][0])
        self.assertIn('Keep it.', watch)
        # your words to a running leg, and their delivery, are in the run's CONTROL, which publish.sh commits
        rec = [json.loads(x) for x in (self.w.run / 'CONTROL/messages-to-legs.jsonl').read_text().splitlines()]
        sent = [r for r in rec if r['kind'] == 'sent']
        self.assertEqual((sent[0]['label'], sent[0]['mode'], sent[0]['text']), ('A1.A1a', 'live', 'The code word is ZEBRA.'))
        self.assertEqual(sent[0]['source'], 'say')
        self.assertTrue(any(r['kind'] == 'answer' and r['id'] == 'QA1-001' and r['text'] == 'Keep it.' for r in rec))
        end = time.time() + 10
        while not any(r['kind'] == 'delivered' and r['id'] == sent[0]['id'] for r in rec):
            self.assertLess(time.time(), end)
            time.sleep(0.5)
            rec = [json.loads(x) for x in (self.w.run / 'CONTROL/messages-to-legs.jsonl').read_text().splitlines()]
        self.assertEqual([r['via'] for r in rec if r['kind'] == 'delivered'], ['hook'])
        self.w.legs('close', 'test-run', 'A1a')
        # a stop asked while a leg runs: that leg closes, and no next leg opens
        (self.w.run / '00_GIVE-THE-AGENT/out/order-A1.txt').write_text('01\troom-a\n02\troom-b\n')
        self.w.legs('run', 'test-run', 'A1b-*')
        time.sleep(0.5)
        self.assertIn('stopping: True', self.w.legs('stop', 'test-run'))
        j = self.w.until_job_ends()
        self.assertEqual((j['status'], j['reason']), ('stopped', 'You stopped the list.'))
        self.assertTrue(self.w.committed('A1.A1b-01'))
        self.assertFalse((self.w.run / 'CONTROL/snapshots/A1.A1b-02').exists())
        # step.sh refuses: the list stops and says why
        (self.w.run / 'CONTROL/refuse-step').write_text('the test refuses this leg')
        self.w.legs('run', 'test-run', 'A1b-02')
        j = self.w.until_job_ends()
        self.assertIn('could not prepare A1b-02: step.sh A1b-02 --prepare refused', j['reason'])
        self.assertIn('the test refuses this leg', j['reason'])

    def test_an_answer_to_an_open_leg_reaches_its_next_turn(self):
        # v43.2: an answer given while a leg is open and idle was written to its file alone; the leg's next turn
        # never heard it, and once that turn ran done.sh the next leg's first message did not name it either
        self.w = World([
            [{'tool': 'Bash', 'input': {'command': 'python3 tools/mem.py ask'}, 'output': 'asked',
              'ask': {'id': 'QA1-001', 'question': 'Keep the room?', 'assumption': 'kept'}}, {'say': 'Asked.'}],
            [{'say_prompt': True}, done(), {'say': 'Done.'}]])
        self.w.legs('open', 'test-run', 'A1a')
        end = time.time() + 30
        while '--- turn ends' not in self.w.legs('watch', 'test-run', 'A1a'):
            self.assertLess(time.time(), end)
            time.sleep(0.3)
        out = self.w.legs('answer', 'test-run', 'QA1-001', 'Keep', 'it.')
        self.assertIn('with the next turn', out)
        self.w.legs('say', 'test-run', 'A1a', 'Go', 'on.')
        end = time.time() + 30
        while self.w.legs('watch', 'test-run', 'A1a', '-n', '200').count('--- turn ends') < 2:
            self.assertLess(time.time(), end)
            time.sleep(0.3)
        watch = self.w.legs('watch', 'test-run', 'A1a', '-n', '200')
        heard = [x for x in watch.splitlines() if 'prompt:' in x]
        self.assertTrue(heard and 'answered QA1-001' in heard[0] and 'Go on.' in heard[0], watch[-800:])
        rec = [json.loads(x) for x in (self.w.run / 'CONTROL/messages-to-legs.jsonl').read_text().splitlines()]
        self.assertTrue(any(r['kind'] == 'answer' and r['delivery'] == 'with the next turn' for r in rec), rec)

    def test_a_restart_follows_the_running_turn_and_pauses_the_list(self):
        # the launcher changes its command name when it becomes the CLI; the restart still knows the process
        self.w = World([[{'tool': 'Bash', 'input': {'command': 'sleep 4'}, 'output': '', 'sleep': 4}, done(),
                         {'say': 'Done after the restart.'}]], exec_delay=0.3)
        self.w.legs('run', 'test-run', 'A1a')
        end = time.time() + 20
        while not self.w.calls():
            self.assertLess(time.time(), end)
            time.sleep(0.1)
        time.sleep(0.5)
        self.w.kill()
        self.w.start()
        j = self.w.job()
        self.assertEqual(j['status'], 'paused')
        self.assertIn('restarted', self.w.legs('status', 'test-run'))
        end = time.time() + 30
        while 'Done after the restart.' not in self.w.legs('reply', 'test-run', 'A1a'):
            self.assertLess(time.time(), end)
            time.sleep(0.3)
        aid = json.loads((self.w.run / 'CONTROL/legs/legs.json').read_text())['A1.A1a']['actor']
        st = json.loads((self.w.run / 'CONTROL/legs/actors' / aid / 'state.json').read_text())
        self.assertEqual((st['boundary'], st['confirmed']), ('completed', True))
        self.assertEqual(len(self.w.calls()), 1)   # followed, never started again
        # naming the leg again adopts it: the finished turn is closed, nothing reruns
        self.w.legs('run', 'test-run', 'A1a')
        j = self.w.until_job_ends()
        self.assertEqual([d['label'] for d in j['done']], ['A1.A1a'])
        self.assertTrue(self.w.committed('A1.A1a'))
        self.assertEqual(len(self.w.calls()), 1)

    def test_one_chat_for_every_agent(self):
        self.w = World([[done(), {'say': 'A1a done.'}], [{'say': 'Hello from the interview of A1a.'}],
                        [{'tool': 'Bash', 'input': {'command': 'sleep 2'}, 'output': '', 'sleep': 2}, {'wait_context': 10},
                         done(), {'say': 'Block one closed.'}]])
        self.w.legs('run', 'test-run', 'A1a')
        self.w.until_job_ends()
        chat = subprocess.Popen([sys.executable, str(LEGS), 'chat', 'test-run'], env=self.w.env, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        def type_(line, wait=0.0):
            chat.stdin.write(line + '\n')
            chat.stdin.flush()
            time.sleep(wait)
        time.sleep(1)
        type_('?A1a What did you do?', 4)              # an interview you open: it answers here
        self.w.legs('open', 'test-run', 'A1b-01')       # a running leg: its words and tools come here too
        time.sleep(0.5)
        type_('@A1b-01 Keep going.', 4)
        self.w.legs('note', 'test-run', 'A', 'note', 'from', 'the', 'handler.')
        time.sleep(1.5)
        type_('/quit')
        text = chat.communicate(timeout=15)[0]
        for x in ('handler | to A1a: an interview of its checkpoint answers', 'A1a (interview) | ',
                  'Hello from the interview of A1a.', 'handler | to A1b-01: it hears you beside its next tool result',
                  'A1b-01 | ', 'Bash: sleep 2', 'heard: Message from the principal investigator', 'Keep going.',
                  'message: Stage A1, leg A1b-01.', 'note: A note from the handler.', 'opened A1.A1b-01'):
            self.assertIn(x, text)
        self.assertNotIn('message: What did you do?', text)   # your own line is not echoed back

    def test_words_after_a_close_go_to_the_leg_that_carries_on(self):
        self.w = World([[done(), {'say': 'A1a done.'}],
                        [done(), {'pause': 3}, {'say': 'Block 1 done.'}],
                        [done(), {'say': 'Block 2 done.'}]])
        self.w.legs('run', 'test-run', 'A1a')
        self.w.until_job_ends()
        self.assertIn('first message', self.w.legs('say', 'test-run', 'A1a', 'Read', 'room-b', 'first.'))
        self.w.legs('run', 'test-run', 'A1b-01', 'A1b-02')
        marker = self.w.run / '00_GIVE-THE-AGENT/out/_closes/A1-A1b-01.closed'
        end = time.time() + 20
        while not marker.exists():   # A1b-01 has run done.sh and pauses: no tool call is left in its turn
            self.assertLess(time.time(), end)
            time.sleep(0.05)
        self.assertIn('is working', self.w.legs('say', 'test-run', 'A1b-01', 'Missed', 'words.'))
        j = self.w.until_job_ends()
        self.assertEqual([d['label'] for d in j['done']], ['A1.A1b-01', 'A1.A1b-02'])

        def prompt(c):
            return c['argv'][c['argv'].index('--') + 1]
        first, second = prompt(self.w.calls()[1]), prompt(self.w.calls()[2])
        self.assertTrue(first.startswith('Stage A1, leg A1b-01.'))   # the leg's first message, then your words
        self.assertIn('written after A1.A1a closed):\nRead room-b first.', first)
        self.assertIn('written after A1.A1b-01 closed):\nMissed words.', second)
        self.assertNotIn('Read room-b first.', second)                   # delivered once
        rec = [json.loads(x) for x in (self.w.run / 'CONTROL/messages-to-legs.jsonl').read_text().splitlines()]
        self.assertEqual([(r['kind'], r.get('mode') or r.get('via') or r.get('to'), r['label']) for r in rec],
                         [('sent', 'next-leg', 'A1.A1a'), ('delivered', 'first message', 'A1.A1b-01'),
                          ('sent', 'live', 'A1.A1b-01'), ('carried', "the next leg's first message", 'A1.A1b-01'),
                          ('delivered', 'first message', 'A1.A1b-02')])
        self.assertEqual(list((self.w.run / 'CONTROL/legs/next-leg').glob('*.json')), [])
        self.assertIn('legs.py interview', self.w.legs('say', 'test-run', 'A1a', 'Late.', ok=False))
        self.assertIn('Send it in parts', self.w.legs('say', 'test-run', 'A1b-02', 'x' * 8001, ok=False))

    def test_a_close_that_cannot_advance_stops_a_list_until_accepted(self):
        self.w = World([[{'say': 'Stopped early.'}], [done(), {'say': 'Block 1.'}]])
        self.w.legs('run', 'test-run', 'A1a')
        self.w.until_job_ends()
        self.assertIn('advances: False', self.w.legs('close', 'test-run', 'A1a', '--force'))
        self.w.legs('run', 'test-run', 'A1a', 'A1b-01')   # naming it again does not skip it
        j = self.w.until_job_ends()
        self.assertEqual((j['status'], j['done']), ('stopped', []))
        self.assertIn('the run cannot go on from it', j['reason'])
        self.assertIn('--accept A1.A1a', j['reason'])
        self.w.legs('run', 'test-run', 'A1a', 'A1b-01', '--accept', 'A1a')
        j = self.w.until_job_ends()
        self.assertEqual([d['label'] for d in j['done']], ['A1.A1b-01'])
        # a snapshot that is only a COMMITTED file is not a close to go on from
        bad = self.w.run / 'CONTROL/snapshots/A1.A1b-02'
        bad.mkdir()
        (bad / 'COMMITTED').write_text('0000\n')
        self.w.legs('run', 'test-run', 'A1b-02')
        self.assertIn('does not bind its checkpoint', self.w.until_job_ends()['reason'])

    def test_an_open_leg_is_not_talked_to_once_the_run_moves_on(self):
        self.w = World([[{'say': 'Stopped early.'}], [done(), {'say': 'Block 1.'}]])
        self.w.legs('run', 'test-run', 'A1a')
        self.w.until_job_ends()
        self.w.legs('open', 'test-run', 'A1b-01')
        end = time.time() + 20
        while 'Block 1.' not in self.w.legs('reply', 'test-run', 'A1b-01'):
            self.assertLess(time.time(), end)
            time.sleep(0.3)
        out = self.w.legs('say', 'test-run', 'A1a', 'Hello.', ok=False)
        self.assertIn('moved on to A1b-01', out)
        self.assertEqual(len(self.w.calls()), 2)   # no turn started
        aid = json.loads((self.w.run / 'CONTROL/legs/legs.json').read_text())['A1.A1a']['actor']
        self.assertEqual(list((self.w.run / 'CONTROL/legs/actors' / aid / 'inbox').glob('*.json')), [])   # nothing queued

    def test_a_request_must_be_signed_fresh_and_well_formed(self):
        self.w = World([])
        req = self.w.run / 'CONTROL/legs/requests'
        res = self.w.run / 'CONTROL/legs/results'
        req.mkdir(parents=True)
        key = (self.w.data / 'key').read_text().strip()

        def put(rid, body, signed=True, age=0):
            body = dict(body, id=rid, cmd='ping', run='test-run', ttl=60)
            sig = hmac.new(key.encode(), json.dumps(body, sort_keys=True, ensure_ascii=False).encode(), hashlib.sha256)
            path = req / ('%s.json' % rid)
            path.write_text(json.dumps(dict(body, sig=sig.hexdigest() if signed else 'wrong')))
            if age:
                os.utime(path, (time.time() - age, time.time() - age))
        (req / 'r0.json').write_text('[]')            # not a request: skipped, and the handler lives on
        put('r1', {}, signed=False)
        put('r2', {}, age=120)                        # older than its time to live, by the file's own time
        put('r3', {})
        end = time.time() + 10
        while not all((res / ('%s.json' % r)).exists() for r in ('r1', 'r2', 'r3')):
            self.assertLess(time.time(), end)
            time.sleep(0.1)
        r1, r2, r3 = (json.loads((res / ('%s.json' % r)).read_text()) for r in ('r1', 'r2', 'r3'))
        self.assertFalse(r1['ok'])
        self.assertIn('not signed', r1['error'])
        self.assertFalse(r2['ok'])
        self.assertIn('expired', r2['error'])
        self.assertTrue(r3['ok'])
        self.assertIsNone(self.w.server.poll())
        self.assertNotIn(key, (req / 'taken/r3.json').read_text())   # the key never travels
        self.assertEqual(os.stat(self.w.data / 'key').st_mode & 0o077, 0)
        self.assertIn('handler: running', self.w.legs('status'))
        # the handler keeps nothing of a run beside the repository: its folder holds the heartbeat, clock, lock and key
        self.assertEqual(sorted(p.name for p in self.w.data.iterdir()), ['clock', 'key', 'server.json', 'server.lock'])

    def test_a_turn_that_ends_while_the_handler_is_down_is_settled_not_repeated(self):
        self.w = World([[{'tool': 'Bash', 'input': {'command': 'sleep 2'}, 'output': '', 'sleep': 2}, done(),
                         {'say': 'Finished while nobody watched.'}]])
        self.w.legs('run', 'test-run', 'A1a')
        end = time.time() + 20
        while not self.w.calls():
            self.assertLess(time.time(), end)
            time.sleep(0.1)
        self.w.kill()
        time.sleep(4)                                  # the turn ends while no handler runs
        self.w.start()
        aid = json.loads((self.w.run / 'CONTROL/legs/legs.json').read_text())['A1.A1a']['actor']
        st = json.loads((self.w.run / 'CONTROL/legs/actors' / aid / 'state.json').read_text())
        self.assertEqual((st['boundary'], st['confirmed'], st['active_turn_id']), ('completed', True, None))
        self.assertFalse((self.w.run / 'CONTROL/active_launch.json').exists())
        self.assertFalse((self.w.run / 'CONTROL/pending_launch.json').exists())
        self.w.legs('run', 'test-run', 'A1a')
        j = self.w.until_job_ends()
        self.assertEqual([d['label'] for d in j['done']], ['A1.A1a'])
        self.assertTrue(j['done'][0]['advances'])
        self.assertEqual(len(self.w.calls()), 1)       # settled, never started again

    def test_a_pause_between_two_legs_stops_the_list(self):
        self.w = World([[done(), {'say': 'A1a done.'}], [done(), {'say': 'never'}]])
        (self.w.run / 'CONTROL/harness/step.sh').write_text(
            '#!/usr/bin/env bash\nsleep 2\nexec python3 "$(dirname "$0")/harness_stub.py" step "$@"\n')
        self.w.legs('run', 'test-run', 'A1a', 'A1b-01')
        end = time.time() + 20
        while not self.w.committed('A1.A1a'):
            self.assertLess(time.time(), end)
            time.sleep(0.1)
        self.assertIn('stops before its next leg', self.w.legs('pause', 'test-run'))
        j = self.w.until_job_ends()
        self.assertEqual((j['status'], [d['label'] for d in j['done']]), ('stopped', ['A1.A1a']))

    def test_the_ignore_rules_keep_the_handler_out_of_git(self):
        if not shutil.which('git'):
            self.skipTest('git is not installed')
        self.w = World([])
        repo = self.w.t / 'repo'
        repo.mkdir()
        shutil.copy(ADAPTER.parents[2] / '.gitignore', repo / '.gitignore')
        subprocess.run(['git', 'init', '-q'], cwd=str(repo), check=True)

        def ignored(path):
            return subprocess.run(['git', 'check-ignore', '-q', path], cwd=str(repo), check=False).returncode == 0
        self.assertTrue(ignored('aggregator/runs/claude-v43-1/CONTROL/legs/actors/x/events.jsonl'))
        self.assertTrue(ignored('aggregator/runs/claude-v43-1/CONTROL/legs/requests/taken/x.json'))
        self.assertTrue(ignored('aggregator/runs/claude-v43-1/interview-workspaces/A1.A1a__x/00_GIVE-THE-AGENT/out/a.md'))
        self.assertFalse(ignored('aggregator/runs/claude-v43-1/CONTROL/messages-to-legs.jsonl'))
        # interview transcripts: committed only by J's decision, one by one (2026-10-06); the list is committed
        self.assertTrue(ignored('aggregator/runs/claude-v43-1/interviews/A1.A1c__x.jsonl'))
        self.assertTrue(ignored('aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/handling/interviews/A1.A1c__x.jsonl'))
        self.assertFalse(ignored('aggregator/runs/claude-v43-1/CONTROL/interviews.tsv'))
        self.assertTrue(ignored('aggregator/runs/claude-v43-1--C2-1/CONTROL/RUN.json'))   # a branch never reaches main
        self.assertFalse(ignored('aggregator/runs/claude-v43-1/CONTROL/RUN.json'))

    def test_a_branch_from_a_close_with_a_new_card_is_published_apart_from_main(self):
        if not shutil.which('git'):
            self.skipTest('git is not installed')
        self.w = w = World([[done(), {'say': 'A1a done.'}], [{'say': 'Interview answer.'}],
                            [done(), {'say': 'Parent, block 1.'}],
                            [{'write': {'path': 'handling/interviews/private.md', 'text': 'private'}}, done(),
                             {'say': 'Branch, block 1.'}]], git=True)
        w.legs('run', 'test-run', 'A1a')
        w.until_job_ends()
        self.assertIn('Interview answer.', w.legs('interview', 'test-run', 'A1a', 'A', 'question.'))
        w.legs('run', 'test-run', 'A1b-01')
        self.assertEqual([d['label'] for d in w.until_job_ends()['done']], ['A1.A1b-01'])
        self.assertEqual(w.git('log', '--format=%s').splitlines()[:2], ['close A1.A1b-01', 'close A1.A1a'])
        base = w.git('rev-parse', 'HEAD^')
        # another run's close of the same label, committed later, touches this run too (publish.sh adds everything)
        (w.run / 'CONTROL/harness/later.txt').write_text('changed after the close\n')
        w.git('add', '-A')
        w.git('commit', '-q', '-m', 'close A1.A1a')
        main = w.git('rev-parse', 'HEAD')
        sid = json.loads((w.run / 'CONTROL/sessions.json').read_text())['A1.A1a']['session_id']
        # the branch: named <parent>--<name>, from a verified close, its first leg the next one
        self.assertIn('two hyphens', w.legs('branch', 'test-run', 'A1a', 'test-run-b1', '--leg', 'A1b-01', ok=False))
        self.assertIn('must be in stage A1', w.legs('branch', 'test-run', 'A1a', 'test-run--b1', '--leg', 'B1a', ok=False))
        for leg in ('A1a', 'A1c', 'A1b-02'):   # Codex's order: no repeated, skipped or out-of-count step
            self.assertIn('does not come right after', w.legs('branch', 'test-run', 'A1a', 'test-run--b1', '--leg', leg, ok=False))
        out = w.legs('branch', 'test-run', 'A1a', 'test-run--b1', '--leg', 'A1b-01')
        self.assertIn('CLAUDE_CONFIG_DIR', out)
        br = w.runs / 'test-run--b1'
        b = json.loads((br / 'BRANCH.json').read_text())
        self.assertEqual((b['status'], b['source_run'], b['checkpoint'], b['target_leg'], b['base_commit'], b['inherited']),
                         ('draft', 'test-run', 'A1.A1a', 'A1b-01', base, ['A1.A1a']))
        # the state of the close: its folder (and the tokens close.sh wrote after it), sessions and checkpoint
        self.assertTrue((br / 'CONTROL/snapshots/A1.A1a/COMMITTED').exists())
        self.assertFalse((br / 'CONTROL/snapshots/A1.A1b-01').exists())
        self.assertFalse((br / '00_GIVE-THE-AGENT/out/_closes/A1-A1b-01.closed').exists())
        self.assertTrue((br / 'CONTROL/.cc/projects/run' / (sid + '.jsonl')).exists())
        self.assertIn('tokens', json.loads((br / '00_GIVE-THE-AGENT/RUN.json').read_text())['legs'][0])
        # a new card for the stage: in its drop and, since A1 was handed, in the analyst's folder; no tools
        card = w.t / 'card.md'
        card.write_text('# A1, the branch\'s card\n')
        out = w.legs('branch-put', 'test-run--b1', 'stages/STAGE-A1-reading.md', '--file', str(card), '--stage', 'A1')
        self.assertIn('workspace/stages/STAGE-A1-reading.md', out)
        self.assertEqual((br / '00_GIVE-THE-AGENT/stages/STAGE-A1-reading.md').read_text(), card.read_text())
        tool = w.t / 'x.py'
        tool.write_text('print(1)\n')
        self.assertIn('not executables', w.legs('branch-put', 'test-run--b1', 'shelves/x.py', '--file', str(tool),
                                                '--stage', 'A1', ok=False))
        self.assertIn('existing card', w.legs('branch-put', 'test-run--b1', 'stages/STAGE-A1-other.md', '--file', str(card),
                                              '--stage', 'A1', ok=False))
        # the inputs are frozen to their modes too: a card made executable outside branch-put stops the setup
        drop = br / 'DROPS/A1/stages/STAGE-A1-reading.md'
        os.chmod(drop, 0o755)
        self.assertIn('stage deliveries changed', w.legs('prepare-branch', 'test-run--b1', ok=False))
        os.chmod(drop, 0o644)
        # a card replaced by a link to the same text is refused, never followed
        text = drop.read_text()
        outside = w.t / 'same-card.md'
        outside.write_text(text)
        drop.unlink()
        drop.symlink_to(outside)
        self.assertIn('A link where an input should be', w.legs('prepare-branch', 'test-run--b1', ok=False))
        drop.unlink()
        drop.write_text(text)
        os.chmod(drop, 0o644)
        # the arms and the settings template are frozen with the harness
        arm = br / 'CONTROL/arm.json'
        before = arm.read_text()
        arm.write_text(before.replace('medium', 'high'))
        self.assertIn('arms or settings template changed', w.legs('prepare-branch', 'test-run--b1', ok=False))
        arm.write_text(before)
        # sealed and published: one commit on analysis/<run> whose parent is the fork point, main untouched
        w.git('init', '-q', '--bare', str(w.t / 'remote.git'))
        w.git('remote', 'add', 'origin', str(w.t / 'remote.git'))
        out = w.legs('prepare-branch', 'test-run--b1')
        self.assertIn('setup before A1b-01', out)
        self.assertIn('pushed analysis/test-run--b1', out)
        setup = w.git('rev-parse', 'analysis/test-run--b1')
        self.assertEqual(w.git('rev-parse', setup + '^'), base)
        ckid = (w.run / 'CONTROL/snapshots/A1.A1a/COMMITTED').read_text().strip()
        self.assertEqual(w.git('rev-parse', 'analysis-checkpoints/' + ckid), base)
        p = 'aggregator/runs/test-run/'
        self.assertEqual(set(w.git('diff', '--name-only', base, setup).split()),
                         {p + x for x in ('BRANCH.json', 'LINEAGE.json', 'CONTROL/harness/publish.sh', 'CONTROL/harness/step.sh',
                                          'CONTROL/harness/step-parent.sh',
                                          'DROPS/A1/stages/STAGE-A1-reading.md', '00_GIVE-THE-AGENT/stages/STAGE-A1-reading.md')})
        self.assertIn('setup is sealed', w.legs('branch-put', 'test-run--b1', 'stages/STAGE-A1-reading.md', '--file',
                                                str(card), '--stage', 'A1', ok=False))
        self.assertIn('sealed', w.legs('branch-status', 'test-run--b1'))
        self.assertIn('has not started', w.legs('say', 'test-run--b1', 'A1b-01', 'Hello.', ok=False))
        self.assertEqual(json.loads((br / 'BRANCH.json').read_text())['harness_changed'].keys(),
                         {'CONTROL/harness/publish.sh', 'CONTROL/harness/step.sh'})
        self.assertEqual((br / 'CONTROL/harness/step-parent.sh').read_text(), STEP)
        r = subprocess.run(['bash', str(br / 'CONTROL/harness/step.sh'), 'A1b-01'], env=w.env, capture_output=True, text=True)
        self.assertIn('starts through legs.py', r.stderr)
        # its first leg continues the close's conversation, told it is a branch and what changed
        w.legs('run', 'test-run--b1', 'A1b-01')
        self.assertEqual([d['label'] for d in w.until_job_ends(run=br)['done']], ['A1.A1b-01'])
        argv = w.calls(br)[0]['argv']
        self.assertEqual((argv[argv.index('--resume') + 1], '--fork-session' in argv), (sid, True))
        prompt = argv[argv.index('--') + 1]
        self.assertTrue(prompt.startswith('This is analysis branch test-run--b1 from test-run after A1.A1a.'), prompt[:200])
        self.assertIn('stage/A1/stages/STAGE-A1-reading.md', prompt)
        self.assertEqual(w.git('log', '--format=%s', '-3', 'analysis/test-run--b1').splitlines(),
                         ['Analysis test-run--b1: verified A1b-01', 'Analysis test-run--b1: setup before A1b-01',
                          'close A1.A1a'])
        # an interview transcript is never published from a branch, at any depth
        self.assertTrue((br / '00_GIVE-THE-AGENT/handling/interviews/private.md').exists())
        self.assertNotIn('handling/interviews', w.git('ls-tree', '-r', '--name-only', 'analysis/test-run--b1'))
        lineage = json.loads(w.git('show', 'analysis/test-run--b1:' + p + 'LINEAGE.json'))
        self.assertEqual((lineage['kind'], lineage['leg']), ('verified-leg', 'A1.A1b-01'))
        self.assertEqual(w.git('rev-parse', 'HEAD'), main)
        self.assertNotIn('test-run--b1', w.git('status', '--porcelain', '--ignored=no'))
        remote = w.git('ls-remote', 'origin')
        self.assertIn(w.git('rev-parse', 'analysis/test-run--b1') + '\trefs/heads/analysis/test-run--b1', remote)
        self.assertIn('refs/tags/analysis-checkpoints/' + ckid, remote)
        self.assertNotIn('refs/heads/main', remote)
        self.assertIn('pushed analysis/test-run--b1', w.legs('publish-branch', 'test-run--b1'))   # again: nothing new
        self.assertEqual(w.git('log', '--format=%s', '-1', 'analysis/test-run--b1'), 'Analysis test-run--b1: verified A1b-01')
        # the parent's own A1b-01 is untouched, and the two differ where the branch changed its inputs
        self.assertIn('Parent, block 1.', w.legs('reply', 'test-run', 'A1b-01', '--leg'))
        self.assertIn('Branch, block 1.', w.legs('reply', 'test-run--b1', 'A1b-01', '--leg'))
        # a branch after the interview: the interview stays with the parent, its row in BRANCH.json only
        w.legs('branch', 'test-run', 'A1b-01', 'test-run--b2', '--leg', 'A1b-02')
        b2 = w.runs / 'test-run--b2'
        self.assertEqual(len(json.loads((b2 / 'BRANCH.json').read_text())['interviews_omitted']), 1)
        self.assertFalse((b2 / 'CONTROL/interviews.tsv').exists())
        self.assertEqual([x.name for x in (b2 / 'CONTROL/.cc/projects').iterdir()], ['run'])
        # a branch made before the inputs were frozen with their modes is refused, not checked against old hashes
        bj = json.loads((b2 / 'BRANCH.json').read_text())
        bj.pop('inputs_version')
        (b2 / 'BRANCH.json').write_text(json.dumps(bj))
        self.assertIn('Make it again', w.legs('prepare-branch', 'test-run--b2', ok=False))


class TreeHashTest(unittest.TestCase):
    def test_an_input_folder_is_hashed_with_its_modes_and_never_through_a_link(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('test_branches', ADAPTER / 'branches.py')
        B = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(B)
        t = Path(tempfile.mkdtemp(prefix='tree-hash-')).resolve()
        try:
            (t / 'f/sub').mkdir(parents=True)
            (t / 'f/a.md').write_text('a')
            (t / 'f/sub/b.md').write_text('b')
            before = B.tree_hash(t / 'f')
            os.chmod(t / 'f/a.md', 0o755)
            self.assertNotEqual(B.tree_hash(t / 'f'), before)
            os.chmod(t / 'f/a.md', 0o644)
            (t / 'f/in').symlink_to('sub')   # a link inside the folder: refused for drops, recorded for the analyst's
            with self.assertRaisesRegex(B.Error, 'A link where an input should be'):
                B.tree_hash(t / 'f')
            self.assertNotEqual(B.tree_hash(t / 'f', links=True), before)
            (t / 'out.md').write_text('a')
            (t / 'f/out').symlink_to('../out.md')   # a link that leaves the folder: refused either way
            with self.assertRaisesRegex(B.Error, 'leaves its folder'):
                B.tree_hash(t / 'f', links=True)
            (t / 'f/out').unlink()
            (t / 'f/abs').symlink_to(t / 'f/a.md')   # an absolute target would point into the parent from a branch
            with self.assertRaisesRegex(B.Error, 'absolute target'):
                B.tree_hash(t / 'f', links=True)
        finally:
            shutil.rmtree(t)


if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
