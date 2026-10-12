#!/usr/bin/env python3
"""B4: the frozen scheme's tests for named third-order themes, read from out/scheme_final.jsonl (the scheme the
readers held). Prints id, family, name, gloss, must_show, must_not_show, decide_when_both and discriminators.

    python3 out/_analysis/b4_scheme.py T3-001 T3-023 [...] [--fields=must_show,decide_when_both] [--pair]

--pair prints only the discriminators between the themes named, not each theme's whole list.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = ("gloss", "must_show", "must_not_show", "decide_when_both", "discriminators")


def main():
    want = [a for a in sys.argv[1:] if a.startswith("T3-")]
    fields = F
    for a in sys.argv[1:]:
        if a.startswith("--fields="):
            fields = tuple(a.split("=", 1)[1].split(","))
    S = {r["id"]: r for r in (json.loads(x) for x in open(os.path.join(ROOT, "out", "scheme_final.jsonl"), encoding="utf-8") if x.strip())}
    for t in want:
        r = S.get(t)
        if not r:
            print("%s: not in scheme_final.jsonl" % t); continue
        print("%s %s %s" % (t, r.get("family"), r.get("name")))
        for f in fields:
            v = r.get(f)
            if f == "discriminators":
                for d in v or []:
                    if "--pair" in sys.argv and isinstance(d, dict) and d.get("vs") not in want:
                        continue
                    if isinstance(d, dict):
                        print("  disc vs %s: %s" % (d.get("against") or d.get("vs") or d.get("other") or "?", d.get("question") or d))
                    else:
                        print("  disc: %s" % d)
            elif v:
                print("  %s: %s" % (f, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
        print()


if __name__ == "__main__":
    main()
