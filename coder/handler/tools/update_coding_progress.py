from pathlib import Path
import datetime
import json

yard = Path(__file__).resolve().parents[1]
items = []
suffix = '-gpt56-calibration-v1'
store_names = {p.name[:-len(suffix)] for p in (yard / '_lead_sessions').glob('*' + suffix)}
store_names |= {p.name[:-len(suffix + '.tar.zst')]
                for p in (yard / '_lead_sessions').glob('*' + suffix + '.tar.zst')}
for sub in store_names:
    room = yard / 'rooms' / sub
    state = json.loads((room / 'STATE.json').read_text())
    store = yard / '_lead_sessions' / (sub + '-gpt56-calibration-v1')
    archive = store.with_name(store.name + '.tar.zst')
    status = state.get('coding_status', 'queued')
    if store.is_dir() and (store / 'RUNNING.json').exists():
        status = 'lead running'
    elif status == 'lead first turn running':
        status = 'first lead checkpoint saved'
    receipt = room / 'validation/RUN-RECEIPT.json'
    tokens = None
    if receipt.exists():
        tokens = json.loads(receipt.read_text()).get('reported_total_tokens')
    items.append({'subreddit': sub, 'items': state['items_in_window'], 'status': status,
                  'reported_tokens': tokens,
                  'store': str(store if store.exists() else archive),
                  'store_kind': 'directory' if store.exists() else 'tar.zst',
                  'canonical_room': str(room)})
items.sort(key=lambda r: (r['items'], r['subreddit']))
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
data = {'updated_utc': now, 'model': 'gpt-5.6-sol', 'effort': 'xhigh',
        'prompt_version': 'lead-calibration-v1', 'rooms': items}
text = '# Coding progress\n\nUpdated: ' + now + '\n\nModel: GPT-5.6 Sol. Prompt: lead-calibration-v1.\n\n'
text += '| Subreddit | Items | Status | Reported tokens |\n|---|---:|---|---:|\n'
for r in items:
    text += '| {subreddit} | {items} | {status} | {tokens} |\n'.format(**r, tokens=f"{r['reported_tokens']:,}" if r['reported_tokens'] is not None else '—')
text += '\nTokens are reported input plus output, including cached input; they are not a cost estimate.\n'
text += 'Idle case-lead stores are kept as verified tar.zst archives and restored before native continuation. Completed run mirrors and validation receipts are in each canonical room.\n'
(yard / 'CODING-PROGRESS.json').write_text(json.dumps(data, indent=2) + '\n')
(yard / 'CODING-PROGRESS.md').write_text(text)
outputs = Path('/Users/arrieta/Documents/Codex/2026-09-07/in-x20/outputs')
(outputs / 'CODING-PROGRESS.md').write_text(text)
print(json.dumps(data, indent=2))
