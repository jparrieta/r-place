"""B1c: new kinds per hundred second-order themes read in the first pass, by room.

usage: python3 out/_analysis/b1c_discovery.py [--bin 500]

The rooms in the order the first pass read them: the first placement event naming each room as the
room being read (`at`) in kinds-B1.jsonl. Each room's second-order themes from the store. Each mint in
theme_discovery.jsonl is set at the end of its room (`sub`). Prints the mints by bins of second-order
themes read, the first and last hundred themes, the rate by tenths of the rooms read, and the run of
themes and rooms since the last mint.
"""
import collections
import json
import sys

sys.path.insert(0, "tools")
import saturation as S  # noqa: E402

binw = int(sys.argv[sys.argv.index("--bin") + 1]) if "--bin" in sys.argv else 500

st = S.store(".")
nthemes = collections.Counter(t.get("sub") for t in st["themes"])

seq = []
seen = set()
with open("out/kinds-B1.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        at = r.get("at")
        if at and at not in seen:
            seen.add(at)
            seq.append(at)

cum = {}
pos = {}
c = 0
for i, s in enumerate(seq, 1):
    c += nthemes[s]
    cum[s] = c
    pos[s] = i
total = c

mints = []
with open("out/theme_discovery.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            mints.append(json.loads(line))

missing = [m["theme"] for m in mints if m.get("sub") not in cum]
xs = sorted((cum[m["sub"]], pos[m["sub"]], m["theme"], m["sub"]) for m in mints if m.get("sub") in cum)

print("rooms in reading order: %d; second-order themes in them: %d; mints: %d (unmatched: %s)"
      % (len(seq), total, len(mints), ", ".join(missing) or "none"))
print("overall: %.2f new kinds per hundred second-order themes" % (100.0 * len(xs) / total))
first100 = sum(1 for x in xs if x[0] <= 100)
last100 = sum(1 for x in xs if x[0] > total - 100)
print("first hundred themes: %d new kinds; last hundred: %d" % (first100, last100))
print("\nby bins of %d second-order themes read" % binw)
print("from\tto\tmints\tper_hundred")
lo = 0
while lo < total:
    hi = min(lo + binw, total)
    n = sum(1 for x in xs if lo < x[0] <= hi)
    print("%d\t%d\t%d\t%.2f" % (lo + 1, hi, n, 100.0 * n / (hi - lo)))
    lo = hi
print("\nby tenths of the rooms read")
print("rooms\tthemes\tmints\tper_hundred")
n_rooms = len(seq)
prev_t = 0
prev_r = 0
for k in range(1, 11):
    r_hi = round(n_rooms * k / 10)
    t_hi = cum[seq[r_hi - 1]]
    n = sum(1 for x in xs if prev_r < x[1] <= r_hi)
    print("%d-%d\t%d\t%d\t%.2f" % (prev_r + 1, r_hi, t_hi - prev_t, n, 100.0 * n / max(1, t_hi - prev_t)))
    prev_t, prev_r = t_hi, r_hi
last = xs[-1]
print("\nlast mint: %s in %s, room %d of %d, at %d themes; since: %d rooms and %d second-order themes"
      % (last[2], last[3], last[1], n_rooms, last[0], n_rooms - last[1], total - last[0]))
