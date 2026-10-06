"""Prepare one authorised room and run its first calibrated native lead turn."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

YARD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(YARD / '_tools'))
import room

sub = sys.argv[1]
assert re.fullmatch(r'[A-Za-z0-9_]+', sub)
source = YARD / 'rooms' / sub
store = YARD / '_lead_sessions' / (sub + '-gpt56-calibration-v1')
archive = store.with_name(store.name + '.tar.zst')
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
PRIOR_RUN_RECODE_ALLOWLIST = {'liverpoolfc'}

def run(args):
    return subprocess.run([sys.executable, '-B', *map(str, args)], env=env, check=True)

if (source / 'run').exists() or store.exists() or archive.exists():
    raise SystemExit('Existing run or store; inspect before continuing.')
source_state = room.load_state(str(source))
count = source_state.get('items_in_window') if source_state else None
if not isinstance(count, int) or not 500 <= count <= 50000:
    raise SystemExit('Missing room state or outside the authorised 500..50000 item range.')
if (sub not in PRIOR_RUN_RECODE_ALLOWLIST
        and any(r.get('kind') == 'coder' for r in source_state.get('prior_runs', []))):
    raise SystemExit('Previously coded room: outside this wave.')
v = room._brief_validation(str(source))
if v['required'] and not v['passed']:
    run([YARD / '_tools/room.py', 'check', '--room', source, '--brief'])
v = room._brief_validation(str(source))
if v['required'] and not v['passed']:
    raise SystemExit('Brief has no current passing receipt.')

run([YARD / '_tools/codex_lead.py', '--store', store, 'init', '--room', source,
     '--model', 'gpt-5.6-sol', '--effort', 'medium'])
doc = (YARD / 'CASE-LEAD-PROMPT.md').read_bytes()
calibration = doc.decode().split('<!-- BEGIN LEAD PROMPT -->', 1)[1].split('<!-- END LEAD PROMPT -->', 1)[0].strip()
base = subprocess.check_output([sys.executable, '-B', str(YARD / '_tools/room.py'),
                              'message', 'lead', '--room', str(store / 'workspace/room')],
                             text=True, env=env)
prompt = (base.rstrip() + '\n\n' + calibration + '\n').encode()
prompt_file = store / 'state/lead-opening.txt'
prompt_file.write_bytes(prompt)
receipt = {'version': 'lead-calibration-v2', 'model': 'gpt-5.6-sol', 'effort': 'medium',
           'document': str(YARD / 'CASE-LEAD-PROMPT.md'),
           'document_sha256': hashlib.sha256(doc).hexdigest(),
           'message_sha256': hashlib.sha256(prompt).hexdigest(),
           'message_path': str(prompt_file), 'created_utc': room.now(),
           'source_brief_sha256': hashlib.sha256((source / 'brief/out/brief.md').read_bytes()).hexdigest()}
(store / 'state/prompting.json').write_text(json.dumps(receipt, indent=2) + '\n')
st = room.load_state(str(source))
st['lead_store'] = str(store)
st['lead_model'] = 'gpt-5.6-sol'
st['lead_prompt_version'] = receipt['version']
st['coding_status'] = 'lead first turn running'
st.setdefault('notes', []).append({'at': room.now(), 'note': 'Started native case lead using lead-calibration-v2; completed runs will be mirrored here. Source brief retained.'})
room.save_state(str(source), st)
run([YARD / '_tools/codex_lead.py', '--store', store, 'turn', '--prompt-file', prompt_file,
     '--label', 'lead-first'])
if '--complete' in sys.argv[2:]:
    run([Path(__file__).resolve().parent / 'continue_yard_room.py', sub])
