#!/usr/bin/env python3
"""D1a: the payload measured (stage D1 §3) and the checks of §4 that validate.py D1 does not make itself, read-only
over the built folders. Writes nothing.

    python3 out/_analysis/d1_payload.py

Prints: the task payloads from handoff-D/tasks/index.tsv (median and p90 as handoff.py takes them, largest), the part
every task shares and the room's own documents; the verdict packets (median, p90, largest, over 50 KB, without an end
marker); the rooms above the declared session figure (SESSION_BYTES); and the checks: the room sets agree (store,
tasks, index rows, packets, expectations), MODEL.md is MODEL-D1.md and fits the ceiling, every task's MODEL.md begins
with it, VERSION equals vlib.model_hash, the sealed expectations equal EXPECTATIONS-D1.jsonl and no copy sits in a
served folder, the folder hash recomputes and equals handoff-D.sha256 and RUN.json, the vocabulary's counts.
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
H = os.path.join(OUT, "handoff-D")
V = os.path.join(OUT, "verdict-D")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

WORD_CEILING = 6000
SESSION_BYTES = 1000000          # declared in notes-D1.md §3: about 250,000 tokens at about 4 bytes a token
PACKET_CEILING = 50 * 1024
SHARED = ("RETURN-D.md", "VOCABULARY.json", "LADDER.md", "VERSION")


def q(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2], xs[int(0.9 * (len(xs) - 1))], xs[-1]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(H, "tasks", "index.tsv"), encoding="utf-8")]
cols, rows = rows[0], rows[1:]
pay = {r[0]: int(r[cols.index("payload_bytes")]) for r in rows}
top = open(os.path.join(H, "MODEL.md"), "rb").read()
shared = sum(os.path.getsize(os.path.join(H, f)) for f in SHARED) + len(top)
med, p90, big = q(pay.values())
print("tasks %d; payload bytes: median %d, p90 %d, largest %d (%s)" % (
    len(pay), med, p90, big, [s for s, b in pay.items() if b == big]))
print("shared by every task (RETURN-D.md, VOCABULARY.json, LADDER.md, VERSION, the global MODEL.md): %d bytes" % shared)
own = {s: b - shared for s, b in pay.items()}
m2, p2, b2 = q(own.values())
print("the room's own part (TASK.md, documents, appended model entries): median %d, p90 %d, largest %d" % (m2, p2, b2))
over = sorted(((b, s) for s, b in pay.items() if b > SESSION_BYTES), reverse=True)
print("rooms above %d bytes (about %d tokens): %d" % (SESSION_BYTES, SESSION_BYTES // 4, len(over)))
for b, s in over:
    fs = sorted(((os.path.getsize(os.path.join(H, "tasks", s, f)), f) for f in os.listdir(os.path.join(H, "tasks", s))),
                reverse=True)[:2]
    print("  %s\t%d bytes (about %d tokens); largest files %s" % (s, b, b // 4, ", ".join("%s %d" % (f, n) for n, f in fs)))
for lim in (500000, 2000000, 4000000):
    print("rooms above %d bytes: %d" % (lim, sum(1 for b in pay.values() if b > lim)))

pk = {f[:-3]: os.path.join(V, f) for f in os.listdir(V) if f.endswith(".md") and f != "RETURN-D2v.md"}
ps = {s: os.path.getsize(p) for s, p in pk.items()}
m3, p3, b3 = q(ps.values())
print("verdict packets %d: bytes median %d, p90 %d, largest %d (%s); over %d: %d" % (
    len(ps), m3, p3, b3, [s for s, b in ps.items() if b == b3], PACKET_CEILING,
    sum(1 for b in ps.values() if b > PACKET_CEILING)))
tails = {s: open(p, encoding="utf-8").read().rstrip().splitlines()[-1] for s, p in pk.items()}
print("packets' last lines: %d distinct shapes; first: %r" % (
    len({t.replace(s, "<sub>") for s, t in tails.items()}), sorted(tails.items())[0][1][:120]))

store = {json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"), encoding="utf-8")
         if l.strip()}
tdirs = {d for d in os.listdir(os.path.join(H, "tasks")) if os.path.isdir(os.path.join(H, "tasks", d))}
exp = [json.loads(l) for l in open(os.path.join(OUT, "EXPECTATIONS-D1.jsonl"), encoding="utf-8") if l.strip()]
esubs = [e["sub"] for e in exp]
print("rooms: store %d, task folders %d, index rows %d, packets %d, expectation lines %d (distinct %d); all equal: %s" % (
    len(store), len(tdirs), len(pay), len(pk), len(esubs), len(set(esubs)),
    store == tdirs == set(pay) == set(pk) == set(esubs) and len(esubs) == len(set(esubs))))

d1 = open(os.path.join(OUT, "MODEL-D1.md"), "rb").read()
print("MODEL.md equals MODEL-D1.md: %s; words %d (ceiling %d)" % (top == d1, len(top.decode("utf-8").split()),
                                                                     WORD_CEILING))
bad = [s for s in tdirs if not open(os.path.join(H, "tasks", s, "MODEL.md"), "rb").read().startswith(top)]
print("tasks whose MODEL.md does not begin with the global model: %d" % len(bad))
ver = open(os.path.join(H, "VERSION"), encoding="utf-8").read().strip()
mh = vlib.model_hash(OUT)
tv = {open(os.path.join(H, "tasks", s, "VERSION"), encoding="utf-8").read().strip() for s in tdirs}
print("VERSION %s; vlib.model_hash %s; equal: %s; task VERSIONs distinct %d, equal: %s" % (
    ver, mh, ver == mh, len(tv), tv == {mh}))

sealed = os.path.join(OUT, "sealed", "EXPECTATIONS.jsonl")
print("sealed EXPECTATIONS.jsonl equals EXPECTATIONS-D1.jsonl: %s" % (sha(sealed) == sha(os.path.join(OUT, "EXPECTATIONS-D1.jsonl"))))
served = []
for top_dir in (H, V):
    for d, _, fs in os.walk(top_dir):
        served += [os.path.relpath(os.path.join(d, f), OUT) for f in fs if "EXPECT" in f.upper() or "FIELD" in f.upper()]
print("files named EXPECT* or FIELD* in handoff-D/ or verdict-D/: %s" % (served or "none"))

rows_h = []
for d, dirs, fs in os.walk(H):
    dirs[:] = sorted(x for x in dirs if x != "recheck")
    for f in sorted(fs):
        p = os.path.join(d, f)
        rows_h.append("%s  %s\n" % (os.path.relpath(p, H), vlib.sha(p)))
fh = hashlib.sha256("".join(rows_h).encode("utf-8")).hexdigest()
rec = open(os.path.join(OUT, "handoff-D.sha256"), encoding="utf-8").read().strip()
run = json.load(open(os.path.join(ROOT, "RUN.json")))["handoff_D"]["first"]
print("folder hash recomputed %s; handoff-D.sha256 equal: %s; RUN.json equal: %s; RUN.json version equal: %s" % (
    fh, fh == rec, fh == run["folder_hash"], run["version"] == mh))

voc = json.load(open(os.path.join(H, "VOCABULARY.json"), encoding="utf-8"))
st = {}
for e in voc["elements"] + voc["arrows"]:
    st[e.get("status", "no status")] = st.get(e.get("status", "no status"), 0) + 1
print("vocabulary: elements %d, arrows %d, together %d; third %d, fourth %d, dimensions %d; status marks %s" % (
    len(voc["elements"]), len(voc["arrows"]), len(voc["elements"]) + len(voc["arrows"]), len(voc["third"]),
    len(voc["fourth"]), len(voc["dimensions"]), st))
model = {e["id"]: e.get("status") for e in vlib_rows} if (vlib_rows := [json.loads(l) for l in open(
    os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8") if l.strip()]) else {}
cands = sorted(i for i, s in model.items() if s == "candidate")
inv = {e["id"] for e in voc["elements"]}
print("candidates in model/elements.jsonl: %s; served in the vocabulary with no status: %s" % (
    cands, sorted(i for i in cands if i in inv and not [e for e in voc["elements"] if e["id"] == i][0].get("status"))))
