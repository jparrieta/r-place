#!/usr/bin/env python3
"""E1d: the tables of the audit's sections 4 and 5, printed from the check leg's outputs so that none is typed by hand.

    python3 out/audit-E1/reconstruction_tables.py > out/audit-E1/reconstruction_tables.md

Reads audit-E1/reconstruction_validate.json, audit-E1/reconstruction_causes.json and audit-E1/versioned_judgments.json.
Prints four markdown tables: fidelity by verdict; fidelity by branch (with the room, since each sampled branch holds
one room); the causes of the lines read; the versioned judgments of the thirty rooms.
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
A = os.path.join(ROOT, "out", "audit-E1")
ORDER = ("composes", "composes-with-residue", "cannot-tell", "does-not-compose")


def load(n):
    return json.load(open(os.path.join(A, n), encoding="utf-8"))


def main():
    v, c, j = load("reconstruction_validate.json"), load("reconstruction_causes.json"), load("versioned_judgments.json")
    print("**Fidelity by verdict** (the first return's ruled fixed-global verdict, model e15f9647…)\n")
    print("| verdict | rooms | mean fidelity | claims | yes | partly | no | unresolved | contradicted |")
    print("|---|---|---|---|---|---|---|---|---|")
    for k in ORDER:
        x = v["by_verdict"].get(k)
        if x:
            print("| %s | %d | %.3f | %s | %s | %s | %s | %s | %s |" % (k, x["rooms"], x["mean_fidelity"], format(x["claims"], ","),
                  format(x["yes"], ","), x["partly"], x["no"], x["unresolved"], x["contradicted"]))
    t = v["totals"]
    print("| all | %d | %.3f | %s | %s | %s | %s | %s | %s |\n" % (v["valid"], v["mean_fidelity"], format(t["claims"], ","),
          format(t["yes"], ","), t["partly"], t["no"], t["unresolved"], t["contradicted"]))
    print("**Fidelity by branch** (the room's most specific branch; each sampled branch holds one room)\n")
    print("| branch | room | verdict | fidelity | claims | yes | partly | no | unresolved |")
    print("|---|---|---|---|---|---|---|---|---|")
    rows = sorted(v["rows"], key=lambda r: (r["branch"] == "none", r["branch"], r["sub"].lower()))
    for r in rows:
        print("| %s | %s | %s | %.3f | %d | %d | %d | %d | %d |" % (r["branch"], r["sub"], r["verdict"], r["fidelity"],
              r["claims"], r["yes"], r["partly"], r["no"], r["unresolved"]))
    x = v["by_branch"]["none"]
    print("| none, together | %d rooms | | %.3f (mean) | %d | %d | %d | %d | %d |\n" % (x["rooms"], x["mean_fidelity"],
          x["claims"], x["yes"], x["partly"], x["no"], x["unresolved"]))
    print("**The causes of the lines read** (the analyst's reading, one cause per line)\n")
    lo, ot = c["by_cause_low_rooms"], c["by_cause_no_lines_other_rooms"]
    print("| cause | the 7 rooms below 0.8 (no, partly, unresolved) | the other 23 rooms (no lines) | all |")
    print("|---|---|---|---|")
    for k in ("particular", "evidence", "reader", "shared", "unresolved", "unsupported"):
        print("| %s | %d | %d | %d |" % (k, lo.get(k, 0), ot.get(k, 0), lo.get(k, 0) + ot.get(k, 0)))
    print("| all | %d | %d | %d |\n" % (sum(lo.values()), sum(ot.values()), sum(lo.values()) + sum(ot.values())))
    tags = {}
    for grp in c["by_tag"].values():
        for k, n in grp.items():
            if k.startswith("particular/"):
                tags[k.split("/")[1]] = tags.get(k.split("/")[1], 0) + n
    print("Inside particular: " + "; ".join("%s %d" % (k, n) for k, n in sorted(tags.items(), key=lambda kv: -kv[1])) + ".\n")
    print("**Fidelity lost in each room below 0.8, by cause** (a no line costs 1 and a partly line 0.5, over yes, partly and no)\n")
    print("| room | fidelity | particular | evidence | reader | unresolved |")
    print("|---|---|---|---|---|---|")
    fid = {r["sub"]: r["fidelity"] for r in v["rows"]}
    for s, d in sorted(c["fidelity_lost_low_rooms"].items(), key=lambda kv: fid[kv[0]]):
        print("| %s | %.3f | %.3f | %.3f | %.3f | %.3f |" % (s, fid[s], d.get("particular", 0), d.get("evidence", 0),
              d.get("reader", 0), d.get("unresolved", 0)))
    print("\n**The versioned judgments of the thirty** (first return e15f9647…; re-check, manifest and readers 46384686…)\n")
    print("| room | branch | fixed-global, first return | fixed-global, re-check | adapted-local status / grade | shared-branch status | fidelity | unresolved claims |")
    print("|---|---|---|---|---|---|---|---|")
    for x in j["table"]:
        print("| %s | %s | %s | %s | %s / %s | %s | %.3f | %d |" % (x["sub"], x["branch"], x["first_return"], x["recheck"],
              x["local_status"], x["local_grade"], x["shared_status"] or "no branch", x["fidelity"], x["unresolved"]))


if __name__ == "__main__":
    main()
