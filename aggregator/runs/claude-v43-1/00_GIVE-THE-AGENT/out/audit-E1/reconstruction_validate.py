#!/usr/bin/env python3
"""E1 section 4, the check leg (E1d): the reconstruction returns validated from the readers' raw files, and fidelity.

    python3 out/audit-E1/reconstruction_validate.py > out/audit-E1/reconstruction_validate.json
    python3 out/audit-E1/reconstruction_validate.py --lines > out/reconstruction-E1.jsonl

The rule, declared before the run (E1d), after the principal investigator's message of 27 October 22:51Z: fleet.py
judged all 30 returns exhausted because each reader ended its lines with a marker the packet asked for and
RETURN-E1.md did not name, so the returns are validated here from the raw files.
- For each sampled room (reconstruction-sample-E1.jsonl): the newest raw file, out/_fleet_raw/E1/<sub>/r*.raw.txt by
  modification time. Its lines are read in order; a final line that is not JSON is dropped and recorded; any other
  line that is not JSON makes the return invalid.
- A valid return: claim lines with sub equal to the room, accounted one of yes, partly, no, unresolved, and a last
  summary line whose counts equal the claim lines (claims, yes, partly, no, unresolved). A mismatch is recorded and
  the claim lines decide.
- Fidelity: yes plus half of partly, over yes, partly and no; unresolved apart. Contradicted: no lines whose reason
  begins "contradicts".
- By branch and by verdict (the sample's): rooms, mean fidelity, the claims and their four counts summed.
Amended at E1d, after the first run (its output kept as reconstruction_validate.superseded-1.json): a sub written
r/<room> is read as the room, since the packets name each room so and RETURN-E1.md's template does not say which
form. The form written is recorded (sub_written), and the rooms valid under the first rule are counted apart
(valid_strict).
"""
import collections, glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
ACC = ("yes", "partly", "no", "unresolved")


def main():
    sample = [json.loads(l) for l in open(os.path.join(OUT, "reconstruction-sample-E1.jsonl"), encoding="utf-8") if l.strip()]
    rows, problems = [], []
    for s in sample:
        sub = s["sub"]
        files = sorted(glob.glob(os.path.join(OUT, "_fleet_raw", "E1", sub, "r*.raw.txt")), key=os.path.getmtime)
        rec = dict(s)
        if not files:
            rec["valid"] = rec["valid_strict"] = False
            problems.append((sub, "no raw file"))
            rows.append(rec)
            continue
        p = files[-1]
        lines = [l for l in open(p, encoding="utf-8").read().split("\n") if l.strip()]
        dropped = None
        try:
            json.loads(lines[-1])
        except ValueError:
            dropped = lines.pop()
        objs, bad = [], 0
        for l in lines:
            try:
                objs.append(json.loads(l))
            except ValueError:
                bad += 1
        claims = [o for o in objs if not o.get("summary")]
        summ = [o for o in objs if o.get("summary")]
        c = collections.Counter(o.get("accounted") for o in claims)
        contra = sum(1 for o in claims if o.get("accounted") == "no" and str(o.get("reason", "")).lower().startswith("contradict"))
        other = [o.get("accounted") for o in claims if o.get("accounted") not in ACC]
        written = sorted({str(o.get("sub")) for o in objs})
        strict_wrong = sum(1 for o in objs if o.get("sub") != sub)
        wrong_sub = sum(1 for o in objs if o.get("sub") not in (sub, "r/" + sub))
        sm = summ[-1] if summ else {}
        mismatch = [k for k in ("yes", "partly", "no", "unresolved") if sm.get(k) != c.get(k, 0)] + \
                   (["claims"] if sm.get("claims") != len(claims) else [])
        den = c["yes"] + c["partly"] + c["no"]
        ok = bad == 0 and bool(summ) and not other
        rec.update({"valid": ok and not wrong_sub, "valid_strict": ok and not strict_wrong,
                    "sub_written": written[0] if len(written) == 1 else written,
                    "raw_file": os.path.relpath(p, OUT), "attempts": len(files),
                    "marker_dropped": dropped[:40] if dropped else None,
                    "claims": len(claims), **{k: c.get(k, 0) for k in ACC}, "contradicted": contra,
                    "fidelity": round((c["yes"] + 0.5 * c["partly"]) / den, 3) if den else None,
                    "model_version": (sm.get("model_version") or "")[:12], "local_status": sm.get("local_status"),
                    "summary_mismatch": mismatch, "non_json_lines": bad, "other_values": other[:3], "wrong_sub": wrong_sub})
        if not rec["valid"] or mismatch:
            problems.append((sub, {"valid": rec["valid"], "mismatch": mismatch, "bad": bad, "other": other[:3]}))
        rows.append(rec)
    if "--lines" in sys.argv:
        for r in rows:
            print(json.dumps({k: r.get(k) for k in ("sub", "branch", "verdict", "fidelity", "claims", "yes", "partly", "no",
                                                    "unresolved", "contradicted", "model_version", "local_status",
                                                    "raw_file", "marker_dropped", "sub_written", "valid", "valid_strict")},
                             ensure_ascii=False))
        return
    def agg(key, keep):
        g = collections.defaultdict(list)
        for r in rows:
            if r.get("fidelity") is not None and keep(r):
                g[r[key]].append(r)
        return {k: {"rooms": len(v), "mean_fidelity": round(sum(x["fidelity"] for x in v) / len(v), 3),
                    **{a: sum(x[a] for x in v) for a in ("claims",) + ACC + ("contradicted",)}} for k, v in sorted(g.items())}
    vals = [r["fidelity"] for r in rows if r.get("fidelity") is not None and r.get("valid")]
    strict = [r["fidelity"] for r in rows if r.get("fidelity") is not None and r.get("valid_strict")]
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1d)")[1].strip(),
                      "rooms": len(rows), "valid": sum(1 for r in rows if r.get("valid")),
                      "valid_strict": sum(1 for r in rows if r.get("valid_strict")),
                      "markers_dropped": dict(collections.Counter(r.get("marker_dropped") for r in rows)),
                      "sub_written": dict(collections.Counter("r/<room>" if str(r.get("sub_written")).startswith("r/") else "<room>" for r in rows)),
                      "mean_fidelity": round(sum(vals) / len(vals), 3) if vals else None,
                      "mean_fidelity_strict": round(sum(strict) / len(strict), 3) if strict else None,
                      "min_max": [min(vals), max(vals)] if vals else None,
                      "totals": {a: sum(r.get(a, 0) for r in rows if r.get("valid")) for a in ("claims",) + ACC + ("contradicted",)},
                      "local_status": dict(collections.Counter(r.get("local_status") for r in rows)),
                      "model_version": dict(collections.Counter(r.get("model_version") for r in rows)),
                      "by_verdict": agg("verdict", lambda r: r.get("valid")),
                      "by_branch": agg("branch", lambda r: r.get("valid")),
                      "by_verdict_strict": agg("verdict", lambda r: r.get("valid_strict")),
                      "problems": problems, "rows": rows}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
