#!/usr/bin/env python3
"""E1 section 1, the moves and provenance (E1b-03): the D6 proposals against their evidence and their record; the
data files across D6a-09 to D6a-18; the tier history by stage and tier. Prints JSON.

    python3 out/audit-E1/provenance_D6.py > out/audit-E1/provenance_D6.json

The rule, declared before the run (E1b-03):
- Each line of proposals-D6.jsonl: its evidence, every concept id resolved against package/store/codes.jsonl, every
  ledger line id against adaptations.jsonl, adaptations-recheck.jsonl and adjudications.jsonl, every file named
  against out/; its status and base model version; and the diary lines that name its id, read whole by script from
  out/diary/ (stage, leg, kind, time). A proposal whose evidence does not resolve, or that no diary line records, has
  no provenance and is a defect.
- The data files across D6a-09 to D6a-18: each file's hash in the last snap of D6a-08 and in the last snap of D6a-18,
  for the model, the tiers, the tree, the ledgers, the room forms, the D6 files and the departures and defects; a file
  that moved is listed.
- tier_history.jsonl by stage and by tier (its `tier` field, else `level`), with the events after C5.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
KEY_FILES = ["model/elements.jsonl", "model/arrows.jsonl", "model/history.jsonl", "tier_history.jsonl",
             "scheme_final.jsonl", "assignments_final.jsonl", "fourth/fourth.jsonl", "dimensions.jsonl",
             "branches.jsonl", "branches-D5.jsonl", "crosslinks.jsonl", "adaptations.jsonl", "adaptations-recheck.jsonl",
             "adjudications.jsonl", "verdicts-D.jsonl", "findings.jsonl", "propositions.jsonl", "proposals-D6.jsonl",
             "amendments-D6.jsonl", "fractal-D6.jsonl", "retelling-D6.md", "room-forms-tree-rooms.tsv",
             "room-forms-D5.jsonl", "departures.jsonl", "defects.jsonl", "account.md"]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def snaps():
    out = []
    for p in glob.glob(os.path.join(OUT, "_snap", "*.sha256")):
        with open(p, encoding="utf-8") as f:
            m = re.search(r"^# snap (\S+) (\S+) at (\S+)", f.readline())
            if not m:
                continue
            files = {}
            for line in f:
                parts = line.rstrip("\n").split("  ", 3)
                if len(parts) == 4:
                    files[parts[3]] = parts[0]
        out.append({"name": os.path.basename(p)[:-7], "stage": m.group(1), "label": m.group(2), "t": m.group(3), "files": files})
    return sorted(out, key=lambda s: s["t"])


def main():
    codes = {(c["sub"], c["code_id"]) for c in jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))}
    line_ids = set()
    for f in ("adaptations.jsonl", "adaptations-recheck.jsonl", "adjudications.jsonl"):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            for r in jl(p):
                for k in ("id", "line_id", "line"):
                    if isinstance(r.get(k), str):
                        line_ids.add(r[k])
    diary = []
    for p in sorted(glob.glob(os.path.join(OUT, "diary", "*.jsonl"))):
        for r in jl(p):
            diary.append(r)
    props = jl(os.path.join(OUT, "proposals-D6.jsonl"))
    rows = []
    for pr in props:
        ev = pr.get("evidence") or {}
        res = {"id": pr["id"], "leg": pr.get("leg"), "status": pr.get("status"),
               "base": (pr.get("base_model_version") or "")[:12], "evidence_keys": sorted(ev) if isinstance(ev, dict) else type(ev).__name__}
        cs = ev.get("codes", []) if isinstance(ev, dict) else []
        bad_c = [c for c in cs if tuple(c.split(":", 1)) not in codes]
        res["codes"], res["codes_unresolved"] = len(cs), bad_c
        other = {k: v for k, v in ev.items() if k != "codes"} if isinstance(ev, dict) else {}
        unres = []
        n_other = 0
        for k, v in other.items():
            for x in (v if isinstance(v, list) else [v]):
                if not isinstance(x, str):
                    continue
                n_other += 1
                if x.endswith((".md", ".json", ".jsonl", ".txt", ".tsv", ".py")) or "/" in x:
                    path = x.split(" ")[0].split("#")[0]
                    if not (os.path.exists(os.path.join(OUT, path)) or os.path.exists(os.path.join(ROOT, path))):
                        unres.append(x)
                elif re.match(r"^[A-Za-z0-9_]+-\d{3}$", x) and x not in line_ids:
                    unres.append(x)
        res["other_evidence"], res["other_unresolved"] = n_other, unres
        dl = [d for d in diary if pr["id"] in json.dumps(d, ensure_ascii=False)]
        res["diary_lines"] = len(dl)
        res["first_diary"] = [(d.get("t"), d.get("stage"), d.get("leg"), d.get("kind")) for d in dl[:2]]
        rows.append(res)
    S = snaps()
    def last(leg):
        c = [s for s in S if s["stage"] == "D6" and leg in s["name"]]
        return c[-1] if c else None
    a, b = last("D6a-08"), last("D6a-18")
    moved = {}
    if a and b:
        for f in KEY_FILES:
            ha, hb = a["files"].get(f), b["files"].get(f)
            moved[f] = "same" if ha == hb else "moved" if ha and hb else "absent then" if not ha else "absent now"
    T = jl(os.path.join(OUT, "tier_history.jsonl"))
    by = collections.defaultdict(collections.Counter)
    for t in T:
        by[t.get("stage")][str(t.get("tier") or t.get("level"))] += 1
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-03):")[1].strip(),
                      "proposals": rows,
                      "D6a_08_to_18": {"from": a["name"] if a else None, "to": b["name"] if b else None, "files": moved},
                      "tier_history_by_stage_and_tier": {k: dict(v) for k, v in by.items()}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
