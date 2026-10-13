#!/usr/bin/env python3
"""B4c, read-only: what each arm left in out/_fleet_raw/. Per packet, the reader files present, and for arm 1 each
meta's reader, reissue, valid and why; the arm's log.jsonl keys; for arm 2 the state files' replicate, reissue and
valid. Prints only.

    python3 out/_analysis/b4c_returns_survey.py
"""
import collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "out", "_fleet_raw")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    a1 = os.path.join(RAW, "B4")
    kinds = collections.Counter()
    for pk in sorted(d for d in os.listdir(a1) if d.startswith("S05-")):
        fs = sorted(os.listdir(os.path.join(a1, pk)))
        kinds[" ".join(fs)] += 1
        for f in fs:
            if f.endswith(".meta.json"):
                m = json.load(open(os.path.join(a1, pk, f), encoding="utf-8"))
                if not m.get("valid") or m.get("reissue"):
                    print("arm1 %s %s reader=%s group=%s reissue=%s valid=%s why=%s" % (
                        pk, f, m.get("reader"), m.get("group"), m.get("reissue"), m.get("valid"), str(m.get("why"))[:200]))
    print("arm1 file sets per packet:")
    for k, n in kinds.most_common():
        print("  %3d  %s" % (n, k))
    lg = jl(os.path.join(a1, "log.jsonl"))
    print("arm1 log lines %d; keys %s" % (len(lg), sorted({k for x in lg for k in x})))
    print("arm1 log lines with replicate-like keys: %s" % [x for x in lg if "replicate" in x][:2])
    a2 = os.path.join(RAW, "B4-openai-astra")
    kinds = collections.Counter()
    for pk in sorted(d for d in os.listdir(a2) if d.startswith("S05-")):
        fs = sorted(f for f in os.listdir(os.path.join(a2, pk)) if re.match(r"^oa\d+\.(jsonl|state\.json|raw\.txt)$", f))
        kinds[" ".join(fs)] += 1
        for f in fs:
            if f.endswith(".state.json"):
                s = json.load(open(os.path.join(a2, pk, f), encoding="utf-8"))
                if not s.get("valid") or s.get("reissue") or s.get("replicate") != int(f[2]):
                    print("arm2 %s %s replicate=%s reissue=%s valid=%s state=%s reason=%s" % (
                        pk, f, s.get("replicate"), s.get("reissue"), s.get("valid"), s.get("state"), s.get("reason")))
    print("arm2 file sets per packet:")
    for k, n in kinds.most_common():
        print("  %3d  %s" % (n, k))


if __name__ == "__main__":
    main()
