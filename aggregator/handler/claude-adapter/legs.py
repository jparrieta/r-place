#!/usr/bin/env python3
"""legs.py: the Claude leg handler. No website: a handler you use from Claude Code or Cowork.

One process on the Mac, `legs.py serve`, starts and follows the analyst's sessions. It uses the adapter
(actor.py) and the run's own harness: step.sh prepares a leg, one headless turn runs it, close.sh closes
it. Every other command is a client. A client drops a request file into the run's CONTROL/legs/requests/
and reads the answer in CONTROL/legs/results/. So the same commands work in Terminal on the Mac, in
Claude Code on the Mac or through Remote Control from the phone, and in Cowork, whose shell reaches the
folder but cannot start programs on the Mac.

What the handler keeps of a run (its sessions' streams, requests and results, the list's state) is in that
run's CONTROL/legs/: the analyst's settings deny it CONTROL, and the repository's .gitignore keeps it out of
git. Your words to legs, and their delivery, go to CONTROL/messages-to-legs.jsonl, which is committed; an
interview's transcript stays in the run's Claude folder until E2a. Beside the repository,
.rplace-claude-legs/ holds only the handler's heartbeat, its lock and its key.

    legs.py serve                                   the handler itself, on the Mac (leave it running)
    legs.py status [RUN]                            what runs, what waits for you
    legs.py legs RUN                                every leg of a run: closed, open, running
    legs.py open RUN LEG [--wait S]                 step.sh, then the leg's first turn
    legs.py close RUN LEG [--force] [--wait S]      close.sh, once
    legs.py run RUN LEGS... [--through-interviews]  several legs in order; stops at every gate
    legs.py stop RUN [--now]                        stop the list after this leg (--now: interrupt the turn)
    legs.py pause RUN                               the running leg pauses at its next safe stop
    legs.py say RUN LEG TEXT [--wait S]             talk to a leg (TEXT "-" reads standard input)
    legs.py interview RUN LEG TEXT [--new]          open (or go on with) an interview of a closed leg
    legs.py reply RUN LEG [--interview]             the leg's last reply, or its interview's
    legs.py watch RUN [LEG] [-n N] [-f] [--full]    what the analyst does: -f live, leg after leg; --full whole
    legs.py answer RUN QID TEXT                     answer a question the analyst asked (mem.py ask)
    legs.py wait RUN [--timeout S]                  return when the run needs you
    legs.py chat RUN [--full]                       one window to talk to every agent of the run (Terminal)
    legs.py branch SOURCE CHECKPOINT NEW --leg LEG  an analysis branch from a verified close (branches.py)
    legs.py branch-put NEW PATH --file F [--stage NN]   replace a stage card or add data, while draft
    legs.py branch-status NEW                       the branch's record and publication
    legs.py prepare-branch NEW                      seal, publish the setup to Git, prepare the first leg
    legs.py publish-branch NEW                      publish again after a failed push
    legs.py note RUN TEXT                           a handler's line in that chat

--wait (and wait's --timeout) bounds how long the command waits for an answer; the handler goes on either way.
A shell with a time limit (Cowork's, about three minutes) passes --wait 150 and reads the rest with status,
legs or reply. RUN is a run's folder name under aggregator/runs (claude-v43-1). LEG is a leg id (A1b-02) or a label
(A1.A1b-02). LEGS in `run` are leg ids, ranges (A1b-01..A1b-06), a stage whose repeated steps have a
declared count (A1: A1a, one A1b leg per block declared in out/order-A1.txt, A1c), or A1b-* (the declared
blocks). A leg already closed is skipped, and a leg closed at a pause continues as LEG-p2.

Talking to a leg (`say`; J, 2026-10-05):
- the leg's turn runs: the words reach the analyst beside its next tool result (inbox_hook.py);
- the leg is open and its turn has ended: the words start a new turn in the leg's own session;
- the leg is the last close: its conversation goes on in the next leg, which gets the words (live or in a new
  turn when it is open, else in its first message); words that missed a closing leg's turn go there too;
- an older close is talked to only in an interview.
An interview (`interview`) is you opening a closed leg to talk to it as it was: a fork of its checkpoint in a
copy of its folder, recorded in CONTROL/interviews.tsv, which E2 reads. Nothing said there reaches the run.
Later words continue the leg's latest interview; --new opens another.

A list of legs (`run`) stops, and says why in `status` and `wait`, when: step.sh refuses a leg; a turn
fails or is interrupted; the analyst ends its turn without closing the leg; close.sh refuses; a leg closes
at a pause, at its packets (the dispatch is yours, in Terminal), or at an interview point (unless
--through-interviews); a close cannot advance the run; a stage finishes before the listed legs run out;
you stop it; the list ends. A question the analyst asks does not stop it: you are told, and you answer.

An analysis branch (`branch`) is a new run, aggregator/runs/<SOURCE>--<name>/, from one verified close of
SOURCE, made and published as the Codex controller makes its branches (branches.py). Its first leg is the
one after that close. While it is a draft, `branch-put` replaces a stage card or adds data. `prepare-branch`
seals it and commits the setup to the Git branch analysis/<run>; every close after that is committed there
too, and main never holds the branch.
"""
import argparse
import contextlib
import hashlib
import hmac
import importlib.util
import json
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]          # aggregator/handler/claude-adapter -> the repository
_spec = importlib.util.spec_from_file_location('claude_legs_actor', HERE / 'actor.py')
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
sys.modules['claude_legs_actor'] = A   # branches.py uses this copy, so both raise the same Error
_bspec = importlib.util.spec_from_file_location('claude_legs_branches', HERE / 'branches.py')
B = importlib.util.module_from_spec(_bspec)
_bspec.loader.exec_module(B)
Error = A.Error
BEAT = 5          # seconds between the handler's heartbeats
STALE = 60        # a heartbeat older than this: the handler is not running
SERVE_HINT = ('The handler is not running on the Mac. Start it there, in Terminal, in the repository folder:\n'
              '  python3 aggregator/handler/claude-adapter/legs.py serve')


# ---- where things are ----------------------------------------------------------------------------
def home():
    """The handler's own folder, beside the repository: its heartbeat, lock and key, nothing of a run."""
    v = os.environ.get('RPLACE_LEGS_DATA')   # the tests only
    return Path(v) if v else REPO.parent / '.rplace-claude-legs'


def runs_dir():
    v = os.environ.get('RPLACE_LEGS_RUNS')   # the tests only
    return Path(v) if v else REPO / 'aggregator/runs'


def sign(key, body):
    """The request's signature: HMAC-SHA256 of its canonical JSON under the handler's key. The key never travels."""
    return hmac.new(key.encode(), json.dumps(body, sort_keys=True, ensure_ascii=False).encode(), hashlib.sha256).hexdigest()


def next_pause(leg):
    """The leg that continues a leg closed at a pause, as close.sh names it: A1b-03-p2, then -p3."""
    m = re.match(r'^(.*)-p(\d+)$', leg)
    return '%s-p%d' % (m.group(1), int(m.group(2)) + 1) if m else leg + '-p2'


def events_of(path, start=0):
    """The whole JSON lines of an events.jsonl from byte `start`: (rows, the byte after the last whole line).
    A line that does not parse (a write cut short) is skipped, never repeated."""
    if not path.exists() or path.stat().st_size <= start:
        return [], start
    with path.open('rb') as f:
        f.seek(start)
        chunk = f.read()
    done = chunk.rfind(b'\n') + 1
    rows = []
    for r in chunk[:done].decode('utf-8', 'replace').splitlines():
        try:
            row = json.loads(r) if r.strip() else None
        except ValueError:
            row = None
        if isinstance(row, dict):
            rows.append(row)
    return rows, start + done


def run_path(name):
    A.identity(name)
    p = (runs_dir() / name).resolve()
    if not (p / 'CONTROL/harness/protocol_guard.py').is_file():
        raise Error('No Claude run named %s under aggregator/runs' % name)
    return p


def rdir(name):
    """What the handler keeps of one run: CONTROL/legs/, denied to the analyst and kept out of git."""
    return run_path(name) / 'CONTROL/legs'


def handled_runs():
    """The runs the handler has records of."""
    d = runs_dir()
    return sorted(p.name for p in d.glob('*') if (p / 'CONTROL/legs').is_dir()) if d.is_dir() else []


_steps = {}


