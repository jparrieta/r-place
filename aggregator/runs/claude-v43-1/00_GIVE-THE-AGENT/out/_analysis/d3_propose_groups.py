"""D3a-55: per candidate group in the propose specs, count lines and rooms and the
lifted third-order, fourth-order and dimension nodes, read from the packets' lift lines.
Counts only; no ledger is written."""
import argparse
import collections
import re

ap = argparse.ArgumentParser()
ap.add_argument("--packets", nargs="+", required=True)
ap.add_argument("--specs", nargs="+", required=True)
ap.add_argument("--rooms", action="store_true", help="list the rooms of each group")
a = ap.parse_args()

lift = {}
cur = None
for p in a.packets:
    for line in open(p, encoding="utf-8"):
        m = re.match(r"^== (\S+)\s+propose", line)
        if m:
            cur = m.group(1)
            continue
        m = re.search(r"lift (\S+?):\S+ > (\S+) > (\S+) > (\S+)\s*$", line)
        if m and cur:
            lift[cur] = (m.group(1), m.group(2), m.group(3), m.group(4))
            cur = None

groups = collections.defaultdict(list)
for s in a.specs:
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        lid, cls = line.split("|")[:2]
        if cls.startswith("C-"):
            groups[cls].append(lid)

for cls in sorted(groups, key=lambda c: -len(groups[c])):
    ids = groups[cls]
    rooms = sorted({lift[i][0] for i in ids})
    t3 = collections.Counter(lift[i][1] for i in ids)
    t4 = collections.Counter(lift[i][2] for i in ids)
    dim = collections.Counter(lift[i][3] for i in ids)
    print(f"{cls}: lines {len(ids)}, rooms {len(rooms)}")
    print("  T4:", dict(t4.most_common()))
    print("  D:", dict(dim.most_common()))
    print("  T3 (top 6):", dict(t3.most_common(6)))
    if a.rooms:
        print("  rooms:", ", ".join(rooms))
missing = [i for c in groups for i in groups[c] if i not in lift]
print("ids with no lift found:", missing if missing else "none")
