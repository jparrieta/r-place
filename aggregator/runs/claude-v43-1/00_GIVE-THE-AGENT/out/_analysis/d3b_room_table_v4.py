#!/usr/bin/env python3
"""D3b, second batch: the per-room table for notes-D3.md, by the rule logged at D3b before the first table was
built (diary, 2026-10-22T05:08:46), with every room back. It supersedes d3b_room_table.py for the second batch and
leaves that script and its tables unchanged. Changes: (1) the batch column says first batch or second batch, read
from the first table (d3b_room_table_v3.md), since both batches now sit in adaptations-recheck.jsonl; (2) the
verdict before is my D3a-56 ruling where the first readers split, else their agreed verdict, and it never reads a
re-check ruling; (3) the verdict after is my D3b ruling (G62) where the re-check readers split, else their agreed
verdict, each with its model version; (4) no room is pending. Writes the table as markdown to --out (under
out/_analysis/); prints its totals.

    python3 out/_analysis/d3b_room_table_v4.py --revised R01,P05,P21,P22,A21 --out out/_analysis/d3b_room_table_v4.md
"""
import argparse, collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--revised", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
if not os.path.abspath(a.out).startswith(os.path.join(OUT, "_analysis") + os.sep):
    raise SystemExit("--out must be under out/_analysis/")
