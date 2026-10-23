#!/usr/bin/env python3
"""D3b: the per-room table for notes-D3.md (stage section 5; QD3-009 (3)), by the rule logged at D3b before it was
built. One row for each analysed room, from the ledgers. Writes the table as markdown to --out; prints its totals.

    python3 out/_analysis/d3b_room_table.py --revised R01,P05,P21,P22,A21 --out out/_analysis/d3b_room_table.md
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
REISSUE_CUT = "reissue: cut off mid-room"
REISSUE_MARK = "reissue: end marker to be repaired (rule 6)"


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
allrooms = sorted(scope["affected_rooms"], key=str.lower)
relying, contrast = scope["relying"], set(scope["contrasting_cases"])
old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
first = {r["sub"] for r in new}
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

vb, vbv = {}, {}
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("ruled_by") == "analyst":
        vb[r["sub"]] = r["verdict"] + " (ruled)"
        vbv[r["sub"]] = (r.get("model_version") or "")[:8]
    elif r["sub"] not in vb:
        vs = {e.get("verdict") for e in r.get("readers", [])}
        vb[r["sub"]] = vs.pop() if len(vs) == 1 else "split"
        vbv[r["sub"]] = "/".join(sorted({(e.get("model_version") or "")[:8] for e in r.get("readers", [])}))


def after_verdict(s):
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
    if s not in first:
        return "pending, second batch"
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
    return "; ".join(parts) if parts else "nothing pointed at the rewrite; a test of the revised model"


# The ten reissued rooms are the rooms with neither a labeler return nor a re-check verdict (ingest rejected them);
# the handler's answer to QD3-009 names the one whose end marker is to be repaired, the others were cut off mid-room.
reissue = {}
for s in allrooms:
    if s not in first and s not in vfleet:
        reissue[s] = REISSUE_MARK if s == "traaaaaaannnnnnnnnns" else REISSUE_CUT
print("reissued rooms %d: %s" % (len(reissue), ", ".join("%s (%s)" % (s, r[9:]) for s, r in sorted(reissue.items()))))
if len(reissue) != 10 or list(reissue.values()).count(REISSUE_MARK) != 1:
    raise SystemExit("the reissued rooms do not match the handler's answer (10, one end marker)")
rows, tot = [], collections.Counter()
for s in allrooms:
    if s in first:
        batch = "first batch"
    else:
        batch = "pending, second batch (%s)" % reissue.get(s, "not started")
    tot["rooms " + batch.split(" (")[0]] += 1
    if batch != "first batch":
        tot["rooms " + batch] += 1
    va, vav = after_verdict(s)
    c = counts(by_new[s]) if s in first else collections.Counter()
    for k, v in c.items():
        tot["lines " + k] += v
    ev = evidence(s)
    for t in ("fixed", "stands", "corrected again", "not corrected", "proposal named by", "NONPORTABLE line",
              "proposal not named", "new correction", "nothing pointed"):
        if t in ev:
            tot["rooms: " + t] += 1
    lines = ("%d: %d / %d / %d / %d / %d / %d" % (len(by_new[s]), c["shared"], c["corr"], c["lim"], c["part"],
                                                   c["rej"], c["pend"])) if s in first else "none yet"
    rows.append("| %s | %s | %s | %s (%s) → %s%s | %s | %s | %s |" % (
        s, batch, why(s), vb.get(s, "none"), vbv.get(s, ""), va, (" (%s)" % vav) if vav else "", local_status(s),
        lines, ev))
headline = ("| Room | Batch | Why re-checked (recheck-scope.json) | Verdict before (version) → re-check readers (version) "
            "| Local status | Re-check lines: shared / corrections / limits / particulars / rejected / pending | "
            "What the evidence pointed at, and the re-check |")
sep = "|---|---|---|---|---|---|---|"
open(a.out, "w", encoding="utf-8").write("\n".join([headline, sep] + rows) + "\n")
print("rows %d; %s" % (len(rows), dict(sorted(tot.items()))))
print("wrote %s" % a.out)
