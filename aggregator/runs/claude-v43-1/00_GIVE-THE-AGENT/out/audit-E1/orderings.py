#!/usr/bin/env python3
"""E1 section 1, orderings proved by snaps. For each ordering the stage file names, what the snaps in out/_snap/ show:
the snap's hash equals the file's as it stands, or the file moved after the snap, and when.

    python3 out/audit-E1/orderings.py > out/audit-E1/orderings.json

Declared before the run (E1a). A snap is out/_snap/<name>.sha256: a header '# snap <stage> <label> at <utc> over out'
and lines '<sha256>  <size>  <mtime>  <path>'. Snaps are ordered by the header's time. For each key file the script
gives its history: every distinct hash in snap order, with the first and last snap that hold it, and whether the file
as it stands has the last one. The orderings:
  1. the scheme frozen before B3's first batch (scheme_final.jsonl; B3's first fleet call in _fleet_raw/B3/log.jsonl);
  2. prior.md sections 1 to 6 sealed before B1's first theme_discovery.jsonl line (prior.md's hashes before and after);
  3. sections 7 and 8 sealed at D1 (_closes/prior-D1.sha256) before DROPS/D was ingested (the first snap listing
     adaptations.jsonl);
  4. the model hashed at C5's close (_closes/model-C5.sha256) before D1, and the model's later hashes (D3, D6, now);
  5. every D4 move or cut snap before projections-D4.jsonl and the chunk-share tree (no such snap lists them);
  6. every D6 proposal: its first snap, whether its line changed after, its status, and its base model version.
The move snaps against the moves are in moves.py. A snap holds hashes only, so a file's sections cannot be told apart
by it; where a whole file moved, the script says so and the audit section reads what moved.
"""
import glob, hashlib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402


def snaps():
    out = []
    for p in glob.glob(os.path.join(OUT, "_snap", "*.sha256")):
        with open(p, encoding="utf-8") as f:
            head = f.readline()
            m = re.search(r"^# snap (\S+) (\S+) at (\S+)", head)
            if not m:
                continue
            files = {}
            for line in f:
                parts = line.rstrip("\n").split("  ", 3)
                if len(parts) == 4:
                    files[parts[3]] = parts[0]
        out.append({"name": os.path.basename(p)[:-7], "stage": m.group(1), "label": m.group(2), "t": m.group(3),
                    "files": files})
    return sorted(out, key=lambda s: s["t"])


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None


def history(sn, rel):
    runs = []
    for s in sn:
        h = s["files"].get(rel)
        if h is None:
            continue
        if runs and runs[-1]["hash"] == h:
            runs[-1]["last"], runs[-1]["n"] = (s["name"], s["t"]), runs[-1]["n"] + 1
        else:
            runs.append({"hash": h, "first": (s["name"], s["t"]), "last": (s["name"], s["t"]), "n": 1})
    now = sha(os.path.join(OUT, rel))
    return {"distinct_hashes_in_order": len(runs), "runs": [dict(r, hash=r["hash"][:12]) for r in runs],
            "now": now[:12] if now else None, "now_equals_last_snap": bool(runs) and runs[-1]["hash"] == now}


def first_t(p, key="t"):
    for l in open(p, encoding="utf-8"):
        if l.strip():
            try:
                return json.loads(l).get(key)
            except ValueError:
                return None


