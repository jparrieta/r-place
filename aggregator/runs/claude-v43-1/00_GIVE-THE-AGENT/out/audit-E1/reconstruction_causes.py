#!/usr/bin/env python3
"""E1 section 4, the check leg (E1d): the causes of a low reconstruction score, separated by reading.

    python3 out/audit-E1/reconstruction_causes.py > out/audit-E1/reconstruction_causes_lines.jsonl
    python3 out/audit-E1/reconstruction_causes.py --tally out/audit-E1/reconstruction_causes.tsv > out/audit-E1/reconstruction_causes.json

The rule, declared before any line is read (E1d):
- A low score is a fidelity below 0.8 in out/reconstruction-E1.jsonl. In those rooms every no, partly and unresolved
  line is read; in the other rooms every no line is read, so that a cause found in the low rooms can be compared
  with the rest. The other rooms' partly lines are not read (a limit, stated where the result is reported).
- The first mode prints, per selected room, a header line (the room, its fidelity, verdict and branch, the
  adapted-local status line of its packet and its second-order themes as the packet gives them), then the selected
  claim lines from the room's newest raw file (as reconstruction_validate.py chose it, the final marker dropped).
- Each line read is given one cause in reconstruction_causes.tsv (room, claim, cause, a few words of why), from the
  claim, the reader's reason, the packet's skeleton and the room's themes:
  unsupported: the coder's claim goes past the room's record (a motive, figure or event no theme of the room and no
    cited line holds);
  evidence: the record cannot show it, or the skeleton's line on it is absent, unobserved or not testable for want
    of evidence (the canvas, off-platform work, what the threads do not say);
  particular: the room's themes hold it, and no skeleton line carries it (a particular the return did not record);
  shared: the skeleton's element applies and is lined, and its statement does not hold what the room did (the
    order, the condition, the actor), or the model has no element for a kind of act that is not the room's alone;
  reader: the skeleton does state it, with the room's line on it, and the reader's no or partly is mistaken;
  unresolved lines keep their own cause, "unresolved", and are reported apart.
- Clarified after reading the first page (simonfraser and Madeon), before any cause was written: a particular is any
  fact of the room the coder's account states from the record and no skeleton line carries, though no theme names it
  (an interval the coder measured, which layer carried an act, a counterpart room named, a detail of an act, the
  room's business off the canvas, the coder's reading of the room as a whole, a line the room proposed that the model
  did not take); reader also covers a line that is not a claim of the coder's account (a theme of the room, or a
  sentence about the coder's evidence, scored as a claim) and a no where the skeleton's only line is pending. Each
  cause carries a tag (interval, order, layer, named-room, detail, off-canvas, synthesis, proposed, and so on) so the
  kinds inside a cause can be counted.
- The tally mode checks that every selected line has exactly one cause and prints the counts by cause, by room, by
  verdict and by branch, and each cause's share of the fidelity lost in each low room (a no line costs 1, a partly
  line 0.5, over the room's yes, partly and no).
"""
import collections, glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
LOW = 0.8
CAUSES = ("unsupported", "evidence", "particular", "shared", "reader", "unresolved")


def rooms():
    return [json.loads(l) for l in open(os.path.join(OUT, "reconstruction-E1.jsonl"), encoding="utf-8") if l.strip()]


def claim_lines(r):
    lines = [l for l in open(os.path.join(OUT, r["raw_file"]), encoding="utf-8").read().split("\n") if l.strip()]
    if r.get("marker_dropped"):
        lines = lines[:-1]
    return [o for o in map(json.loads, lines) if not o.get("summary")]


def selected(r):
    acc = ("no", "partly", "unresolved") if r["fidelity"] < LOW else ("no",)
    return [o for o in claim_lines(r) if o.get("accounted") in acc]


def packet(sub):
    t = open(os.path.join(OUT, "_packets-E1", sub + ".md"), encoding="utf-8").read()
    status = next((l for l in t.split("\n") if l.startswith("Adapted-local status")), "")
    themes = t.split("## The room's second-order themes", 1)[1].split("This is the end of the packet")[0].strip()
    return status, themes


def main():
    R = rooms()
    if "--tally" in sys.argv:
        tsv = sys.argv[sys.argv.index("--tally") + 1]
        cls, tags = collections.defaultdict(list), {}
        for l in open(tsv, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                f = l.rstrip("\n").split("\t")
                cls[(f[0], int(f[1]))].append(f[2])
                tags[(f[0], int(f[1]))] = f[3].split(":")[0] if ":" in f[3] and f[2] != "evidence" else f[2]
        need, errs, rows = set(), [], []
        for r in R:
            den = r["yes"] + r["partly"] + r["no"]
            for o in selected(r):
                k = (r["sub"], int(o["claim"]))
                need.add(k)
                got = cls.get(k, [])
                if len(got) != 1 or got[0] not in CAUSES:
                    errs.append([k[0], k[1], got])
                    continue
                cost = {"no": 1.0, "partly": 0.5}.get(o["accounted"], 0.0) / den
                rows.append({"sub": r["sub"], "verdict": r["verdict"], "branch": r["branch"], "low": r["fidelity"] < LOW,
                             "accounted": o["accounted"], "cause": got[0], "tag": tags[k], "cost": cost})
        by_tag = {grp: dict(collections.Counter(x["cause"] + "/" + x["tag"] for x in rows if keep(x)))
                  for grp, keep in (("low_rooms", lambda x: x["low"]), ("no_lines_other_rooms", lambda x: not x["low"]))}
        extra = sorted(set(cls) - need)
        def count(keep, key):
            g = collections.defaultdict(collections.Counter)
            for x in rows:
                if keep(x):
                    g[x[key]][x["cause"]] += 1
            return {k: dict(v) for k, v in sorted(g.items())}
        loss = collections.defaultdict(lambda: collections.defaultdict(float))
        for x in rows:
            if x["low"]:
                loss[x["sub"]][x["cause"]] += x["cost"]
        print(json.dumps({"rule": __doc__.split("The rule, declared before any line is read (E1d):")[1].strip(),
                          "selected": len(need), "classified": len(rows), "errors": errs, "extra": extra,
                          "by_cause_low_rooms": dict(collections.Counter(x["cause"] for x in rows if x["low"])),
                          "by_cause_no_lines_other_rooms": dict(collections.Counter(x["cause"] for x in rows if not x["low"])),
                          "by_cause_no_lines_all_rooms": dict(collections.Counter(x["cause"] for x in rows if x["accounted"] == "no")),
                          "by_tag": by_tag,
                          "by_room": count(lambda x: True, "sub"),
                          "by_verdict_no_lines": count(lambda x: x["accounted"] == "no", "verdict"),
                          "by_branch_no_lines": count(lambda x: x["accounted"] == "no", "branch"),
                          "fidelity_lost_low_rooms": {s: {c: round(v, 3) for c, v in d.items()} for s, d in sorted(loss.items())}},
                         ensure_ascii=False, indent=1))
        return
    for r in sorted(R, key=lambda r: r["fidelity"]):
        status, themes = packet(r["sub"])
        print(json.dumps({"room": r["sub"], "fidelity": r["fidelity"], "verdict": r["verdict"], "branch": r["branch"],
                          "status": status, "themes": themes}, ensure_ascii=False))
        for o in selected(r):
            print(json.dumps({"sub": r["sub"], "claim": o.get("claim"), "accounted": o.get("accounted"),
                              "element": o.get("element"), "text": o.get("text"), "reason": o.get("reason")},
                             ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
