#!/usr/bin/env python3
"""E1 section 1, the manifest, whole: run_manifest.json names the model, seed and decoding behind every figure.

    python3 out/audit-E1/manifest.py > out/audit-E1/manifest.json

Declared before the run (E1a). Every entry of out/run_manifest.json with its stage, step or leg, model fields, seeds
and decoding, and which of the three it lacks. Then the figures of the fleets and readers, each with the stage whose
entry should carry it: B2 (stability-B2.md, the gold and stability rounds), B3 (fidelity-B3.md, position-B3.md),
B4 (transmission-B4.md, transmission-after-revision-B4.md), C2 (the hostile reader, review-C2.md), C5 (the three
readers, account-readers-C5.md), D2 (the verdict fleet, verdicts-D.jsonl), D3 (the labelers and the re-check readers,
adaptations-recheck.jsonl). A figure whose stage has no entry naming a model, a seed and a decoding has no
provenance and is listed.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
FIGS = [("B2", "stability-B2.md"), ("B3", "fidelity-B3.md"), ("B3", "position-B3.md"), ("B4", "transmission-B4.md"),
        ("B4", "transmission-after-revision-B4.md"), ("C2", "review-C2.md"), ("C5", "account-readers-C5.md"),
        ("D2", "verdicts-D.jsonl"), ("D3", "adaptations-recheck.jsonl")]


def has(e, pat):
    return any(re.search(pat, k) and e.get(k) not in (None, "", [], {}) for k in e)


def main():
    m = json.load(open(os.path.join(OUT, "run_manifest.json"), encoding="utf-8"))
    rows = []
    for i, e in enumerate(m, 1):
        rows.append({"n": i, "stage": e.get("stage"), "step": e.get("step") or e.get("leg"),
                     "model_keys": sorted(k for k in e if re.search(r"model", k)),
                     "has_model": has(e, r"model$|_model$|^model"), "has_seed": has(e, r"seed"),
                     "has_decoding": has(e, r"decoding|effort|temperature"),
                     "keys": sorted(e)})
    figs = []
    for st, f in FIGS:
        ents = [r for r in rows if r["stage"] == st]
        ok = [r for r in ents if r["has_model"] and r["has_seed"] and r["has_decoding"]]
        figs.append({"stage": st, "file": f, "exists": os.path.exists(os.path.join(OUT, f)), "entries": len(ents),
                     "entries_complete": len(ok), "provenance": "complete" if ok else ("partial" if ents else "none")})
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a).")[1].strip(), "entries": len(m),
                      "stages_with_entries": sorted({r["stage"] for r in rows}), "rows": rows, "figures": figs,
                      "figures_without_complete_provenance": [f for f in figs if f["provenance"] != "complete"]}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