revised = {e.strip() for e in a.revised.split(",") if e.strip()}


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
allrooms = sorted(scope["affected_rooms"], key=str.lower)
relying, contrast = scope["relying"], set(scope["contrasting_cases"])
old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
returned = {r["sub"] for r in new}
vfleet = {r["sub"]: r for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl"))}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
by_old = collections.defaultdict(list)
for l in old:
    by_old[l["sub"]].append(l)
by_new = collections.defaultdict(list)
for l in new:
    by_new[l["sub"]].append(l)

firstbatch = set()
for line in open(os.path.join(OUT, "_analysis", "d3b_room_table_v3.md"), encoding="utf-8"):
    cells = [c.strip() for c in line.split("|")]
    if len(cells) > 3 and cells[2] == "first batch":
        firstbatch.add(cells[1])

vb, vbv, va, vav = {}, {}, {}, {}
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("ruled_by") == "analyst" and r.get("recheck"):
        va[r["sub"]] = r["verdict"] + " (ruled)"
        vav[r["sub"]] = (r.get("model_version") or "")[:8]
    elif r.get("ruled_by") == "analyst":
        vb[r["sub"]] = r["verdict"] + " (ruled)"
        vbv[r["sub"]] = (r.get("model_version") or "")[:8]
    elif r["sub"] not in vb:
        vs = {e.get("verdict") for e in r.get("readers", [])}
        vb[r["sub"]] = vs.pop() if len(vs) == 1 else "split"
        vbv[r["sub"]] = "/".join(sorted({(e.get("model_version") or "")[:8] for e in r.get("readers", [])}))


def after_verdict(s):
    if s in va:
        return va[s], vav[s]
    r = vfleet.get(s)
    if not r:
        return "none returned", ""
    vs = [e.get("verdict") for e in r.get("readers", [])]
    ver = "/".join(sorted({(e.get("model_version") or "")[:8] for e in r.get("readers", [])}))
    return (vs[0] if len(set(vs)) == 1 else "split " + "/".join(sorted(set(vs)))), ver


def local_status(s):
    p = os.path.join(OUT, "rooms", s, "model-D-recheck.md")
    if not os.path.exists(p):
        return "none"
    m = re.search(r"local_status:\s*(validated|unresolved|insufficient-evidence)", open(p, encoding="utf-8").read())
    return m.group(1) if m else "unstated"


def dk(l):
    r = last.get(l["id"])
    return (r["decision"], r.get("kind")) if r else ("unruled", None)


def counts(lines):
    c = collections.Counter()
    for l in lines:
        d, k = dk(l)
        if d in ("accept", "modify") and k in ("specification", "elaboration"):
            c["shared"] += 1
        elif d in ("accept", "modify") and k == "correction":
            c["corr"] += 1
        elif d in ("accept", "modify") and k in (None, "none"):
            c["lim"] += 1
        elif d in ("accept", "modify") and k == "proposal":
            c["prop"] += 1
        elif d in ("accept", "modify"):
            c["other"] += 1
        elif d == "particular":
            c["part"] += 1
        elif d == "reject":
            c["rej"] += 1
        elif d == "pending":
            c["pend"] += 1
        else:
            c["unruled"] += 1
    return c


def why(s):
    if s in contrast:
        return "contrasting case"
    g = collections.OrderedDict()
    for item in relying.get(s, []):
        head, _, tail = item.rpartition(" ")
        g.setdefault(head, []).append(tail)
    return "; ".join("%s %s" % (h, " ".join(sorted(v))) for h, v in g.items()) or "unstated"


def evidence(s):
    ea = sorted({l["element"] for l in by_old[s] if dk(l)[0] in ("accept", "modify") and dk(l)[1] == "correction"})
    cb = set()
    for l in by_old[s]:
        if l.get("op") != "propose":
            continue
        r = last.get(l["id"])
        if r and r["decision"] == "accept" and r.get("kind") == "proposal":
            m = re.search(r"candidate ([A-Z]\d\d)", r.get("reason", ""))
            if m:
                cb.add(m.group(1))
    newcorr = {l["element"] for l in by_new[s] if dk(l)[0] in ("accept", "modify") and dk(l)[1] == "correction"}
    newprop = [l["id"] for l in by_new[s] if l.get("op") == "propose" and dk(l) == ("accept", "proposal")]
    parts = []
    for x in ea:
        stands = x in newcorr
        if x in revised:
            parts.append("%s correction: %s" % (x, "stands" if stands else "fixed"))
        else:
            parts.append("%s correction, no revision: %s" % (
                x, "corrected again (a G61 (1) repeat)" if stands else "not corrected"))
    named, unnamed, nonport = [], [], []
    for x in sorted(cb):
        ok = any(l.get("element") == x and l.get("op") != "absent" and dk(l)[0] in ("accept", "modify")
                 and dk(l)[1] in ("specification", "elaboration", "correction") for l in by_new[s])
        ok = ok or any(l.get("op") == "propose" and dk(l)[0] == "reject" and
                       ("the candidate %s states" % x) in (last[l["id"]].get("reason") or "") for l in by_new[s])
        np = (not ok) and any(l.get("element") == x and l.get("op") != "absent" and dk(l)[0] == "particular"
                              and l.get("portable") is False for l in by_new[s])
        if np:
            nonport.append(x)
        else:
            (named if ok else unnamed).append(x)
    if named:
        parts.append("proposal named by " + " ".join(named))
    if nonport:
        parts.append("proposal named by %s in a NONPORTABLE line, a particular by G6" % " ".join(nonport))
    if unnamed:
        parts.append("proposal not named by " + " ".join(unnamed))
    for x in sorted(newcorr - set(ea)):
        parts.append("new correction on %s, held" % x)
    if newprop:
        parts.append("new proposal accepted, held (%s)" % ", ".join(newprop))
    return "; ".join(parts) if parts else "nothing pointed at the rewrite; a test of the revised model"


rows, tot = [], collections.Counter()
for s in allrooms:
    if s not in returned:
        raise SystemExit("%s has no re-check line; the second batch is not complete" % s)
    batch = "first batch" if s in firstbatch else "second batch"
    tot["rooms " + batch] += 1
    av, avv = after_verdict(s)
    tot["after " + av] += 1
    c = counts(by_new[s])
    for k, v in c.items():
        tot["lines " + k] += v
    ev = evidence(s)
    for t in ("fixed", "stands", "corrected again", "not corrected", "proposal named by", "NONPORTABLE line",
              "proposal not named", "new correction", "new proposal", "nothing pointed"):
        if t in ev:
            tot["rooms: " + t] += 1
            tot["rooms: %s (%s)" % (t, batch)] += 1
    lines = "%d: %d / %d / %d / %d / %d / %d" % (len(by_new[s]), c["shared"], c["corr"], c["lim"], c["part"],
                                                c["rej"], c["pend"])
    if c["prop"]:
        lines += " (+%d proposal accepted)" % c["prop"]
    rows.append("| %s | %s | %s | %s (%s) → %s (%s) | %s | %s | %s |" % (
        s, batch, why(s), vb.get(s, "none"), vbv.get(s, ""), av, avv, local_status(s), lines, ev))
headline = ("| Room | Batch | Why re-checked (recheck-scope.json) | Verdict before (version) → after (version) "
            "| Local status | Re-check lines: shared / corrections / limits / particulars / rejected / pending | "
            "What the evidence pointed at, and the re-check |")
sep = "|---|---|---|---|---|---|---|"
open(a.out, "w", encoding="utf-8").write("\n".join([headline, sep] + rows) + "\n")
print("first-batch rooms read from d3b_room_table_v3.md: %d" % len(firstbatch))
print("rows %d; %s" % (len(rows), dict(sorted(tot.items()))))
print("wrote %s" % a.out)
