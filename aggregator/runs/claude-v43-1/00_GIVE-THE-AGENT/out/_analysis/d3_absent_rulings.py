#!/usr/bin/env python3
"""Write one element's absent-line rulings file after every line has been read whole.

Lines that need a judgment have no default: an evidenced absence (observed-absent, not-needed)
must be named in the map as a specification or a reject, and a line ingest marked portable false
must be named as a particular or a reject. Any line named under "reject" is rejected with its
reason. Every other line is unobserved or not-testable and is ruled under G2 as an evidence limit
(kind none), its reason naming the line's own concepts. The script refuses to write if the map
names an id the element does not have, or misses a line that needs a judgment.

--guard REGEX prints the evidence-limit lines whose concept labels match it, for a second look.

  python3 out/_analysis/d3_absent_rulings.py --element P22 --map out/_analysis/d3_rulings/P22-absent-map.json \
      --out out/_analysis/d3_rulings/P22-absent.jsonl --guard "correct|clean|version"
"""
import argparse
import json
import re
import subprocess
import sys


def read_lines(element, total):
    lines = []
    for off in range(0, total, 100):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element,
                              "--op", "absent", "--offset", str(off), "--limit", str(min(100, total - off))],
                             capture_output=True, text=True).stdout
        for blk in out.split("\n== ")[1:]:
            head = blk.split("\n", 1)[0]
            lid = head.split()[0]
            obs = re.search(r"observation: (\S+)", blk)
            codes = re.search(r"codes: (.*)", blk)
            pairs = re.findall(r"(c\d{4}) (.*?)(?=; c\d{4} |$)", codes.group(1)) if codes else []
            lines.append({"id": lid, "obs": obs.group(1) if obs else "?",
                          "nonportable": "NONPORTABLE" in head, "codes": pairs})
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--total", type=int, required=True, help="the element's absent lines, as the packet header gives")
    ap.add_argument("--map", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--guard", default="")
    ap.add_argument("--rules", default="G2, G13 and G13a", help="the ruling rules an evidence-limit reason names")
    ap.add_argument("--limit-clause", default="none shows members after hour 73 contesting which version of the "
                    "room's work or of the event is kept, so P22 is not shown",
                    help="why the concepts do not show the element (P22's wording by default)")
    a = ap.parse_args()
    m = json.load(open(a.map))
    rej, spec, part = m.get("reject", {}), m.get("specification", {}), m.get("particular", {})
    lines = read_lines(a.element, a.total)
    ids = [x["id"] for x in lines]
    if len(ids) != a.total or len(set(ids)) != a.total:
        sys.exit(f"read {len(ids)} lines ({len(set(ids))} distinct), expected {a.total}")
    unknown = [i for i in list(rej) + list(spec) + list(part) if i not in ids]
    if unknown:
        sys.exit(f"map names ids the element does not have: {unknown}")
    errors, rows, guard = [], [], []
    for x in lines:
        i = x["id"]
        if i in rej:
            rows.append({"adaptation": i, "decision": "reject", "reason": rej[i]})
        elif x["nonportable"]:
            if i not in part:
                errors.append(f"{i}: portable false, not named as particular or reject")
                continue
            rows.append({"adaptation": i, "decision": "particular", "kind": "none", "reason": part[i]})
        elif x["obs"] in ("observed-absent", "not-needed"):
            if i not in spec:
                errors.append(f"{i}: {x['obs']}, not named as specification or reject")
                continue
            rows.append({"adaptation": i, "decision": "accept", "kind": "specification", "reason": spec[i]})
        elif x["obs"] in ("unobserved", "not-testable"):
            if i in spec or i in part:
                errors.append(f"{i}: {x['obs']} but named as specification or particular")
                continue
            shown = "; ".join(f"{c} {lab}" for c, lab in x["codes"]) or "no concept"
            rows.append({"adaptation": i, "decision": "accept", "kind": "none",
                         "reason": f"read whole, {a.rules}: marked {x['obs']}; its concepts are {shown}; "
                                   f"{a.limit_clause}, an evidence limit"})
            if a.guard and any(re.search(a.guard, lab, re.I) for _, lab in x["codes"]):
                guard.append(i)
        else:
            errors.append(f"{i}: observation {x['obs']} not handled")
    if errors:
        sys.exit("refused:\n" + "\n".join(errors))
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    counts = {}
    for r in rows:
        k = r["decision"] + "/" + r.get("kind", "-")
        counts[k] = counts.get(k, 0) + 1
    print(f"wrote {len(rows)} rulings to {a.out}: {counts}")
    if a.guard:
        print(f"evidence-limit lines whose labels match the guard ({len(guard)}): {' '.join(guard)}")


if __name__ == "__main__":
    main()
