"""Stage A1 section 1 checks that mem.py audit and facts do not serve.

Run from the folder root: python3 out/_analysis/a1_checks.py > out/_analysis/a1_checks-A1.txt
Prints each input's path, size and sha256 first, then the counts. Declared in departures.jsonl (A1a).
"""
import hashlib, json, math, os, re, statistics, sys
from collections import Counter, defaultdict

ROOT = "."
INPUTS = {
    "rooms": "package/store/rooms.jsonl",
    "codes": "package/store/codes.jsonl",
    "themes": "package/store/themes.jsonl",
    "items": "package/store/items.jsonl",
    "threads": "package/store/threads.jsonl",
    "unjoined": "package/store/_unjoined.jsonl",
    "retracted": "package/store/_retracted.jsonl",
    "build": "package/store/_build.json",
    "artworks": "package/canvas/artworks.jsonl",
}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


print("## inputs")
for k, p in INPUTS.items():
    print(f"{p}  {os.path.getsize(p)} bytes  sha256 {sha(p)}")
tree_files = sorted(os.listdir("trees"))
th = hashlib.sha256()
tsize = 0
for t in tree_files:
    b = open(os.path.join("trees", t), "rb").read()
    th.update(t.encode() + b)
    tsize += len(b)
print(f"trees/ ({len(tree_files)} files)  {tsize} bytes  sha256 over names+bytes {th.hexdigest()}")

rooms = {r["sub"]: r for r in jl(INPUTS["rooms"])}
codes = jl(INPUTS["codes"])
themes = jl(INPUTS["themes"])
items = jl(INPUTS["items"])
threads = jl(INPUTS["threads"])
unjoined = jl(INPUTS["unjoined"])
retracted = jl(INPUTS["retracted"])
build = json.load(open(INPUTS["build"]))

print("\n## concepts and themes")
sum_room_codes = sum(r["codes"] for r in rooms.values())
coder = sum(t.get("n_codes_coder") or 0 for t in themes)
print(f"sum of rooms.jsonl codes {sum_room_codes}; store codes.jsonl lines {len(codes)}; "
      f"themes n_codes_coder sum {coder}; retracted {len(retracted)}; coder less retracted {coder - len(retracted)}")
sum_n_codes = sum(t.get("n_codes") or 0 for t in themes)
print(f"themes n_codes (after retraction) sum {sum_n_codes}")
per_room_themes = Counter(t["sub"] for t in themes)
print(f"second-order themes {len(themes)}; rooms with none {sum(1 for s in rooms if per_room_themes[s] == 0)}; "
      f"with one {sum(1 for s in rooms if per_room_themes[s] == 1)}; with two {sum(1 for s in rooms if per_room_themes[s] == 2)}")
mism = [s for s in rooms if rooms[s]["themes"] != per_room_themes[s]]
print(f"rooms whose rooms.jsonl themes differs from themes.jsonl lines: {len(mism)} {mism[:10]}")
per_room_codes = Counter(c["sub"] for c in codes)
mism = [s for s in rooms if rooms[s]["codes"] != per_room_codes[s]]
print(f"rooms whose rooms.jsonl codes differs from codes.jsonl lines: {len(mism)} {mism[:10]}")

print("\n## unjoined")
item_ids = {(i["sub"], i["item_id"]) for i in items}
not_held = [c for c in codes if (c["sub"], c["item_id"]) not in item_ids]
state_unj = [c for c in codes if c.get("state") == "unjoined"]
uj = {(u["sub"], u["code_id"]) for u in unjoined}
print(f"_unjoined.jsonl {len(unjoined)}; codes whose item items.jsonl lacks {len(not_held)}; codes with state unjoined {len(state_unj)}; "
      f"recomputed set equals _unjoined: {uj == {(c['sub'], c['code_id']) for c in not_held}}")

print("\n## forest headers over trees/")
pat = re.compile(r"# items (\d+): coded (\d+), bridge (\d+), removed (\d+), dropped (\d+)")
pat_t = re.compile(r"# threads given (\d+), with at least one code (\d+)")
tot = Counter()
bad = []
for t in tree_files:
    head = open(os.path.join("trees", t)).read(3000)
    m = pat.search(head); mt = pat_t.search(head)
    if not m or not mt:
        bad.append(t); continue
    for k, v in zip(["items", "coded", "bridge", "removed", "dropped"], m.groups()):
        tot[k] += int(v)
    tot["threads_given"] += int(mt.group(1)); tot["threads_with_codes"] += int(mt.group(2))
print(f"forest header totals: {dict(tot)}; files without a parsable header {bad}")
fs = Counter()
for r in rooms.values():
    for k, v in (r.get("forest") or {}).items():
        if isinstance(v, (int, float)) and k != "coverage_of_coded_items":
            fs[k] += v
print(f"rooms.jsonl forest.* sums: {dict(fs)}")
st = Counter(i.get("state") for i in items)
print(f"store items.jsonl {len(items)} by state {dict(st)}; threads.jsonl {len(threads)}")
print(f"_build.json: { {k: build[k] for k in build if isinstance(build[k], (int, float))} }")

