#!/usr/bin/env python3
"""Attach a preserved completed coder stream after a failed atomic attachment."""
import argparse
import hashlib
import json
from pathlib import Path

from checkpoints import atomic, capture, locked, now, read_json


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--store', required=True)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--audit', required=True)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()

    store = Path(args.store).resolve()
    audit = Path(args.audit).resolve()
    receipt = read_json(audit / 'receipt.json')
    source = audit / 'stdout.jsonl'
    data = source.read_bytes()
    parsed = rows(source)
    if receipt.get('status') != 'failed-not-attached':
        raise SystemExit('Audit is not a preserved failed attachment.')
    if not any(r.get('type') == 'turn.completed' for r in parsed):
        raise SystemExit('Preserved stream has no completed turn.')
    if not any(r.get('type') == 'item.completed' and r.get('item', {}).get('type') == 'agent_message'
               for r in parsed):
        raise SystemExit('Preserved stream has no agent message.')

    target = store / 'workspace/room/run/fleet' / ('batch_' + args.batch.zfill(2)) / 'out/_transcript.jsonl'
    if target.read_bytes():
        raise SystemExit('Target transcript is not empty.')
    recovery = {
        'kind': 'exact-coder-stream-attachment',
        'created_utc': now(),
        'source': str(source),
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'source_bytes': len(data),
        'original_receipt': str(audit / 'receipt.json'),
        'original_status': receipt['status'],
        'batch': args.batch.zfill(2),
    }
    with locked(store):
        if (store / 'RUNNING.json').exists():
            raise SystemExit('Store is busy.')
        atomic(target, data)
        recovery_path = store / 'state' / ('transcript-recovery-' + args.batch.zfill(2) + '.json')
        atomic(recovery_path, (json.dumps(recovery, indent=2) + '\n').encode())
        checkpoint = capture(store, {'kind': 'completed', 'agent': 'scheduler-transcript-recovery',
                                     'recovery': recovery}, args.label)
    print(json.dumps({'checkpoint': checkpoint, **recovery}, indent=2))


if __name__ == '__main__':
    main()
