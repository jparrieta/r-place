#!/usr/bin/env python3
"""D3b, G61 (3) with G2, G3 and G6: the rulings for one packet of flagged re-check absent lines, read in the packet
d3b_packet.py printed (the same filter, order, offset and limit, rebuilt here so the ids match). A rows file gives
the lines whose reading changes the default, one a line: 'id|REJ|evidence' (the concepts show the element: reject),
'id|SPEC|evidence' (an evidenced absence the concepts show: accept, specification, G3) or 'id|LIM|evidence' (an
evidenced absence the concepts do not show: an evidence limit, G3). Every other line takes the default: NONPORTABLE
lines are particulars (G6); unobserved and not-testable lines are evidence limits (G2: accept, kind none), each reason
naming the line's cited concepts by label; an observed-absent or not-needed line must be named in the rows file. The
rulings go to d3_rulings/<name>.jsonl, for d3b_adjudicate_batch.py; an existing file is never overwritten.

    python3 out/_analysis/d3b_absent_rows.py --element K07 --offset 0 --limit 100 --packet d3b_pk_K07_abs_000.txt \
        --rows out/_analysis/d3_rulings/K07-abs-000-rows.txt --name recheck-K07-abs-000 [--write]
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--offset", type=int, required=True)
ap.add_argument("--limit", type=int, required=True)
ap.add_argument("--packet", required=True)
ap.add_argument("--rows")
ap.add_argument("--name", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
# every flagged list of the leg (the first batch's and the second's); only unruled lines are taken
take = {r["adaptation"] for p in sorted(glob.glob(os.path.join(RD, "recheck-absent-flagged*.jsonl"))) for r in jl(p)}
new = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
       if r.get("element") == a.element and r["id"] not in ruled and r["op"] == "absent" and r["id"] in take]
new.sort(key=lambda r: (r["sub"].lower(), r["op"], r["id"]))
page = new[a.offset:a.offset + a.limit]
ids = {r["id"] for r in page}
subs = {r["sub"] for r in page}
lab = {}
for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8"):
    c = json.loads(l)
    if c["sub"] in subs:
        lab[(c["sub"], c["code_id"])] = c.get("first_order")
ov = {}
if a.rows:
    for n, l in enumerate(open(a.rows, encoding="utf-8"), 1):
        l = l.rstrip("\n")
        if not l.strip():
            continue
        i, cls, ev = l.split("|", 2)
        if i not in ids:
            sys.exit("rows line %d: %s is not in this packet" % (n, i))
        if cls not in ("REJ", "SPEC", "LIM", "CLAUSE") or not ev.strip():
            sys.exit("rows line %d: class must be REJ, SPEC, LIM or CLAUSE, with evidence" % n)
        if i in ov:
            sys.exit("rows line %d: %s twice" % (n, i))
        ov[i] = (cls, ev.strip())
pk = a.packet
out, tally = [], {}
for r in page:
    i, s, e, obs = r["id"], r["sub"], a.element, r.get("observation")
    cs = codes(r)
    seen = "; ".join("%s %s" % (c, lab.get((s, c), "?")) for c in cs) or "no concept cited"
    if r.get("portable") is False:
        row = {"adaptation": i, "decision": "particular", "kind": "particular",
               "reason": "G6 and G61 (3), read in %s: absent, %s, on %s; the line is marked NONPORTABLE (%s), so it "
                         "is a particular by construction" % (pk, obs, e, ", ".join(r.get("nonportable_hits") or []))}
        if i in ov:
            sys.exit("%s is NONPORTABLE; G6 rules it before any reading, so it takes no rows line" % i)
    elif i in ov and ov[i][0] == "REJ":
        row = {"adaptation": i, "decision": "reject", "kind": None,
               "reason": "G2 and G61 (3), read in %s, quotes read: %s; the concepts show %s as stated, so the claim "
                         "of absence (%s) fails" % (pk, ov[i][1], e, obs)}
    elif i in ov and ov[i][0] == "SPEC":
        if obs not in ("observed-absent", "not-needed"):
            sys.exit("%s: SPEC is for an evidenced absence; this line is %s" % (i, obs))
        row = {"adaptation": i, "decision": "accept", "kind": "specification",
               "reason": "G3 and G61 (3), read in %s: marked %s; %s; the evidenced absence holds, a specification"
                         % (pk, obs, ov[i][1])}
    elif i in ov and ov[i][0] == "LIM":
        if obs not in ("observed-absent", "not-needed"):
            sys.exit("%s: LIM is for an evidenced absence; an unread limit takes the default" % i)
        row = {"adaptation": i, "decision": "accept", "kind": "none",
               "reason": "G3 and G61 (3), read in %s: marked %s; %s; the concepts do not show the absence or the lack "
                         "of need, so the line is reclassified as an evidence limit, counted apart" % (pk, obs, ov[i][1])}
    elif i in ov and ov[i][0] == "CLAUSE":
        if obs in ("observed-absent", "not-needed"):
            sys.exit("%s: CLAUSE is for an unobserved or not-testable line" % i)
        row = {"adaptation": i, "decision": "accept", "kind": "none",
               "reason": "G2 and G61's reading 3, read in %s: absent, %s, and its how confines the claim to the clause "
                         "move 173 added to %s's statement (a planned or agreed change repaired away until its keepers "
                         "are told); %s; the room's keeping stands in its accepted lines, and the clause is not shown in "
                         "these concepts, a limit of the record counted apart and carried to %s's re-examination"
                         % (pk, obs, e, ov[i][1], e)}
    else:
        if obs in ("observed-absent", "not-needed"):
            sys.exit("%s claims an evidenced absence (%s): name it in the rows file (G3)" % (i, obs))
        row = {"adaptation": i, "decision": "accept", "kind": "none",
               "reason": "G2 and G61 (3), read in %s: absent, %s; the cited concepts (%s) do not show %s as stated, "
                         "and the room's placements on its tier send the line to reading but do not show it alone; "
                         "the line marks a limit of the record, counted apart" % (pk, obs, seen, e)}
    out.append(row)
    k = "%s/%s" % (row["decision"], row["kind"])
    tally[k] = tally.get(k, 0) + 1
print("%s %s packet [%d, %d): %d rulings; %s" % (a.name, a.element, a.offset, a.offset + len(page), len(out), tally))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
p = os.path.join(RD, a.name + ".jsonl")
if os.path.exists(p):
    sys.exit("refused: %s exists; never overwrite" % p)
with open(p, "w", encoding="utf-8") as f:
    for x in out:
        f.write(json.dumps({k: v for k, v in x.items() if v is not None}, ensure_ascii=False) + "\n")
print("wrote %s" % p)
