#!/usr/bin/env python3
"""D6a-09: departures.jsonl line 21, the dated amendment J asked for (ruling 1d, 27 Oct 09:27 Berlin): the widening of the
branch-naming rule, first stated at D6a-04 and in use from D6a-02, with whether it applies backwards and the check of the
earlier placements it touches. The counts are read from _analysis/d6a09_branch_rule_check.json. No branch line changes.
Prints one JSON line; append with >>.

    python3 out/_analysis/d6a09_departure.py >> out/departures.jsonl
"""
import collections, json, os

AN = os.path.dirname(os.path.abspath(__file__))
chk = json.load(open(os.path.join(AN, "d6a09_branch_rule_check.json"), encoding="utf-8"))
by = chk["by_reading"]
widened = chk["not_key_element"]
early = [o for o in widened if o["leg"] in ("D6a-01", "D6a-02", "D6a-03")]
fmt = lambda o: "%s at %s in %s (%s, %s)" % (o["branch"], o["cell"], o["form"], o["reading"], o["leg"])  # noqa: E731
print(json.dumps({
    "stage": "D6", "leg": "D6a-09", "date": "2026-10-27",
    "provision": "The branch-naming rule of stage D6. As stated at D6a-02: a branch is named at a form's cell where it "
                 "leans to the form at 1.5 times its share or more, holds two or more of the cell's holders, and its own "
                 "key matches the cell. As amended: the key matches the cell where (i) the key's element is the cell's "
                 "element; (ii) the key's fourth-order theme is a theme of the cell's element; (iii) the cell is an arrow "
                 "and the key's element is one of its ends; or (iv) the cell is an arrow and the key's fourth-order theme "
                 "is a theme of its antecedent. Failing these, (v) a branch may be named where its own words of change "
                 "name the act the cell's deciding lines describe and the dry run of its rooms' lines bears it out. A "
                 "branch line may also stand at a cell its form leaves untouched, at the branch's key element or an end "
                 "of the arrow, with the branch's share of the form's holders.",
    "why": "J's ruling 1d (27 October, 09:27 Berlin, through the handler): record the D6a-04 widening of the "
           "branch-naming rule as a dated amendment, stating whether it applies backwards, and check the earlier "
           "placements it touches. A ruling rule changes only by a dated amendment that says whether it applies "
           "backwards (J, 16 October, 19:08 Berlin). The widening was written into notes-D6.md at D6a-04 as a licence, "
           "not as an amendment, though it was already in use at D6a-02.",
    "applies_backwards": "True, to every branch line from D6a-01: the widened readings were in use before they were "
                         "stated. No branch line is rewritten, moved or removed (J's ruling 1: no data file changes).",
    "scope": "Of the %d branch lines in fractal-D6.jsonl, %d stand on (i), the rule as stated; %d stand on the widened "
             "readings: %s. Of these, %d were written before D6a-04: %s. Every widened line leans to its form at 1.5 or "
             "more and holds two or more of the cell's holders, except F35 at A12 in E, where form E leaves A12 "
             "untouched and the line stands on F35's own rooms there (r/borussiadortmund, r/clashroyale, r/GuildWars2)."
             % (chk["lines"], by.get("key element", 0), len(widened),
                ", ".join("%s %d" % (k, v) for k, v in sorted(by.items()) if k != "key element"),
                len(early), "; ".join(fmt(o) for o in early)),
    "check": [
        "F08 at P05 in F (D6a-03): reading (v). F08's key is on P14 (Workarounds, T4-009), not on keeping. It leans to F "
        "at 1.51 and holds 2 of the cell's 7 holders (r/wildhockey, r/eesti). Its change says a stale target undoes the "
        "room's own new design, and both rooms' lines keep the machines and the design together. It stands, as the "
        "weakest of the four.",
        "F35 at A12 in E (D6a-01): reading (iii). F35's key is on P01, A12's antecedent. Form E leaves A12 untouched; "
        "the line stands on three of F35's rooms in E that restrict the bare answer. It stands as a line below the "
        "form's lean.",
        "F11 at P01 in D (D6a-01): reading (v). F11's key is on P13 (Transition, T4-028); P01's theme is Mobilization "
        "(T4-005). It leans to D at 2.62 and holds 3 of the cell's 16 holders. Its change says that on another canvas "
        "the room recruits, builds and defends again, and two of the three rooms reopen the call for a later canvas or "
        "a remake (r/bindingofisaac, r/sadboys). It stands.",
        "F12 at P01 in D (D6a-01): reading (v), as F11. It leans to D at 2.69 and holds the same 3 of 16; in "
        "r/bindingofisaac the restart on the later canvas brings an urgent call for defenders. It stands.",
    ],
}, ensure_ascii=False))