def steps(run):
    """The run's own steps.py (CONTROL/harness, beside its steps.tsv), else the instrument's."""
    p = run / 'CONTROL/harness/steps.py'
    if not p.is_file():
        p = REPO / 'aggregator/instrument/tools/steps.py'
    key = str(p)
    if key not in _steps:
        spec = importlib.util.spec_from_file_location('claude_legs_steps_%d' % len(_steps), p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _steps[key] = mod
    return _steps[key]


def leg_of(run, x):
    """(stage, leg, label) for a leg id or a label; ValueError if the instrument has no such leg."""
    x = (x or '').strip()
    leg = x.split('.', 1)[1] if '.' in x else x
    d = steps(run).parse(leg)
    if '.' in x and x.split('.', 1)[0].upper() != d['stage']:
        raise ValueError('%s: the leg belongs to stage %s' % (x, d['stage']))
    return d['stage'], leg, '%s.%s' % (d['stage'], leg)


def committed(run, label):
    return (run / 'CONTROL/snapshots' / label / 'COMMITTED').is_file()


def cut_of(run, nn, leg):
    """The cut the analyst closed the leg at (done.sh's marker), or None if it did not close it."""
    m = run / '00_GIVE-THE-AGENT/out/_closes' / ('%s-%s.closed' % (nn, leg))
    if not m.is_file():
        return None
    rows = [r.split() for r in m.read_text().splitlines() if r.strip()]
    return rows[-1][1] if rows and len(rows[-1]) > 1 else 'close'


def finished(run, nn, label):
    p = run / 'CONTROL/stage-state' / nn / 'FINISHED'
    return p.is_file() and p.read_text().strip().split('\t')[-1] == label


def close_state(run, label):
    """What a committed close allows: 'advances', 'paused' (a pause whose snapshot is whole), or why it cannot be
    built on (OpenAI review 2026-10-05, finding 3)."""
    try:
        d, _ = B.snapshot_ok(run, label)
    except Exception as e:   # a snapshot missing a file or holding bad JSON is a reason too
        return str(e) if isinstance(e, Error) else 'its snapshot does not verify (%r)' % e
    if A.harness(run).advance(run, label):
        return 'advances'
    if A.saved_cut(d, label) == 'pause':
        return 'paused'
    return 'it was forced, or its validation is incomplete'


def pending_leg(run, leg, accept=()):
    """The leg still to run for a leg id: itself, its continuation after a pause (-p2, -p3), or None when its
    close may be built on. A close that cannot (forced, incomplete, or a snapshot that does not verify) stops
    the list, unless you accept it by name."""
    m = re.match(r'^(.*?)(?:-p(\d+))?$', leg)
    base, k, nn = m.group(1), int(m.group(2) or 1), leg[:2]
    while True:
        cur = base if k == 1 else '%s-p%d' % (base, k)
        label = '%s.%s' % (nn, cur)
        if not committed(run, label):
            return cur
        state = close_state(run, label)
        if state == 'paused':
            k += 1
            continue
        if state == 'advances' or label in accept:
            return None
        raise Error('%s is closed, but the run cannot go on from it: %s. Read its validation report in the snapshot; '
                    'to go on from it anyway, run the list again with --accept %s' % (label, state, label))


def declared_blocks(run):
    """The A1 blocks in out/order-A1.txt, in order of appearance (mem.py's reading of the file)."""
    p = run / '00_GIVE-THE-AGENT/out/order-A1.txt'
    blocks = []
    if p.is_file():
        for line in p.read_text(encoding='utf-8').splitlines():
            f = line.strip().split('\t') if '\t' in line else line.split()
            if len(f) > 1 and not f[0].startswith('#') and f[0] not in blocks:
                blocks.append(f[0])
    return blocks


def asks_open(run):
    ag = run / '00_GIVE-THE-AGENT/out'
    rows = []
    if (ag / 'asks.jsonl').is_file():
        for line in (ag / 'asks.jsonl').read_text(encoding='utf-8').splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if isinstance(r, dict) and r.get('id') and not (ag / '_answers' / ('%s.md' % r['id'])).exists():
                rows.append(r)
    return rows


# ---- the handler's records -----------------------------------------------------------------------
_reg_lock = threading.Lock()


def registry(name):
    return A.read(rdir(name) / 'legs.json', {}) or {}


def register(name, label, **fields):
    with _reg_lock:
        r = registry(name)
        e = r.setdefault(label, {})
        for k, v in fields.items():
            if k == 'interview':
                e.setdefault('interviews', []).append(v)
            else:
                e[k] = v
        A.write(rdir(name) / 'legs.json', r)


def log(name, text):
    rdir(name).mkdir(parents=True, exist_ok=True)
    with (rdir(name) / 'events.log').open('a', encoding='utf-8') as f:
        f.write('%s  %s\n' % (A.stamp(), text.replace('\n', ' ')))


_said_lock = threading.Lock()


def said(name, **row):
    """One line of CONTROL/messages-to-legs.jsonl: your words to a leg (running, open, or for the next leg), then
    their delivery. It sits beside sessions.json, outside CONTROL/legs/, so publish.sh commits it at every close; the
    analyst's settings deny it CONTROL. Interviews are not written here: CONTROL/interviews.tsv lists them."""
    with _said_lock:
        with (run_path(name) / 'CONTROL/messages-to-legs.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(dict({'utc': A.now()}, **row), ensure_ascii=False) + '\n')


LIMIT = 8000   # one message's characters in the analyst's context (inbox_hook.py); a longer one goes in parts


def last_close(run):
    """The run's last close (CONTROL/snapshots/INDEX.tsv), or None."""
    p = run / 'CONTROL/snapshots/INDEX.tsv'
    rows = [r.split('\t')[0] for r in p.read_text().splitlines()[1:] if r.strip()] if p.exists() else []
    return rows[-1] if rows else None


def wait_next(name, after, text, origin=None):
    """Your words for the next leg's first message, written after the close of `after`: the next leg carries on
    that conversation (J, 2026-10-05). Kept in CONTROL/legs/next-leg/ until a leg's first turn takes them."""
    q = rdir(name) / 'next-leg'
    q.mkdir(parents=True, exist_ok=True)
    mid = 'next-%s-%020d-%s' % (time.strftime('%Y%m%dT%H%M%S', time.gmtime()), time.time_ns(), uuid.uuid4().hex[:6])
    A.write(q / (mid + '.json'), {'id': mid, 'after': after, 'text': text, 'origin': origin, 'utc': A.now()})
    return mid


def waiting_next(name):
    q = rdir(name) / 'next-leg'
    return [m for m in (A.read(p) for p in sorted(q.glob('*.json'))) if isinstance(m, dict)] if q.is_dir() else []


def hold(name, words, a):
    """Words for the next leg, now in leg a's prompt: out of the queue, marked with the actor that holds them."""
    taken = rdir(name) / 'next-leg/taken'
    taken.mkdir(parents=True, exist_ok=True)
    for m in words:
        A.write(taken / (m['id'] + '.json'), dict(m, held_in=a.state['id']))
        (rdir(name) / 'next-leg' / (m['id'] + '.json')).unlink(missing_ok=True)


def delivered(name, a, turn):
    """Once a leg's first turn runs: a delivery row for each of your words its prompt carried."""
    taken = rdir(name) / 'next-leg/taken'
    rows = [m for m in (A.read(p) for p in sorted(taken.glob('*.json'))) if isinstance(m, dict)] if taken.is_dir() else []
    mine = [m for m in rows if m.get('held_in') == a.state['id'] and not m.get('delivered')]
    for m in mine:
        said(name, kind='delivered', id=m['id'], label=a.state['label'], via='first message', turn=turn)
        A.write(taken / (m['id'] + '.json'), dict(m, delivered=A.now()))
    if mine:
        log(name, '%s: its first message carries %d message(s) of yours written after %s'
            % (a.state['label'], len(mine), mine[-1].get('after')))


def checked(text):
    text = (text or '').strip()
    if not text:
        raise Error('Nothing to say')
    if len(text) > LIMIT:
        raise Error('%d characters: the analyst takes %d in one message. Send it in parts.' % (len(text), LIMIT))
    return text


def notify(text):
    """A notification on the Mac's screen; nothing elsewhere."""
    if sys.platform == 'darwin' and shutil.which('osascript'):
        try:
            subprocess.run(['osascript', '-e', 'display notification %s with title "r/place legs"' % json.dumps(text[:200])],
                           capture_output=True, timeout=10)
        except Exception:
            pass


def github(name, label, status):
    """A close that did not reach GitHub needs you; the commit, if there is one, goes up with the next push."""
    if status != 'pushed':
        how = ('legs.py publish-branch %s (it pushes analysis/%s; main is not involved)' % (name, name)
               if B.branch_of(run_path(name)) else 'commit and push the repository (git push)')
        needs(name, label, 'not on GitHub', 'close.sh\'s publication: %s' % status,
              'The checkpoint is safe on the Mac. To put it on GitHub: %s.' % how)


_needs_lock = threading.Lock()


def needs(name, label, kind, why, todo):
    """Something for you: written where `status` and `wait` read it, logged, and shown on the Mac. needs-you.json
    holds the latest; needs-you.jsonl every one, in order, so `wait` shows each one once (v43.2)."""
    row = {'utc': A.now(), 'run': name, 'leg': label, 'kind': kind, 'why': why, 'todo': todo}
    with _needs_lock:
        A.write(rdir(name) / 'needs-you.json', row)
        with (rdir(name) / 'needs-you.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    log(name, 'NEEDS YOU (%s) %s: %s | %s' % (kind, label or '-', why, todo))
    notify('%s %s: %s' % (name, label or '', why))


# ---- the list of legs ----------------------------------------------------------------------------
class Planner:
    """The legs of a `run` request, named as late as they can be: A1's blocks only once A1a declared them."""
    def __init__(self, run, tokens, accept=()):
        self.run, self.st, self.accept = run, steps(run), tuple(accept)
        self.rows = self.st.table()
        self.items, self.skipped, self.ahead = [], [], None
        for t in tokens:
            self.items.extend(self.parse(t))
        if not self.items:
            raise Error('Name the legs to run')

    def parse(self, t):
        t = t.strip()
        stages = self.st.stages(self.rows)
        if t.upper() in stages:
            nn, out = t.upper(), []
            for r in self.rows:
                if r['stage'] != nn:
                    continue
                if r['repeat'] == 'no':
                    out.append(nn + r['step'])
                elif (nn, r['step']) == ('A1', 'b'):
                    out.append(('declared', 'A1', 'b'))
                else:
                    raise Error('Stage %s repeats step %s%s, and nothing declares how often: give its legs as a range, '
                                'for example %s%s-01..%s%s-04' % (nn, nn, r['step'], nn, r['step'], nn, r['step']))
            return out
        if t.endswith('-*'):
            if t[:-2] != 'A1b':
                raise Error('%s: only A1b has its legs declared (out/order-A1.txt); give a range' % t)
            return [('declared', 'A1', 'b')]
        if '..' in t:
            a, b = (self.st.parse(x) for x in t.split('..', 1))
            if (a['stage'], a['step']) != (b['stage'], b['step']) or not (a['count'] or '').isdigit() \
                    or not (b['count'] or '').isdigit() or a['cont'] or b['cont'] or int(a['count']) > int(b['count']):
                raise Error('%s: a range is one repeated step, counted upward, for example A1b-01..A1b-06' % t)
            return ['%s%s-%02d' % (a['stage'], a['step'], n) for n in range(int(a['count']), int(b['count']) + 1)]
        self.st.parse(t)
        return [t]

    def _next(self):
        while self.items:
            x = self.items.pop(0)
            if isinstance(x, tuple):
                blocks = declared_blocks(self.run)
                if not blocks:
                    raise Error('A1b: no blocks are declared in out/order-A1.txt yet (leg A1a declares them)')
                self.items[0:0] = ['A1b-%02d' % (i + 1) for i in range(len(blocks))]
                continue
            leg = pending_leg(self.run, x, self.accept)
            if leg is None:
                self.skipped.append(x)
                continue
            return leg
        return None

    def next(self):
        if self.ahead is not None:
            x, self.ahead = self.ahead[0], None
            return x
        return self._next()

    def peek(self):
        if self.ahead is None:
            self.ahead = (self._next(),)
        return self.ahead[0]

    def preview(self):
        out = []
        for x in self.items:
            out.append('A1b, one leg per declared block' if isinstance(x, tuple) else x)
        return out


# ---- the handler process -------------------------------------------------------------------------
class Server:
    def __init__(self, key):
        self.h, self.key = home(), key
        self.cache, self.locks, self.jobs = {}, {}, {}
        self.guard = threading.RLock()
        self.stopping = threading.Event()

    def actor(self, name, aid):
        with self.guard:
            if (name, aid) not in self.cache:
                self.cache[(name, aid)] = A.ClaudeActor(aid, data=rdir(name))
            return self.cache[(name, aid)]

    def lock(self, name):
        with self.guard:
            return self.locks.setdefault(name, threading.RLock())

    @contextlib.contextmanager
    def held(self, name, req):
        """The run's lock for a request: waited for only until the client stops waiting, so a request never acts
        after its client has given up."""
        lock = self.lock(name)
        if not lock.acquire(timeout=max(0.0, req['_deadline'] - time.monotonic())):
            raise Error('The run is busy: a list is preparing or closing a leg. Nothing was done; try again shortly.')
        if time.monotonic() > req['_deadline']:
            lock.release()
            raise Error('The request\'s time to live ran out before the run was free; nothing was done')
        try:
            yield
        finally:
            lock.release()

    def job(self, name):
        """The run's list, while it runs. A list that has saved its end is over, though its thread may still be
        posting the notice (osascript on the Mac): its state says so before the thread is gone."""
        with self.guard:
            j = self.jobs.get(name)
            return j if j and j['thread'].is_alive() and j['state'].get('status') == 'running' else None

    def no_job(self, name, label=None):
        j = self.job(name)
        if j and (label is None or j['state'].get('current') == label):
            raise Error('A list of legs runs on %s (now at %s). Stop it first: legs.py stop %s'
                        % (name, j['state'].get('current') or 'its start', name))

    def leg_actor(self, name, label):
        return (registry(name).get(label) or {}).get('actor')

    def live(self, name):
        """The leg actors of a run whose turn runs now."""
        out = []
        for label, e in registry(name).items():
            if e.get('actor'):
                a = self.actor(name, e['actor'])
                if a.state.get('active_turn_id'):
                    out.append((label, a))
        return out

    # ---- requests ----
    def handle(self, req, where, age, read_at=None):
        try:
            rid = A.identity(str(req.get('id')))
            results = rdir(where) / 'results'
        except Exception as e:
            print('A request without a usable id or run was dropped: %r' % e)
            return
        try:
            sig = str(req.pop('sig', ''))
            if not secrets.compare_digest(sig, sign(self.key, req)):
                raise Error('The request is not signed with the handler\'s key')
            if req.get('run') != where:
                raise Error('The request names run %s but sits in %s' % (req.get('run'), where))
            ttl = float(req.get('ttl') or 0)
            if age > ttl:
                # aged by the file's own time on this machine's clock: a request that waited while no handler ran
                # is never acted on later, by surprise
                raise Error('The request expired before the handler read it; nothing was done')
            if not 0 < ttl <= 600:   # a NaN fails this too
                raise Error('The request carries an impossible time to live (%r); nothing was done' % req.get('ttl'))
            # fixed when the file was read, not when a worker took it up (OpenAI review 2026-10-05, finding 6)
            req['_deadline'] = (read_at or time.monotonic()) + max(0.0, ttl - age)
            if time.monotonic() > req['_deadline']:
                raise Error('The request waited past its time to live for a free worker; nothing was done')
            fn = getattr(self, 'do_' + str(req.get('cmd')), None)
            if fn is None:
                raise Error('No command %s' % req.get('cmd'))
            out = {'ok': True, 'result': fn(req)}
        except (Error, ValueError) as e:
            out = {'ok': False, 'error': str(e)}
        except Exception as e:
            traceback.print_exc()
            out = {'ok': False, 'error': 'handler error: %r' % e}
        A.write(results / (rid + '.json'), dict(out, cmd=req.get('cmd'), utc=A.now()))

    def run_of(self, req):
        run = run_path(str(req.get('run')))
        return run, run.name

    def do_ping(self, req):
        return {'pid': os.getpid()}

    @staticmethod
    def first_turn(a):
        """The leg's first turn: a branch's notice, the leg's first message, then your words written after the last
        close (J, 2026-10-05). A start that fails inside the turn's launch keeps all of that in the inbox as the leg's
        prompt; a retry sends it once, with words written since. A start refused before that queues nothing, and
        your words stay waiting (CONTROL/legs/next-leg/). Called under the run's lock, so no `say` slips between."""
        name = a.rundir.name
        words = waiting_next(name) if a.state.get('role') == 'aggregator' else []
        texts = ['Message from the principal investigator (%s, written after %s closed):\n%s'
                 % (m.get('utc', ''), m.get('after'), m.get('text', '')) for m in words]
        if a.undelivered():   # a retry: the failed start's prompt waits in the inbox; newer words join it
            for t in texts:
                a.queue(t, kind='prompt')
            a.save()
            hold(name, words, a)
            r = a.continue_queued()
        else:
            notice = B.notice(a.rundir, a.state.get('leg')) if a.state.get('role') == 'aggregator' else ''
            text = '\n\n'.join([notice + (a.base / 'first-message.txt').read_text().rstrip('\n')] + texts)
            try:
                r = a.message(text)
            except BaseException:
                if any(m.get('text') == text for _, m in a.undelivered()):
                    hold(name, words, a)   # queued with the failed start's prompt: they go out with its retry
                raise
            hold(name, words, a)
        delivered(name, a, (r.get('turn') or {}).get('id'))
        return r

    def carry_forward(self, name, label, a):
        """Your words that still waited in the leg when it closed go to the leg that carries on its conversation:
        the next leg's first message (J, 2026-10-05; OpenAI review 2026-10-05, finding 4). Each is written there
        before it is marked carried, so a crash between the two loses nothing."""
        def hand(m):
            mid = wait_next(name, label, m.get('text', ''), origin=m.get('id'))
            said(name, kind='carried', id=m.get('id'), label=label, to='the next leg\'s first message', next_id=mid)
            log(name, 'your words to %s missed its turn: they go into the next leg\'s first message' % label)
        a.carry(hand)

    def new_leg(self, run, leg, label):
        # interviews' folders are made before any leg's settings are rendered, so every leg's settings deny them
        (run / 'interview-workspaces').mkdir(exist_ok=True)
        for line in B.check_leg(run, leg):   # an analysis branch: sealed and published before its first leg
            log(run.name, line.strip())
        aid = 'leg-%s-%s-%s' % (run.name, leg, time.strftime('%Y%m%dT%H%M%S', time.gmtime()))
        A.create(aid, run, leg, data=rdir(run.name))   # the run's step.sh LEG --prepare; no turn yet
        register(run.name, label, actor=aid, opened_utc=A.now())
        log(run.name, 'prepared %s (step.sh), actor %s' % (label, aid))
        return aid

    def do_open(self, req):
        run, name = self.run_of(req)
        _, leg, label = leg_of(run, req.get('leg'))
        with self.held(name, req):
            self.no_job(name)
            if committed(run, label):
                raise Error('%s is closed. Talk to it as it was in an interview: legs.py interview %s %s'
                            % (label, name, leg))
            aid = self.leg_actor(name, label)
            if aid:
                st = self.actor(name, aid).state
                if st.get('closed') or st.get('active_turn_id'):
                    raise Error('%s is %s' % (label, 'closed' if st.get('closed') else 'running'))
                if st.get('last_turn_id'):
                    raise Error('%s is open and its turn has ended. Talk to it with say, or close it.' % label)
            else:
                aid = self.new_leg(run, leg, label)
            r = self.first_turn(self.actor(name, aid))
        log(name, 'opened %s: its first turn runs' % label)
        return {'label': label, 'actor': aid, 'turn': (r.get('turn') or {}).get('id')}

    def summary(self, run, receipt):
        notes = []
        logp = receipt.get('log')
        if logp and Path(logp).is_file():
            for line in Path(logp).read_text(errors='replace').splitlines():
                s = line.strip()
                if s.startswith(('INTERVIEW POINT', 'paused at', 'next ', 'QUESTIONS', 'stage ', 'FORCED', 'model audit')) \
                        or (s.startswith('Q') and ':' in s):
                    notes.append(s)
        return {'label': receipt['label'], 'checkpoint': receipt['checkpoint_id'], 'cut': receipt.get('cut'),
                'advances': receipt.get('scientific'), 'forced': receipt.get('forced'),
                'publication': (receipt.get('publication') or {}).get('status'), 'repeated': bool(receipt.get('repeated')),
                'notes': notes}

    def do_close(self, req):
        run, name = self.run_of(req)
        nn, leg, label = leg_of(run, req.get('leg'))
        force = bool(req.get('force'))
        with self.held(name, req):
            self.no_job(name, label)
            aid = self.leg_actor(name, label)
            if aid:
                a = self.actor(name, aid)
                s = self.summary(run, a.close(force=force))
                self.carry_forward(name, label, a)   # after the close: if it is refused, they wait in the open leg
            else:
                # a leg the handler did not open (a terminal leg): the run's close.sh, as you would type it
                args = ['bash', str(run / 'CONTROL/harness/close.sh'), nn, leg] + (['--force'] if force else [])
                # stderr with stdout: publish.sh reports a failed push on stderr; its own process group: a Ctrl-C to
                # the handler never cuts a close
                r = subprocess.run(args, cwd=str(run), env=A.clean_env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, timeout=7200, start_new_session=True, check=False)
                if r.returncode:
                    raise Error('close.sh %s %s exited %d: %s' % (nn, leg, r.returncode, A.tail(r.stdout, 800)))
                s = {'label': label, 'checkpoint': (run / 'CONTROL/snapshots' / label / 'COMMITTED').read_text().strip(),
                     'cut': A.saved_cut(run / 'CONTROL/snapshots' / label, label), 'publication': A.publication(r.stdout)['status'],
                     'output': A.tail(r.stdout, 1500)}
        log(name, 'closed %s: checkpoint %s, cut %s, git %s' % (label, s['checkpoint'], s.get('cut'), s.get('publication')))
        github(name, label, s.get('publication'))
        return s

    def do_say(self, req):
        """Your words to a leg (J, 2026-10-05). A running leg hears them beside its next tool result; an open leg
        answers in a new turn of its session. A closed leg's conversation goes on in the next leg: the next leg gets
        them, live or in a new turn when it is open, else in its first message. Only the last close is talked to
        this way; an older one, as it was, only in an interview (do_interview)."""
        run, name = self.run_of(req)
        _, leg, label = leg_of(run, req.get('leg'))
        text = checked(req.get('text'))
        # who typed it: 'chat' is J's own window; 'say' is the command, J's or the handler's on J's word (v43.2)
        source = req.get('source') if req.get('source') in ('chat', 'say') else 'say'
        to = label
        if committed(run, label):
            with self.held(name, req):
                last = last_close(run)
                if label != last:
                    raise Error('%s is closed, and the run has moved on since (its last close is %s). To talk to %s as '
                                'it was at its close, open an interview: legs.py interview %s %s' % (label, last, leg, name, leg))
                # the leg after it, if one is prepared or open: the run's current leg, as step.sh last wrote it
                cur = (run / '00_GIVE-THE-AGENT/.leg').read_text().strip() if (run / '00_GIVE-THE-AGENT/.leg').is_file() else None
                after = []
                c = run / 'CONTROL'
                nxt = '%s.%s' % (cur[:2], cur) if cur else None
                # step.sh writes .leg before refusals it can still make: a leg counts as opened only once a launch
                # or a session names it
                opened = nxt and (nxt in (A.read(c / 'sessions.json') or {}) or
                                  nxt in ((A.read(c / 'pending_launch.json') or {}).get('label'),
                                          (A.read(c / 'active_launch.json') or {}).get('label')))
                if opened and cur != label.split('.', 1)[1] and not committed(run, nxt):
                    e = registry(name).get(nxt) or {}
                    if not e.get('actor') or actor_state(name, e['actor']).get('closed'):
                        raise Error('%s was opened by hand in a Terminal: the handler cannot deliver words to it, and '
                                    'words typed there are not recorded apart. Let it finish, close it with legs.py '
                                    'close %s %s, then talk to the next leg.' % (cur, name, cur))
                    after = [nxt]
                if not after or not actor_state(name, registry(name)[after[0]]['actor']).get('turns'):
                    mid = wait_next(name, label, text)
                    nxt = after[0] if after else None
                    said(name, kind='sent', label=label, mode='next-leg', id=mid, to=nxt, source=source, text=text)
                    log(name, 'you to %s (closed; for the next leg\'s first message): %s' % (label, text[:300]))
                    return {'label': label, 'to': nxt, 'actor': None, 'mode': 'next-leg', 'interview': False,
                            'queued': mid, 'turn': None}
                to = after[0]
        aid = self.leg_actor(name, to)
        if not aid:
            raise Error('%s is neither open in the handler nor closed. Open it (legs.py open %s %s); a leg opened '
                        'in Terminal is closed there, or with legs.py close.' % (to, name, to.split('.', 1)[-1]))
        a = self.actor(name, aid)
        if not a.state.get('turns'):
            # its first turn carries the leg's first message (and a branch's notice): open starts it
            raise Error('%s is prepared and has not started. Start it with legs.py open %s %s; then talk to it.'
                        % (to, name, to.split('.', 1)[-1]))
        with a.guard:   # the turn cannot end between this look and the message (audit 13)
            j = self.job(name)
            if j and j['state'].get('current') == to and not a.state.get('active_turn_id'):
                raise Error('The list is closing %s now. Wait for its close, then talk to the next leg.' % to)
            r = a.message(text)
        mode = 'live' if r.get('queued') else 'turn'
        log(name, 'you to %s%s (%s): %s' % (to, '' if to == label else ' (carrying on %s)' % label, mode, text[:300]))
        said(name, kind='sent', label=to, written_to=None if to == label else label, actor=aid,
             session=a.state.get('session_id'), mode=mode, id=r.get('queued') or (r.get('turn') or {}).get('id'),
             source=source, text=text)
        return {'label': to, 'for': label, 'actor': aid, 'mode': mode, 'interview': False, 'queued': r.get('queued'),
                'turn': (r.get('turn') or {}).get('id') if r.get('new_turn_started') else None}

    def do_interview(self, req):
        """An interview (J, 2026-10-05: "an interview is me, asking to open leg/stage x and talking to it"): a fork of
        a closed leg's checkpoint in a copy of its folder, recorded in CONTROL/interviews.tsv, which E2 reads. It
        remembers the leg; nothing said there reaches the run. Later words continue the leg's latest interview;
        new opens another."""
        run, name = self.run_of(req)
        _, leg, label = leg_of(run, req.get('leg'))
        text = checked(req.get('text'))
        if not committed(run, label):
            raise Error('%s is not closed: an interview opens a closed leg\'s checkpoint. Talk to it with say.' % label)
        snap = run / 'CONTROL/snapshots' / label
        if not (snap / 'agent.tar.gz').is_file():
            raise Error('%s was closed files-only: there is no session to talk to' % label)
        with self.held(name, req):
            ivs = (registry(name).get(label) or {}).get('interviews') or []
            aid = None if req.get('new') or not ivs else ivs[-1]
            if aid is None:
                (run / 'interview-workspaces').mkdir(exist_ok=True)
                aid = 'iv-%s-%s-%s' % (name, leg, time.strftime('%Y%m%dT%H%M%S', time.gmtime()))
                A.restore(str(snap), aid, mode='interview', data=rdir(name))
                register(name, label, interview=aid)
                log(name, 'interview of %s opened from its checkpoint, actor %s' % (label, aid))
        r = self.actor(name, aid).message(text)
        log(name, 'you to %s (interview): %s' % (label, text[:300]))
        return {'label': label, 'actor': aid, 'mode': 'interview', 'interview': True, 'queued': r.get('queued'),
                'turn': (r.get('turn') or {}).get('id') if r.get('new_turn_started') else None}

    def do_answer(self, req):
        run, name = self.run_of(req)
        qid, text = str(req.get('qid') or ''), (req.get('text') or '').strip()
        if not text:
            raise Error('Nothing to answer')
        if (B.branch_of(run) or {}).get('status') == 'draft':
            raise Error('%s is a draft branch: an answer would change its inputs. prepare-branch first.' % name)
        for label, a in self.live(name):
            if any(r['id'] == qid for r in a.asks()):
                r = a.answer(qid, {'answer': text})
                log(name, 'you answered %s, to the running leg %s' % (qid, label))
                said(name, kind='answer', id=qid, label=label, delivery='beside the next tool result', text=text)
                return r
        # an open leg whose turn has ended: queued for its next turn (v43.2: written to the file alone, it reached
        # no turn of that leg, and a leg that then ran done.sh left it unnamed)
        for label, e in registry(name).items():
            if not e.get('actor'):
                continue
            a = self.actor(name, e['actor'])
            if a.state.get('closed') or not a.state.get('turns') or a.state.get('active_turn_id'):
                continue
            try:
                a.current()
            except A.Error:
                continue
            if any(r['id'] == qid for r in a.asks()):
                r = a.answer(qid, {'answer': text})
                log(name, 'you answered %s, to the open leg %s: it hears it with its next turn' % (qid, label))
                said(name, kind='answer', id=qid, label=label, delivery='with the next turn', text=text)
                return r
        if not any(r.get('id') == qid for r in asks_open(run)):
            raise Error('%s is not an open question of %s (out/asks.jsonl)' % (qid, name))
        p = run / '00_GIVE-THE-AGENT/out/_answers' / (A.identity(qid) + '.md')
        A.atomic(p, text + '\n')
        os.chmod(p, 0o444)
        log(name, 'you answered %s in out/_answers; the next leg\'s first message names it' % qid)
        said(name, kind='answer', id=qid, label=None, delivery='the next leg\'s first message', text=text)
        return {'answered': qid, 'file': 'out/_answers/%s.md' % qid, 'delivery': 'the next leg\'s first message names it'}

    def do_pause(self, req):
        run, name = self.run_of(req)
        if (B.branch_of(run) or {}).get('status') == 'draft':
            raise Error('%s is a draft branch: no leg runs yet, and a pause would change its inputs.' % name)
        live = self.live(name)
        if self.job(name) and not live:
            # between two legs: the next step.sh would clear .pause, so the list itself stops before its next leg
            A.write(rdir(name) / 'stop.json', {'utc': A.now(), 'now': False, 'why': 'pause'})
            log(name, 'pause asked between two legs: the list stops before its next leg')
            return {'pause': 'No turn runs now; the list stops before its next leg.'}
        if live:
            label, a = live[0]
            r = a.pause()
            log(name, 'pause asked of %s' % label)
            return dict(r, label=label)
        r = subprocess.run(['bash', str(run / 'CONTROL/harness/pause.sh')], cwd=str(run), env=A.clean_env(),
                           capture_output=True, text=True, timeout=60, start_new_session=True, check=False)
        if r.returncode:
            raise Error('pause.sh exited %d: %s' % (r.returncode, A.tail(r.stderr or r.stdout)))
        log(name, 'pause asked (pause.sh); no turn runs')
        return {'pause': r.stdout.strip()}

    def do_branch(self, req):
        """An analysis branch from a verified close of this run (codex: branch SOURCE CHECKPOINT RUN --leg)."""
        _, name = self.run_of(req)
        with self.held(name, req):
            r = B.create(name, str(req.get('checkpoint')), str(req.get('new')), str(req.get('leg')))
        log(name, 'branch %s made from %s (draft)' % (req.get('new'), r['branch']['checkpoint']))
        return dict(r, next='Replace cards or data with branch-put, then prepare-branch %s' % req.get('new'))

    def do_branch_put(self, req):
        _, name = self.run_of(req)
        up = rdir(name) / 'uploads' / A.identity(str(req.get('upload')))
        with self.held(name, req):
            r = B.put(name, req.get('path'), up, str(req.get('sha256')), req.get('stage'))
        os.replace(up, up.with_name('used-' + up.name))
        log(name, 'branch file: %s' % ', '.join(r['paths']))
        return r

    def do_prepare_branch(self, req):
        """Seal the setup, publish it to analysis/<run>, and prepare the first leg without a turn."""
        run, name = self.run_of(req)
        with self.held(name, req):
            b = B.branch_of(run)
            if not b:
                raise Error('%s is not an analysis branch' % name)
            pub = B.publish(name)
            nn, leg, label = leg_of(run, b['target_leg'])
            aid = self.leg_actor(name, label) or self.new_leg(run, leg, label)
        log(name, 'branch sealed and published; %s prepared' % label)
        return {'run': name, 'lines': pub['lines'], 'ref': pub['ref'], 'first_leg': label, 'actor': aid,
                'next': 'Start it: legs.py open %s %s, or legs.py run %s ...' % (name, leg, name)}

    def do_publish_branch(self, req):
        """The setup, or the last close, committed and pushed again, at an idle close (Codex: publish at an idle
        branch boundary). Never reruns analysis."""
        run, name = self.run_of(req)
        with self.held(name, req):
            b = B.branch_of(run)
            if not b:
                raise Error('%s is not an analysis branch' % name)
            if self.live(name) or (run / 'CONTROL/pending_launch.json').exists():
                raise Error('A leg of %s runs or is prepared: publish at an idle close' % name)
            own = B.own_closes(run, b)
            if own:
                label = own[-1]
                nn, leg = label.split('.', 1)
                cut = cut_of(run, nn, leg)
                kind = ('pause' if cut == 'pause' else 'finished' if finished(run, nn, label)
                        else 'interview-point' if cut == 'interview' else 'close')
                pub = B.publish(name, label, kind)
            else:
                pub = B.publish(name)
        for line in pub['lines']:
            log(name, line.strip())
        return {'run': name, 'lines': pub['lines'], 'ref': pub['ref'], 'commit': pub['commit']}

    def do_stop(self, req):
        _, name = self.run_of(req)
        now = bool(req.get('now'))
        A.write(rdir(name) / 'stop.json', {'utc': A.now(), 'now': now})
        log(name, 'stop asked%s' % (' now: the running turn is interrupted' if now else ' after this leg'))
        hit = []
        if now:
            for label, a in self.live(name):
                threading.Thread(target=a.interrupt, daemon=True).start()
                hit.append(label)
        return {'stopping': bool(self.job(name)) or bool(hit), 'interrupted': hit,
                'note': None if self.job(name) or hit else 'No list of legs runs on %s.' % name}

    def do_run(self, req):
        run, name = self.run_of(req)
        tokens = req.get('legs') or []
        with self.held(name, req):
            self.no_job(name)
            plan = Planner(run, tokens, req.get('accept') or [])
            stop = rdir(name) / 'stop.json'
            if stop.exists():
                old = rdir(name) / 'stops'
                old.mkdir(parents=True, exist_ok=True)
                os.replace(stop, old / ('%s.json' % time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())))
            state = {'id': uuid.uuid4().hex[:12], 'run': name, 'legs': tokens, 'through_interviews': bool(req.get('through_interviews')),
                     'status': 'running', 'current': None, 'phase': None, 'done': [], 'skipped': [], 'reason': None,
                     'started_utc': A.now()}
            A.write(rdir(name) / 'job.json', state)
            t = threading.Thread(target=self.job_loop, args=(run, state, plan), daemon=True)
            with self.guard:
                self.jobs[name] = {'thread': t, 'state': state}
            t.start()
        log(name, 'list started: %s' % ' '.join(tokens))
        return {'job': state['id'], 'legs': plan.preview()}

    # ---- the list, leg by leg ----
    def save_job(self, name, state, **fields):
        state.update(fields)
        A.write(rdir(name) / 'job.json', state)

    def halt(self, name, state, why, todo, status='stopped'):
        self.save_job(name, state, status=status, reason=why, todo=todo, phase=None, ended_utc=A.now())
        try:   # the list is over once saved: a failed notice never saves it again over a newer list's
            needs(name, state.get('current'), 'list ' + status, why, todo)
        except Exception as e:
            log(name, 'the notice for the list\'s end failed: %r' % e)

    def stop_asked(self, name):
        return A.read(rdir(name) / 'stop.json')

    def job_loop(self, run, state, plan):
        name = run.name
        try:
            while True:
                if self.stop_asked(name):
                    return self.halt(name, state, 'You stopped the list.', 'Start it again with legs.py run %s ...' % name)
                leg = plan.next()
                state['skipped'] = plan.skipped
                if leg is None:
                    return self.halt(name, state, 'The list is done%s.' % (
                        ' (already closed, skipped: %s)' % ', '.join(plan.skipped) if plan.skipped else ''),
                        'Name the next legs: legs.py run %s ...' % name, status='completed')
                nn, leg, label = leg_of(run, leg)
                self.save_job(name, state, current=label, phase='preparing')
                with self.lock(name):
                    aid = self.leg_actor(name, label)
                    if aid and self.actor(name, aid).state.get('closed'):
                        aid = None
                    if not aid:
                        try:
                            aid = self.new_leg(run, leg, label)
                        except Error as e:
                            return self.halt(name, state, 'could not prepare %s: %s' % (leg, e),
                                             'Read the refusal; fix it, then run the list again.')
                a = self.actor(name, aid)
                if not a.state.get('last_turn_id') and not a.state.get('active_turn_id'):
                    if self.stop_asked(name):   # asked while step.sh prepared this leg: it stays prepared, unstarted
                        return self.halt(name, state, 'You stopped the list. %s is prepared; its first turn did not start.'
                                         % label, 'Start it again with legs.py run %s ...' % name)
                    with self.lock(name):   # no `say` slips between the words it takes and its turn
                        self.first_turn(a)
                    log(name, '%s: its first turn runs' % label)
                self.save_job(name, state, phase='running', actor=aid)
                if self.follow(name, state, label, a) == 'unfollowed':
                    return self.halt(name, state, '%s: its turn is recorded as running, but nothing follows it.' % label,
                                     'Restart the handler (Ctrl-C, then serve): it settles the turn. Then run the list again.')
                st = a.state
                if st.get('boundary') != 'completed':
                    return self.halt(name, state, '%s: the turn ended %s: %s' % (label, st.get('boundary'),
                                     (st.get('error') or {}).get('message') if isinstance(st.get('error'), dict) else st.get('error')),
                                     'Look at it (legs.py watch %s %s). Talk to it with say, or close it with legs.py close %s %s --force.'
                                     % (name, leg, name, leg))
                if cut_of(run, nn, leg) is None:
                    return self.halt(name, state, '%s: the analyst ended its turn without closing the leg.' % label,
                                     'Read its last words (legs.py reply %s %s); talk to it with say, or close it with --force.'
                                     % (name, leg))
                self.save_job(name, state, phase='closing')
                with self.lock(name):
                    try:
                        s = self.summary(run, a.close())
                    except Error as e:
                        return self.halt(name, state, 'close.sh refused %s: %s' % (label, e),
                                         'Read the refusal; then close it yourself (legs.py close %s %s) and run the list again.'
                                         % (name, leg))
                    self.carry_forward(name, label, a)   # your words that missed its turn: into the next leg
                state['done'].append(s)
                self.save_job(name, state, phase=None)
                log(name, 'closed %s: checkpoint %s, cut %s, advances %s, git %s' % (label, s['checkpoint'], s['cut'],
                                                                                    s['advances'], s.get('publication')))
                github(name, label, s.get('publication'))
                if s['cut'] == 'pause':
                    return self.halt(name, state, '%s paused at a safe stop.' % label,
                                     'When you are ready: legs.py run %s %s (it continues as %s).' % (name, leg, next_pause(leg)))
                if s['cut'] == 'packets-out':
                    return self.halt(name, state, '%s built its packets; the dispatch is next.' % label,
                                     'In Terminal, in the run folder: bash CONTROL/harness/dispatch.sh %s, then run the check leg '
                                     'it names.' % ('D2' if nn == 'D1' else nn))
                if s['cut'] == 'interview' and not state.get('through_interviews'):
                    return self.halt(name, state, '%s closed at an interview point.' % label,
                                     'Interview it: legs.py interview %s %s "...". Then run the next legs.' % (name, leg),
                                     status='completed')
                if not s['advances']:
                    return self.halt(name, state, '%s closed, but its close cannot advance the run (forced, or the '
                                     'validation is incomplete).' % label, 'Read its validation report in the snapshot.')
                nxt = plan.peek()
                if nxt and finished(run, nn, label) and nxt[:2] == nn:
                    return self.halt(name, state, 'Stage %s finished at %s before the listed legs ran out (next: %s).'
                                     % (nn, label, nxt), 'Name the next stage\'s legs.', status='completed')
        except (Error, ValueError) as e:
            return self.halt(name, state, str(e), 'Fix what it names, then run the list again.')
        except Exception as e:
            traceback.print_exc()
            return self.halt(name, state, 'The handler failed: %r' % e, 'Look at the handler\'s Terminal window.')

    def follow(self, name, state, label, a):
        seen = {r['id'] for r in asks_open(a.rundir)}
        interrupting = False
        while a.state.get('active_turn_id'):
            try:
                a.wait(3)
            except Error:
                pass
            if a.state.get('active_turn_id') and not (a.worker and a.worker.is_alive()):
                return 'unfollowed'
            stop = self.stop_asked(name)
            if stop and stop.get('now') and not interrupting:
                interrupting = True
                threading.Thread(target=a.interrupt, daemon=True).start()
            fresh = [r for r in asks_open(a.rundir) if r['id'] not in seen]
            for r in fresh:
                seen.add(r['id'])
                needs(name, label, 'question', '%s asks: %s (meanwhile: %s)' % (r['id'], r.get('question'), r.get('assumption')),
                      'Answer: legs.py answer %s %s "..."' % (name, r['id']))

    def deliveries(self):
        """Each live message's receipt into messages-to-legs.jsonl: beside a tool result (the hook), or with the
        prompt of the leg's next turn. One that missed a closing leg's turn is recorded by carry_forward instead
        ("carried"), and its delivery in the next leg's first message."""
        while not self.stopping.is_set():
            for name in handled_runs():
                try:
                    path = run_path(name) / 'CONTROL/messages-to-legs.jsonl'
                    if not path.exists():
                        continue
                    rows = [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
                    done = {r['id'] for r in rows if r.get('kind') in ('delivered', 'carried')}
                    for r in rows:
                        if r.get('kind') != 'sent' or r.get('mode') != 'live' or r.get('id') in done:
                            continue
                        rec = A.read(rdir(name) / 'actors' / r['actor'] / 'inbox/delivered' / ('%s.json' % r['id']))
                        if rec and rec.get('via') != 'carried':
                            said(name, kind='delivered', label=r['label'], id=r['id'], via=rec.get('via'),
                                 tool=rec.get('tool'), delivered_utc=rec.get('utc'))
                except Exception as e:
                    print('the message record of %s could not be updated: %r' % (name, e))
            self.stopping.wait(2)

    # ---- after a restart ----
    def recover(self):
        for name in handled_runs():
            d = rdir(name)
            for label, e in registry(name).items():
                for aid in [e.get('actor')] + list(e.get('interviews') or []):
                    if not aid:
                        continue
                    try:
                        a = self.actor(name, aid)
                        if a.state.get('active_turn_id'):
                            a.open()   # follows a turn whose process lives on, else records it as interrupted
                            log(name, 'after the restart, %s: %s' % (label, 'followed again' if a.state.get('active_turn_id')
                                                                      else a.state.get('boundary')))
                    except Exception as err:
                        log(name, 'after the restart, %s could not be opened: %s' % (aid, err))
            j = A.read(d / 'job.json')
            if j and j.get('status') == 'running':
                j.update(status='paused', reason='The handler restarted while the list ran.')
                A.write(d / 'job.json', j)
                needs(name, j.get('current'), 'list paused', 'The handler restarted while the list ran.',
                      'Run the list again; closed legs are skipped, and a running leg is followed.')


def serve():
    h = home()
    h.mkdir(parents=True, exist_ok=True)
    lockf = (h / 'server.lock').open('a')
    try:
        import fcntl
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit('Another handler runs already (its heartbeat is in %s).' % (h / 'server.json').name)
    keyp = h / 'key'
    if not keyp.exists():
        A.atomic(keyp, secrets.token_hex(24) + '\n')
    os.chmod(keyp, 0o600)
    if not shutil.which(os.environ.get('RPLACE_CLAUDE_BIN') or 'claude'):
        sys.exit('claude is not on PATH in this Terminal.')
    if sys.platform == 'darwin' and shutil.which('caffeinate'):
        subprocess.Popen(['caffeinate', '-i', '-w', str(os.getpid())])   # the Mac stays awake while the handler runs
    s = Server(keyp.read_text().strip())
    s.recover()
    pool = ThreadPoolExecutor(max_workers=16)

    def beat():
        while not s.stopping.is_set():
            A.write(h / 'server.json', {'pid': os.getpid(), 'beat': time.time(), 'beat_utc': A.now(),
                                        'started_utc': started, 'legs_sha256': A.sha(Path(__file__)),
                                        'actor_sha256': A.sha(HERE / 'actor.py')})
            s.stopping.wait(BEAT)
    started = A.now()
    threading.Thread(target=beat, daemon=True).start()
    threading.Thread(target=s.deliveries, daemon=True).start()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: s.stopping.set())
    print('The leg handler runs (pid %d). Leave this window open; Ctrl-C stops the handler, not a running turn.' % os.getpid())
    while not s.stopping.is_set():
        for p in sorted(runs_dir().glob('*/CONTROL/legs/requests/*.json')):
            taken = p.parent / 'taken' / p.name
            taken.parent.mkdir(exist_ok=True)
            try:
                age = time.time() - p.stat().st_mtime
                os.replace(p, taken)
            except FileNotFoundError:
                continue
            try:
                req = json.loads(taken.read_text(encoding='utf-8'))
            except (ValueError, OSError):
                req = None
            if not isinstance(req, dict):
                print('%s  not a request, skipped: %s' % (A.stamp(), taken.name))
                continue
            print('%s  %s %s %s' % (A.stamp(), req.get('cmd'), req.get('run') or '', req.get('leg') or ''))
            pool.submit(s.handle, req, p.parents[3].name, age, time.monotonic())   # runs/<run>/CONTROL/legs/requests/<id>.json
        s.stopping.wait(0.3)
    print('The handler stops. A turn that runs goes on; the next `legs.py serve` follows it again.')
    pool.shutdown(wait=False)


# ---- the client ----------------------------------------------------------------------------------
def alive():
    """The handler's heartbeat, if it is fresh. Measured against a file the client touches now, so the two times
    come from the same clock (the folder's), whatever the client's own clock says (Cowork's shell runs elsewhere)."""
    beat, probe = home() / 'server.json', home() / 'clock'
    try:
        probe.touch()
        fresh = probe.stat().st_mtime - beat.stat().st_mtime < STALE
    except OSError:
        return None
    return A.read(beat) if fresh else None


def submit(cmd, timeout, **fields):
    h, d = home(), rdir(fields['run'])
    if not (h / 'key').exists():
        sys.exit(SERVE_HINT)
    if not alive():
        print('Warning: no recent heartbeat from the handler. ' + SERVE_HINT, file=sys.stderr)
        timeout = min(timeout, 20)
    rid = '%s-%020d-%s' % (time.strftime('%Y%m%dT%H%M%S', time.gmtime()), time.time_ns(), uuid.uuid4().hex[:6])
    body = dict(fields, id=rid, cmd=cmd, utc=A.now(), ttl=min(timeout, 60))
    A.write(d / 'requests' / (rid + '.json'), dict(body, sig=sign((h / 'key').read_text().strip(), body)))
    end = time.time() + timeout
    res = d / 'results' / (rid + '.json')
    while time.time() < end:
        if res.exists():
            r = A.read(res)
            if not r.get('ok'):
                sys.exit('Refused: ' + str(r.get('error')))
            return r['result']
        time.sleep(0.5)
    sys.exit('No answer from the handler within %d s. It may still be working on it (legs.py status). %s'
             % (timeout, '' if alive() else SERVE_HINT))


def actor_state(name, aid):
    return A.read(rdir(name) / 'actors' / aid / 'state.json') or {}


def final_text(name, aid):
    st = actor_state(name, aid)
    t = st.get('last_turn_id')
    r = A.read(rdir(name) / 'actors' / aid / 'turns' / t / 'result.json') if t else None
    return (r or {}).get('result') or ''


def pick(name, label=None, interview=False):
    """The actor a reading command means. For a leg: its own session, or with --interview its latest interview.
    Without a leg: the run's running leg, else the one opened last."""
    reg = registry(name)
    if label:
        e = reg.get(label) or {}
        ivs = e.get('interviews') or []
        aid = (ivs or [None])[-1] if interview else e.get('actor')
        if not aid:
            sys.exit('The handler has no %s for %s' % ('interview' if interview else 'session of its own', label))
        return aid
    rows = [(e.get('opened_utc') or '', e.get('actor')) for e in reg.values() if e.get('actor')]
    for _, aid in rows:
        if actor_state(name, aid).get('active_turn_id'):
            return aid
    if not rows:
        sys.exit('The handler has opened no leg of %s' % name)
    return sorted(rows)[-1][1]


def line_of(row, full=False):
    """One event as text. Short: one line each, tool outputs left out. Full (--full): the analyst's words whole,
    every tool call whole, and each tool's output as the stream gave it (stream.py keeps 20,000 characters of
    one output; the rest stays in the turn's stream.jsonl)."""
    n = row.get('native') or {}
    m, p = n.get('method'), n.get('params') or {}
    it = p.get('item') or {}
    when = (row.get('utc') or '')[11:19]

    def one(s, k=300):
        if full:
            return str(s or '').rstrip()
        s = ' '.join(str(s or '').split())
        return s if len(s) <= k else s[:k] + ' ...'

    def block(s):
        s = str(s or '').rstrip()
        return ('\n' + '\n'.join('      ' + x for x in s.splitlines())) if s else ''
    if m == 'item/completed' and it.get('type') == 'agentMessage':
        return '%s analyst: %s' % (when, one(it.get('text'), 1200))
    if m == 'item/completed' and it.get('type') == 'userMessage':
        return '%s message: %s' % (when, one(' '.join(c.get('text', '') for c in it.get('content') or [])))
    if m == 'item/started':
        return '%s   %s%s' % (when, one(it.get('command') or it.get('type')),
                              block(it.get('aggregatedOutput')) if full and it.get('aggregatedOutput') else '')
    if m == 'item/completed' and it.get('type') == 'dynamicToolCall':
        return '%s   [%s] %s' % (when, one(it.get('command'), 120), one(it.get('aggregatedOutput'), 200))
    if m == 'item/completed' and it.get('type') in ('commandExecution', 'fileChange', 'webSearch'):
        if full:
            return '%s   %s %s:%s' % (when, 'failed' if it.get('status') == 'failed' else 'output of',
                                       one(it.get('command'), 120), block(it.get('aggregatedOutput')) or ' (none)')
        return '%s   failed: %s' % (when, one(it.get('command'))) if it.get('status') == 'failed' else None
    if m == 'turn/started':
        return '%s --- turn starts' % when
    if m == 'turn/completed':
        t = p.get('turn') or {}
        return '%s --- turn ends: %s%s' % (when, t.get('status'), (' (%s)' % one((t.get('error') or {}).get('message'), 200))
                                           if t.get('error') else '')
    if m == 'item/tool/requestUserInput':
        q = (p.get('questions') or [{}])[0].get('question', '')
        return '%s QUESTION %s%s' % (when, p.get('requestKey'), block(q) if full else '')
    if m == 'rplace/messageDelivered':
        return '%s   your message %s delivered (%s)' % (when, p.get('messageId'), p.get('via'))
    return None


def show(result):
    if isinstance(result, dict):
        for k, v in result.items():
            if v in (None, [], ''):
                continue
            if isinstance(v, list):
                print('%s:' % k)
                for x in v:
                    print('  %s' % (json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x))
            else:
                print('%s: %s' % (k, v))
    else:
        print(result)


def cmd_status(a):
    st = alive()
    print('handler: %s' % ('running, pid %s, since %s' % (st['pid'], st.get('started_utc')) if st else
                           'NOT RUNNING. ' + SERVE_HINT))
    names = [a.run] if a.run else handled_runs()
    for name in names:
        print('\n%s' % name)
        j = A.read(rdir(name) / 'job.json')
        if j:
            print('  list: %s, at %s%s (%d closed)%s' % (j.get('status'), j.get('current') or '-',
                  ', ' + j['phase'] if j.get('phase') else '', len(j.get('done') or []),
                  '; ' + j['reason'] if j.get('reason') else ''))
        for label, e in sorted(registry(name).items()):
            s = actor_state(name, e.get('actor')) if e.get('actor') else {}
            if s.get('active_turn_id'):
                print('  running: %s (turn %s)' % (label, s['active_turn_id'][:8]))
            for iv in e.get('interviews') or []:
                if actor_state(name, iv).get('active_turn_id'):
                    print('  interview answering: %s' % label)
        try:
            for q in asks_open(run_path(name)):
                print('  question %s (%s): %s' % (q['id'], q.get('leg'), q.get('question')))
        except Error:
            pass
        n = A.read(rdir(name) / 'needs-you.json')
        if n:
            print('  needs you (%s, %s): %s\n    %s' % (n.get('kind'), n.get('utc', '')[:19], n.get('why'), n.get('todo')))


def cmd_legs(a):
    run = run_path(a.run)
    reg = registry(run.name)
    labels = set(reg)
    index = run / 'CONTROL/snapshots/INDEX.tsv'
    if index.exists():
        labels |= {r.split('\t')[0] for r in index.read_text().splitlines()[1:] if r.strip()}
    labels |= set(A.read(run / 'CONTROL/sessions.json', {}) or {})
    order = {r['stage']: i for i, r in enumerate(steps(run).table())}
    for label in sorted(labels, key=lambda x: (order.get(x[:2], 99), x)):
        nn, leg = label.split('.', 1)
        e = reg.get(label) or {}
        s = actor_state(run.name, e['actor']) if e.get('actor') else {}
        if committed(run, label):
            state = 'closed (%s)' % (cut_of(run, nn, leg) or 'forced')
        elif s.get('active_turn_id'):
            state = 'running'
        elif s.get('last_turn_id'):
            state = 'open, turn ended %s; the analyst %s the leg' % (s.get('boundary'), 'closed' if cut_of(run, nn, leg) else 'did not close')
        elif s:
            state = 'prepared'
        else:
            state = 'opened outside the handler, not closed'
        iv = len(e.get('interviews') or [])
        print('%-16s %s%s' % (label, state, '; %d interview%s' % (iv, '' if iv == 1 else 's') if iv else ''))


def cmd_watch(a):
    """The last N events, or (--follow) every event as it comes, like the terminal. Without a LEG, --follow goes
    on through every leg the handler opens after it, in the order they were opened, each read to its end, so a
    short leg is never skipped. Ctrl-C ends the watching; the legs go on."""
    label = leg_of(run_path(a.run), a.leg)[2] if a.leg else None
    seen = {}            # actor -> bytes of its events.jsonl already shown
    shown = [None]       # the actor whose header was printed last

    def show_from(aid, start, tail=None):
        rows, end = events_of(rdir(a.run) / 'actors' / aid / 'events.jsonl', start)
        out = [x for x in (line_of(r, a.full) for r in rows) if x]
        if tail is not None:
            out = out[-tail:]
        if out and shown[0] != aid:
            st = actor_state(a.run, aid)
            print('=== %s%s' % (st.get('label'), ' (interview)' if st.get('role') == 'interview' else ''), flush=True)
            shown[0] = aid
        for x in out:
            print(x, flush=True)
        return end

    def order():
        """The actors to show: the leg's own (with LEG), else every leg actor in the order the handler opened them."""
        if label:
            try:
                return [pick(a.run, label, a.interview)]
            except SystemExit:
                return []
        rows = sorted((e.get('opened_utc') or '', e['actor']) for e in registry(a.run).values() if e.get('actor'))
        return [aid for _, aid in rows]

    try:
        first = pick(a.run, label, a.interview)
    except SystemExit:
        if not a.follow:
            raise
        first = None   # nothing opened yet: the first leg the handler opens is shown from its start
    if first:
        seen[first] = show_from(first, 0, tail=a.n)
    if not a.follow:
        return
    known = set(order())   # legs opened before this watch began, except the one shown, are history
    try:
        while True:
            for aid in order():
                if aid in seen:
                    seen[aid] = show_from(aid, seen[aid])
                elif aid not in known:
                    seen[aid] = show_from(aid, 0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()


def cmd_reply(a):
    label = leg_of(run_path(a.run), a.leg)[2]
    aid = pick(a.run, label, a.interview)
    st = actor_state(a.run, aid)
    if st.get('active_turn_id'):
        print('(%s is still answering; its last finished reply follows)' % label)
    print(final_text(a.run, aid) or '(no finished reply yet)')


def cmd_say(a, cmd='say'):
    text = sys.stdin.read() if a.text == ['-'] else ' '.join(a.text)
    r = submit(cmd, 180, run=a.run, leg=a.leg, text=text, new=getattr(a, 'new', False), source='say')
    aid = r['actor']
    if r['mode'] == 'next-leg':
        print('%s is closed. Its conversation goes on in the next leg%s: your words go into its first message.'
              % (r['label'], ' (%s, prepared)' % r['to'] if r.get('to') else ''))
        return
    if r.get('for') and r['for'] != r['label']:
        print('%s is closed; %s carries on its conversation and gets your words.' % (r['for'], r['label']))
    if r['mode'] == 'live':
        print('%s is working. Your words reach it beside its next tool result.' % r['label'])
        end = time.time() + min(a.wait, 120)
        rec = rdir(a.run) / 'actors' / aid / 'inbox/delivered' / ('%s.json' % r['queued'])
        while time.time() < end and not rec.exists():
            time.sleep(1)
        d = A.read(rec)
        leg = r['label'].split('.', 1)[-1]
        print('Delivered %s, beside %s. Its answer comes in its stream: legs.py watch %s %s'
              % (d.get('utc'), d.get('tool') or 'a tool result', a.run, leg) if d else
              'Not delivered yet; it waits for the next tool call (legs.py watch %s %s).' % (a.run, leg))
        return
    print('%s: %s' % (r['label'], 'an interview of its checkpoint answers' if r['interview']
                      else 'a new turn in its session answers'))
    end = time.time() + a.wait
    while time.time() < end:
        st = actor_state(a.run, aid)
        if not st.get('active_turn_id') and st.get('last_turn_id') == r['turn']:
            print(final_text(a.run, aid) if st.get('boundary') == 'completed' else
                  'The turn ended %s: %s' % (st.get('boundary'), st.get('error')))
            return
        time.sleep(2)
    print('Still answering. Read it later: legs.py reply %s %s%s' % (a.run, r['label'].split('.', 1)[-1],
                                                                   ' --interview' if r['interview'] else ''))


def cmd_interview(a):
    cmd_say(a, 'interview')


def cmd_wait(a):
    """Returns at once with a notice you have not seen through wait, else when one comes (OpenAI review 2026-10-05,
    finding 9): CONTROL/legs/needs-you.seen holds the time of the last one shown."""
    p, seen = rdir(a.run) / 'needs-you.jsonl', rdir(a.run) / 'needs-you.seen'
    end = time.time() + a.timeout
    while True:
        rows = []
        if p.exists():
            for line in p.read_text(encoding='utf-8').splitlines():
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
        try:
            k = int(seen.read_text().strip()) if seen.exists() else 0
        except ValueError:   # the time of one notice, as before v43.2: show what follows it
            k = 0
        if len(rows) > k:
            for n in rows[k:]:
                print('%s needs you (%s): %s\n  %s' % (n.get('leg') or a.run, n.get('kind'), n.get('why'), n.get('todo')))
            A.atomic(seen, str(len(rows)) + '\n')
            return
        if time.time() >= end:
            break
        time.sleep(2)
    j = A.read(rdir(a.run) / 'job.json') or {}
    print('Nothing new in %d s. The list is %s, at %s.' % (a.timeout, j.get('status', 'not started'), j.get('current') or '-'))


CHAT_HELP = """Each line you type goes to one agent of the run. Its answers, its words and its tool calls show here.
  text             to the agent named in the prompt (at the start: the running leg, else the last opened)
  @A1b-02 text     to that leg, and it stays the one you talk to. A running leg hears you beside its next tool
                   result, an open one in a new turn. The last closed leg's conversation goes on in the next leg,
                   which gets your words; an older closed leg only in an interview.
  ?A1a text        an interview of a closed leg (you open it to talk to it as it was); ?A1a+ a new one
  /to A1b-02       talk to that leg from now on, without sending anything
  /tools           show or hide tool calls      /full   show or hide tool outputs
  /help            this text                    /quit   leave the chat (Ctrl-D too); the legs go on
Lines marked "handler |" come from the handler: what it prepared and closed, what needs you, and its notes."""


def cmd_chat(a):
    """One window to talk to every agent of a run: your lines go out with `say`; every agent's words, tool calls and
    answers come back here as they happen, each line marked with its leg, with the handler's notices between."""
    try:
        import readline
    except ImportError:
        readline = None
    run = run_path(a.run)
    name = run.name
    rdir(name).mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    opts = {'tools': True, 'full': a.full, 'to': None, 'iv': False}
    seen = {}
    mine = set()   # the lines sent from this chat, already on the screen
    stop = threading.Event()

    def prompt():
        return '%s%s> ' % (opts['to'] or '?', ' (interview)' if opts['iv'] else '')

    def out(text):
        with lock:
            if sys.stdin.isatty():   # the line you are typing stays under the new lines
                buf = readline.get_line_buffer() if readline else ''
                sys.stdout.write('\r\x1b[K' + text + '\n' + prompt() + buf)
            else:
                sys.stdout.write(text + '\n')
            sys.stdout.flush()

    def who(aid):
        st = actor_state(name, aid)
        leg = (st.get('label') or aid).split('.', 1)[-1]
        return leg + (' (interview)' if st.get('role') == 'interview' else '')

    def actors():
        rows = []
        for e in registry(name).values():
            if e.get('actor'):
                rows.append((e.get('opened_utc') or '', e['actor']))
            for iv in e.get('interviews') or []:
                rows.append((actor_state(name, iv).get('created_utc') or '', iv))
        return [aid for _, aid in sorted(rows)]

    def pump(aid, start):
        rows, end = events_of(rdir(name) / 'actors' / aid / 'events.jsonl', start)
        tag = who(aid) if rows else ''
        for row in rows:
            n = row.get('native') or {}
            m, it = n.get('method'), (n.get('params') or {}).get('item') or {}
            if m == 'item/completed' and it.get('type') == 'userMessage' and \
                    ' '.join(c.get('text', '') for c in it.get('content') or []).strip() in mine:
                continue   # your own line is already on the screen; the harness's first message is shown
            if not opts['tools'] and (m == 'item/started' or (m == 'item/completed' and it.get('type') != 'agentMessage')):
                continue
            x = line_of(row, opts['full'])
            if x:
                out('%s | %s' % (tag, x))
        return end

    def follow():
        log_path = rdir(name) / 'events.log'
        log_pos = log_path.stat().st_size if log_path.exists() else 0
        for aid in actors():   # what happened before the chat opened is history, except the last few lines
            path = rdir(name) / 'actors' / aid / 'events.jsonl'
            seen[aid] = path.stat().st_size if path.exists() else 0
        while not stop.is_set():
            try:
                for aid in actors():
                    seen[aid] = pump(aid, seen.get(aid, 0))
                if log_path.exists() and log_path.stat().st_size > log_pos:
                    with log_path.open('rb') as f:
                        f.seek(log_pos)
                        chunk = f.read()
                    done = chunk.rfind(b'\n') + 1
                    log_pos += done
                    for line in chunk[:done].decode().splitlines():
                        text = line[22:] if len(line) > 22 else line
                        if text.startswith('you to '):
                            continue
                        out('handler | %s %s' % (line[11:19], text))
            except Exception as e:   # a half-written file: look again
                out('handler | (the chat could not read a record: %s)' % e)
            stop.wait(0.5)

    def send(leg, text, new=False, iv=False):
        mine.add(text)
        try:
            r = submit('interview' if iv else 'say', 180, run=name, leg=leg, text=text, new=new, source='chat')
        except SystemExit as e:
            out('handler | not sent: %s' % e)
            return
        if r['mode'] == 'next-leg':
            out('handler | %s is closed: your words go into the next leg\'s first message' % r['label'].split('.', 1)[-1])
            return
        how = {'live': 'it hears you beside its next tool result', 'turn': 'a new turn in its session answers',
               'interview': 'an interview of its checkpoint answers'}.get(r['mode'], r['mode'])
        via = '' if not r.get('for') or r['for'] == r['label'] else ' (carrying on %s)' % r['for'].split('.', 1)[-1]
        out('handler | to %s%s: %s' % (r['label'].split('.', 1)[-1], via, how))

    try:
        opts['to'] = actor_state(name, pick(name)).get('label', '').split('.', 1)[-1] or None
    except SystemExit:
        opts['to'] = None
    print(CHAT_HELP)
    print('Run %s. %s' % (name, 'You talk to %s.' % opts['to'] if opts['to'] else 'Name a leg: @A1a text, or /to A1a.'))
    threading.Thread(target=follow, daemon=True).start()
    try:
        while True:
            try:
                line = input(prompt() if sys.stdin.isatty() else '')
            except EOFError:
                break
            line = line.strip()
            if not line:
                continue
            if line in ('/quit', '/exit'):
                break
            if line == '/help':
                out(CHAT_HELP)
                continue
            if line in ('/tools', '/full'):
                opts[line[1:]] = not opts[line[1:]]
                out('handler | %s %s' % (line[1:], 'on' if opts[line[1:]] else 'off'))
                continue
            new, iv = False, opts['iv']
            if line.startswith('/to '):
                target, text, iv = line[4:].strip(), '', False
            elif line[:1] in ('@', '?'):
                target, _, text = line[1:].partition(' ')
                iv = line[0] == '?'
                if target.endswith('+'):
                    target, new = target[:-1], True
            else:
                target, text = opts['to'], line
            if not target:
                out('handler | name a leg first: @A1a your words')
                continue
            try:
                leg = leg_of(run, target)[1]
            except ValueError as e:
                out('handler | %s' % e)
                continue
            opts['to'], opts['iv'] = leg, iv
            if text.strip():
                send(leg, text.strip(), new, iv)
            else:
                out('handler | you talk to %s%s now' % (leg, '\'s interview' if iv else ''))
    except KeyboardInterrupt:
        pass
    stop.set()
    print()


def cmd_branch_status(a):
    run = run_path(a.run)
    b = B.branch_of(run)
    if not b:
        sys.exit('%s is not an analysis branch' % a.run)
    show(B.summary(b))
    pub = A.read(run / 'publication.json')
    if pub:
        print('publication:')
        show({k: v for k, v in pub.items() if k != 'commits'})
        for label, c in (pub.get('commits') or {}).items():
            print('  %s  %s' % (c[:12], label))


def cmd_branch_put(a):
    src = Path(a.file).expanduser()
    if not src.is_file():
        sys.exit('No file %s' % src)
    digest = A.sha(src)
    up = rdir(a.run) / 'uploads' / ('%s-%s' % (digest[:16], uuid.uuid4().hex[:6]))
    up.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, up)
    show(submit('branch_put', 300, run=a.run, path=a.path, stage=a.stage, upload=up.name, sha256=digest))


def cmd_note(a):
    """The handler's line in the chat (and in the run's events.log): for a summary or a reminder to J."""
    log(a.run, 'note: ' + ' '.join(a.text))




def main(argv=None):
    ap = argparse.ArgumentParser(prog='legs.py', description='The Claude leg handler.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('serve')
    p = sub.add_parser('status'); p.add_argument('run', nargs='?')
    p = sub.add_parser('legs'); p.add_argument('run')
    p = sub.add_parser('open'); p.add_argument('run'); p.add_argument('leg'); p.add_argument('--wait', type=int, default=900)
    p = sub.add_parser('close'); p.add_argument('run'); p.add_argument('leg'); p.add_argument('--force', action='store_true')
    p.add_argument('--wait', type=int, default=7200)
    p = sub.add_parser('run'); p.add_argument('run'); p.add_argument('legs', nargs='+')
    p.add_argument('--through-interviews', action='store_true')
    p.add_argument('--accept', action='append', default=[], help='a close that cannot advance, accepted by name')
    p = sub.add_parser('stop'); p.add_argument('run'); p.add_argument('--now', action='store_true')
    p = sub.add_parser('pause'); p.add_argument('run')
    p = sub.add_parser('say'); p.add_argument('run'); p.add_argument('leg'); p.add_argument('text', nargs='+')
    p.add_argument('--wait', type=int, default=540)
    p = sub.add_parser('interview'); p.add_argument('run'); p.add_argument('leg'); p.add_argument('text', nargs='+')
    p.add_argument('--new', action='store_true'); p.add_argument('--wait', type=int, default=540)
    for c in ('reply', 'watch'):
        p = sub.add_parser(c); p.add_argument('run'); p.add_argument('leg', nargs='?' if c == 'watch' else None)
        if c == 'watch':
            p.add_argument('-n', type=int, default=40)
            p.add_argument('--follow', '-f', action='store_true', help='every event as it comes, leg after leg')
            p.add_argument('--full', action='store_true', help='words and commands whole, and every tool output')
        g = p.add_mutually_exclusive_group()
        g.add_argument('--interview', dest='interview', action='store_true', default=None, help='its latest interview')
        g.add_argument('--leg', dest='interview', action='store_false', help='the leg\'s own session')
    p = sub.add_parser('answer'); p.add_argument('run'); p.add_argument('qid'); p.add_argument('text', nargs='+')
    p = sub.add_parser('wait'); p.add_argument('run'); p.add_argument('--timeout', type=int, default=540)
    p = sub.add_parser('chat'); p.add_argument('run'); p.add_argument('--full', action='store_true')
    p = sub.add_parser('branch'); p.add_argument('source'); p.add_argument('checkpoint'); p.add_argument('new')
    p.add_argument('--leg', required=True)
    p = sub.add_parser('branch-put'); p.add_argument('run'); p.add_argument('path'); p.add_argument('--file', required=True)
    p.add_argument('--stage')
    for c in ('branch-status', 'prepare-branch', 'publish-branch'):
        p = sub.add_parser(c); p.add_argument('run')
    p = sub.add_parser('note'); p.add_argument('run'); p.add_argument('text', nargs='+')
    a = ap.parse_args(argv)
    if a.cmd == 'serve':
        return serve()
    reads = {'status': cmd_status, 'legs': cmd_legs, 'watch': cmd_watch, 'reply': cmd_reply, 'say': cmd_say, 'interview': cmd_interview, 'wait': cmd_wait,
             'chat': cmd_chat, 'note': cmd_note, 'branch-status': cmd_branch_status, 'branch-put': cmd_branch_put}
    if a.cmd in reads:
        return reads[a.cmd](a)
    if a.cmd == 'open':
        show(submit('open', a.wait, run=a.run, leg=a.leg))
    elif a.cmd == 'close':
        show(submit('close', a.wait, run=a.run, leg=a.leg, force=a.force))
    elif a.cmd == 'run':
        show(submit('run', 120, run=a.run, legs=a.legs, through_interviews=a.through_interviews,
                    accept=[leg_of(run_path(a.run), x)[2] for x in a.accept]))
    elif a.cmd == 'stop':
        show(submit('stop', 60, run=a.run, now=a.now))
    elif a.cmd == 'pause':
        show(submit('pause', 60, run=a.run))
    elif a.cmd == 'branch':
        show(submit('branch', 1800, run=a.source, checkpoint=a.checkpoint, new=a.new, leg=a.leg))
    elif a.cmd == 'prepare-branch':
        show(submit('prepare_branch', 1800, run=a.run))
    elif a.cmd == 'publish-branch':
        show(submit('publish_branch', 1800, run=a.run))
    elif a.cmd == 'answer':
        show(submit('answer', 60, run=a.run, qid=a.qid, text=' '.join(a.text)))


if __name__ == '__main__':
    main()
