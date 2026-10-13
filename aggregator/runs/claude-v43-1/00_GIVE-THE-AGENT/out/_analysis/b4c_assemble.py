#!/usr/bin/env python3
"""B4c: assemble both arms' returns of the blind sample (notes-B4.md, "The check (B4c)", declared before any figure).

What it reads, and only that:
  arm 1  out/_fleet_raw/B4/<packet>/r<k>.jsonl, the accepted returns (never <reader>.failed.txt), each with its
         r<k>.meta.json, which must say valid; and r<k>.raw.txt, whose JSON lines must equal the .jsonl's
  arm 2  out/_fleet_raw/B4-openai-astra/<packet>/oa<k>.jsonl with oa<k>.state.json (valid) and oa<k>.raw.txt,
         which must match SHA256SUMS and whose JSON lines must equal the .jsonl's; nothing under interrupted-*
  the cells     out/_analysis/b4b_order*.json (four records): each packet's items by position, checked against
                out/_packets-B4/MANIFEST.json (count and codes_by_item's fleet ids, in order)
  the ids       out/fleet_ids.jsonl, fleet ids back to room ids; out/scheme_final.jsonl, the frozen theme ids
  the strata    out/sample-B4.jsonl (U and A, packets S05-01 to S05-34), out/sample-B4-R.jsonl (R, S05-35 to S05-48)

Each pass-1 item line is keyed on (packet, position). The typed T2- id is a label: it must translate back to the
cell's item, and the typed room must be that item's room. Every concept id in support, support_by_theme,
also_present and the multiplacement records must translate back to a concept of that item. Every third-order id
must be in the frozen scheme. A line that fails is refused by name and its reading is missing. Lines with
"revises" are the second pass, kept apart; prediction lines are kept apart. In each packet the two accepted
returns, ordered by reader number, are readings 1 and 2.

Writes (dry run without --write): out/_analysis/b4c_readings.jsonl (every pass-1 reading, room ids),
out/_analysis/b4c_pass2.jsonl, out/_analysis/b4c_predictions.jsonl, out/_analysis/b4c_assemble.json (counts,
refusals, checks).

    python3 out/_analysis/b4c_assemble.py [--write]
"""
import argparse, collections, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
RAW = os.path.join(OUT, "_fleet_raw")
ARMS = {"deepseek-v4.1-flash": ("B4", r"^r(\d+)\.jsonl$"), "openai-gpt-6-astra": ("B4-openai-astra", r"^oa(\d+)\.jsonl$")}
ORDERS = ("b4b_order.json", "b4b_order_R.json", "b4b_order_R_all.json", "b4b_order_R_ua.json")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def raw_json_lines(p):
    rows = []
    for ln in open(p, encoding="utf-8"):
        s = ln.strip()
        if s.startswith("{"):
            try:
                rows.append(json.loads(s))
            except ValueError:
                rows.append({"__unparsed__": s[:80]})
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    man = json.load(open(os.path.join(OUT, "_packets-B4", "MANIFEST.json"), encoding="utf-8"))
    cells = {}
    for f in ORDERS:
        for pk, its in json.load(open(os.path.join(AN, f), encoding="utf-8"))["packets"].items():
            cells[pk] = [tuple(i.split("/")) for i in its]
    if sorted(cells) != sorted(man):
        sys.exit("the order records and MANIFEST.json name different packets")
    back, fwd, codes = {}, {}, collections.defaultdict(set)
    for r in jl(os.path.join(OUT, "fleet_ids.jsonl")):
        back[r["fleet"]] = (r["sub"], r["id"])
        if r["kind"] == "t":
            fwd[(r["sub"], r["id"])] = r["fleet"]
    for pk, its in cells.items():
        if len(its) != man[pk]["items"] or [fwd[k] for k in its] != list(man[pk]["codes_by_item"]):
            sys.exit("%s: the order record and MANIFEST.json disagree on the items" % pk)
        for k in its:
            codes[k] = set(man[pk]["codes_by_item"][fwd[k]])
    scheme = {r["id"] for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    s0 = {(x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "sample-B4.jsonl"))}
    sr = {(x["sub"], x["theme_id"]): x for x in jl(os.path.join(OUT, "sample-B4-R.jsonl"))}
    sums = {}
    for ln in open(os.path.join(RAW, "B4-openai-astra", "SHA256SUMS"), encoding="utf-8"):
        h, f = ln.rstrip("\n").split("  ", 1)
        sums[f] = h

    readings, pass2, preds, refused, checks = [], [], [], [], collections.Counter()
    for arm, (folder, pat) in ARMS.items():
        base = os.path.join(RAW, folder)
        for pk in sorted(cells):
            d = os.path.join(base, pk)
            acc = sorted((int(re.match(pat, f).group(1)), f) for f in os.listdir(d) if re.match(pat, f))
            if len(acc) != 2:
                refused.append({"arm": arm, "packet": pk, "why": "%d accepted returns, not 2" % len(acc)})
                continue
            for rep, (num, f) in enumerate(acc, 1):
                rid = f[:-len(".jsonl")]
                where = "%s %s/%s" % (arm, pk, rid)
                if arm.startswith("deepseek"):
                    m = json.load(open(os.path.join(d, rid + ".meta.json"), encoding="utf-8"))
                    if m.get("valid") is not True:
                        refused.append({"arm": arm, "packet": pk, "reader": rid, "why": "meta not valid"}); continue
                else:
                    st = json.load(open(os.path.join(d, rid + ".state.json"), encoding="utf-8"))
                    if st.get("valid") is not True:
                        refused.append({"arm": arm, "packet": pk, "reader": rid, "why": "state not valid"}); continue
                    rel = "%s/%s.raw.txt" % (pk, rid)
                    if sums.get(rel) != sha(os.path.join(d, rid + ".raw.txt")):
                        refused.append({"arm": arm, "packet": pk, "reader": rid, "why": "raw.txt does not match SHA256SUMS"}); continue
                    checks["arm2 raw.txt matches SHA256SUMS"] += 1
                lines = jl(os.path.join(d, f))
                if lines != raw_json_lines(os.path.join(d, rid + ".raw.txt")):
                    checks["%s: .jsonl differs from raw.txt's JSON lines" % arm] += 1
                    print("NOTE %s: .jsonl differs from raw.txt's JSON lines" % where)
                else:
                    checks["%s: .jsonl equals raw.txt's JSON lines" % arm] += 1
                seen = collections.Counter()
                for i, x in enumerate(lines, 1):
                    w = "%s line %d" % (where, i)
                    if "predicted_confusion" in x:
                        preds.append(dict(x, arm=arm, packet=pk, reader=rid)); continue
                    if "revises" in x:
                        p = x.get("revises")
                        if not isinstance(p, int) or not 1 <= p <= len(cells[pk]):
                            refused.append({"arm": arm, "packet": pk, "reader": rid, "line": i, "why": "pass 2 revises no cell"}); continue
                        k = cells[pk][p - 1]
                        pass2.append({"arm": arm, "packet": pk, "reader": rid, "replicate": rep, "position": p,
                                      "sub": k[0], "theme_id": k[1], "third_order": x.get("third_order"),
                                      "changed": x.get("changed"), "why_changed": x.get("why_changed")})
                        continue
                    if "theme_id" not in x or "position" not in x:
                        refused.append({"arm": arm, "packet": pk, "reader": rid, "line": i, "why": "neither an item, a prediction nor a pass-2 line"}); continue
                    p = x["position"]
                    if not isinstance(p, int) or not 1 <= p <= len(cells[pk]):
                        refused.append({"arm": arm, "packet": pk, "reader": rid, "line": i, "why": "position %r is no cell" % p}); continue
                    k = cells[pk][p - 1]
                    why = []
                    if back.get(x["theme_id"]) != k:
                        why.append("typed %s is not the cell's item %s/%s" % (x["theme_id"], k[0], k[1]))
                    if re.sub(r"^r/", "", str(x.get("sub"))) != k[0]:
                        why.append("typed room %s is not %s" % (x.get("sub"), k[0]))
                    to = x.get("third_order")
                    if not isinstance(to, list) or any(t not in scheme for t in to):
                        why.append("third_order %r outside the frozen scheme" % (to,))
                    cited = list(x.get("support") or [])
                    for v in (x.get("support_by_theme") or {}).values():
                        cited += v
                    for v in (x.get("also_present") or {}).values():
                        cited += v
                    for mp in x.get("multiplacement_log") or []:
                        for fld in ("support_primary", "support_additional"):
                            cited += list(mp.get(fld) or [])
                    foreign = sorted({c for c in cited if c not in codes[k]})
                    if foreign:
                        why.append("concepts not the item's own: %s" % foreign)
                    if why:
                        refused.append({"arm": arm, "packet": pk, "reader": rid, "line": i, "position": p, "why": "; ".join(why)}); continue
                    seen[p] += 1
                    tr = lambda ids: [back[c][1] for c in ids or []]
                    stratum = "R" if int(pk[4:]) >= 35 else s0[k]["stratum"]
                    readings.append({"arm": arm, "packet": pk, "reader": rid, "replicate": rep, "position": p,
                                     "sub": k[0], "theme_id": k[1], "item": "%s/%s" % k, "stratum": stratum,
                                     "third_order": to, "multi": x.get("multi"), "confidence": x.get("confidence"),
                                     "read": x.get("read"), "families_opened": x.get("families_opened"), "bag": x.get("bag"),
                                     "support": tr(x.get("support")),
                                     "support_by_theme": {t: tr(v) for t, v in (x.get("support_by_theme") or {}).items()},
                                     "also_present": {t: tr(v) for t, v in (x.get("also_present") or {}).items()},
                                     "why": x.get("why"), "multiplacement_log": x.get("multiplacement_log") or []})
                dup = [p for p, n in seen.items() if n > 1]
                if dup:
                    refused.append({"arm": arm, "packet": pk, "reader": rid, "why": "positions given twice: %s" % dup})
                    readings = [r for r in readings if not (r["arm"] == arm and r["packet"] == pk and r["reader"] == rid and r["position"] in dup)]
                miss = [p for p in range(1, len(cells[pk]) + 1) if not seen.get(p)]
                if miss:
                    refused.append({"arm": arm, "packet": pk, "reader": rid, "why": "positions without a pass-1 line: %s" % miss})

    per = collections.Counter((r["arm"], r["stratum"]) for r in readings)
    due = collections.Counter()
    for pk, its in cells.items():
        for k in its:
            due["R" if int(pk[4:]) >= 35 else s0[k]["stratum"]] += 2
    print("readings by arm and stratum (due per arm: %s):" % dict(due))
    for k in sorted(per):
        print("  %s %s %d" % (k[0], k[1], per[k]))
    print("pass-2 lines %s; prediction lines %s" % (dict(collections.Counter(r["arm"] for r in pass2)),
                                                     dict(collections.Counter(r["arm"] for r in preds))))
    print("checks %s" % dict(checks))
    print("refused %d" % len(refused))
    for r in refused:
        print("  REFUSED %s" % json.dumps(r))
    if not a.write:
        return
    for name, rows in (("b4c_readings.jsonl", readings), ("b4c_pass2.jsonl", pass2), ("b4c_predictions.jsonl", preds)):
        p = os.path.join(AN, name)
        if os.path.exists(p):
            sys.exit("%s exists" % p)
        with open(p, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump({"readings": {"%s %s" % k: n for k, n in sorted(per.items())}, "due_per_arm": dict(due),
               "pass2": len(pass2), "predictions": len(preds), "checks": dict(checks), "refused": refused,
               "inputs": {"assign_final": sha(os.path.join(OUT, "assign_final.jsonl")),
                          "sample_B4": sha(os.path.join(OUT, "sample-B4.jsonl")),
                          "sample_B4_R": sha(os.path.join(OUT, "sample-B4-R.jsonl")),
                          "manifest": sha(os.path.join(OUT, "_packets-B4", "MANIFEST.json"))}},
              open(os.path.join(AN, "b4c_assemble.json"), "w", encoding="utf-8"), indent=1)
    print("wrote b4c_readings.jsonl (%d), b4c_pass2.jsonl (%d), b4c_predictions.jsonl (%d), b4c_assemble.json"
          % (len(readings), len(pass2), len(preds)))


if __name__ == "__main__":
    main()
