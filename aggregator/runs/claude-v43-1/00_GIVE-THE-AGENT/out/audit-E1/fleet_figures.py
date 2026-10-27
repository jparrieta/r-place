#!/usr/bin/env python3
"""E1 section 1, the figures restated where a reader will find them, each beside FLEET.md section 2's definition.

    python3 out/audit-E1/fleet_figures.py > out/audit-E1/fleet_figures.json

Declared before the run (E1a). For each figure file the run wrote (stability-B2.md, fidelity-B3.md, position-B3.md,
transmission-B4.md, transmission-after-revision-B4.md), every line that names fidelity, alpha, Jaccard, stability,
transmission, position or agreement and holds a number, with its line number: the figures as the run stated them.
The verdict fleet's disagreement rate is recomputed from verdicts-D.jsonl: of the first return's rooms with two or more
readers, those whose readers' verdicts are not all the same. FLEET.md section 2's definitions are printed beside them
(the lines of that section that name the same words). What each licenses is written in the audit section; none of
them is called reliability or intra-rater.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
FILES = ["stability-B2.md", "fidelity-B3.md", "position-B3.md", "transmission-B4.md", "transmission-after-revision-B4.md"]
KEY = re.compile(r"fidelity|alpha|jaccard|stabilit|transmission|position|agreement|disagree", re.I)
NUM = re.compile(r"\d\.\d+|\d+ of \d+|\d+(\.\d+)? per cent|\d+%")


def main():
    figs = {}
    for f in FILES:
        p = os.path.join(OUT, f)
        if not os.path.exists(p):
            figs[f] = None
            continue
        figs[f] = [{"line": n, "text": l.strip()[:300]} for n, l in enumerate(open(p, encoding="utf-8"), 1)
                   if KEY.search(l) and NUM.search(l)]
    fleet = open(os.path.join(ROOT, "FLEET.md"), encoding="utf-8").read()
    m = re.search(r"^## 2\.(.*?)(?=^## \d|\Z)", fleet, re.M | re.S)
    sec2 = [l.strip()[:300] for l in (m.group(1).splitlines() if m else []) if KEY.search(l)]
    first, multi, differ = 0, 0, 0
    for l in open(os.path.join(OUT, "verdicts-D.jsonl"), encoding="utf-8"):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get("recheck"):
            continue
        first += 1
        vs = [x.get("verdict") for x in (r.get("readers") or []) if x.get("verdict")]
        if len(vs) >= 2:
            multi += 1
            differ += len(set(vs)) > 1
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a).")[1].strip(),
                      "figures": figs, "fleet_md_section_2_lines": sec2,
                      "verdict_fleet": {"first_return_lines": first, "rooms_with_two_or_more_readers": multi,
                                        "readers_disagree": differ,
                                        "disagreement_rate": round(differ / multi, 4) if multi else None}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
