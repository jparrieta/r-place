#!/usr/bin/env python3
"""B4a: turn my ruling drafts for one chunk of an adjudication packet into section 7's lines and append them to
out/disagreements.jsonl.

    python3 out/_analysis/b4_rule_append.py --packet 1 --draft out/_adjudication-B4/packet-01/rulings-01.jsonl [--write]

A draft line (one per item, written by me while reading the blind chunk):
  {"n": 3, "r": ["T3-023", "T3-095"], "t": "genuine-joint", "c": "arguable", "w": "one clause from the material",
   "q": "c0041" | "a participant's words" | the scheme sentence (scheme-ambiguous), "f": field, "th": theme,
   "br": "T3-001|T3-023" or absent, "sup": {"T3-095": ["c0044"]} (only where neither reading placed a theme, or to
   override), "ap": {"T3-...": ["c..", "c..", "c.."]} (a bag's other themes), "u": true (unresolved; then "r": [])}
The script reads index.tsv (the unblinding key) only to name the item: it adds sub, theme_id, the two readers' lists
in replicate order, class and B1 grouping; takes each placed theme's concepts from the reader line that placed it
(a primary: the line's support less its records' added concepts; an added theme: its record's support_additional
less the primary's); sets named_neither; turns a concept id in "q" into that concept's words (cut at a word boundary,
a substring of the store's text); and checks everything with the close-check's own functions (vlib.support_problems,
also_present_problems, cites_resolve) before anything is written. One line per item; an item already ruled is refused.

    --replace: the draft's items must already be ruled; their lines are rewritten in place, each marked "revised"
    with the UTC time, and the old file is kept as disagreements.superseded-<utc>.jsonl (a ruling corrected, not
    deleted).
"""
import argparse, collections, datetime, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib

