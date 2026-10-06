"""Controller facade for Claude. Archives stay in the owning harness store.

The reference store binds their complete file inventory. It is not a portable
runtime bundle, and cannot authorize eviction of the shared Claude run.
"""
import hashlib
import json
import tarfile
from pathlib import PurePosixPath
from .common import *
from . import backends

FORMAT = 'rplace-claude-v1'
COMMON = {'checkpoint.json', 'fs.tar.gz', 'fs.sha256', 'agent.tar.gz',
          'agent-files.sha256', 'transcript.jsonl'}
CLOSE = COMMON | {'instrument.tar.gz', 'validation.json', 'validation-report.txt', 'cost.json'}


def _member(name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or str(p) != name:
        raise Error('Unsafe Claude archive path: ' + name)
    return p


def _tar(path, prefix, manifest):
    """Verify bytes and entries without extraction. Links need separate acceptance."""
    expected = {}
    for line in manifest.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        kind, mode, digest, rel, tail = line.split('\t', 4)
        _member(rel)
        if rel in expected or kind not in ('file', 'directory'):
            raise Error('Claude linked, special or duplicate entries are not admitted: ' + rel)
        expected[rel] = (kind, mode, digest, tail)
    actual = {}; root_seen = False
    with tarfile.open(path, 'r:gz') as tar:
        for m in tar:
            n = m.name.rstrip('/')
            _member(n)
            if n == prefix:
                if root_seen or not m.isdir(): raise Error('Invalid Claude archive root')
                root_seen = True
                continue
            if not n.startswith(prefix + '/') or not (m.isfile() or m.isdir()):
                raise Error('Unsafe Claude archive entry: ' + n)
            rel = n[len(prefix) + 1:]
            if rel in actual: raise Error('Duplicate Claude archive entry: ' + rel)
            if m.isfile():
                h = hashlib.sha256(); size = 0
                with tar.extractfile(m) as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        h.update(chunk); size += len(chunk)
                actual[rel] = ('file', oct(m.mode), h.hexdigest(), str(size))
            else:
                actual[rel] = ('directory', oct(m.mode), '-', '-')
    if not root_seen or actual != expected: raise Error('Claude archive differs from its entry inventory')
    return {rel: {'sha256': row[2], 'bytes': int(row[3]), 'mode': int(row[1], 8)}
            for rel, row in actual.items() if row[0] == 'file'}


def _close_boundary(folder, receipt, state, sid):
    """Read already verified archive entries, never the changing live workspace."""
    try:
        stage, leg = state['label'].split('.', 1)
        with tarfile.open(folder / 'fs.tar.gz', 'r:gz') as tar:
            def saved(name):
                with tar.extractfile('00_GIVE-THE-AGENT/' + name) as stream:
                    return stream.read().decode('utf-8')
            marker = saved(f'out/_closes/{stage}-{leg}.closed').strip().splitlines()[-1].split()
            records = json.loads(saved('RUN.json'))['legs']
        if len(marker) != 2 or marker[1] not in ('close', 'interview', 'packets-out') or receipt.get('cut') != marker[1]:
            raise Error('Claude close cut differs from its saved marker or cannot advance')
        row = next((r for r in reversed(records) if r.get('stage') == stage and r.get('leg') == leg), None)
        if not row or row.get('session') != sid or (row.get('cut') or 'close') != marker[1]:
            raise Error('Claude saved leg record differs from its session or cut')
    except (KeyError, ValueError, IndexError, TypeError, AttributeError) as exc:
        raise Error('Claude saved leg record or close marker is missing or malformed') from exc


def validate(folder, receipt, state, scientific=False):
    folder = inside(folder)
    # No linked files or directories in the envelope, even before opening JSON.
    observed = inventory(folder)
    kind = receipt.get('kind')
    if receipt.get('backend') != 'claude' or receipt.get('format') != FORMAT or kind not in ('capture', 'close'):
        raise Error('Invalid Claude receipt type')
    required = CLOSE if kind == 'close' else COMMON
    if not required <= observed.keys(): raise Error('Incomplete Claude archive set')
    ck = read(folder / 'checkpoint.json', {})
    sid = state.get('session_id') or state.get('thread_id')
    if not sid or receipt.get('actor') != state['id'] or receipt.get('session') != sid:
        raise Error('Claude receipt belongs to another actor or session')
    if not receipt.get('last_turn') or receipt['last_turn'] != state.get('last_turn_id'):
        raise Error('Claude receipt belongs to another turn')
    if ck.get('subject') != 'aggregator' or ck.get('session', {}).get('session_id') != sid:
        raise Error('Claude checkpoint session or subject differs')
    if kind == 'close':
        if ck.get('label') != state.get('label') or ck.get('kind') != 'agent-and-files':
            raise Error('Claude close label or snapshot kind differs')
        if not (folder / 'COMMITTED').is_file() or not ck.get('checkpoint_id') or (folder / 'COMMITTED').read_text().strip() != ck['checkpoint_id'] or receipt.get('checkpoint_id') != ck['checkpoint_id']:
            raise Error('Claude close commit does not bind its checkpoint')
        digests = {}
        for line in (folder / 'MANIFEST.sha256').read_text().splitlines():
            digest, rel = line.split(maxsplit=1); rel = rel.lstrip('*')
            _member(rel)
            if rel in digests: raise Error('Duplicate Claude manifest entry')
            digests[rel] = digest
        if not required <= digests.keys(): raise Error('Claude close manifest is incomplete')
        if set(digests)!=set(observed)-{'MANIFEST.sha256','COMMITTED'}:
            raise Error('Claude close manifest does not cover the saved folder')
    else:
        if ck.get('actor') != state['id'] or ck.get('last_turn') != state.get('last_turn_id') or ck.get('boundary') != state.get('boundary') or ck.get('label') != state.get('label'):
            raise Error('Claude capture boundary differs')
        if Path(ck.get('claude_run', '')).resolve() != Path(state['claude_run']).resolve():
            raise Error('Claude capture belongs to another run')
        digests = read(folder / 'DIGESTS.json', {})
        if not required <= digests.keys(): raise Error('Claude capture digests are incomplete')
        if set(digests)!=set(observed)-{'DIGESTS.json'}:
            raise Error('Claude capture digests do not cover the saved folder')
    for rel, digest in digests.items():
        _member(rel)
        if observed.get(rel, {}).get('sha256') != digest: raise Error('Claude archive digest mismatch: ' + rel)
    if receipt.get('digests') != digests: raise Error('Claude receipt differs from archive digests')
    fs = _tar(folder / 'fs.tar.gz', '00_GIVE-THE-AGENT', folder / 'fs.sha256')
    native = _tar(folder / 'agent.tar.gz', '.cc', folder / 'agent-files.sha256')
    transcript_hash = sha(folder / 'transcript.jsonl')
    project = ck.get('session', {}).get('project', 'run')
    if ck['session'].get('transcript_sha256') != transcript_hash or native.get('projects/' + project + '/' + sid + '.jsonl', {}).get('sha256') != transcript_hash:
        raise Error('Claude transcript and native archive disagree')
    if scientific:
        validation = ck.get('validation', {})
        report = read(folder / 'validation.json', {})
        if kind != 'close' or state.get('boundary') != 'completed' or receipt.get('forced') or ck.get('forced'):
            raise Error('A capture or forced stop cannot advance a study')
        if receipt.get('scientific') is not True:
            raise Error('Claude receipt does not authorize scientific advancement')
        _close_boundary(folder, receipt, state, sid)
        if any(validation.get(k) is not True for k in ('complete', 'completed_turn', 'launcher_exited')) or validation.get('validator_exit_code') != 0:
            raise Error('Claude scientific validation is incomplete')
        if any(validation.get(k) != v for k, v in report.items()) or not report or validation.get('report_sha256') != sha(folder / 'validation-report.txt'):
            raise Error('Claude validation report is not bound to the close')
        if ck['session'].get('boundary_verified') is not True:
            raise Error('Claude transcript boundary is unverified')
    return {'format': FORMAT, 'backend': 'claude', 'subject': state.get('role'),
            'boundary': state.get('boundary'), 'thread_id': sid, 'last_turn_id': state['last_turn_id'],
            'files': {'workspace/' + n: v for n, v in fs.items()}, 'checkpoint_metadata': ck}


def register(receipt, state, scientific=False):
    if receipt.get('kind') == 'close':
        folder = inside(Path(state['claude_run']) / receipt['snapshot'], Path(state['claude_run']))
        if folder != Path(state['claude_run']).resolve() / 'CONTROL/snapshots' / state['label']:
            raise Error('Claude close path differs from the actor label')
    else:
        folder = inside(receipt['archive'], actor_dir(state['id']) / 'captures')
    manifest = validate(folder, receipt, state, scientific)
    record = {'backend': 'claude', 'format': FORMAT, 'folder': str(folder), 'receipt': receipt,
              'state': {k: state.get(k) for k in ('id', 'role', 'label', 'session_id', 'thread_id', 'last_turn_id', 'boundary', 'claude_run')},
              'files': inventory(folder), 'scientific': scientific}
    encoded = json.dumps(record, sort_keys=True).encode(); digest = hashlib.sha256(encoded).hexdigest()
    ck = identity(state['id'] + '-claude-' + digest[:20]); dest = DATA / 'checkpoints' / ck
    result = {'backend': 'claude', 'format': FORMAT, 'checkpoint': ck, 'actor': state['id'],
              'role': state.get('role'), 'boundary': state.get('boundary'), 'sha256': digest,
              'archive_path': str(folder), 'portable': False, 'scientific': scientific,
              'session': manifest['thread_id'], 'last_turn': state['last_turn_id']}
    with lock(DATA / 'locks' / ('checkpoint-' + ck + '.lock')):
        if (dest / 'COMMITTED').exists():
            verify(ck)
            return read(dest / 'receipt.json')
        dest.mkdir(parents=True, exist_ok=True)
        atomic(dest / 'backend.json', encoded)
        write(dest / 'receipt.json', result)
        atomic(dest / 'COMMITTED', digest + '\n')
    return result


def verify(checkpoint):
    dest = DATA / 'checkpoints' / identity(checkpoint)
    digest = (dest / 'COMMITTED').read_text().strip()
    if sha(dest / 'backend.json') != digest: raise Error('Claude checkpoint reference changed')
    record = read(dest / 'backend.json'); receipt = read(dest / 'receipt.json', {})
    if receipt.get('backend') != 'claude' or receipt.get('checkpoint') != checkpoint or receipt.get('sha256') != digest:
        raise Error('Claude checkpoint receipt changed')
    folder = inside(record['folder'])
    if inventory(folder) != record['files']: raise Error('Claude saved archive set changed')
    result = validate(folder, record['receipt'], record['state'], record['scientific'])
    result.update(checkpoint=checkpoint, record=record)
    return result


def restore(checkpoint, actor, mode='interview'):
    if mode != 'interview': backends.require({'backend': 'claude'}, 'continuation')
    backends.require({'backend': 'claude'}, 'restore')
    record = verify(checkpoint)['record']
    backends.require({**record['state'], 'backend': 'claude'}, 'restore')
    state = backends.claude_module().restore(record['folder'], identity(actor), mode='interview', data=DATA)
    state.update(parent_checkpoint=checkpoint, checkpoint=None)
    write(actor_dir(actor) / 'state.json', state)
    return state


class Actor:
    """Keep foreign runtime state and methods behind an explicit admission gate."""
    def __init__(self, actor):
        self._actor = backends.claude_module().ClaudeActor(actor, data=DATA)

    @property
    def state(self): return self._actor.state
    @property
    def base(self): return self._actor.base
    @property
    def workspace(self): return self._actor.workspace
    @property
    def guard(self): return self._actor.guard
    @property
    def capabilities(self): return backends.capabilities(self.state)
    def save(self): return self._actor.save()
    def release(self): return self._actor.release()
    def open(self):
        backends.require(self.state, 'open'); return self._actor.open()
    def message(self, text):
        backends.require(self.state, 'message'); return self._actor.message(text)
    def answer(self, key, answers):
        backends.require(self.state, 'answer'); return self._actor.answer(key, answers)
    def pause(self):
        backends.require(self.state, 'pause'); return self._actor.pause()
    def interrupt(self):
        backends.require(self.state, 'interrupt'); return self._actor.interrupt()
    def wait(self, timeout=3600): return self._actor.wait(timeout)
    def final(self): return self._actor.final()
    def checkpoint(self, interrupt=False):
        backends.require(self.state, 'checkpoint')
        result = register(self._actor.checkpoint(interrupt=interrupt), self.state)
        self.state.update(checkpoint=result['checkpoint'], controller_checkpoint=result['checkpoint'], status='saved')
        self.save()
        return result
    def close(self):
        backends.require(self.state, 'close')
        result = self._actor.close()
        receipt = register(result, self.state, scientific=True)
        self.state.update(platform_checkpoint=self.state.get('checkpoint'), checkpoint=receipt['checkpoint'],
                          controller_checkpoint=receipt['checkpoint'])
        self.save()
        return receipt
