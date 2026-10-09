"""A Claude leg as an actor: legs.py runs the v43 run's legs with it; the OpenAI controller does not admit it yet.

The controller (aggregator/handler/codex/runtime, OpenAI's) keeps one store per actor in its data
folder: state.json, events.jsonl, messages.jsonl. `codex/ADAPTERS.md` sets the interface a backend must
offer before the controller admits it; this file offers it for state['backend'] == 'claude':
create, open, release, workspace, capabilities, message, continue_queued, wait, answer, interrupt,
pause, checkpoint, close, final and restore. The adapter sits beside the harness, not in it:
build.sh fingerprints every file under aggregator/handler/claude, and a v43 rebuild must keep it.

What differs from a Codex actor, on purpose:
- The analyst works in the run's own folder, in place, as in a terminal leg. The run's harness
  (CONTROL/harness) prepares the leg (step.sh --prepare), renders its settings, confirms its session
  and closes it (close.sh), as for a terminal leg. `workspace` names that folder.
- A turn is one headless process, `claude -p --output-format stream-json`, the prompt as its
  argument, the leg's session opened, forked or resumed as step.sh prepared it. Its raw stream goes to
  turns/<id>/stream.jsonl; a follower thread turns each line into panel events (stream.py).
- A message sent while a turn runs goes into the store's inbox, and the adapter's PostToolUse hook
  (inbox_hook.py) gives it to the analyst beside its next tool result, with a receipt. A message no
  tool call picked up stays queued and visible; it never opens a turn by itself. It goes with the next
  message J sends, or with continue_queued().
- A question the analyst asks with `mem.py ask` is a question that does not block (isBlocking false),
  shown while idle too. The answer is written to out/_answers/<id>.md, read-only, without a turn.
- checkpoint() saves: the analyst's folder and the leg's session, verified, in the store. close() is
  the scientific close, once: the run's close.sh. Its git publication is reported apart.
- restore() opens an interview in a copy of a saved folder. A Claude run continues its analysis only
  through its next leg (create() after step.sh), never from a copy: restore refuses that mode.
"""
from pathlib import Path
import contextlib
import datetime
import fcntl
import hashlib
import importlib.util
import io
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import threading
import time
import uuid

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]          # aggregator/handler/claude-adapter -> the repository
FORMAT = 'rplace-claude-v1'
INTERVIEW = ('This is an interview, not a leg. The principal investigator wants to talk with you about the work so far. '
             'You are in a copy of your folder exactly as it stood at the saved point; the run goes on elsewhere, and '
             'nothing you do here reaches it. Answer from what you did and read; read files through the verbs; write only '
             'what the principal investigator asks for.')
OPTIONAL = ('--include-partial-messages', '--forward-subagent-text', '--permission-prompts')
ASK = re.compile(r'Q[A-Z0-9]{1,4}-\d{3,}')
# what a close.sh snapshot holds (close.sh; the controller's claude_backend.CLOSE names the same set)
CLOSE_FILES = {'checkpoint.json', 'fs.tar.gz', 'fs.sha256', 'agent.tar.gz', 'agent-files.sha256', 'transcript.jsonl',
               'instrument.tar.gz', 'validation.json', 'validation-report.txt', 'cost.json'}


class Error(RuntimeError):
    pass


def _sibling(name):
    """stream.py beside this file, whether the controller loads this file by path or as a package."""
    key = '_claude_adapter_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, HERE / (name + '.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sys.modules[key] = mod
    return sys.modules[key]


stream = _sibling('stream')


# ---- small helpers, written as the controller's common.py writes them ----------------------------
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def identity(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}', value) or '..' in value:
        raise Error('Invalid identifier: ' + repr(value))
    return value


def read(path, default=None):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else default


