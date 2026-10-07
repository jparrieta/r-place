# Handler's own audit of the A1 catch-up, independent of checks/stage_A1.py.
# For each block's room: case.md and brief.md served whole (union of read spans = total lines),
# and a note line for the room logged in that block's leg after both reads.
import json, sys, glob, os, collections
OUT = sys.argv[1] if len(sys.argv) > 1 else 'aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out'
lo, hi = (int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '20-33').split('-'))
blocks = collections.defaultdict(list)
for l in open(os.path.join(OUT, '_analysis/catchup-A1.tsv')).read().splitlines()[1:]:
    b, tier, sub = l.split('\t')[:3]; blocks[int(b)].append(sub)
spans = collections.defaultdict(list); total = {}; last_read = {}
for l in open(os.path.join(OUT, '_mem_reads-A1.jsonl')):
    o = json.loads(l)
    if o['verb'] in ('case', 'brief') and o['args'] and not o.get('refused'):
        k = (o['verb'], o['args'][0]); s = o['offset']
        spans[k].append((s, s + o['lines'])); total[k] = o['total']; last_read[k] = o['t']
def whole(k):
    if k not in total: return False
    cov = 0; end = 0
    for a, b in sorted(spans[k]):
        if b > end: cov += b - max(a, end); end = b
    return cov >= total[k]
notes = collections.defaultdict(list)
for f in glob.glob(os.path.join(OUT, 'diary', '*.jsonl')):
    for l in open(f):
        try: o = json.loads(l)
        except Exception: continue
        if o.get('kind') == 'note' and str(o.get('leg', '')).startswith('A1b-'):
            notes[o['leg']].append((o['t'], o.get('text', '')))
bad = 0
for b in range(lo, hi + 1):
    leg = 'A1b-%02d' % b; probs = []
    for sub in blocks[b]:
        for v in ('case', 'brief'):
            if not whole((v, sub)): probs.append('%s %s not whole' % (sub, v))
        hit = [t for t, x in notes[leg] if sub in x]
        if not hit: probs.append('%s no note in %s' % (sub, leg))
        elif all(max(last_read.get(('case', sub), ''), last_read.get(('brief', sub), '')) > t for t in hit):
            probs.append('%s note before reads' % sub)
    bad += len(probs)
    print('%s: %d rooms, %s' % (leg, len(blocks[b]), 'ok' if not probs else '; '.join(probs[:6]) + (' ...' if len(probs) > 6 else '')))
print('problems', bad)
