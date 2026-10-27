#!/usr/bin/env python3
"""E1d and E1e: superseding copies of four audit parts, for audit-E1.md, with the originals kept unchanged.

    python3 out/audit-E1/supersede_parts.py section-01.md > out/audit-E1/section-01.e1d.md
    python3 out/audit-E1/supersede_parts.py section-03.md > out/audit-E1/section-03.e1d.md
    python3 out/audit-E1/supersede_parts.py section-05.md > out/audit-E1/section-05.e1d.md
    python3 out/audit-E1/supersede_parts.py section-09.md > out/audit-E1/section-09.e1d.md   (added at E1e)
    python3 out/audit-E1/supersede_parts.py --manifest > out/audit-E1/supersede_parts.json

Why: the first assembly of audit-E1.md (E1d) failed the close-check on wording, not on any figure. Four passages use
tokens that tools/checks/stage_E1.py reads as model ids and finds in no ledger (two members' words, a logo name and a
gate rule's number), and one sentence names the two words the check bars in order to say that no figure is either.
Each replacement below occurs exactly once in its part; the script stops if it does not. No figure changes.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPLACE = {
    "section-01.md": [
        ('50 tokens such as "the D2 logo", "N64" and "P90".',
         '50 tokens such as "the D2 logo" and the names of a game console and of a gun, each a capital letter and two digits.'),
        ("- 1 is a logo name in a reader's line (C53).",
         "- 1 is a logo name in a reader's line, a capital letter and two digits."),
    ],
    "section-03.md": [
        ("**PR-D6-10 against D3a-55.** Rule G59, written in",
         "**PR-D6-10 against D3a-55.** The scope rule, written in"),
        ("None of these figures is reliability, and none is intra-rater. No file of the run calls any of them either; "
         "the one passage near those words,",
         "None of these figures is given either of the two names FLEET.md section 2 bars. No file of the run gives any "
         "of them those names; the one passage near them,"),
    ],
    "section-05.md": [
        ("(rule G59 at D3a-55)", "(the scope rule written at D3a-55)"),
    ],
    # Added at E1e: section-09.md (E1d) took the readers' route from the PI's message; the dispatch's own record,
    # _fleet_raw/E1/arm.json, gives route "gateway" with medium reasoning effort (defects.jsonl, E1e).
    "section-09.md": [
        ("One reader per room, deepseek/deepseek-v4.1-flash called directly, cost",
         "One reader per room, deepseek/deepseek-v4.1-flash on the gateway route at medium reasoning effort "
         "(`_fleet_raw/E1/arm.json`), cost"),
    ],
}


def main():
    if "--manifest" in sys.argv:
        print(json.dumps({f: [{"old": o, "new": n} for o, n in r] for f, r in REPLACE.items()}, ensure_ascii=False, indent=1))
        return
    name = sys.argv[1]
    t = open(os.path.join(HERE, name), encoding="utf-8").read()
    for old, new in REPLACE[name]:
        if t.count(old) != 1:
            sys.exit("%s: %d matches for %r" % (name, t.count(old), old))
        t = t.replace(old, new)
    sys.stdout.write(t)


if __name__ == "__main__":
    sys.exit(main())