def atomic(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    b = data.encode() if isinstance(data, str) else data
    q = p.with_name('.' + p.name + '.' + uuid.uuid4().hex)
    try:
        with q.open('xb') as f:
            f.write(b)
            f.flush()
            os.fsync(f.fileno())
        os.replace(q, p)
    finally:
        q.unlink(missing_ok=True)


def write(path, value):
    atomic(path, json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def unlock(f):
    """Release a lock file taken with flock(LOCK_EX) and close it."""
    try:
        fcntl.flock(f, fcntl.LOCK_UN)
    finally:
        f.close()


@contextlib.contextmanager
def flock(path, wait=False):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | (0 if wait else fcntl.LOCK_NB))
        except BlockingIOError as e:
            raise Error('Resource is busy: ' + str(p)) from e
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def append(path, **data):
    """One line of events.jsonl or messages.jsonl, as the controller's event() writes it."""
    with flock(str(path) + '.lock', wait=True):
        with Path(path).open('a') as f:
            f.write(json.dumps({'utc': now(), **data}, ensure_ascii=False) + '\n')
            f.flush()
            os.fsync(f.fileno())


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def process_identity(pid):
    """A process's start time. With its pid it names the process across an exec: a launcher that becomes the CLI
    (a shell script, env, node) keeps both and changes its command name (OpenAI review 2026-10-05, finding 1)."""
    ps = shutil.which('ps') or 'ps'
    r = subprocess.run([ps, '-p', str(int(pid)), '-o', 'lstart='], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def same_process(pid, ident):
    """True while the process recorded as (pid, ident) runs. A record from before this rule also carries the
    command name after the start time. Without a recorded identity, a live pid counts as the process: unsure
    is never taken for ended."""
    now = process_identity(pid)
    if not now:
        return False
    if not ident:
        try:
            os.kill(int(pid), 0)
            return True
        except (ProcessLookupError, PermissionError, ValueError):
            return False
    return ident == now or ident.startswith(now + ' ')


def saved_cut(d, label):
    """The cut a snapshot's analyst closed its leg at: done.sh's marker, read from the snapshot's fs.tar.gz."""
    nn, leg = label.split('.', 1)
    try:
        with tarfile.open(Path(d) / 'fs.tar.gz') as t:
            data = t.extractfile('00_GIVE-THE-AGENT/out/_closes/%s-%s.closed' % (nn, leg)).read().decode('utf-8', 'replace')
    except (KeyError, AttributeError, OSError, tarfile.TarError):
        return None
    rows = [x.split() for x in data.splitlines() if x.strip()]
    return rows[-1][1] if rows and len(rows[-1]) > 1 else None


def tail(text, n=1200):
    text = text or ''
    return text if len(text) <= n else '...' + text[-n:]


def data_dir():
    """The controller's data folder: its common.DATA when that module loads, else the same rule."""
    v = os.environ.get('RPLACE_ADAPTER_DATA')     # the adapter's own tests only
    if v:
        return Path(v)
    try:
        spec = importlib.util.spec_from_file_location('_rplace_codex_common',
                                                      REPO / 'aggregator/handler/codex/runtime/common.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return Path(mod.DATA)
    except Exception:
        return REPO.parent / '.rplace-runtime'


def harness(run):
    """The run's own copy of protocol_guard.py (CONTROL/harness), loaded once per run."""
    p = Path(run) / 'CONTROL/harness/protocol_guard.py'
    if not p.is_file():
        raise Error('No Claude harness in this run: CONTROL/harness/protocol_guard.py is missing')
    name = '_claude_guard_' + hashlib.sha256(str(p.resolve()).encode()).hexdigest()[:12]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sys.modules[name] = mod
    return sys.modules[name]


def features(exe):
    """The CLI's version and which optional stream flags it offers (--help), so an older CLI runs."""
    def out(args):
        try:
            return subprocess.run([exe] + args, capture_output=True, text=True, timeout=60).stdout
        except (OSError, subprocess.TimeoutExpired):
            return ''
    helptext = out(['--help'])
    return {'version': (out(['--version']).strip().splitlines() or [''])[0],
            'flags': [f for f in OPTIONAL if f in helptext]}


def clean_env():
    env = os.environ.copy()
    env.pop('AGGREGATOR_LOCK_RUN', None)   # the harness scripts take the run's lock themselves
    return env


class Proc:
    """A turn's process: a child of this controller, or one found alive after a controller restart."""
    def __init__(self, pid, popen=None, ident=None):
        self.pid, self.popen, self.ident = pid, popen, ident

    def poll(self):
        if self.popen is not None:
            return self.popen.poll()
        return None if same_process(self.pid, self.ident) else -1

    def signal(self, sig):
        try:
            os.kill(self.pid, sig)
        except ProcessLookupError:
            pass

    def wait(self, timeout):
        end = time.monotonic() + timeout
        while self.poll() is None:
            if time.monotonic() > end:
                return False
            time.sleep(0.2)
        return True


class Ended(Proc):
    """A turn's process that ended while no controller followed it: its stream is read to the end, then settled."""
    def __init__(self):
        Proc.__init__(self, 0, None, None)

    def poll(self):
        return -1

    def signal(self, sig):
        pass

    def wait(self, timeout):
        return True


class Live:
    """What the controller's status reads for questions_live: server.p.poll()."""
    def __init__(self, proc):
        self.p = proc

    def close(self):
        pass


def group_alive(pid):
    """True while any process of the turn's process group (its pid) remains: a tool left running."""
    if not pid:
        return False
    ps = shutil.which('ps') or 'ps'
    r = subprocess.run([ps, '-axo', 'pgid='], capture_output=True, text=True)
    return str(int(pid)) in r.stdout.split()


def publication(text):
    """publish.sh's report, from close.sh's output: its own receipt, never the snapshot's."""
    lines = [x.strip() for x in (text or '').splitlines() if x.strip().startswith(('git:', 'manual:'))]
    status = 'not reported'
    for x in lines:
        for key, value in (('git: pushed', 'pushed'), ('git: committed', 'committed'), ('nothing new to commit', 'nothing new'),
                           ('push failed', 'committed, push failed'), ('not in a repository', 'no repository'),
                           ('no remote set', 'committed, no remote'), ('cannot enter', 'failed'), ('add failed', 'add failed')):
            if key in x:
                status = value
    return {'status': status, 'lines': lines}


def verify_saved(g, d):
    """A saved folder (an adapter capture or a close.sh snapshot): both archives against their per-entry
    manifests, and the transcript against the recorded boundary. Returns checkpoint.json."""
    d = Path(d)
    ck = read(d / 'checkpoint.json')
    if not ck or ck.get('subject') != 'aggregator':
        raise Error('%s holds no aggregator checkpoint' % d)
    g.verify_archive(d / 'fs.tar.gz', '00_GIVE-THE-AGENT', d / 'fs.sha256')
    if (d / 'agent.tar.gz').exists():
        g.verify_archive(d / 'agent.tar.gz', '.cc', d / 'agent-files.sha256')
        s = ck['session']
        project = s.get('project', 'run')
        entry = g.load_manifest(d / 'agent-files.sha256').get('projects/%s/%s.jsonl' % (project, s['session_id']))
        if not entry or entry[2] != s['transcript_sha256'] or sha(d / 'transcript.jsonl') != s['transcript_sha256']:
            raise Error('the saved transcript is not the recorded boundary')
    digests = read(d / 'DIGESTS.json')
    if digests:
        for name, value in digests.items():
            if sha(d / name) != value:
                raise Error('%s changed since it was saved' % name)
    return ck


class ClaudeActor:
    def __init__(self, actor, data=None):
        self.data = Path(data) if data else data_dir()
        self.base = self.data / 'actors' / identity(actor)
        self.state = read(self.base / 'state.json')
        if not self.state:
            raise Error('Unknown actor ' + actor)
        if self.state.get('backend') != 'claude':
            raise Error('Not a Claude actor: ' + actor)
        self.guard = threading.RLock()
        self.condition = threading.Condition(self.guard)
        self.lease = None
        self.proc = None
        self.server = None
        self.runlock = None
        self.lock_wait = None   # seconds finish() waits for the run's lock; None: RPLACE_ADAPTER_LOCK_WAIT, else 600
        self.worker = None
        self.stop_requested = None
        self.rundir = Path(self.state['claude_run'])
        self.ag = Path(self.state.get('workspace') or self.rundir / '00_GIVE-THE-AGENT')
        self.project = self.state.get('project', 'run')
        self.inbox = self.base / 'inbox'
        self.seen = set()

    # ---- what the controller asks of every backend (ADAPTERS.md) ------------------------------
    @property
    def workspace(self):
        """The analyst's root: the run's own folder for a leg, its copy for an interview."""
        return self.ag

    def leg(self):
        return self.state.get('role') != 'interview'

    def capabilities(self):
        return {'backend': 'claude', 'format': FORMAT, 'workspace': str(self.ag), 'role': self.state.get('role'),
                'steer': 'beside the next tool result, with a receipt (inbox_hook.py)',
                'queued_messages_start_turns': False,
                'native_questions': False,
                'durable_questions': 'mem.py ask; answered while idle, without a turn; answer files read-only',
                'cards': 'through message()',
                'pause': 'the folder\'s .pause and a note to the analyst',
                'checkpoint': 'the folder and the session, saved and verified in the store; never a close',
                'close': 'the run\'s close.sh, once' if self.leg() else None,
                'restore_modes': ['interview']}

    # ---- the store ------------------------------------------------------------------------------
    def save(self):
        write(self.base / 'state.json', self.state)

    def emit(self, method, **params):
        append(self.base / 'events.jsonl', native={'method': method, 'params': params})

    def note(self, key, head, text, status='completed'):
        self.emit('item/completed', threadId=self.state.get('thread_id'), turnId=self.state.get('active_turn_id'),
                  item={'type': 'dynamicToolCall', 'id': key, 'command': head, 'status': status,
                        'aggregatedOutput': stream.clip(text)})

    def transcript(self, sid):
        if str(uuid.UUID(sid)) != sid:
            raise Error('invalid session id')
        return self.rundir / 'CONTROL/.cc/projects' / self.project / (sid + '.jsonl')

    # ---- ownership ------------------------------------------------------------------------------
    def open(self):
        with self.guard:
            current = read(self.base / 'state.json', {})
            if current.get('evicted'):
                raise Error('Actor store is archived; restore its checkpoint as a new actor.')
            if self.lease:
                return self.state
            lease = flock(self.base / 'owner.lock')
            lease.__enter__()
            try:
                self.state = current or self.state
                self.seen = {p.name for p in (self.inbox / 'delivered').glob('*.json')}
                previous = read(self.base / 'native-process.json')
                alive = bool(previous) and same_process(previous['pid'], previous.get('identity'))
                if alive and previous.get('turn') == self.state.get('active_turn_id'):
                    # the controller restarted during a turn: follow the same process to its end
                    self.lease = lease
                    self.attach(previous)
                    return self.state
                if alive:
                    raise Error('A Claude process of this actor is still running (pid %s) outside any recorded '
                                'turn. Inspect it before a second owner opens.' % previous['pid'])
                (self.base / 'native-process.json').unlink(missing_ok=True)
                if self.state.get('active_turn_id'):
                    self.lease = lease
                    self.settle(self.state['active_turn_id'])
                if self.state.get('pending_finalize') and not self.state.get('active_turn_id'):
                    lock = self.lock_run(0)   # finished only with the run's lock; else start, save or close does it
                    if lock:
                        try:
                            self.finalize_pending()
                        finally:
                            unlock(lock)
                self.state['undelivered'] = [m.get('id') for _, m in self.undelivered()]
                self.save()
                self.lease = lease
            except BaseException:
                self.lease = None   # a failed settle leaves no owner behind
                lease.__exit__(None, None, None)
                raise
        self.surface(None)   # open questions show while idle too
        return self.state

    def lock_run(self, wait):
        """The run's lock (CONTROL/.protocol.lock), waited for up to `wait` seconds; None while another owner keeps
        it, and then nothing of the run is written."""
        lock = (self.rundir / 'CONTROL/.protocol.lock').open('a')
        end = time.monotonic() + wait
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return lock
            except BlockingIOError:
                if time.monotonic() >= end:
                    lock.close()
                    return None
                time.sleep(0.5)

    def finalize_pending(self):
        """A turn that ended while another owner held the run's lock: its run files are written now, under the lock
        the caller holds, and only while it is still the leg's last turn and the run is still at this leg
        (independent review of the recheck round, 2026-10-05)."""
        pf = self.state.pop('pending_finalize', None)
        if not pf:
            return
        turn = pf['turn']
        if turn != self.state.get('last_turn_id') or self.state.get('active_turn_id'):
            self.note('finalize-dropped-' + turn, 'A held turn was superseded', 'A later turn ran; this turn\'s run '
                      'files were never written.', status='failed')
            return
        try:
            status, error = self.run_writes(turn, pf['rc'], pf['status'], pf['error'])
            status, error = self.check_turn(turn, self.base / 'turns' / turn, status, error)
        except BaseException:
            self.state['pending_finalize'] = pf   # still held: the next start, save or close tries again
            raise
        self.state.update(boundary=status, status='idle' if status == 'completed' else status, error=error)
        self.note('finalized-' + turn, 'The held turn was finished', 'Under the run\'s lock; the turn is %s.' % status,
                  status='completed' if status == 'completed' else 'failed')
        self.save()

    def settle(self, turn):
        """A turn whose process ended while no controller followed it: its stream is read to the end and its boundary
        settled from its own result line (finish(): the launch's exit recorded, the session confirmed), as if it had
        been followed. Without a stream, the turn is recorded as interrupted."""
        tdir = self.base / 'turns' / turn
        if not (tdir / 'stream.jsonl').is_file():
            self.state.update(active_turn_id=None, status='interrupted', boundary='interrupted', questions=[],
                              error='The turn ended while no controller followed it, and left no stream.')
            return
        offset = int((read(tdir / 'offset.json') or {}).get('offset', 0))
        self.note('settled-' + turn, 'The turn ended while no controller followed it',
                  'Its stream is read to the end from byte %d; its own result line settles the boundary.' % offset)
        self.proc = Ended()
        self.server = Live(self.proc)
        self.lock_wait = 0   # never waited for here: open() runs before the handler serves; a held lock defers
        try:
            self.follow(turn, offset)
        finally:
            self.lock_wait = None

    def release(self):
        with self.guard:
            if self.proc and self.proc.poll() is None:
                return   # a live turn keeps its owner
            if self.lease:
                self.lease.__exit__(None, None, None)
                self.lease = None

    # ---- the inbox ------------------------------------------------------------------------------
    def queue(self, text, kind='message', item=None):
        # nanoseconds first: the inbox and the hook deliver in name order, so ids sort as the messages were sent
        mid = '%s-%020d-%s' % (time.strftime('%Y%m%dT%H%M%S', time.gmtime()), time.time_ns(), uuid.uuid4().hex[:6])
        write(self.inbox / (mid + '.json'), {'id': mid, 'kind': kind, 'text': text, 'utc': stamp(), 'item': item})
        self.state['undelivered'] = [m.get('id') for _, m in self.undelivered()]
        return mid

    def undelivered(self):
        done = self.inbox / 'delivered'
        out = []
        for p in sorted(self.inbox.glob('*.json')):
            if not (done / p.name).exists():
                m = read(p)
                if isinstance(m, dict):
                    out.append((p, m))
        return out

    def carry(self, hand):
        """J's messages that still wait when the leg has closed, handed to whoever carries on its conversation
        (legs.py: the next leg's first message). hand(message) takes each first; only then is it marked
        delivered "via carried": delivered once, and never lost with the closed leg (OpenAI review, finding 4)."""
        with self.guard:
            if self.state.get('active_turn_id'):
                raise Error('A turn is running; its queued messages reach it beside its next tool result')
            out = []
            for p, m in self.undelivered():
                if m.get('kind') == 'message':
                    hand(m)
                    write(self.inbox / 'delivered' / p.name, {'id': m.get('id'), 'via': 'carried', 'utc': stamp(), 'turn': None})
                    out.append(m)
            self.state['undelivered'] = [m.get('id') for _, m in self.undelivered()]
            self.save()
            return out

    def current(self):
        """A leg's new turn is for the run's current leg only: the folder has moved on if step.sh has since
        prepared or opened another leg (OpenAI review 2026-10-05, finding 2). Raises before anything is written."""
        if not self.leg():
            return
        current = (self.ag / '.leg').read_text().strip() if (self.ag / '.leg').is_file() else None
        pend = read(self.rundir / 'CONTROL/pending_launch.json') or {}
        if current != self.state.get('leg') or (pend and pend.get('label') != self.state['label']):
            raise Error('The run has moved on to %s since %s was opened: its folder is no longer this leg\'s. Talk to '
                        'the current leg, or open an interview of this one.' % (pend.get('label') or current, self.state['label']))

    def receipt(self, mid):
        """A message's delivery receipt, or None while it waits."""
        return read(self.inbox / 'delivered' / (mid + '.json'))

    def receipts(self):
        """Show each message the hook delivered, once, with its receipt."""
        for p in sorted((self.inbox / 'delivered').glob('*.json')):
            if p.name in self.seen:
                continue
            self.seen.add(p.name)
            r = read(p, {})
            self.emit('rplace/messageDelivered', messageId=r.get('id'), via=r.get('via'), utc=r.get('utc'),
                      tool=r.get('tool'), turnId=r.get('turn') or self.state.get('active_turn_id'))
            if r.get('via') == 'hook':
                self.note('delivered-' + p.stem, 'Message delivered beside the analyst\'s tool result',
                          'Delivered %s, after %s.' % (r.get('utc'), r.get('tool') or 'a tool call'))

    # ---- questions the analyst asks with mem.py ask ---------------------------------------------
    def asks(self):
        p = self.ag / 'out/asks.jsonl'
        rows = []
        if p.exists():
            for line in p.read_text(encoding='utf-8').splitlines():
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if isinstance(r, dict) and isinstance(r.get('id'), str) and ASK.fullmatch(r['id']):
                    rows.append(r)
        return rows

    def answered(self, qid):
        return (self.ag / 'out/_answers' / (qid + '.md')).exists()

    def surface(self, turn):
        """Every open question becomes a panel question. It does not block the analyst, and it shows while
        no turn runs too."""
        with self.guard:
            known = {q.get('requestKey') for q in self.state.get('questions', [])}
            changed = False
            for r in self.asks():
                qid = r['id']
                if qid in known or self.answered(qid):
                    continue
                text = '%s, leg %s, %s\n%s\n\nMeanwhile the analyst: %s' % (
                    qid, r.get('leg', '?'), r.get('t', ''), r.get('question', ''), r.get('assumption', ''))
                params = {'threadId': self.state.get('thread_id'), 'turnId': turn, 'requestId': qid,
                          'requestKey': qid, 'isBlocking': False,
                          'questions': [{'id': 'answer', 'header': qid, 'question': text}]}
                self.state.setdefault('questions', []).append(params)
                self.emit('item/tool/requestUserInput', **params)
                changed = True
            open_now = [r['id'] for r in self.asks() if not self.answered(r['id'])]
            if open_now != self.state.get('open_asks'):
                self.state['open_asks'] = open_now
                changed = True
            if changed:
                self.save()

    def answer(self, key, answers):
        """A durable answer: written now, idle or not, and never a reason to start a turn."""
        with self.guard:
            rows = {r['id']: r for r in self.asks()}
            if key not in rows:
                raise Error('No question %s in out/asks.jsonl' % key)
            if self.answered(key):
                raise Error('%s is already answered: out/_answers/%s.md' % (key, key))
            if (not isinstance(answers, dict) or not answers
                    or any(not isinstance(v, str) or not v.strip() or len(v) > 20000 for v in answers.values())):
                raise Error('Supply one nonempty answer for every question')
            text = (answers.get('answer') or '\n\n'.join(answers.values())).strip()
            path = self.ag / 'out/_answers' / (key + '.md')
            atomic(path, text + '\n')
            os.chmod(path, 0o444)   # the controller's file: the analyst reads it, never edits it
            q = next((x for x in self.state.get('questions', []) if x.get('requestKey') == key), None)
            questions = q['questions'] if q else [{'id': 'answer', 'question': rows[key].get('question', '')}]
            self.state['questions'] = [x for x in self.state.get('questions', []) if x.get('requestKey') != key]
            self.state['open_asks'] = [x for x in self.state.get('open_asks', []) if x != key]
            self.emit('rplace/questionAnswered', requestKey=key, questions=questions, answers=answers)
            mid = self.queue('The principal investigator answered %s.\nYour question: %s\nHis answer: %s\nThe answer '
                             'is also in `python3 tools/mem.py asks %s`. Revisit the work that rested on your assumption '
                             '(%s).' % (key, rows[key].get('question', ''), text, key, rows[key].get('assumption', '')),
                             kind='answer', item=key)
            self.save()
            return {'answered': key, 'new_turn_started': False, 'file': 'out/_answers/%s.md' % key, 'message': mid,
                    'delivery': 'beside the next tool result' if self.state.get('active_turn_id')
                    else 'with the next turn J starts; it is in the answer file now'}

    # ---- turns ----------------------------------------------------------------------------------
    def message(self, text):
        """Start a turn when idle, or queue for the running one. Returns its delivery state."""
        if not isinstance(text, str) or not text.strip():
            raise Error('Message is empty')
        self.open()
        with self.guard:
            if self.state.get('closed'):
                raise Error('This leg is closed. Open the next leg, or an interview with restore().')
            if not self.state.get('active_turn_id'):
                self.current()   # a refused turn leaves no trace of the words
            append(self.base / 'messages.jsonl', role='user', text=text)
            key = 'user-' + uuid.uuid4().hex[:12]
            self.emit('item/completed', threadId=self.state.get('thread_id'), turnId=self.state.get('active_turn_id'),
                      item={'type': 'userMessage', 'id': key, 'content': [{'type': 'text', 'text': text}]})
            if self.state.get('active_turn_id'):
                mid = self.queue(text, item=key)
                self.save()
                self.note('queued-' + mid, 'Message queued for the analyst',
                          'It reaches the analyst beside its next tool result, with a receipt. If the turn ends first, '
                          'it waits for your next message; it never opens a turn by itself.')
                return {'queued': mid, 'delivery': 'pending', 'receipt': None,
                        'turn': {'id': self.state['active_turn_id'], 'status': 'working'}, 'new_turn_started': False}
            return self.start(text)

    def continue_queued(self):
        """J's explicit word to send what waits in the inbox as a turn of its own."""
        self.open()
        with self.guard:
            if self.state.get('active_turn_id'):
                raise Error('A turn is running; queued messages reach it beside its next tool result')
            if not self.undelivered():
                raise Error('Nothing is queued')
            return self.start(None)

    @staticmethod
    def prompt(pending, text):
        """The turn's prompt: what waits in the inbox, then the new text."""
        parts = []
        for _, m in pending:
            if m.get('kind') == 'message':
                parts.append('Message from the principal investigator (%s):\n%s' % (m.get('utc', ''), m.get('text', '')))
            else:
                parts.append(m.get('text', ''))
        if text:
            parts.append(text)
        return '\n\n'.join(parts)

    def start(self, text):
        with self.guard:
            if self.proc and self.proc.poll() is None:
                raise Error('A turn is running')
            if self.state.get('closed'):
                raise Error('This leg is closed')
            run, c = self.rundir, self.rundir / 'CONTROL'
            g = harness(run)
            leg = self.leg()
            sid = self.state['session_id']
            path = self.transcript(sid)
            if path.exists():
                rows = g.messages(path)
                if not rows or not any(r.get('sessionId') == sid for r in rows):
                    raise Error('The session transcript holds nothing under its own id; preserve it for recovery')
                session = ['--resume', sid]
            elif self.state['mode'] == 'fork':
                session = ['--resume', self.state['parent_session'], '--fork-session', '--session-id', sid]
            elif self.state['mode'] in ('shared', 'resumed'):
                raise Error('The recorded transcript is missing; refusing a fresh replacement')
            else:
                session = ['--session-id', sid]
            env = clean_env()
            if env.get('ANTHROPIC_API_KEY') and not self.state.get('api_ok'):
                raise Error('ANTHROPIC_API_KEY is set; a subscription leg refuses it, as step.sh does without --api-ok')
            lock = None
            if leg:
                lock = (c / '.protocol.lock').open('a')
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as e:
                    lock.close()
                    raise Error('A handler operation or another launch holds this run (CONTROL/.protocol.lock)') from e
                try:   # checked again under the run's lock: refused before anything is written or queued
                    self.current()
                except BaseException:
                    unlock(lock)
                    raise
            try:
                if leg:
                    self.finalize_pending()   # a held turn's run files first, before another launch
                    label = self.state['label']
                    g.settings(run, g.stage_of(label))
                    model, ent = g.arm_for(run, label)
                    effort = ent.get('effort')
                    g.seed_trust(run)
                else:
                    model, effort = self.state['model'], self.state.get('effort')
                    try:
                        g.seed_trust(run, str(self.ag))
                    except Exception as e:   # interview.sh tolerates this too
                        self.note('trust-' + uuid.uuid4().hex[:8], 'Folder trust not seeded', repr(e))
                pending = self.undelivered()
                body = self.prompt(pending, text)
                if not body.strip():
                    raise Error('Nothing to send')
                if not leg and not self.state.get('turns'):
                    body = INTERVIEW + '\n\n' + body
                turn = uuid.uuid4().hex
                tdir = self.base / 'turns' / turn
                tdir.mkdir(parents=True)
                # the transcript's last row as the turn starts: at its end, the last row must be new, the model's,
                # and under this session (OpenAI recheck 2026-10-05, blocker 2)
                start_rows = g.messages(path) if path.exists() else []
                fork = self.state.get('parent_session') if '--fork-session' in session else None
                parent = self.transcript(fork) if fork else None
                write(tdir / 'transcript-start.json', {
                    'last': g.message_id(start_rows[-1]) if start_rows else None, 'rows': len(start_rows),
                    'model': model, 'fork_parent': fork,
                    # a fork's first turn copies its parent's messages with their ids, under the new session's id,
                    # and leaves the parent's other lines behind (claude 2.1.289, J's Mac, 5 October): the copies
                    # are told by their ids, never by a line count
                    'parent_ids': [g.message_id(r) for r in g.messages(parent)] if parent else []})
                hooks = tdir / 'adapter-settings.json'
                adapter_settings = {'hooks': {'PostToolUse': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': ' '.join(
                    shlex.quote(x) for x in (sys.executable, str(HERE / 'inbox_hook.py'), str(self.inbox)))}]}]}}
                # fast mode (J, 2026-10-09 09:27 Berlin): a headless turn takes /fast only from its --settings, so
                # the switch is fast-mode.json beside this file ({"fastMode": true|false}), read at each turn's launch;
                # absent or unreadable means off. Billed from usage credits, not the plan's limits.
                try:
                    if json.loads((HERE / 'fast-mode.json').read_text()).get('fastMode') is True:
                        adapter_settings['fastMode'] = True
                except (OSError, ValueError, AttributeError):
                    pass
                write(hooks, adapter_settings)
                flags = set(self.state['runtime'].get('flags', []))
                cmd = [self.state['runtime']['executable'], '-p', '--output-format', 'stream-json', '--verbose']
                cmd += [f for f in ('--include-partial-messages', '--forward-subagent-text') if f in flags]
                cmd += session + ['--settings', str(hooks), '--strict-mcp-config', '--permission-mode', 'dontAsk']
                if '--permission-prompts' in flags:
                    cmd += ['--permission-prompts', 'none']
                cmd += ['-n', ('leg-' if leg else 'interview-') + self.state['label'], '--model', model]
                if effort:
                    cmd += ['--effort', effort]
                cmd += ['--', body]
                env.update(CLAUDE_CONFIG_DIR=str(c / '.cc'), CLAUDE_CODE_PROJECT_DIR_NAME=self.project,
                           CLAUDE_CODE_SUBAGENT_MODEL=model, CLAUDE_CODE_DISABLE_AUTO_MEMORY='1')
                if leg:
                    env['STAGE'] = g.stage_of(self.state['label'])
                write(tdir / 'command.json', {'argv': cmd[:-1] + ['<prompt: prompt.txt>'], 'cwd': str(self.ag),
                                              'utc': now()})
                atomic(tdir / 'prompt.txt', body)
                if leg:
                    write(c / 'active_launch.json', dict(self.state.get('pending') or {}, handler_pid=os.getpid(),
                                                         started_utc=now(), adapter_actor=self.state['id'],
                                                         adapter_turn=turn))
                with (tdir / 'stream.jsonl').open('wb') as out, (tdir / 'stderr.log').open('wb') as err:
                    popen = subprocess.Popen(cmd, cwd=str(self.ag), env=env, stdin=subprocess.DEVNULL, stdout=out,
                                             stderr=err, start_new_session=True)
            except BaseException as e:
                if leg:
                    (c / 'active_launch.json').unlink(missing_ok=True)
                if lock:
                    fcntl.flock(lock, fcntl.LOCK_UN)
                    lock.close()
                # what waited in the inbox still waits, and J's new text joins it: a failed start delivers
                # nothing, loses nothing, and starts nothing later by itself
                if text:
                    first = leg and not self.state.get('turns')
                    self.queue(text, kind='prompt' if first else 'message')
                self.state.update(error='The turn could not start: %s' % e,
                                  undelivered=[m.get('id') for _, m in self.undelivered()])
                self.save()
                raise
            self.runlock = lock
            delivered = []
            for p, m in pending:   # delivered with the prompt, now that the process runs
                write(self.inbox / 'delivered' / p.name, {'id': m.get('id'), 'via': 'prompt', 'utc': stamp(), 'turn': turn})
                delivered.append(m.get('id'))
            ident = None
            for _ in range(10):
                ident = process_identity(popen.pid)
                if ident:
                    break
                time.sleep(0.05)
            self.proc = Proc(popen.pid, popen, ident)
            self.server = Live(self.proc)
            write(self.base / 'native-process.json', {'pid': popen.pid, 'identity': ident, 'utc': now(), 'turn': turn,
                                                      'stream': str(tdir / 'stream.jsonl')})
            self.stop_requested = None
            self.state.update(active_turn_id=turn, status='working', error=None, leg_started=True, last_pid=popen.pid,
                              turns=self.state.get('turns', 0) + 1, undelivered=[])
            self.save()
            self.emit('turn/started', threadId=sid, turn={'id': turn, 'status': 'inProgress'})
            self.receipts()
            if text is None:
                self.note('followup-' + turn, 'Turn opened by J for queued messages', body)
            self.surface(turn)
            self.worker = threading.Thread(target=self.follow, args=(turn, 0), daemon=True)
            self.worker.start()
            return {'turn': {'id': turn, 'status': 'working'}, 'new_turn_started': True, 'delivered_with_prompt': delivered}

    def attach(self, rec):
        """After a controller restart: follow a turn's process that is still alive."""
        turn = rec['turn']
        if self.leg():
            lock = (self.rundir / 'CONTROL/.protocol.lock').open('a')
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.runlock = lock
            except BlockingIOError:
                lock.close()
                self.note('attached-lock-' + turn, 'Run lock held elsewhere', 'A handler operation holds '
                          'CONTROL/.protocol.lock; the turn is followed, read only, and nothing of the run is written '
                          'before the lock is free.')
        self.proc = Proc(rec['pid'], None, rec.get('identity'))
        self.server = Live(self.proc)
        offset = int((read(self.base / 'turns' / turn / 'offset.json') or {}).get('offset', 0))
        self.note('attached-' + turn, 'Controller restarted; following the running turn again',
                  'pid %s, from byte %d of its stream' % (rec['pid'], offset))
        self.worker = threading.Thread(target=self.follow, args=(turn, offset), daemon=True)
        self.worker.start()

    def follow(self, turn, offset):
        tdir = self.base / 'turns' / turn
        t = stream.Translator(self.state.get('thread_id'), turn)
        buf, last_poll, ended = b'', 0.0, False
        try:
            with (tdir / 'stream.jsonl').open('rb') as f:
                f.seek(offset)
                while True:
                    chunk = f.read(1 << 16)
                    if chunk:
                        buf += chunk
                        *lines, buf = buf.split(b'\n')
                        for line in lines:
                            if line.strip():
                                self.line(t, line, tdir)
                        offset = f.tell() - len(buf)
                    if time.monotonic() - last_poll > 1:
                        last_poll = time.monotonic()
                        self.surface(turn)
                        self.receipts()
                        write(tdir / 'offset.json', {'offset': offset})
                    if not chunk:
                        if ended:          # the process had ended and its stream is drained
                            if buf.strip():
                                self.line(t, buf, tdir)
                            break
                        if self.proc.poll() is not None:
                            ended = True   # read once more: what it wrote before it ended
                            continue
                        time.sleep(0.1)
        except Exception as e:
            write(self.base / 'callback-error.json', {'error': repr(e), 'utc': now(), 'turn': turn})
        self.finish(turn, t, tdir)

    def line(self, t, raw, tdir):
        try:
            m = json.loads(raw)
        except ValueError:
            return self.note('unreadable-%s' % uuid.uuid4().hex[:8], 'A stream line that is not JSON',
                             raw.decode('utf-8', 'replace'))
        for method, params in t.feed(m):
            self.emit(method, **params)
        if m.get('type') == 'system' and m.get('subtype') == 'init':
            write(tdir / 'init.json', m)
        if m.get('type') == 'result':
            write(tdir / 'result.json', m)

    def finish(self, turn, t, tdir):
        rc = self.proc.popen.wait() if self.proc.popen is not None else None
        r = t.result or read(tdir / 'result.json') or {}
        if self.stop_requested == turn:
            status, error = 'interrupted', None
        elif r.get('subtype') == 'success' and not r.get('is_error') and rc in (0, None):
            status, error = 'completed', None
        else:
            errtext = tail((tdir / 'stderr.log').read_text(errors='replace')) if (tdir / 'stderr.log').exists() else ''
            status, error = 'failed', {'message': str(r.get('result') or r.get('subtype') or
                                                  'claude exited %s. %s' % (rc, errtext))}
        # the init line, also when a restart read the stream from past it (finding 7); without one, the session the
        # CLI ran is unknown, and a completed boundary is not claimed
        init = t.init or read(tdir / 'init.json') or {}
        if status == 'completed' and not init.get('session_id'):
            status, error = 'failed', {'message': 'The stream has no init line: the session the CLI ran is unknown'}
        (self.base / 'native-process.json').unlink(missing_ok=True)
        if init.get('session_id') and init['session_id'] != self.state['session_id']:
            # the CLI ran another session than the leg's: the boundary fails, whatever the result said
            error = {'message': 'The CLI ran session %s, not the leg\'s %s' % (init['session_id'], self.state['session_id'])}
            status = 'failed' if status != 'interrupted' else status
            self.note('session-' + turn, 'The CLI ran another session than the leg\'s', error['message'], status='failed')
        if self.leg():
            # the run's files are written under the run's lock only; while another owner keeps it, nothing of the
            # run is written, the turn stays uncertain, and the next open() finishes it (OpenAI recheck, blocker 3)
            if not self.runlock:
                wait = self.lock_wait
                if wait is None:
                    wait = float(os.environ.get('RPLACE_ADAPTER_LOCK_WAIT', '600'))
                self.runlock = self.lock_run(wait)
            if self.runlock:
                try:
                    status, error = self.run_writes(turn, rc, status, error)
                    self.state.pop('pending_finalize', None)
                except Exception as e:
                    status, error = 'failed', {'message': 'The turn\'s run files could not be written: %r' % e}
                    self.note('run-writes-' + turn, 'The turn\'s run files could not be written', repr(e), status='failed')
            else:
                self.state['pending_finalize'] = {'turn': turn, 'rc': rc, 'status': status, 'error': error}
                self.note('uncertain-' + turn, 'The run lock stayed held', 'Nothing of the run was written for this '
                          'turn; opening the leg again finishes it.', status='failed')
                status, error = 'uncertain', {'message': 'Another owner held the run lock when this turn ended; '
                                                         'nothing of the run was written. Opening the leg again finishes it.'}
        if self.runlock:   # released only now: confirm() writes sessions.json and RUN.json under it
            unlock(self.runlock)
            self.runlock = None
        status, error = self.check_turn(turn, tdir, status, error)
        write(tdir / 'exit.json', {'exit_code': rc, 'status': status, 'utc': now()})
        self.receipts()
        with self.condition:
            waiting = [m.get('id') for _, m in self.undelivered()]
            self.state.update(active_turn_id=None, last_turn_id=turn, boundary=status,
                              status='idle' if status == 'completed' else status, error=error, questions=[],
                              undelivered=waiting,
                              usage={k: r.get(k) for k in ('usage', 'total_cost_usd', 'num_turns', 'duration_ms',
                                                           'modelUsage') if k in r},
                              effective={k: init.get(k) for k in ('session_id', 'model', 'permissionMode',
                                                                  'claude_code_version', 'cwd') if k in init})
            self.proc, self.server = None, None
            self.save()
            self.emit('turn/completed', threadId=self.state.get('thread_id'),
                      turn={'id': turn, 'status': status, 'error': error})
            if waiting:
                # never a turn by itself: J's next message, or continue_queued(), sends them
                self.note('waiting-' + turn, '%d message(s) not delivered before the turn ended' % len(waiting),
                          'They wait in the inbox and go with your next message, or with continue_queued(). '
                          'No turn was started.')
            self.condition.notify_all()
        self.surface(None)

    def run_writes(self, turn, rc, status, error):
        """Under the run's lock, and only while the run is at this leg: the launch's exit, this turn's active launch
        cleared, the session confirmed once, from this leg's own pending launch."""
        c = self.rundir / 'CONTROL'
        try:
            self.current()
        except Error as e:
            self.note('moved-on-' + turn, 'The run moved on before this turn\'s run files were written', str(e),
                      status='failed')
            return 'failed', {'message': 'Nothing of the run was written for this turn: %s' % e}
        exit_rec = {'launch_id': self.state.get('launch_id'), 'label': self.state['label'],
                    'session_id': self.state['session_id'], 'exited_utc': now(), 'adapter_turn': turn}
        if rc is not None:
            exit_rec['exit_code'] = rc
        else:   # the process ended while no controller followed it: only its own stream speaks for it
            exit_rec.update(exit_code=0 if status == 'completed' else 1,
                            exit_inferred_from='the stream\'s %s result line; this handler did not start the process '
                            '(a restart), so its exit status is unknown' % ('success' if status == 'completed'
                                                                            else 'missing or failed'))
        write(c / 'last_launch_exit.json', exit_rec)
        if (read(c / 'active_launch.json') or {}).get('adapter_turn') == turn:   # never another launch's record
            (c / 'active_launch.json').unlink()
        pend = read(c / 'pending_launch.json') or {}
        if not self.state.get('confirmed') and pend and (pend.get('label') != self.state['label'] or (
                self.state.get('launch_id') and pend.get('launch_id') != self.state['launch_id'])):
            msg = 'Session not confirmed: the pending launch is %s (%s), not this leg\'s' % (pend.get('label'),
                                                                                         pend.get('launch_id'))
            self.note('confirm-' + turn, 'Session not confirmed', msg, status='failed')
            return ('failed', {'message': msg}) if status != 'interrupted' else (status, error)
        if not self.state.get('confirmed'):
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    ok = harness(self.rundir).confirm(self.rundir)
            except Exception as e:
                ok = False
                buf.write(repr(e))
            self.state['confirmed'] = bool(ok)
            if not ok:
                # an unconfirmed session fails the boundary: the turn may have run, but not as this leg
                msg = 'Session not confirmed: %s' % (buf.getvalue().strip() or 'no new message under the id')
                self.note('confirm-' + turn, 'Session not confirmed', msg, status='failed')
                if status != 'interrupted':
                    status, error = 'failed', {'message': msg}
        return status, error

    def check_turn(self, turn, tdir, status, error):
        """Every completed turn, not only the first: every row the turn added is under this session, every reply it
        added was served by the model it was launched with (close.sh's model audit), and the transcript ends on a new
        reply (OpenAI recheck 2026-10-05, blocker 2; independent review: every row, not the last alone). A fork's first
        turn tells the copied history by its message ids."""
        start = read(tdir / 'transcript-start.json')
        if status != 'completed' or start is None:
            return status, error
        g = harness(self.rundir)
        sid = self.state['session_id']
        rows = g.messages(self.transcript(sid))
        n, fork = start.get('rows', 0), start.get('fork_parent')
        want = start.get('model') or self.state.get('model') or ''   # the model this turn was launched with
        why = None
        if fork:   # the parent's messages, copied by the fork with their ids, are history
            old = set(start.get('parent_ids') or [])
            new = [r for r in rows if g.message_id(r) not in old]
        elif n and (len(rows) < n or g.message_id(rows[n - 1]) != start.get('last')):
            new, why = [], 'the transcript changed before this turn\'s rows (it is appended to, never rewritten)'
        else:
            new = rows[n:]
        last = rows[-1] if rows else {}
        if why:
            pass
        elif not new or g.message_id(last) != g.message_id(new[-1]):
            why = 'the turn left no new row in its transcript'
        elif last.get('type') != 'assistant':
            why = 'the transcript does not end on the model\'s reply'
        else:
            for r in new:
                model = (r.get('message') or {}).get('model') or ''
                if r.get('sessionId') != sid:
                    why = 'a row the turn added is under session %s, not %s' % (r.get('sessionId'), sid)
                elif r.get('type') == 'assistant' and want and model not in ('', '<synthetic>') \
                        and not model.startswith(want):
                    why = 'a reply the turn added was served by %s, not the arm\'s %s' % (model, want)
                if why:
                    break
        if why:
            self.note('transcript-' + turn, 'The turn\'s transcript does not show this leg\'s turn', why, status='failed')
            return 'failed', {'message': 'The turn ended, but ' + why}
        return status, error

    def wait(self, timeout=3600):
        end = time.monotonic() + timeout
        with self.condition:
            while self.state.get('active_turn_id'):
                left = end - time.monotonic()
                if left <= 0:
                    raise Error('Turn still running; it remains resumable')
                self.condition.wait(min(left, 2))
        return self.state

    def interrupt(self):
        """SIGINT ends a headless turn; the session stays resumable. Records an interrupted boundary."""
        with self.guard:
            proc, turn = self.proc, self.state.get('active_turn_id')
            if proc and proc.poll() is None:
                self.stop_requested = turn
                proc.signal(signal.SIGINT)
        if proc and not proc.wait(30):
            proc.signal(signal.SIGTERM)
            if not proc.wait(10):
                proc.signal(signal.SIGKILL)
        self.wait(60)

    def pause(self):
        """pause.sh's request, and a note to the analyst when a turn runs. Never marks anything verified."""
        atomic(self.ag / '.pause', 'pause requested %s\n' % stamp())
        if self.leg():
            with (self.rundir / 'CONTROL/handover-events.log').open('a') as f:
                f.write('%s\tpause-requested\n' % stamp())
        if not self.state.get('active_turn_id'):
            return {'pause': 'Already idle. The pause request waits in .pause for the next turn.',
                    'new_turn_started': False}
        how = ('close the leg with `bash tools/done.sh %s --pause`, then stop.' % self.state['label'].split('.')[0]
               if self.leg() else 'then stop.')
        self.queue('The principal investigator asks you to pause at your next safe stop: log where to pick up, ' + how,
                   kind='pause')
        self.save()
        return {'pause': 'Requested. The analyst stops at its next safe stop.', 'new_turn_started': False}

    # ---- saving and closing: two operations ----------------------------------------------------
    def checkpoint(self, interrupt=False):
        """Save the analyst's folder and the session, verified, in the store. Never a close: the leg is not
        marked closed or verified, and close.sh does not run."""
        if interrupt:
            self.interrupt()
        self.open()
        runlock = None
        try:
            with self.guard:
                if self.state.get('active_turn_id'):
                    raise Error('Turn active; pause or stop it before saving')
                if not self.state.get('last_turn_id'):
                    raise Error('No turn to save')
                if group_alive(self.state.get('last_pid')):
                    raise Error('A process the turn started is still running; let it settle before saving')
                if self.leg():
                    # an old leg never saves a folder the run has since moved on with (OpenAI recheck, blocker 1),
                    # checked under the run's lock so no step.sh slips between
                    runlock = self.lock_run(0)
                    if runlock is None:
                        raise Error('A handler operation or another launch holds this run; nothing saved')
                    self.current()
                    self.finalize_pending()
                g = harness(self.rundir)
                sid = self.state['session_id']
                tpath = self.transcript(sid)
                if not tpath.exists():
                    raise Error('No transcript for session %s' % sid)
                expected = sha(tpath)
                cc = self.rundir / 'CONTROL/.cc'
                keep = ('projects', 'projects/' + self.project)
                dest = self.base / 'captures' / ('%s-%s' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()),
                                                            self.state['last_turn_id'][:8]))
                tmp = dest.with_name('.tmp-' + dest.name)
                tmp.mkdir(parents=True)
                try:
                    fs = g.inventory(self.ag)
                    g.save_manifest(tmp / 'fs.sha256', fs)
                    g.archive(self.ag, tmp / 'fs.tar.gz', '00_GIVE-THE-AGENT', fs)
                    g.verify_archive(tmp / 'fs.tar.gz', '00_GIVE-THE-AGENT', tmp / 'fs.sha256')
                    native = {k: v for k, v in g.inventory(cc, True).items()
                              if k in keep or k.startswith('projects/%s/' % self.project)}
                    g.save_manifest(tmp / 'agent-files.sha256', native)
                    g.archive(cc, tmp / 'agent.tar.gz', '.cc', native)
                    g.verify_archive(tmp / 'agent.tar.gz', '.cc', tmp / 'agent-files.sha256')
                    data = tpath.read_bytes()
                    if hashlib.sha256(data).hexdigest() != expected:
                        raise Error('the transcript changed while saving')
                    atomic(tmp / 'transcript.jsonl', data)
                    if g.inventory(self.ag) != fs:
                        raise Error('a writer changed the folder while saving; nothing saved')
                    ck = {'subject': 'aggregator', 'backend': 'claude', 'format': FORMAT, 'kind': 'capture',
                          'actor': self.state['id'], 'role': self.state.get('role'), 'label': self.state['label'],
                          'claude_run': str(self.rundir),
                          'session': {'session_id': sid, 'transcript_sha256': expected, 'project': self.project},
                          'last_turn': self.state['last_turn_id'], 'boundary': self.state.get('boundary'), 'utc': now()}
                    write(tmp / 'checkpoint.json', ck)
                    digests = {n: sha(tmp / n) for n in ('fs.tar.gz', 'fs.sha256', 'agent.tar.gz', 'agent-files.sha256',
                                                         'transcript.jsonl', 'checkpoint.json')}
                    write(tmp / 'DIGESTS.json', digests)
                    verify_saved(g, tmp)
                    os.replace(tmp, dest)
                except BaseException:
                    shutil.rmtree(tmp, ignore_errors=True)
                    raise
                receipt = {'backend': 'claude', 'format': FORMAT, 'kind': 'capture', 'actor': self.state['id'],
                           'session': sid, 'last_turn': self.state['last_turn_id'], 'boundary': self.state.get('boundary'),
                           'archive': str(dest), 'digests': digests, 'verified': True, 'utc': now()}
                self.state.setdefault('captures', []).append({'archive': str(dest), 'utc': receipt['utc'],
                                                              'last_turn': receipt['last_turn']})
                self.state['last_capture'] = receipt
                if self.state.get('status') in ('idle', 'interrupted', 'failed'):
                    self.state['saved'] = True
                self.save()
                self.note('saved-' + dest.name, 'Folder and session saved', 'Verified: %s' % dest.name)
                return receipt
        finally:
            if runlock:
                unlock(runlock)
            self.release()

    def close_receipt(self, d, forced, log, published):
        """A committed close.sh snapshot, verified whole, or an Error: every file named in MANIFEST.sha256
        and nothing beside it, the files a close must hold, COMMITTED bound to checkpoint.json, the leg's
        label, kind and session, both archives entry by entry and the transcript at the recorded boundary
        (the harness's verify_checkpoint). `scientific` is the harness's own rule for advancing a run
        (protocol_guard advance): committed, not forced or paused, validation complete."""
        d = Path(d)
        g = harness(self.rundir)
        if not (d / 'COMMITTED').is_file():
            raise Error('No committed snapshot at %s' % d)
        committed = (d / 'COMMITTED').read_text().strip()
        manifest = d / 'MANIFEST.sha256'
        if not manifest.is_file():
            raise Error('The snapshot %s has no MANIFEST.sha256' % d)
        digests = {}
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            parts = line.split(None, 1)
            name = parts[1].strip().lstrip('*') if len(parts) == 2 else ''
            if not name or name.startswith('/') or '..' in Path(name).parts or name in digests:
                raise Error('An unreadable, unsafe or repeated line in %s: %r' % (manifest, line))
            digests[name] = parts[0]
        present = set()
        for q in d.rglob('*'):
            if q.is_symlink():
                raise Error('A link in the snapshot: %s' % q.relative_to(d))
            if q.is_file():
                present.add(q.relative_to(d).as_posix())
        present -= {'MANIFEST.sha256', 'COMMITTED'}
        if present != set(digests):
            raise Error('MANIFEST.sha256 does not cover the snapshot exactly (unlisted: %s; listed and absent: %s)'
                        % (sorted(present - set(digests)) or 'none', sorted(set(digests) - present) or 'none'))
        missing = CLOSE_FILES - set(digests)
        if missing:
            raise Error('The snapshot lacks %s' % ', '.join(sorted(missing)))
        for name, value in digests.items():
            if sha(d / name) != value:
                raise Error('Snapshot file %s differs from its manifest' % name)
        ck = read(d / 'checkpoint.json') or {}
        if not committed or ck.get('checkpoint_id') != committed:
            raise Error('COMMITTED does not name the checkpoint in checkpoint.json')
        if ck.get('label') != self.state['label'] or ck.get('kind') != 'agent-and-files':
            raise Error('The snapshot is %s (%s), not the leg %s with its agent' % (ck.get('label'), ck.get('kind'),
                                                                                  self.state['label']))
        if (ck.get('session') or {}).get('session_id') != self.state.get('session_id'):
            raise Error('The snapshot holds session %s, not the leg\'s %s' % ((ck.get('session') or {}).get('session_id'),
                                                                          self.state.get('session_id')))
        try:
            g.verify_checkpoint(d)
        except (ValueError, KeyError, OSError, tarfile.TarError) as e:
            raise Error('The snapshot does not verify: %s' % e) from e
        advance = getattr(g, 'advance', None)
        if advance is not None:
            scientific = bool(advance(self.rundir, self.state['label']))
        else:
            scientific = (not ck.get('forced')) and (ck.get('validation') or {}).get('complete') is True
        cut = saved_cut(d, self.state['label'])   # from the snapshot, not the live folder (OpenAI review, finding 8)
        return {'backend': 'claude', 'format': FORMAT, 'kind': 'close', 'actor': self.state['id'],
                'label': self.state['label'], 'checkpoint_id': committed,
                'snapshot': str(d.relative_to(self.rundir)) if self.rundir in d.parents else str(d),
                'session': self.state.get('session_id'), 'last_turn': self.state.get('last_turn_id'),
                'digests': digests, 'verified': True, 'scientific': scientific, 'cut': cut,
                'forced': bool(forced) or bool(ck.get('forced')), 'log': log, 'publication': published, 'utc': now()}

    def close(self, force=False):
        """The scientific close, once: the run's close.sh (confirm, recall probe, trusted check, model audit,
        snapshot). It advances only on a committed, verified snapshot. Git publication is its own receipt."""
        if not self.leg():
            raise Error('An interview is never closed as a leg; save it with checkpoint()')
        self.open()
        try:
            with self.guard:
                if self.state.get('active_turn_id') or (self.proc and self.proc.poll() is None):
                    raise Error('Turn active; pause or stop it before the close')
                label = self.state['label']
                d = self.rundir / 'CONTROL/snapshots' / label
                done = self.state.get('close_receipt')
                if done:
                    # a repeat is verified again from the files, never answered from the record alone
                    fresh = self.close_receipt(d, done.get('forced'), done.get('log'), done.get('publication'))
                    if fresh['checkpoint_id'] != done['checkpoint_id'] or fresh['digests'] != done['digests']:
                        raise Error('The recorded close no longer matches %s; inspect before anything else' % d)
                    return dict(done, repeated=True)
                if (d / 'COMMITTED').exists():
                    receipt = self.close_receipt(d, None, None, {'status': 'closed outside the adapter', 'lines': []})
                else:
                    if not self.state.get('last_turn_id'):
                        raise Error('No turn to close')
                    if self.state.get('pending_finalize'):
                        held = self.lock_run(0)
                        if held is None:
                            raise Error('The last turn\'s run files wait for the run\'s lock, which another owner '
                                        'holds; nothing closed. Try again when it is free.')
                        try:
                            self.current()
                            self.finalize_pending()
                        finally:
                            unlock(held)
                    if self.state.get('boundary') != 'completed' and not force:
                        raise Error('The last turn ended %s. Close with force, recorded as forced, or start another '
                                    'turn first.' % self.state.get('boundary'))
                    if group_alive(self.state.get('last_pid')):
                        raise Error('A process the turn started is still running; let it settle before the close')
                    self.current()   # an old leg never closes a folder the run has since moved on with
                    nn, leg = label.split('.', 1)
                    args = [nn, leg] + (['--force'] if force else [])
                    log = self.base / 'closes' / ('%s-%s.log' % (label, time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())))
                    log.parent.mkdir(parents=True, exist_ok=True)
                    self.state['close_started'] = now()
                    self.save()
                    with log.open('w') as out:
                        rc = subprocess.call(['bash', str(self.rundir / 'CONTROL/harness/close.sh')] + args,
                                             cwd=str(self.rundir), env=clean_env(), stdout=out, stderr=subprocess.STDOUT,
                                             timeout=7200, start_new_session=True)
                    text = log.read_text(errors='replace')
                    self.emit('item/completed', threadId=self.state.get('thread_id'), turnId=None,
                              item={'type': 'commandExecution', 'id': 'close-' + log.stem,
                                    'command': 'close.sh ' + ' '.join(args), 'status': 'completed' if rc == 0 else 'failed',
                                    'aggregatedOutput': stream.clip(text)})
                    if rc:
                        self.state.update(error='close.sh %s exited %d; see the close row' % (' '.join(args), rc))
                        self.save()
                        raise Error('close.sh exited %d: %s' % (rc, tail(text, 600)))
                    receipt = self.close_receipt(d, bool(force), str(log), publication(text))
                # close_receipt raised unless the snapshot verified whole: only now is the leg closed
                self.state.update(closed=True, status='closed', error=None, close_receipt=receipt, checkpoint=label,
                                  scientific=receipt['scientific'])
                self.save()
                return receipt
        finally:
            self.release()

    def final(self):
        turn = self.state.get('last_turn_id')
        r = read(self.base / 'turns' / turn / 'result.json') if turn else None
        if not r:
            raise Error((self.state.get('error') and str(self.state['error'])) or 'No finished turn')
        return r.get('result') or ''


