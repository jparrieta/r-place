#!/usr/bin/env python3
"""E1 section 1, orderings proved by snaps (E1b-02): the move snaps from C2 to D3 in the order of their numbers; the
D4 branch cuts against the projection; the D6 proposals against their snaps and status. Prints JSON.

    python3 out/audit-E1/snap_order.py > out/audit-E1/snap_order.json

The rule, declared before the run (E1b-02):
- A move snap is out/_snap/<stage>-move-<name>-<n>.sha256; its time is its header's. From C2 to D3, the snaps sorted by
  move number should also be sorted by time; every pair where a higher number has an earlier time is listed.
- D4: the branch cuts are the move snaps whose snap changed branches.jsonl from the snap before it (the handler's rule
  for check_orderings, QE1-001). The projection is the first snap that lists projections-D4.jsonl, chunk-share-D4.jsonl
  or chunk-share-D4.md. The ordering holds if every branch cut's snap is earlier than the projection. The D4 snaps that
  list the projection are counted, with how many changed branches.jsonl from the snap before.
- D6: each line of proposals-D6.jsonl with its id, leg, status and base model version; the hash of proposals-D6.jsonl
  in each D6 snap; amendments-D6.jsonl's line count.
"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
PROJ = ("projections-D4.jsonl", "chunk-share-D4.jsonl", "chunk-share-D4.md")


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
        name = os.path.basename(p)[:-7]
        mm = re.match(r"^([A-E]\d)-move-(.+)-(\d+)$", name)
        out.append({"name": name, "stage": m.group(1), "t": m.group(3), "files": files,
                    "move": int(mm.group(3)) if mm else None})
    return sorted(out, key=lambda s: s["t"])


def main():
    S = snaps()
    res = {}
    mv = [s for s in S if s["move"] is not None and s["stage"] in ("C2", "C3", "C4", "C5", "D3")]
    by_n = sorted(mv, key=lambda s: (s["move"], s["t"]))
    inv = [(a["name"], a["t"], b["name"], b["t"]) for a, b in zip(by_n, by_n[1:]) if b["t"] < a["t"]]
    nums = [s["move"] for s in by_n]
    res["C2_to_D3"] = {"move_snaps": len(mv), "numbers": [min(nums), max(nums)] if nums else None,
                       "distinct_numbers": len(set(nums)), "repeated_numbers": sorted({n for n in nums if nums.count(n) > 1}),
                       "missing_numbers": sorted(set(range(min(nums), max(nums) + 1)) - set(nums)) if nums else [],
                       "inversions": inv, "by_stage": {st: [min(s["move"] for s in mv if s["stage"] == st),
                                                           max(s["move"] for s in mv if s["stage"] == st)]
                                                      for st in ("C2", "C3", "C4", "C5", "D3") if any(s["stage"] == st for s in mv)}}
    d4 = [s for s in S if s["stage"] == "D4"]
    prev, cuts, after = None, [], []
    first_proj = next((s for s in S if any(f in s["files"] for f in PROJ)), None)
    for s in d4:
        b = s["files"].get("branches.jsonl")
        changed = prev is not None and b is not None and b != prev
        if s["move"] is not None and changed:
            cuts.append((s["move"], s["name"], s["t"]))
        if any(f in s["files"] for f in PROJ):
            after.append({"name": s["name"], "t": s["t"], "changed_branches": changed})
        if b is not None:
            prev = b
    res["D4"] = {"snaps": len(d4), "first_projection_snap": [first_proj["name"], first_proj["t"]] if first_proj else None,
                 "branch_cuts": len(cuts), "branch_cut_moves": [cuts[0][0], cuts[-1][0]] if cuts else None,
                 "last_branch_cut": cuts[-1][1:] if cuts else None,
                 "branch_cuts_after_projection": [c for c in cuts if first_proj and c[2] >= first_proj["t"]],
                 "snaps_listing_projection": len(after),
                 "of_them_changed_branches": sum(1 for a in after if a["changed_branches"]),
                 "branches_now_equals_last_D4_snap": None}
    import hashlib
    now_b = hashlib.sha256(open(os.path.join(OUT, "branches.jsonl"), "rb").read()).hexdigest()
    last_b = next((s["files"]["branches.jsonl"] for s in reversed(d4) if "branches.jsonl" in s["files"]), None)
    res["D4"]["branches_now_equals_last_D4_snap"] = now_b == last_b
    props = [json.loads(l) for l in open(os.path.join(OUT, "proposals-D6.jsonl"), encoding="utf-8") if l.strip()]
    keys = sorted({k for p in props for k in p})
    res["D6"] = {"keys": keys,
                 "proposals": [{k: p.get(k) for k in ("id", "leg", "status", "base_model_version", "kind", "target") if k in p}
                               for p in props],
                 "file_in_D6_snaps": [(s["name"], s["files"].get("proposals-D6.jsonl", "")[:12]) for s in S
                                      if s["stage"] == "D6" and "proposals-D6.jsonl" in s["files"]][:40],
                 "amendments_D6_lines": sum(1 for l in open(os.path.join(OUT, "amendments-D6.jsonl"), encoding="utf-8")
                                            if l.strip()) if os.path.exists(os.path.join(OUT, "amendments-D6.jsonl")) else None}
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-02):")[1].strip(), **res},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
