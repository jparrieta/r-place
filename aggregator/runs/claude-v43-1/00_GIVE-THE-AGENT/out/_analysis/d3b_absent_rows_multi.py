#!/usr/bin/env python3
"""D3b: d3b_absent_rows.py for a group of small packets read together (d3b_packet_multi.py). For each element named,
rebuilds its packet of unruled flagged re-check absent lines (offset 0, limit 100, the order d3b_packet.py uses), takes
the rows-file lines whose ids fall in it ('id|REJ|evidence', 'id|SPEC|evidence', 'id|LIM|evidence'), gives every other
line the default (G6 for NONPORTABLE; G2 limit for unobserved and not-testable, naming the cited concepts), and writes
d3_rulings/recheck-<element>-abs-000.jsonl. Refuses a rows line whose id is in none of the packets, a NONPORTABLE line
named in the rows, an evidenced absence left to the default, and an existing rulings file.

    python3 out/_analysis/d3b_absent_rows_multi.py --elements A01,A07 --group d3b_pk_group_03.txt \
        --rows out/_analysis/d3_rulings/group-03-rows.txt [--write]
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--elements", required=True)
ap.add_argument("--group", required=True)
ap.add_argument("--rows", required=True)
ap.add_argument("--write", action="store_true")
ap.add_argument("--prefix", default="d3b_pk", help="the packets' name prefix; the second batch uses d3b2_pk")
ap.add_argument("--file-prefix", default="recheck", help="the rulings files' prefix; the second batch uses recheck2")
a = ap.parse_args()
els = a.elements.split(",")


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
allnew = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
          if r["op"] == "absent" and r["id"] in take and r["id"] not in ruled]
pages = {}
for e in els:
    pg = sorted((r for r in allnew if r.get("element") == e), key=lambda r: (r["sub"].lower(), r["op"], r["id"]))
    if len(pg) > 100:
        sys.exit("refused: %s has more than 100 lines" % e)
    pages[e] = pg
subs = {r["sub"] for pg in pages.values() for r in pg}
lab = {}
for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8"):
    c = json.loads(l)
    if c["sub"] in subs:
        lab[(c["sub"], c["code_id"])] = c.get("first_order")
where = {r["id"]: e for e, pg in pages.items() for r in pg}
ov = {}
for n, l in enumerate(open(a.rows, encoding="utf-8"), 1):
    l = l.rstrip("\n")
    if not l.strip():
        continue
    i, cls, ev = l.split("|", 2)
    if i not in where:
        sys.exit("rows line %d: %s is in none of the packets" % (n, i))
    if cls not in ("REJ", "SPEC", "LIM") or not ev.strip() or i in ov:
        sys.exit("rows line %d: bad class, no evidence, or the id twice" % n)
    ov[i] = (cls, ev.strip())
outs, total = {}, {}
for e, pg in pages.items():
    pk = "%s (packet %s_%s_abs_000.txt)" % (a.group, a.prefix, e)
    rows = []
    for r in pg:
        i, s, obs = r["id"], r["sub"], r.get("observation")
        seen = "; ".join("%s %s" % (c, lab.get((s, c), "?")) for c in codes(r)) or "no concept cited"
        if r.get("portable") is False:
            if i in ov:
                sys.exit("%s is NONPORTABLE; G6 rules it first" % i)
            row = {"adaptation": i, "decision": "particular", "kind": "particular",
                   "reason": "G6 and G61 (3), read in %s: absent, %s, on %s; the line is marked NONPORTABLE (%s), so it "
                             "is a particular by construction" % (pk, obs, e, ", ".join(r.get("nonportable_hits") or []))}
        elif i in ov and ov[i][0] == "REJ":
            row = {"adaptation": i, "decision": "reject",
                   "reason": "G2, G61 (3) and G61's readings 2 and 4, read in %s: %s; the room's concepts show %s, so the "
                             "claim of absence (%s) fails" % (pk, ov[i][1], e, obs)}
        elif i in ov and ov[i][0] == "SPEC":
            if obs not in ("observed-absent", "not-needed"):
                sys.exit("%s: SPEC is for an evidenced absence" % i)
            row = {"adaptation": i, "decision": "accept", "kind": "specification",
                   "reason": "G3 and G61 (3), read in %s: marked %s; %s; the evidenced absence holds, a specification"
                             % (pk, obs, ov[i][1])}
        elif i in ov and ov[i][0] == "LIM":
            if obs not in ("observed-absent", "not-needed"):
                sys.exit("%s: LIM is for an evidenced absence" % i)
            row = {"adaptation": i, "decision": "accept", "kind": "none",
                   "reason": "G3 and G61 (3), read in %s: marked %s; %s; the concepts do not show the absence or the "
                             "lack of need, an evidence limit counted apart" % (pk, obs, ov[i][1])}
        else:
            if obs in ("observed-absent", "not-needed"):
                sys.exit("%s claims an evidenced absence: name it in the rows (G3)" % i)
            row = {"adaptation": i, "decision": "accept", "kind": "none",
                   "reason": "G2 and G61 (3), read in %s: absent, %s; the cited concepts (%s) do not show %s as stated, "
                             "and the room's accepted lines on it share none of these codes or show another act; the "
                             "line marks a limit of the record, counted apart" % (pk, obs, seen, e)}
        rows.append(row)
        k = "%s/%s" % (row["decision"], row.get("kind"))
        total[k] = total.get(k, 0) + 1
    outs[e] = rows
print("group %s: %d elements, %d rulings; %s" % (a.group, len(outs), sum(len(v) for v in outs.values()), total))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
for e, rows in outs.items():
    p = os.path.join(RD, "%s-%s-abs-000.jsonl" % (a.file_prefix, e))
    if os.path.exists(p):
        sys.exit("refused: %s exists" % p)
for e, rows in outs.items():
    with open(os.path.join(RD, "%s-%s-abs-000.jsonl" % (a.file_prefix, e)), "w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
print("wrote %d rulings files" % len(outs))