def load(actor):
    return ClaudeActor(actor)


def close(run, actor, force=False):
    """ADAPTERS.md's close(run, actor): the run's own close, once."""
    a = ClaudeActor(actor)
    if Path(run).resolve() != Path(a.state['claude_run']).resolve():
        raise Error('Actor %s belongs to another run' % actor)
    return a.close(force)


def create(actor, run, leg, role='aggregator', study_run=None, executable=None, api_ok=False, prepare=True, data=None):
    """Prepare one idle leg with the run's own step.sh --prepare, then make the actor's store. No inference."""
    run = Path(run).resolve()
    base = (Path(data) if data else data_dir()) / 'actors' / identity(actor)
    if base.exists():
        raise Error('Actor already exists')
    g = harness(run)
    c = run / 'CONTROL'
    if prepare:
        r = subprocess.run(['bash', str(c / 'harness/step.sh'), leg, '--prepare'], cwd=str(run), env=clean_env(),
                           capture_output=True, text=True, timeout=900, start_new_session=True, check=False)
        if r.returncode:
            raise Error('step.sh %s --prepare refused: %s' % (leg, tail(r.stderr or r.stdout, 600)))
    p = read(c / 'pending_launch.json')
    if not p or not p.get('requested_session_id'):
        raise Error('No prepared launch in CONTROL/pending_launch.json')
    label = p['label']
    if label.split('.', 1)[-1] != leg and label != leg:
        raise Error('The prepared launch is %s, not %s' % (label, leg))
    model, ent = g.arm_for(run, label)
    exe = executable or os.environ.get('RPLACE_CLAUDE_BIN') or shutil.which('claude')
    if not exe:
        raise Error('claude is not on PATH')
    found = features(exe)
    first = (c / 'next_prompt.txt').read_text() if (c / 'next_prompt.txt').exists() else ''
    base.mkdir(parents=True)
    try:
        (base / 'inbox' / 'delivered').mkdir(parents=True)
        atomic(base / 'first-message.txt', first)
        state = {'id': actor, 'backend': 'claude', 'format': FORMAT, 'role': role, 'run': study_run,
                 'claude_run': str(run), 'workspace': str(run / '00_GIVE-THE-AGENT'), 'project': 'run',
                 'leg': leg, 'label': label, 'model': model, 'effort': ent.get('effort'), 'status': 'prepared',
                 'thread_id': p['requested_session_id'], 'session_id': p['requested_session_id'],
                 'mode': p.get('mode'), 'parent_session': p.get('parent_session'), 'launch_id': p.get('launch_id'),
                 'pending': p, 'confirmed': False, 'active_turn_id': None, 'last_turn_id': None, 'boundary': None,
                 'created_utc': now(), 'questions': [], 'open_asks': [], 'undelivered': [], 'instructions': '',
                 'read_only': False, 'api_ok': bool(api_ok),
                 'provenance': {'session_id': p['requested_session_id'], 'mode': p.get('mode'),
                                'parent_session': p.get('parent_session'), 'launch_id': p.get('launch_id')},
                 'runtime': {'format': FORMAT, 'executable': exe, 'version': found['version'], 'flags': found['flags'],
                             'adapter_sha256': sha(Path(__file__))}}
        write(base / 'state.json', state)
    except BaseException:
        shutil.rmtree(base)
        raise
    return state


