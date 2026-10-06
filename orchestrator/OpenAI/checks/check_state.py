"""Read-only source check, with explicit optional prepared-run checks."""
from pathlib import Path
import argparse
import csv
import hashlib
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--corpus', action='store_true', help='Also count the rebuilt input store')
parser.add_argument('--run', default='claude-v43-1', help='Prepared Claude run directory name')
parser.add_argument('--fingerprint', help='Expected fingerprint, supplied only after acceptance')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
baseline = Path(__file__).resolve().parents[1] / 'accepted-source.sha256'
expected_digest = 'f019c5d76b9954276b665733f34626fd26198834a14ece58693a1f10db6c7772'
expected = {}
for line in baseline.read_text().splitlines():
    digest, name = line.split('  ', 1)
    expected[name] = digest
actual = {name: hashlib.sha256((repo / name).read_bytes()).hexdigest()
          for name in expected if (repo / name).is_file()}
digest = hashlib.sha256(''.join(f'{name}\t{value}\n' for name, value in sorted(actual.items())).encode()).hexdigest()
with (repo / 'OWNERSHIP.tsv').open() as handle:
    owned = {row['path'] for row in csv.DictReader(handle, delimiter='\t') if row['owner'] == 'codex'}
if Path(args.run).name != args.run or args.run in ('.', '..'):
    parser.error('--run must be a directory name')
run = repo / 'aggregator/runs' / args.run
result = {
    'source_files': len(expected),
    'source_digest': digest,
    'source_changed_or_missing': sorted(name for name in expected if actual.get(name) != expected[name]),
    'ownership_added': sorted(owned - set(expected)),
    'ownership_removed': sorted(set(expected) - owned),
    'prepared_run': str(run),
    'run_present': (run / 'CONTROL/RUN.json').is_file(),
    'run_checks': 'requested' if args.corpus or args.fingerprint else 'not_requested',
    'passed': digest == expected_digest and owned == set(expected),
}
if (args.corpus or args.fingerprint) and not result['run_present']:
    result.update(passed=False, run_checks='unavailable', error='Prepared run is absent; build and acceptance await J.')
if args.fingerprint and result['run_present']:
    fingerprint = json.loads((run / 'CONTROL/RUN.json').read_text()).get('fingerprint')
    result['claude_fingerprint'] = fingerprint
    result['passed'] &= fingerprint == args.fingerprint
if args.corpus and result['run_present']:
    store = run / '00_GIVE-THE-AGENT/package/store'
    with (store / 'rooms.jsonl').open() as handle:
        rooms = [json.loads(line)['sub'] for line in handle if line.strip()]
    counts = {'rooms': len(rooms), 'distinct_rooms': len(set(rooms))}
    for name in ('codes', 'themes'):
        with (store / f'{name}.jsonl').open() as handle:
            counts[name] = sum(bool(line.strip()) for line in handle)
    result['corpus'] = counts
    result['passed'] &= counts == {'rooms': 705, 'distinct_rooms': 705, 'codes': 115388, 'themes': 7844}
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['passed'] else 1)
