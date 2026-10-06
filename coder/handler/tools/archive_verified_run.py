#!/usr/bin/env python3
"""Archive or restore the canonical run of a verified room, one room at a time."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

YARD = Path(__file__).resolve().parents[1]
ZSTD = shutil.which('zstd') or '/opt/homebrew/bin/zstd'
TAR = shutil.which('bsdtar') or '/usr/bin/bsdtar'


def digest(path):
    sha = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            sha.update(chunk)
    return sha.hexdigest()


def inventory(root):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(base) / name
            rel = str(path.relative_to(root))
            if path.is_symlink():
                result[rel] = ('symlink', os.readlink(path))
            elif path.is_file():
                result[rel] = ('file', digest(path))
            elif path.is_dir():
                result[rel] = ('dir', '')
            else:
                raise RuntimeError('Unsupported entry: ' + str(path))
    return result


def members(archive):
    zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
    tar = subprocess.run([TAR, '-tf', '-'], stdin=zstd.stdout,
                         text=True, capture_output=True)
    zstd.stdout.close()
    if zstd.wait() or tar.returncode:
        raise RuntimeError('Archive listing failed: ' + tar.stderr[-1000:])
    names = [x.rstrip('/') for x in tar.stdout.splitlines() if x.strip()]
    if not names or any(x != 'run' and not x.startswith('run/') for x in names):
        raise RuntimeError('Archive contains a path outside run/')
    return names


def test_archive(archive, expected=None):
    subprocess.run([ZSTD, '-q', '-t', str(archive)], check=True)
    names = members(archive)
    temp = Path(tempfile.mkdtemp(prefix='.run-archive-check-'))
    try:
        zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
        tar = subprocess.run([TAR, '-xf', '-', '-C', str(temp)], stdin=zstd.stdout)
        zstd.stdout.close()
        if zstd.wait() or tar.returncode or not (temp / 'run').is_dir():
            raise RuntimeError('Run archive failed test extraction')
        actual = inventory(temp / 'run')
        if expected is not None and actual != expected:
            raise RuntimeError('Test extraction differs from source run')
        for required in ['_manifest.json', 'out/_run.json']:
            json.loads((temp / 'run' / required).read_text())
        return len(names)
    finally:
        shutil.rmtree(temp)


def save_state(path, state):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as stream:
        json.dump(state, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)


def paths(sub):
    if not re.fullmatch(r'[A-Za-z0-9_]+', sub):
        raise RuntimeError('Invalid subreddit name')
    room = YARD / 'rooms' / sub
    return room, room / 'run', room / 'run.tar.zst', room / 'STATE.json'


def archive_one(sub):
    room, run, archive, state_path = paths(sub)
    state = json.loads(state_path.read_text())
    if state.get('coding_status') != 'verified' or not state.get('verified_utc'):
        raise RuntimeError(sub + ' is not verified')
    if not (room / 'validation/RUN-RECEIPT.json').is_file():
        raise RuntimeError(sub + ' has no verified-run receipt')
    queue_path = YARD / '_coding_queue/STATE.json'
    queue = json.loads(queue_path.read_text()) if queue_path.exists() else {}
    if sub in queue.get('active', {}):
        raise RuntimeError(sub + ' is active')
    if not run.is_dir() and archive.is_file():
        count = test_archive(archive)
        sha = digest(archive)
    elif run.is_dir():
        expected = inventory(run)
        if archive.is_file():
            count = test_archive(archive, expected)
            sha = digest(archive)
        else:
            partial = room / 'run.tar.zst.partial'
            partial.unlink(missing_ok=True)
            tar = subprocess.Popen([TAR, '-cf', '-', 'run'], cwd=room,
                                   stdout=subprocess.PIPE)
            packed = subprocess.run([ZSTD, '-q', '-T0', '-6', '-o', str(partial)],
                                    stdin=tar.stdout)
            tar.stdout.close()
            if tar.wait() or packed.returncode:
                partial.unlink(missing_ok=True)
                raise RuntimeError('Run compression failed')
            if inventory(run) != expected:
                partial.unlink(missing_ok=True)
                raise RuntimeError('Run changed during compression')
            count = test_archive(partial, expected)
            sha = digest(partial)
            partial.replace(archive)
        state['run_archive'] = str(archive)
        state['run_archive_sha256'] = sha
        state['run_archive_bytes'] = archive.stat().st_size
        state['run_archived_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save_state(state_path, state)
        shutil.rmtree(run)
    else:
        raise RuntimeError(sub + ' has neither run/ nor a run archive')
    if not state.get('run_archive'):
        state['run_archive'] = str(archive)
        state['run_archive_sha256'] = sha
        state['run_archive_bytes'] = archive.stat().st_size
        state['run_archived_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save_state(state_path, state)
    return {'subreddit': sub, 'archive': str(archive), 'sha256': sha,
            'bytes': archive.stat().st_size, 'members': count}


def restore_one(sub):
    room, run, archive, state_path = paths(sub)
    state = json.loads(state_path.read_text())
    if run.exists() or not archive.is_file():
        raise RuntimeError('Expected only the compressed run archive')
    if digest(archive) != state.get('run_archive_sha256'):
        raise RuntimeError('Run archive checksum differs from STATE.json')
    test_archive(archive)
    temp = Path(tempfile.mkdtemp(prefix='.run-restore-', dir=room))
    try:
        zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
        tar = subprocess.run([TAR, '-xf', '-', '-C', str(temp)], stdin=zstd.stdout)
        zstd.stdout.close()
        if zstd.wait() or tar.returncode or not (temp / 'run').is_dir():
            raise RuntimeError('Run restore failed')
        (temp / 'run').rename(run)
    finally:
        shutil.rmtree(temp)
    return {'subreddit': sub, 'restored': str(run), 'archive_retained': str(archive)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['archive', 'restore', 'archive-all'])
    parser.add_argument('subreddit', nargs='?')
    args = parser.parse_args()
    if args.command == 'archive-all':
        candidates = []
        for room in (YARD / 'rooms').iterdir():
            run = room / 'run'
            state_path = room / 'STATE.json'
            if not run.is_dir() or not state_path.is_file():
                continue
            try:
                state = json.loads(state_path.read_text())
            except (OSError, ValueError):
                continue
            if state.get('coding_status') == 'verified':
                size = sum(path.stat().st_size for path in run.rglob('*') if path.is_file())
                candidates.append((size, room.name))
        errors = []
        for size, sub in sorted(candidates, reverse=True):
            try:
                result = archive_one(sub)
                result['source_bytes'] = size
                print(json.dumps(result), flush=True)
                subprocess.run([sys.executable, '-B', str(YARD / '_tools/status.py'),
                                '--yard', str(YARD), '--no-refresh'],
                               stdout=subprocess.DEVNULL, check=True)
            except Exception as exc:
                errors.append((sub, str(exc)))
                print(json.dumps({'subreddit': sub, 'error': str(exc)}), flush=True)
        print(json.dumps({'archived': len(candidates) - len(errors),
                          'errors': errors}), flush=True)
        if errors:
            raise SystemExit(1)
        return
    if not args.subreddit:
        parser.error('subreddit is required')
    result = archive_one(args.subreddit) if args.command == 'archive' else restore_one(args.subreddit)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