TAX = ("scheme-ambiguous", "item-is-a-bag", "reader-error", "author-error", "genuine-joint", "author-disagrees")
FIELDS = ("must_show", "must_not_show", "decide_when_both", "discriminators")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True); ap.add_argument("--draft", required=True)
    ap.add_argument("--write", action="store_true"); ap.add_argument("--leg", default="B4a-01")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pdir = os.path.join(OUT, "_adjudication-B4", "packet-%02d" % a.packet)
    idx = {}
    for ln in open(os.path.join(pdir, "index.tsv"), encoding="utf-8").read().splitlines()[1:]:
        n, key, cl, ch, arep = ln.split("\t")
        idx[int(n)] = key
    cls = {"%s/%s" % (c["sub"], c["theme_id"]): c for c in jl(os.path.join(OUT, "b3_classes.jsonl"))}
    S = {r["id"]: r for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    lines = collections.defaultdict(dict)
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x["copy_kind"] == "corpus":
            lines["%s/%s" % (x["sub"], x["theme_id"])][x["replicate"]] = x
    recs = collections.defaultdict(list)
    for m in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        if m.get("copy_kind") == "corpus":
            recs[(m["batch"], m["position"])].append(m)
    ctx = {"package": os.path.join(ROOT, "package"), "outdir": OUT}
    vlib.store_codes(ctx)
    ct = vlib.code_themes(vlib.recut_overlay("codes", vlib.jsonl(os.path.join(ROOT, "package", "store", "codes.jsonl")) or [], OUT))
    ids = set(S)
    dp = os.path.join(OUT, "disagreements.jsonl")
    done = {"%s/%s" % (d["sub"], d["theme_id"]) for d in (jl(dp) if os.path.exists(dp) else [])}

    def gate_text(t):
        r = S.get(t, {})
        parts = [str(r.get(f) or "") for f in ("must_show", "must_not_show", "decide_when_both", "varies", "is_not", "gloss", "name")]
        parts += [str(d.get("question") or "") for d in r.get("discriminators") or [] if isinstance(d, dict)]
        return " ".join(" ".join(parts).split())

    def placed_support(key, t):
        """the concepts a reader line cites for theme t, primary or added; None if no reader placed it"""
        for rep in (1, 2):
            x = lines[key].get(rep)
            if not x:
                continue
            s = x.get("third_order") or []
            rs = recs.get((x["batch"], x["position"]), [])
            added = set()
            for m in rs:
                added |= set(m.get("support_additional") or [])
            if s and s[0] == t:
                prim = set()
                for m in rs:
                    prim |= set(m.get("support_primary") or [])
                return sorted(prim or (set(x.get("support") or []) - added) or set(x.get("support") or []))
        for rep in (1, 2):
            x = lines[key].get(rep)
            if not x:
                continue
            for m in recs.get((x["batch"], x["position"]), []):
                if m.get("additional") == t:
                    return sorted(set(m.get("support_additional") or []) - set(m.get("support_primary") or []))
        return None

    out, probs = [], []
    for d in jl(a.draft):
        n = d["n"]
        key = idx.get(n)
        w = "packet %d item %d" % (a.packet, n)
        if key is None:
            probs.append("%s: no such item" % w); continue
        if key in done and not a.replace:
            probs.append("%s (%s): already ruled" % (w, key)); continue
        if a.replace and key not in done:
            probs.append("%s (%s): not ruled yet, nothing to replace" % (w, key)); continue
        sub, tid = key.split("/")
        c = cls[key]
        readers = [c["r1"] or [], c["r2"] or []]
        union = {t for r in readers for t in r}
        ruling = list(d.get("r") or [])
        unres = bool(d.get("u"))
        tax = d.get("t")
        if tax not in TAX:
            probs.append("%s: taxonomy %r" % (w, tax))
        if unres and ruling or (not unres and not ruling):
            probs.append("%s: ruling %s with unresolved %s" % (w, ruling, unres))
        for t in ruling:
            if t not in ids:
                probs.append("%s: %s not in the frozen scheme" % (w, t))
        sup = {}
        for t in ruling:
            v = (d.get("sup") or {}).get(t)
            if v is None:
                v = placed_support(key, t)
            if not v:
                probs.append("%s: no concepts for %s (no reader placed it; give sup)" % (w, t)); continue
            sup[t] = v
        if len(ruling) > 1 and ruling[0] in sup:
            # an added theme keeps the concepts its reader cited for it; the primary gives those up where it keeps
            # others, so each theme has concepts of its own (rule 0); else the added theme gives up the overlap
            added = set()
            for t in ruling[1:]:
                added |= set(sup.get(t) or [])
            rest = [x for x in sup[ruling[0]] if x not in added]
            if rest:
                sup[ruling[0]] = rest
            else:
                for t in ruling[1:]:
                    if t in sup:
                        own = [x for x in sup[t] if x not in sup[ruling[0]]]
                        if own:
                            sup[t] = own
        q = d.get("q") or ""
        if re.fullmatch(r"c\d{4}", q):
            code = ctx["code_text"].get((sub, q))
            if code is None:
                probs.append("%s: quote concept %s not found" % (w, q)); code = ""
            elif (sub, q) not in ct or not vlib.owns(ct[(sub, q)], tid):
                probs.append("%s: quote concept %s is not the item's" % (w, q))
            words = " ".join(str(code).split())
            if len(words) > 240:
                words = words[:240].rsplit(" ", 1)[0]
            q = words
        th = d.get("th") or (ruling[0] if ruling else None)
        if tax == "scheme-ambiguous":
            if d.get("f") not in FIELDS:
                probs.append("%s: scheme-ambiguous without a field" % w)
            if " ".join(q.split()) not in gate_text(th):
                probs.append("%s: quote is not in %s's tests: %r" % (w, th, q[:60]))
        row = {"sub": sub, "theme_id": tid, "readers": readers, "ruling": ruling, "unresolved": unres,
               "taxonomy": tax, "field": d.get("f") if tax == "scheme-ambiguous" else None, "theme": th, "quote": q,
               "boundary_ruling": d.get("br"), "named_neither": bool(set(ruling) - union),
               "confidence": d.get("c"), "why": d.get("w"), "leg": a.leg, "support_by_theme": sup,
               "also_present": d.get("ap") or {}, "class": c["class"], "b1": c["b1"], "packet": a.packet, "n": n}
        if a.replace:
            row["revised"] = stamp
        if ruling:
            for pb in vlib.support_problems(sup, ruling, sub, tid, ct):
                probs.append("%s: %s" % (w, pb))
        for pb in vlib.also_present_problems(row["also_present"], ruling, sub, tid, ct, ids):
            probs.append("%s: %s" % (w, pb))
        if row["confidence"] not in ("clear", "arguable") or not str(row["why"] or "").strip():
            probs.append("%s: confidence or why missing" % w)
        if tax != "scheme-ambiguous" and q:
            # cites_resolve's test (the words a substring of some concept's text), the item's own concepts first
            wq = " ".join(q.split())
            own_texts = [" ".join(str(v).split()) for (s2, c2), v in ctx["code_text"].items() if s2 == sub]
            if not any(wq in t for t in own_texts) and not any(wq in " ".join(str(v).split()) for v in ctx["code_text"].values()):
                probs.append("%s: quote does not resolve to a participant's words" % w)
        out.append(row)
    for p in probs:
        print("PROBLEM " + p)
    tc = collections.Counter(r["taxonomy"] for r in out)
    print("%d rulings: %s; unresolved %d; named_neither %d" % (len(out), dict(tc), sum(r["unresolved"] for r in out),
                                                                 sum(r["named_neither"] for r in out)))
    if probs:
        sys.exit(1)
    if a.write and a.replace:
        new = {"%s/%s" % (r["sub"], r["theme_id"]): r for r in out}
        old = jl(dp)
        keep = os.path.join(OUT, "disagreements.superseded-%s.jsonl" % stamp)
        shutil.copyfile(dp, keep)
        with open(dp, "w", encoding="utf-8") as fh:
            for r in old:
                fh.write(json.dumps(new.get("%s/%s" % (r["sub"], r["theme_id"]), r), ensure_ascii=False) + "\n")
        print("replaced %d lines; old file kept as %s; disagreements.jsonl now %d lines"
              % (len(new), os.path.basename(keep), len(jl(dp))))
    elif a.write:
        with open(dp, "a", encoding="utf-8") as fh:
            for r in out:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("disagreements.jsonl now %d lines" % len(jl(dp)))


if __name__ == "__main__":
    main()