def restore(checkpoint, new_actor, mode='interview', executable=None, data=None):
    """An independent interview in its own copy of a saved folder: an adapter capture (a receipt or its
    folder) or a committed close.sh snapshot (its folder). The saved folder is read, never changed. A
    Claude run continues its analysis only through its next leg, so mode 'continuation' is refused before
    anything is written."""
    if mode != 'interview':
        raise Error('Refused: a Claude run continues its analysis only through its next leg (step.sh, then '
                    'create()), never from a copy. Nothing was written.')
    identity(new_actor)
    base = (Path(data) if data else data_dir()) / 'actors' / new_actor
    if base.exists():
        raise Error('Actor already exists')
    d = Path(checkpoint['archive'] if isinstance(checkpoint, dict) else checkpoint).resolve()
    if d.parent.name == 'snapshots' and d.parent.parent.name == 'CONTROL':
        run = d.parents[2]
        if not (d / 'COMMITTED').exists():
            raise Error('%s is not committed' % d)
    else:
        ck0 = read(d / 'checkpoint.json') or {}
        if not ck0.get('claude_run'):
            raise Error('%s names no run' % d)
        run = Path(ck0['claude_run'])
    g = harness(run)
    ck = verify_saved(g, d)
    if not (d / 'agent.tar.gz').exists():
        raise Error('%s was saved files-only: it holds no session to interview' % d)
    s = ck['session']
    project = s.get('project', 'run')
    label = ck.get('label') or d.name
    model, ent = g.arm_for(run, label)
    exe = executable or os.environ.get('RPLACE_CLAUDE_BIN') or shutil.which('claude')
    if not exe:
        raise Error('claude is not on PATH')
    fork = str(uuid.uuid4())
    ws = run / 'interview-workspaces' / ('%s__%s' % (label, fork))
    proj = run / 'CONTROL/.cc/projects' / ('iv-' + fork)
    if ws.exists() or proj.exists():
        raise Error('The interview folder exists already')
    ws.mkdir(parents=True)

    def extract(tar, dest):
        with tarfile.open(tar) as t:
            try:
                t.extractall(dest, filter='fully_trusted')   # verified member by member above
            except TypeError:
                t.extractall(dest)
    extract(d / 'fs.tar.gz', ws)
    agd = ws / '00_GIVE-THE-AGENT'
    if g.inventory(agd) != g.load_manifest(d / 'fs.sha256'):
        raise Error('The restored folder differs from its manifest')
    tmp = ws / '.sessions-restore'
    extract(d / 'agent.tar.gz', tmp)
    shutil.copytree(tmp / '.cc/projects' / project, proj)
    shutil.rmtree(tmp)
    if sha(proj / (s['session_id'] + '.jsonl')) != s['transcript_sha256']:
        raise Error('The restored session is not the saved boundary')
    g.settings(run, g.stage_of(label), ag=agd, hooks=False)
    with (run / 'CONTROL/interviews.tsv').open('a') as f:
        f.write('%s\t%s\t%s\t%s\n' % (stamp(), label, s['session_id'], fork))
    found = features(exe)
    base.mkdir(parents=True)
    try:
        (base / 'inbox' / 'delivered').mkdir(parents=True)
        state = {'id': new_actor, 'backend': 'claude', 'format': FORMAT, 'role': 'interview', 'run': None,
                 'claude_run': str(run), 'workspace': str(agd), 'project': 'iv-' + fork, 'leg': label.split('.', 1)[-1],
                 'label': label, 'model': model, 'effort': ent.get('effort'), 'status': 'prepared',
                 'thread_id': fork, 'session_id': fork, 'mode': 'fork', 'parent_session': s['session_id'],
                 'parent_checkpoint': str(d), 'confirmed': True, 'active_turn_id': None, 'last_turn_id': None,
                 'boundary': None, 'created_utc': now(), 'questions': [], 'open_asks': [], 'undelivered': [],
                 'instructions': '', 'read_only': False,
                 'provenance': {'session_id': fork, 'mode': 'fork', 'parent_session': s['session_id'],
                                'parent_checkpoint': str(d), 'parent_digests': read(d / 'DIGESTS.json')},
                 'runtime': {'format': FORMAT, 'executable': exe, 'version': found['version'], 'flags': found['flags'],
                             'adapter_sha256': sha(Path(__file__))}}
        write(base / 'state.json', state)
    except BaseException:
        shutil.rmtree(base)
        raise
    return state
