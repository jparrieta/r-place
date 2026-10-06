"""Stage A1 section 3: the reading order, a seeded random shuffle of the analysed set cut into blocks
of about 3 MB (forest, concept and second-order theme bytes, as `mem.py room --size` counts them);
a room above the cap is a block of its own.

Run from the folder root: python3 out/_analysis/a1_order.py > out/_analysis/a1_order-A1.txt
Writes out/order-A1.txt. Declared in departures.jsonl (A1a). Seed 20261006 (the leg's date).
"""
import hashlib, json, os, random
from collections import Counter

SEED = 20261006
CAP = 3_000_000
P = {"rooms": "package/store/rooms.jsonl", "codes": "package/store/codes.jsonl",
     "themes": "package/store/themes.jsonl", "dropped": "out/dropped.jsonl"}
for k, p in P.items():
    print(f"{p}  {os.path.getsize(p)} bytes  sha256 {hashlib.sha256(open(p, 'rb').read()).hexdigest()}")

rooms = [json.loads(l)["sub"] for l in open(P["rooms"]) if l.strip()]
dropped = {json.loads(l)["sub"] for l in open(P["dropped"]) if l.strip()}
# the bytes as `mem.py room --size` counts them: the forest file, each concept's rendered line, each theme's JSON
import sys
sys.path.insert(0, "tools")
import mem
cb, tb = Counter(), Counter()
for l in open(P["codes"], encoding="utf-8"):
    c = json.loads(l)
    cb[c["sub"]] += len(mem.code_line(c).encode("utf-8")) + 1
for l in open(P["themes"], encoding="utf-8"):
    t = json.loads(l)
    tb[t["sub"]] += len(json.dumps(t, ensure_ascii=False).encode("utf-8")) + 1
size = {s: os.path.getsize(f"trees/{s}.md") + cb[s] + tb[s] for s in rooms}
print(f"check against mem.py room denmark --size (179495): {size.get('denmark')}")

analysed = sorted(s for s in rooms if s not in dropped)
rng = random.Random(SEED)
order = analysed[:]
rng.shuffle(order)

blocks, cur, cur_b = [], [], 0
for s in order:
    if size[s] > CAP:
        if cur:
            blocks.append(cur); cur, cur_b = [], 0
        blocks.append([s])
        continue
    if cur and cur_b + size[s] > CAP:
        blocks.append(cur); cur, cur_b = [], 0
    cur.append(s); cur_b += size[s]
if cur:
    blocks.append(cur)

with open("out/order-A1.txt", "w") as f:
    for i, b in enumerate(blocks, 1):
        for s in b:
            f.write(f"{i:02d}\t{s}\n")
print(f"analysed {len(analysed)}; dropped {len(dropped)}; blocks {len(blocks)}; total bytes {sum(size[s] for s in analysed)}")
for i, b in enumerate(blocks, 1):
    print(f"block {i:02d}  {sum(size[s] for s in b) / 1e6:.2f} MB  {len(b)} rooms: {', '.join(b)}")
