"""D3a-55 census of the propose rulings (rules logged before it ran). Counts only; nothing is written."""
import collections, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("op") == "propose"}
adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    if r.get("adaptation") in led and r.get("leg") == "D3a-55":
        adj[r["adaptation"]] = r
cls = {}
for s in glob.glob(os.path.join(RD, "propose-spec-*.txt")):
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            i, c = line.split("|")[:2]
            cls[i] = c
lift = {}
cur = None
for p in glob.glob(os.path.join(OUT, "_analysis", "d3_pk_propose_*.txt")):
    for line in open(p, encoding="utf-8"):
        m = re.match(r"^== (\S+)\s+propose", line)
        if m:
            cur = m.group(1)
            continue
        m = re.search(r"lift \S+ > (\S+) > (\S+) > (\S+)\s*$", line)
        if m and cur:
            lift[cur] = m.groups()
            cur = None
cands = {c["class"]: c for c in json.load(open(os.path.join(RD, "propose-candidates.json"), encoding="utf-8"))}

print("propose lines %d; ruled at D3a-55 %d" % (len(led), len(adj)))
print("(1) by decision:", dict(collections.Counter(r["decision"] for r in adj.values())))
cc = collections.Counter(cls[i] for i in adj)
print("(2) by class:", {k: cc[k] for k in ("OUT", "PART", "NOT", "P-G6")},
      "held", sum(v for k, v in cc.items() if k.startswith("H-")),
      "candidate", sum(v for k, v in cc.items() if k.startswith("C-")))
print("(3) held by:", dict(collections.Counter(cls[i][2:] for i in adj if cls[i].startswith("H-")).most_common()))
by4 = collections.defaultdict(collections.Counter)
for i, r in adj.items():
    by4[lift[i][1]][r["decision"]] += 1
print("(4) by fourth-order node (accept, reject, particular):")
for k in sorted(by4, key=lambda k: -sum(by4[k].values())):
    print("   %s %d: %d, %d, %d" % (k, sum(by4[k].values()), by4[k]["accept"], by4[k]["reject"], by4[k]["particular"]))
print("(5) candidates:")
for c in sorted(cands.values(), key=lambda c: c["id"]):
    ids = [i for i in adj if cls[i] == c["class"]]
    rooms = {led[i]["sub"] for i in ids}
    print("   %s %s: %d lines, %d rooms" % (c["id"], c["name"], len(ids), len(rooms)))
rooms_all = {led[i]["sub"] for i in adj}
acc_rooms = {led[i]["sub"] for i, r in adj.items() if r["decision"] == "accept"}
print("(6) rooms with propose lines %d; with an accepted line %d; with none accepted %d"
      % (len(rooms_all), len(acc_rooms), len(rooms_all - acc_rooms)))
un = [i for i in adj if lift[i][0] == "None"]
print("(7) unplaced %d:" % len(un), dict(collections.Counter(adj[i]["decision"] for i in un)),
      dict(collections.Counter(cls[i] for i in un).most_common()))
