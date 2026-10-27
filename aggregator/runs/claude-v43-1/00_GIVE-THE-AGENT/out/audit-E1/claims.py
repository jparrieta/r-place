#!/usr/bin/env python3
"""E1 section 1, claims against their evidence (contract section 1, two kinds of claim): the table claims-E1.md is
written from.

    python3 out/audit-E1/claims.py > out/audit-E1/claims.json

Declared before the run (E1a). For every proposition (propositions.jsonl) and every branch (branches-D5.jsonl):
  - the kind declared (`carried_by` for a proposition; a branch's `shared_warrant`, `form_or_grouping`, `confidence`);
  - the evidence named: a proposition's `rests_on` (arrows and elements), `finding`, `evidence_gate`; a branch's
    `binds`, `construct_bindings`, `verdicts`, the propositions it holds and fails;
  - the `rival` (a proposition's), or that none is named;
  - the validation it received, by kind, from the records the claim names:
      pattern: each arrow it rests on with its counts (holds, both, share or the like), whether a denominator is
        given, whether the arrow beat its base rate (`base_rate_beaten`), and its bracket fields (`before_h73`,
        `early_late`), against prior.md section 4's brackets;
      words: the exemplar concepts the arrows and findings cite (resolved against codes.jsonl), and the return's
        verdicts on the elements (adaptations by op, from adjudications.jsonl accepted lines).
A claim validated with the other kind's evidence is judged by hand in the audit section; the script lays the fields
side by side and resolves every concept it cites. prior.md section 3's declaration and literature-C3.md's switch
records are read by hand there too.
"""
import collections, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
CID = re.compile(r"\b([A-Za-z0-9_]{2,})[/:](c\d{4,5})\b")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def short(v, n=220):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "…"


def main():
    codes = {(c["sub"].lower(), c["code_id"]) for c in jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))}
    arrows = {a["id"]: a for a in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
    els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
    finds = {f["id"]: f for f in jl(os.path.join(OUT, "findings.jsonl"))}
    def cites(o):
        s = json.dumps(o, ensure_ascii=False)
        got = set(CID.findall(s))
        return {"cited": len(got), "resolve": sum(1 for sub, c in got if (sub.lower(), c) in codes)}
    props = []
    for p in jl(os.path.join(OUT, "propositions.jsonl")):
        ar = []
        for x in p.get("rests_on") or []:
            a = arrows.get(x)
            if a:
                ar.append({"id": x, "counts": short(a.get("counts")), "has_denominator": bool(re.search(r"\b(both|of|n|denominator|rooms)\b", json.dumps(a.get("counts") or {}))),
                           "base_rate_beaten": a.get("base_rate_beaten"), "before_h73": short(a.get("before_h73"), 120),
                           "early_late": short(a.get("early_late"), 160), "grounding": a.get("grounding"),
                           "status": a.get("status"), "exemplars": cites(a)})
            elif x in els:
                ar.append({"id": x, "element": True, "status": els[x].get("status"), "exemplars": cites(els[x].get("evidence"))})
            else:
                ar.append({"id": x, "unresolved": True})
        fs = p.get("finding")
        fs = fs if isinstance(fs, list) else ([fs] if fs else [])
        props.append({"id": p["id"], "carried_by": p.get("carried_by"), "level": p.get("level"),
                      "theorised": p.get("theorised"), "thin": p.get("thin"), "rival": short(p.get("rival")) if p.get("rival") else None,
                      "evidence_gate": short(p.get("evidence_gate")), "rests_on": ar,
                      "findings": [{"id": f, "warrant": (finds.get(f) or {}).get("warrant"), "status": (finds.get(f) or {}).get("status"),
                                    "resolves": f in finds} for f in fs],
                      "falsify_elsewhere": short(p.get("falsify_elsewhere")) if p.get("falsify_elsewhere") else None,
                      "statement": short(p.get("statement"), 300)})
    branches = []
    for b in jl(os.path.join(OUT, "branches-D5.jsonl")):
        branches.append({"branch": b.get("branch"), "n": b.get("n"), "form_or_grouping": b.get("form_or_grouping"),
                         "shared_warrant": short(b.get("shared_warrant"), 160), "shared_status": b.get("shared_status"),
                         "confidence": b.get("confidence"), "verdicts": b.get("verdicts"),
                         "propositions_hold": b.get("propositions_hold"), "propositions_fail": b.get("propositions_fail"),
                         "propositions_not_testable": b.get("propositions_not_testable"),
                         "binds": short(b.get("binds"), 160), "unresolved_members": b.get("unresolved_members") if isinstance(b.get("unresolved_members"), int) else len(b.get("unresolved_members") or []),
                         "exemplars": cites(b), "canvas_read": (b.get("canvas") or {}).get("read")})
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a).")[1].strip(),
                      "propositions": props, "branches": branches,
                      "carried_by": dict(collections.Counter(p["carried_by"] for p in props)),
                      "branch_warrants": dict(collections.Counter(str(b["shared_status"]) for b in branches)),
                      "branch_kinds": dict(collections.Counter(str(b["form_or_grouping"]) for b in branches))},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
