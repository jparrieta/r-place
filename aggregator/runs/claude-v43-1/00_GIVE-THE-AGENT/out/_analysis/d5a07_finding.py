#!/usr/bin/env python3
"""D5a-07: append finding F-025 (rule 14), the bound F07's members put on P05's telling clause. Refuses a second F-025."""
import datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
path = os.path.join(OUT, "findings.jsonl")
if any(json.loads(l).get("id") == "F-025" for l in open(path, encoding="utf-8") if l.strip()):
    raise SystemExit("F-025 exists")
ids = json.load(open(os.path.join(OUT, "_analysis", "d5a07_F07_K_line_ids.json"), encoding="utf-8"))
codes = ["AyyMD:c0109", "AyyMD:c0137", "AyyMD:c0110", "katawashoujo:c0036", "katawashoujo:c0037", "katawashoujo:c0042",
         "megaman:c0045", "megaman:c0025", "megaman:c0074", "fivenightsatfreddys:c0537", "fivenightsatfreddys:c0543"]
row = {
    "stage": "D5", "leg": "D5a-07", "id": "F-025", "tier": "element", "warrant": "read", "status": "bounded",
    "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "statement": ("P05 holds that a change the room has planned or agreed is repaired away as damage until its keepers "
                  "are told of it. The clause presumes that the keepers would accept the change once told. In 31 of the "
                  "59 rooms of branch F07 a re-check line says that informed members rejected the change, so that repair "
                  "enforced a competing design and telling did not settle it; in 20 of them the line names no evidence "
                  "limit. In r/AyyMD a member was told the poll result ('there was a poll , the logo stays GREEN' "
                  "[AyyMD/c0109]) and another answered 'And those people are wrong' [AyyMD/c0137]. In r/katawashoujo the "
                  "original builders, told of a purple background, kept black [katawashoujo/c0037], and the proposer "
                  "yielded [katawashoujo/c0042]."),
    "evidence": ids + codes + ["out/_analysis/d5a07_F07_reading.json", "out/forms/F07-account.md"],
    "bound": ("The telling clause holds where the keepers would accept the planned change once they know of it. It does "
              "not explain repair where informed members reject the change: there the repair is a contest over the "
              "design, which telling does not end. In 36 of F07's 59 rooms, 11 of them among the 31, a re-check line "
              "says the record does not show the agreed change, the untold keepers, the failed telling or the loss, so "
              "the clause is untested there. F-024's two routes (the change read from its shape, informed members "
              "holding it) are not touched. The element's words are unchanged in the frozen model; this is a finding, "
              "not an amendment, and D6 may act on it."),
    "why": ("Rule 14: a claim a branch bounds is a findings line (stage D5, section 5). The bound rests on the members' "
            "re-check lines and on their words through cite.py, not on the cut of the branch."),
    "untested": None, "literature": [], "abductive": None, "prompted_by": "branch F07 (stage D5, leg D5a-07)",
    "refuted_by": ["a room whose informed members rejected a planned change and then stopped repairing it once told, "
                   "without a change of design or a decision"],
    "supersedes": None,
}
with open(path, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
print("appended F-025 with", len(row["evidence"]), "evidence items")
