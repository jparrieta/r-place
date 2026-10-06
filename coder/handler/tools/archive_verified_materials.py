#!/usr/bin/env python3
"""Archive or restore record, brief, and instrument in verified rooms."""

import argparse
import datetime
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from archive_verified_run import YARD, ZSTD, TAR, digest, inventory, save_state

PARTS = ('record', 'brief', 'instrument')


def paths(sub):
    if not re.fullmatch(r'[A-Za-z0-9_]+', sub):
        raise RuntimeError('Invalid subreddit name')
    room = YARD / 'rooms' / sub
    return room, room / 'materials.tar.zst', room / 'STATE.json'


def inventories(root):
    return {part: inventory(root / part) for part in PARTS}


def test_archive(archive, expected=None):
    subprocess.run([ZSTD, '-q', '-t', str(archive)], check=True)
    zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
    tar = subprocess.run([TAR, '-tf', '-'], stdin=zstd.stdout,
                         text=True, capture_output=True)
    zstd.stdout.close()
    if zstd.wait() or tar.returncode:
        raise RuntimeError('Materials archive listing failed')
    names = [x.rstrip('/') for x in tar.stdout.splitlines() if x.strip()]
    if not names or any(not any(x == p or x.startswith(p + '/') for p in PARTS)
                        for x in names):
        raise RuntimeError('Materials archive contains an unexpected path')
    temp = Path(tempfile.mkdtemp(prefix='.materials-archive-check-'))
    try:
        zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
        tar = subprocess.run([TAR, '-xf', '-', '-C', str(temp)], stdin=zstd.stdout)
        zstd.stdout.close()
        if zstd.wait() or tar.returncode or any(not (temp / p).is_dir() for p in PARTS):
            raise RuntimeError('Materials archive failed test extraction')
        actual = inventories(temp)
        if expected is not None and actual != expected:
            raise RuntimeError('Materials test extraction differs from source')
        json.loads((temp / 'brief/_manifest.json').read_text())
        for required in ('brief/out/brief.md', 'record/openings.md', 'instrument/newrun.py'):
            if not (temp / required).is_file():
                raise RuntimeError('Materials archive misses ' + required)
        return len(names)
    finally:
        shutil.rmtree(temp)


def archive_one(sub):
    room, archive, state_path = paths(sub)
    state = json.loads(state_path.read_text())
    if state.get('coding_status') != 'verified' or not state.get('verified_utc'):
        raise RuntimeError(sub + ' is not verified')
    if not (room / 'validation/RUN-RECEIPT.json').is_file():
        raise RuntimeError(sub + ' has no verified-run receipt')
    queue_path = YARD / '_coding_queue/STATE.json'
    queue = json.loads(queue_path.read_text()) if queue_path.exists() else {}
    if sub in queue.get('active', {}):
        raise RuntimeError(sub + ' is active')
    present = [p for p in PARTS if (room / p).is_dir()]
    if present and len(present) != len(PARTS):
        raise RuntimeError(sub + ' has a partial materials directory set')
    if not present and archive.is_file():
        count = test_archive(archive)
        sha = digest(archive)
    elif present:
        expected = inventories(room)
        if archive.is_file():
            count = test_archive(archive, expected)
            sha = digest(archive)
        else:
            partial = room / 'materials.tar.zst.partial'
            partial.unlink(missing_ok=True)
            tar = subprocess.Popen([TAR, '-cf', '-', *PARTS], cwd=room,
                                   stdout=subprocess.PIPE)
            packed = subprocess.run([ZSTD, '-q', '-T0', '-6', '-o', str(partial)],
                                    stdin=tar.stdout)
            tar.stdout.close()
            if tar.wait() or packed.returncode:
                partial.unlink(missing_ok=True)
                raise RuntimeError('Materials compression failed')
            if inventories(room) != expected:
                partial.unlink(missing_ok=True)
                raise RuntimeError('Materials changed during compression')
            count = test_archive(partial, expected)
            sha = digest(partial)
            partial.replace(archive)
        state['materials_archive'] = str(archive)
        state['materials_archive_sha256'] = sha
        state['materials_archive_bytes'] = archive.stat().st_size
        state['materials_archived_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save_state(state_path, state)
        for part in PARTS:
            shutil.rmtree(room / part)
    else:
        raise RuntimeError(sub + ' has neither materials nor an archive')
    if not state.get('materials_archive'):
        state['materials_archive'] = str(archive)
        state['materials_archive_sha256'] = sha
        state['materials_archive_bytes'] = archive.stat().st_size
        state['materials_archived_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save_state(state_path, state)
    return {'subreddit': sub, 'archive': str(archive), 'sha256': sha,
            'bytes': archive.stat().st_size, 'members': count}


def restore_one(sub):
    room, archive, state_path = paths(sub)
    state = json.loads(state_path.read_text())
    if any((room / p).exists() for p in PARTS) or not archive.is_file():
        raise RuntimeError('Expected only the compressed materials archive')
    if digest(archive) != state.get('materials_archive_sha256'):
        raise RuntimeError('Materials archive checksum differs from STATE.json')
    test_archive(archive)
    temp = Path(tempfile.mkdtemp(prefix='.materials-restore-', dir=room))
    try:
        zstd = subprocess.Popen([ZSTD, '-qdc', str(archive)], stdout=subprocess.PIPE)
        tar = subprocess.run([TAR, '-xf', '-', '-C', str(temp)], stdin=zstd.stdout)
        zstd.stdout.close()
        if zstd.wait() or tar.returncode or any(not (temp / p).is_dir() for p in PARTS):
            raise RuntimeError('Materials restore failed')
        for part in PARTS:
            (temp / part).rename(room / part)
    finally:
        shutil.rmtree(temp)
    return {'subreddit': sub, 'restored': list(PARTS), 'archive_retained': str(archive)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['archive', 'restore', 'archive-all'])
    parser.add_argument('subreddit', nargs='?')
    args = parser.parse_args()
    if args.command == 'archive-all':
        candidates = []
        for room in (YARD / 'rooms').iterdir():
            state_path = room / 'STATE.json'
            if not state_path.is_file() or any(not (room / p).is_dir() for p in PARTS):
                continue
            try:
                state = json.loads(state_path.read_text())
            except (OSError, ValueError):
                continue
            if state.get('coding_status') == 'verified':
                size = sum(path.stat().st_size for part in PARTS
                           for path in (room / part).rglob('*') if path.is_file())
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