print("\n## clocks")
last_thread = defaultdict(lambda: None)
for t in threads:
    lh = t.get("last_hour")
    if lh is None:
        continue
    cur = last_thread[t["sub"]]
    last_thread[t["sub"]] = lh if cur is None else max(cur, lh)
for f in ["onset_first_code_hour", "onset_last_code_hour", "items_in_window"]:
    nulls = [s for s, r in rooms.items() if r.get(f) is None]
    print(f"{f}: nulls {len(nulls)} {nulls}")
null_thread = [s for s in rooms if last_thread[s] is None]
print(f"rooms with no thread last_hour: {len(null_thread)} {null_thread}")
gaps = []
for s, r in rooms.items():
    a, b = r.get("onset_last_code_hour"), last_thread[s]
    if a is not None and b is not None:
        gaps.append((b - a, s, a, b))
gaps.sort()
d = [g[0] for g in gaps]
print(f"last thread hour minus last code hour over {len(d)} rooms: min {min(d):.2f} q1 {statistics.quantiles(d, n=4)[0]:.2f} "
      f"median {statistics.median(d):.2f} q3 {statistics.quantiles(d, n=4)[2]:.2f} max {max(d):.2f}")
print(f"rooms with the last code after the last thread hour (negative gap): {[(s, round(a,2), round(b,2)) for g, s, a, b in gaps if g < -0.01]}")
print(f"rooms whose last thread hour passes 97: {sum(1 for g in gaps if g[3] > 97)}; whose last code passes 97: {[(g[1], g[2]) for g in gaps if g[2] > 97]}")
print(f"rooms with last code before hour 73: {sum(1 for g in gaps if g[2] < 73)}; with last thread hour before 73: {sum(1 for g in gaps if g[3] < 73)}")


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


print("\n## the instrument's shape (705 rooms)")
subs = sorted(rooms)
I = [rooms[s]["items_in_window"] for s in subs]
C = [rooms[s]["codes"] for s in subs]
T = [rooms[s]["themes"] for s in subs]
for name, x in [("items_in_window", I), ("concepts", C)]:
    print(f"themes against {name}: raw r {pearson(x, T):.3f}  log r {pearson([math.log(a) for a in x], [math.log(b) for b in T]):.3f}  "
          f"rank rho {pearson(ranks(x), ranks(T)):.3f}")

print("\n## concept reach")
reach = {}
for s in subs:
    cs = [c for c in codes if False]
by_room = defaultdict(lambda: [0, 0])
for c in codes:
    by_room[c["sub"]][0] += 1
    if c.get("theme_id"):
        by_room[c["sub"]][1] += 1
for s in subs:
    n, k = by_room[s]
    reach[s] = k / n if n else None
vals = [reach[s] for s in subs if reach[s] is not None]
print(f"concept reach share over {len(vals)} rooms: min {min(vals):.3f} median {statistics.median(vals):.3f} max {max(vals):.3f}; "
      f"rooms below 1.0: {sum(1 for v in vals if v < 1)}")
srt = sorted(subs, key=lambda s: rooms[s]["items_in_window"])
q = len(srt) // 4
small = [reach[s] for s in srt[:q]]
m_small = statistics.median(small)
print(f"smallest quartile by items_in_window: {q} rooms, items {rooms[srt[0]]['items_in_window']}..{rooms[srt[q-1]]['items_in_window']}; median reach {m_small:.4f}")
dec = 10
print("reach by decile of items_in_window: decile, items range, median reach, share of rooms below the small-quartile median")
first_below = None
rows = []
for d_ in range(dec):
    part = srt[d_ * len(srt) // dec:(d_ + 1) * len(srt) // dec]
    med = statistics.median(reach[s] for s in part)
    below = sum(1 for s in part if reach[s] < m_small) / len(part)
    rows.append((d_, rooms[part[0]]["items_in_window"], rooms[part[-1]]["items_in_window"], med, below))
    print(f"  {d_+1:2d}  {rows[-1][1]}..{rows[-1][2]}  {med:.4f}  {below:.2f}")
for i in range(dec):
    if all(r[3] < m_small for r in rows[i:]):
        first_below = rows[i]; break
print(f"first decile from which every larger decile's median reach is below {m_small:.4f}: {first_below}")
# the running form: the smallest size S such that the median reach of rooms with items > S is below m_small
thr = None
for i, s in enumerate(srt):
    rest = [reach[x] for x in srt[i:]]
    if statistics.median(rest) < m_small:
        thr = rooms[s]["items_in_window"]; break
print(f"running form: smallest items_in_window from which the median reach of all rooms at or above it is below {m_small:.4f}: {thr}")

print("\n## canvas")
arts = jl(INPUTS["artworks"])
print(f"artworks.jsonl lines {len(arts)}; keys of the first line {sorted(arts[0].keys())}")
no_canvas = [s for s, r in rooms.items() if not r.get("canvas_entries")]
print(f"rooms with canvas_entries 0 or null: {no_canvas}")