def main():
    sn = snaps()
    res = {"snaps": len(sn), "first": sn[0]["t"] if sn else None, "last": sn[-1]["t"] if sn else None}
    keys = ["scheme_final.jsonl", "prior.md", "model/elements.jsonl", "model/arrows.jsonl", "fourth/fourth.jsonl",
            "dimensions.jsonl", "branches.jsonl", "crosslinks.jsonl", "projections-D4.jsonl", "chunk-share-D4.jsonl",
            "chunk-share-D4.md", "propositions.jsonl", "findings.jsonl", "proposals-D6.jsonl", "account.md",
            "sealed/EXPECTATIONS.jsonl", "sealed/FIELD.jsonl", "adaptations.jsonl", "adjudications.jsonl"]
    res["histories"] = {k: history(sn, k) for k in keys}
    # 1. the scheme before B3's first batch
    b3 = first_t(os.path.join(OUT, "_fleet_raw", "B3", "log.jsonl"))
    b3_calls = [json.loads(l) for l in open(os.path.join(OUT, "_fleet_raw", "B3", "log.jsonl"), encoding="utf-8") if l.strip()]
    ts = sorted(str(r.get("t") or r.get("utc") or r.get("started") or "") for r in b3_calls if (r.get("t") or r.get("utc") or r.get("started")))
    before = [s for s in sn if ts and s["t"] < ts[0] and "scheme_final.jsonl" in s["files"]]
    res["1_scheme_before_B3"] = {"b3_first_call": ts[0] if ts else None, "b3_log_keys": sorted(b3_calls[0]) if b3_calls else None,
                                 "last_snap_before_listing_scheme": (before[-1]["name"], before[-1]["t"],
                                                                     before[-1]["files"]["scheme_final.jsonl"][:12]) if before else None,
                                 "scheme_now": (sha(os.path.join(OUT, "scheme_final.jsonl")) or "")[:12]}
    # 2. prior.md before B1's first theme
    td = first_t(os.path.join(OUT, "theme_discovery.jsonl"))
    pb = [s for s in sn if td and s["t"] < td and "prior.md" in s["files"]]
    res["2_prior_before_B1_theme"] = {"first_theme_discovery_t": td,
                                      "last_snap_before": (pb[-1]["name"], pb[-1]["t"], pb[-1]["files"]["prior.md"][:12]) if pb else None,
                                      "snaps_before_listing_prior": len(pb)}
    # 3. sections 7 and 8 at D1, before the return was ingested
    seal = open(os.path.join(OUT, "_closes", "prior-D1.sha256")).read().split()[0]
    seal_first = next((s for s in sn if s["files"].get("prior.md") == seal), None)
    ingest = next((s for s in sn if "adaptations.jsonl" in s["files"]), None)
    res["3_prior_sealed_D1_before_ingest"] = {"prior_D1_seal": seal[:12], "prior_now_equals_seal": sha(os.path.join(OUT, "prior.md")) == seal,
                                              "first_snap_with_seal_hash": (seal_first["name"], seal_first["t"]) if seal_first else None,
                                              "first_snap_listing_adaptations": (ingest["name"], ingest["t"]) if ingest else None}
    # 4. the model at C5's close, D3 and D6
    res["4_model"] = {"C5": vlib.frozen_hash(OUT, "C5"), "D3": vlib.frozen_hash(OUT, "D3"), "D6": vlib.frozen_hash(OUT, "D6"),
                      "now": vlib.model_hash(OUT),
                      "C5_close_snaps": [(s["name"], s["t"]) for s in sn if s["stage"] == "C5" and s["label"].startswith("cut-close")][-1:],
                      "first_D1_snap": next(((s["name"], s["t"]) for s in sn if s["stage"] == "D1"), None)}
    # 5. D4 snaps against the projection and the chunk-share tree
    d4 = [s for s in sn if s["stage"] == "D4" and ("-move-" in s["name"] or "-cut-" in s["name"])]
    lists = [(s["name"], [f for f in ("projections-D4.jsonl", "chunk-share-D4.jsonl", "chunk-share-D4.md") if f in s["files"]]) for s in d4]
    proj_first = next(((s["name"], s["t"]) for s in sn if "projections-D4.jsonl" in s["files"]), None)
    res["5_D4"] = {"d4_move_or_cut_snaps": len(d4),
                   "listing_projection_or_chunk_share": [(n, f) for n, f in lists if f],
                   "first_snap_listing_projection": proj_first,
                   "last_D4_move_snap": next(((s["name"], s["t"]) for s in reversed(d4) if "-move-" in s["name"]), None),
                   "branches_now_equals_last_D4_snap": next((s["files"].get("branches.jsonl") for s in reversed(d4) if "branches.jsonl" in s["files"]), None) == sha(os.path.join(OUT, "branches.jsonl"))}
    # 6. the D6 proposals
    props = [json.loads(l) for l in open(os.path.join(OUT, "proposals-D6.jsonl"), encoding="utf-8") if l.strip()]
    res["6_D6_proposals"] = {"n": len(props), "status": sorted({p.get("status") for p in props}),
                             "base_model_version": sorted({str(p.get("base_model_version"))[:12] for p in props}),
                             "frozen_D3": (vlib.frozen_hash(OUT, "D3") or "")[:12],
                             "legs": [(p["id"], p.get("leg")) for p in props],
                             "amendments_D6_lines": sum(1 for l in open(os.path.join(OUT, "amendments-D6.jsonl")) if l.strip()),
                             "proposals_file_history": res["histories"]["proposals-D6.jsonl"]}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main())
