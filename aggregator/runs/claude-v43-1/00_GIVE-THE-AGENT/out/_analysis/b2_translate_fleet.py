#!/usr/bin/env python3
"""B2 from round 3 (and the model for B3): translate a fleet round's returns back to room ids before scoring
(J, 2026-10-12 09:14 Berlin), with out/fleet_ids.jsonl.

For each return line: theme_id (T2-.....) becomes the room's tNN; every concept id (C.......) in support,
also_present and multiplacement_log.codes becomes the room's cNNNN. A fleet id the table lacks, an id of
another room, or a concept of another second-order theme is kept as given and reported (it is the reader's
error, on the record). The returns in _fleet_raw stay as the dispatch left them; translated copies go to
out/_analysis/b2_r<K>_returns/<packet>/<reader>.jsonl, which the round's scorer reads.

    python3 out/_analysis/b2_translate_fleet.py --round 3 [--write]
"""
import argparse, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    fc, ft = {}, {}
    for r in jl(os.path.join(OUT, "fleet_ids.jsonl")):
        if r["kind"] == "c":
            fc[r["fleet"]] = (r["sub"], r["id"], r["theme"])
        else:
            ft[r["fleet"]] = (r["sub"], r["id"])
    raw = os.path.join(OUT, "_fleet_raw", "B2", "round-%s" % a.round)
    dst = os.path.join(OUT, "_analysis", "b2_r%s_returns" % a.round)
    # a rescue record (the handler's, round 3) names the three replies kept per packet; only those are read
    rescue = [f for f in os.listdir(raw) if f.startswith("RESCUE-") and f.endswith(".json")]
    kept = None
    if rescue:
        kept = {pk: set(v["kept"]) for pk, v in json.load(open(os.path.join(raw, sorted(rescue)[-1]), encoding="utf-8"))["packets"].items()}
        print("reading the replies kept by %s" % sorted(rescue)[-1])
    probs, n = [], 0
    for pkd in sorted(os.listdir(raw)):
        d = os.path.join(raw, pkd)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".jsonl") or (kept is not None and f[:-6] not in kept.get(pkd, ())):
                continue
            out = []
            for i, x in enumerate(jl(os.path.join(d, f)), 1):
                n += 1
                where = "%s/%s line %d" % (pkd, f, i)
                # round 3's readers write the room as "r/name"; the table writes "name"
                sub, fid = re.sub(r"^/?r/", "", str(x.get("sub") or "")), x.get("theme_id")
                x = dict(x, sub=sub)
                tt = ft.get(fid)
                if tt is None or tt[0] != sub:
                    probs.append("%s: theme id %s is %s" % (where, fid, "not in the table" if tt is None else "r/%s's" % tt[0]))
                    tid = fid
                else:
                    tid = tt[1]
                y = dict(x, theme_id=tid, fleet_theme_id=fid)

                def tr(c):
                    m = fc.get(c)
                    if m is None:
                        probs.append("%s: concept %s is not in the table" % (where, c)); return c
                    if m[0] != sub or m[2] != tid:
                        probs.append("%s: concept %s is %s/%s's (of %s), not the item's" % (where, c, m[0], m[1], m[2]))
                    return m[1]
                y["support"] = [tr(c) for c in x.get("support") or []]
                if isinstance(x.get("also_present"), dict):
                    y["also_present"] = {t: [tr(c) for c in (cs if isinstance(cs, list) else [cs])]
                                         for t, cs in x["also_present"].items()}
                ml = x.get("multiplacement_log")
                if isinstance(ml, dict) and ml.get("codes"):
                    y["multiplacement_log"] = dict(ml, codes=[tr(c) for c in ml["codes"]])
                for k, v in list((x.get("why") or {}).items()):
                    y.setdefault("why_fleet", {})[k] = v
                y["why"] = {k: re.sub(r"C\d{7}", lambda m: (fc.get(m.group(0)) or (None, m.group(0)))[1], str(v))
                            for k, v in (x.get("why") or {}).items()}
                y.pop("why_fleet", None)
                out.append(y)
            if a.write:
                os.makedirs(os.path.join(dst, pkd), exist_ok=True)
                with open(os.path.join(dst, pkd, f), "w", encoding="utf-8") as fh:
                    for y in out:
                        fh.write(json.dumps(y, ensure_ascii=False) + "\n")
    for p in probs:
        print(p)
    print("%d lines; %d id problems%s" % (n, len(probs), "; translated copies in %s" % dst if a.write else ""))


if __name__ == "__main__":
    main()
