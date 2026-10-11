"""Handler metrics for a closed leg: python3 leg_metrics.py RUN_DIR LEG ACTOR_DIR START_ISO"""
import json, sys, collections, datetime as dt
run, leg, actor, start = sys.argv[1:5]
def ts(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
t0 = ts(start)
seen = {}; first = last = None
for l in open(f'{run}/CONTROL/snapshots/B1.{leg}/transcript.jsonl'):
    d = json.loads(l)
    if d.get('type') != 'assistant' or 'timestamp' not in d: continue
    t = ts(d['timestamp'])
    if t < t0: continue
    m = d.get('message', {}); mid = m.get('id'); u = m.get('usage') or {}
    if not mid: continue
    seen[mid] = u; first = first or t; last = t
ctx = [u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0) for u in seen.values()]
cr = sum(u.get('cache_read_input_tokens', 0) for u in seen.values()); out = sum(u.get('output_tokens', 0) for u in seen.values())
print(f'calls {len(seen)}, mean ctx {sum(ctx)/len(ctx)/1e3:.0f}k, cache read {cr/1e6:.1f}M, output {out/1e3:.0f}k, span {first:%H:%M}-{last:%H:%M}Z {(last-first).total_seconds()/60:.0f} min')
starts = []
for l in open(f'{actor}/events.jsonl'):
    d = json.loads(l); n = d.get('native') or {}
    if n.get('method') != 'item/started': continue
    it = (n.get('params') or {}).get('item') or {}
    if it.get('type') in ('userMessage', 'agentMessage', 'reasoning'): continue
    starts.append(ts(d['utc']))
starts.sort(); groups = []
for s in starts:
    if groups and (s - groups[-1][-1]).total_seconds() <= 1.5: groups[-1].append(s)
    else: groups.append([s])
print(f'tool items {len(starts)}, groups {len(groups)}, single-call share {sum(1 for g in groups if len(g)==1)/len(groups):.2f}')
