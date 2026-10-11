"""Handler, read-only: Chao2 estimates after each room of B1 in read order, from saturation.py's own
replay and ledger. Run from the run's 00_GIVE-THE-AGENT. Prints the first room at which each stopping
criterion holds, with the share of words read."""
import sys, os, collections, json
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
import saturation as S
root, out = '.', 'out'
st = S.store(root)
R = S.replay(root, out, 'B1', st)
seq = R['seq']
an = set(S.analysed(root, out, st))
w = S.words(st); tot = sum(w[s] for s in an)
by_at = collections.defaultdict(list)
for at, sub, k in S.holdings(root, out, an):
    by_at[at].append((sub, k))
held, waiting, read = collections.defaultdict(set), collections.defaultdict(set), set()
rows, cw = [], 0
for i, r in enumerate(seq, 1):
    read.add(r); cw += w[r]
    held[r] |= waiting.pop(r, set())
    for sub, k in by_at[r]:
        (held if sub in read else waiting)[sub].add(k)
    e = S.estimates([held[x] for x in seq[:i]])
    if e['Q0'] is None: continue
    comp = e['S'] / (e['S'] + e['Q0'])
    rows.append((i, cw / tot, e['S'], e['Q1'], e['Q2'], e['C'], e['Q0'], comp))
print('last', rows[-1], 'status T', R['now']['T'], 'S', R['now']['S'], 'Q0', R['now']['Q0'], 'C', R['now']['C'])
def first(name, f):
    for row in rows:
        if row[0] >= 30 and f(row):
            print('%-28s room %4d  words %5.1f%%  S %3d  C %.4f  Q0 %6.2f  S/Chao2 %.3f' % (name, row[0], 100*row[1], row[2], row[5], row[6], row[7])); return
    print('%-28s never' % name)
for t in (0.95, 0.99, 0.995, 0.998): first('coverage C >= %s' % t, lambda r, t=t: r[5] >= t)
for t in (0.80, 0.90, 0.95): first('S/Chao2 >= %s' % t, lambda r, t=t: r[7] >= t)
for t in (5, 1): first('Q0 < %s' % t, lambda r, t=t: r[6] < t)
for i in (100, 200, 300, 400, 500, 600, len(rows)):
    r = rows[min(i, len(rows)) - 1]; print('at room %4d words %5.1f%% S %3d Q1 %2d Q2 %2d C %.4f Q0 %6.2f S/Chao2 %.3f' % (r[0], 100*r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
