#!/usr/bin/env python3
"""Archive and restore complete case-lead stores one at a time."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checkpoints import locked

YARD = Path(__file__).resolve().parents[1]
SESSIONS = YARD / '_lead_sessions'
SUFFIX = '-gpt56-calibration-v1'
ARCHIVE_SUFFIX = '.tar.zst'
ZSTD = shutil.which('zstd') or '/opt/homebrew/bin/zstd'
BSDTAR = shutil.which('bsdtar') or '/usr/bin/bsdtar'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)


def paths(sub):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', sub):
        raise RuntimeError('Invalid subreddit name.')
    store = SESSIONS / (sub + SUFFIX)
    return store, store.with_name(store.name + ARCHIVE_SUFFIX), YARD / 'rooms' / sub


def locked_archive():
    SESSIONS.mkdir(exist_ok=True)
    stream = (SESSIONS / '.archive.lock').open('a+')
    fcntl.flock(stream, fcntl.LOCK_EX)
    return stream


def archive_members(archive):
    zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
    tar = subprocess.run([BSDTAR, '-tf', '-'], stdin=zstd.stdout, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    zstd.stdout.close()
    zstd_code = zstd.wait()
    if zstd_code or tar.returncode:
        raise RuntimeError('Archive listing failed: ' + tar.stderr[-1000:])
    return [line.rstrip('/') for line in tar.stdout.splitlines() if line.strip()]


def tree_inventory(root):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base = Path(base)
        for name in sorted(dirs + files):
            path = base / name
            rel = str(path.relative_to(root))
            if path.is_symlink():
                result[rel] = ['symlink', os.readlink(path)]
            elif path.is_file():
                result[rel] = ['file', digest(path)]
            elif path.is_dir():
                result[rel] = ['dir', '']
            else:
                raise RuntimeError('Unsupported filesystem entry: ' + str(path))
    return result


def extract_checked(archive, root_name, expected=None):
    temp = Path(tempfile.mkdtemp(prefix='.archive-check-', dir=SESSIONS))
    try:
        zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
        tar = subprocess.run([BSDTAR, '-xf', '-', '-C', str(temp)], stdin=zstd.stdout)
        zstd.stdout.close()
        zstd_code = zstd.wait()
        root = temp / root_name
        if zstd_code or tar.returncode or not root.is_dir():
            raise RuntimeError(f'Archive test extraction failed: zstd={zstd_code}, tar={tar.returncode}')
        actual = tree_inventory(root)
        if expected is not None and actual != expected:
            raise RuntimeError('Test-extracted archive differs from the source inventory.')
        for required in ['STORE.json', 'HEAD.json', 'state/lead.json']:
            json.loads((root / required).read_text())
        return actual
    finally:
        shutil.rmtree(temp, ignore_errors=True)


def validate_archive(archive, root_name):
    subprocess.run([ZSTD, '-q', '-t', str(archive)], check=True)
    members = archive_members(archive)
    if not members or any(name != root_name and not name.startswith(root_name + '/') for name in members):
        raise RuntimeError('Archive contains a path outside its case-lead root.')
    required = {root_name + '/STORE.json', root_name + '/HEAD.json', root_name + '/state/lead.json'}
    missing = required - set(members)
    if missing:
        raise RuntimeError('Archive is missing fork state: ' + ', '.join(sorted(missing)))
    return len(members)


def update_room(sub, store=None, archive=None, sha256=None, archive_bytes=None):
    _, _, room = paths(sub)
    state_path = room / 'STATE.json'
    if not state_path.exists():
        return
    state = json.loads(state_path.read_text())
    if archive:
        state['lead_archive'] = str(archive)
        state['lead_archive_sha256'] = sha256
        state['lead_archive_bytes'] = archive_bytes
        state.pop('lead_store', None)
        note = 'Compressed complete forkable case-lead store after work ended.'
    else:
        state['lead_store'] = str(store)
        state.pop('lead_archive', None)
        state.pop('lead_archive_sha256', None)
        state.pop('lead_archive_bytes', None)
        note = 'Restored compressed case-lead store for continuation.'
    state.setdefault('notes', []).append({'at': now(), 'note': note})
    atomic_json(state_path, state)


def archive_one(sub):
    store, archive, _ = paths(sub)
    lock = locked_archive()
    try:
        if archive.exists() and not store.exists():
            members = validate_archive(archive, store.name)
            archive_sha = digest(archive)
            extract_checked(archive, store.name)
            update_room(sub, archive=archive, sha256=archive_sha,
                        archive_bytes=archive.stat().st_size)
            return {'subreddit': sub, 'status': 'already-archived', 'archive': str(archive),
                    'bytes': archive.stat().st_size, 'members': members, 'sha256': archive_sha}
        if not store.is_dir():
            raise RuntimeError('Case-lead store does not exist: ' + str(store))
        with locked(store):
            if (store / 'RUNNING.json').exists():
                raise RuntimeError('Case lead is running; archive only after it exits.')
            if archive.exists():
                archived_inventory = extract_checked(archive, store.name)
                if archived_inventory != tree_inventory(store):
                    raise RuntimeError('Both archive and a different source store exist.')
                archive_sha = digest(archive)
                members = validate_archive(archive, store.name)
                update_room(sub, archive=archive, sha256=archive_sha,
                            archive_bytes=archive.stat().st_size)
                shutil.rmtree(store)
                return {'subreddit': sub, 'status': 'reconciled-archive', 'archive': str(archive),
                        'bytes': archive.stat().st_size, 'members': members, 'sha256': archive_sha}
            marker = {'version': 1, 'subreddit': sub, 'store_name': store.name,
                      'created_utc': now(), 'format': 'tar+zstd',
                      'restore_tool': str(Path(__file__).resolve())}
            atomic_json(store / 'ARCHIVE.json', marker)
            source_inventory = tree_inventory(store)
            partial = archive.with_name(archive.name + '.partial')
            partial.unlink(missing_ok=True)
            tar = subprocess.Popen([BSDTAR, '-cf', '-', store.name], cwd=SESSIONS,
                                   stdout=subprocess.PIPE)
            zstd = subprocess.run([ZSTD, '-q', '-T0', '-6', '-o', str(partial)],
                                  stdin=tar.stdout)
            tar.stdout.close()
            tar_code = tar.wait()
            if tar_code or zstd.returncode:
                partial.unlink(missing_ok=True)
                raise RuntimeError(f'Compression failed: tar={tar_code}, zstd={zstd.returncode}')
            if tree_inventory(store) != source_inventory:
                partial.unlink(missing_ok=True)
                raise RuntimeError('Case-lead store changed during compression.')
            members = validate_archive(partial, store.name)
            extract_checked(partial, store.name, source_inventory)
            archive_sha = digest(partial)
            os.replace(partial, archive)
            update_room(sub, archive=archive, sha256=archive_sha,
                        archive_bytes=archive.stat().st_size)
            shutil.rmtree(store)
        return {'subreddit': sub, 'status': 'archived', 'archive': str(archive),
                'bytes': archive.stat().st_size, 'members': members, 'sha256': archive_sha}
    finally:
        lock.close()


def restore_one(sub):
    store, archive, room = paths(sub)
    lock = locked_archive()
    try:
        if store.is_dir() and not archive.exists():
            return {'subreddit': sub, 'status': 'already-restored', 'store': str(store)}
        if store.exists() or not archive.is_file():
            raise RuntimeError('Expected exactly one compressed case-lead archive.')
        state_path = room / 'STATE.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        expected_sha = state.get('lead_archive_sha256')
        if not expected_sha:
            raise RuntimeError('Room state has no required archive SHA-256.')
        actual_sha = digest(archive)
        if actual_sha != expected_sha:
            raise RuntimeError('Archive checksum differs from room state.')
        members = validate_archive(archive, store.name)
        temp = Path(tempfile.mkdtemp(prefix='.restore-', dir=SESSIONS))
        try:
            zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
            tar = subprocess.run([BSDTAR, '-xf', '-', '-C', str(temp)], stdin=zstd.stdout)
            zstd.stdout.close()
            zstd_code = zstd.wait()
            if zstd_code or tar.returncode or not (temp / store.name).is_dir():
                raise RuntimeError(f'Restore failed: zstd={zstd_code}, tar={tar.returncode}')
            (temp / store.name).rename(store)
        finally:
            shutil.rmtree(temp, ignore_errors=True)
        update_room(sub, store=store)
        descriptor_path = store / 'STORE.json'
        descriptor = json.loads(descriptor_path.read_text())
        relocated = dict(descriptor)
        relocated.update({'source_room': str(room), 'store_path': str(store),
                          'room': str(store / 'workspace' / 'room'),
                          'cwd': str(store / 'workspace' / 'room' / 'run')})
        if relocated != descriptor:
            atomic_json(descriptor_path, relocated)
            runtime_path = store / 'state' / 'runtime.json'
            if runtime_path.exists():
                atomic_json(runtime_path, relocated)
        archive.unlink()
        return {'subreddit': sub, 'status': 'restored', 'store': str(store),
                'members': members, 'sha256': actual_sha}
    finally:
        lock.close()


def archive_all():
    stores = [path for path in SESSIONS.iterdir()
              if path.is_dir() and path.name.endswith(SUFFIX)]
    stores.sort(key=lambda path: sum(f.stat().st_size for f in path.rglob('*') if f.is_file()),
                reverse=True)
    results = []
    for store in stores:
        sub = store.name[:-len(SUFFIX)]
        result = archive_one(sub)
        results.append(result)
        print(json.dumps(result), flush=True)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['archive', 'restore', 'archive-all'])
    parser.add_argument('subreddit', nargs='?')
    args = parser.parse_args()
    if args.command == 'archive-all':
        archive_all()
    elif not args.subreddit:
        parser.error('subreddit is required')
    elif args.command == 'archive':
        print(json.dumps(archive_one(args.subreddit), indent=2))
    else:
        print(json.dumps(restore_one(args.subreddit), indent=2))


if __name__ == '__main__':
    main()
