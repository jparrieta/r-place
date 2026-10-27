#!/usr/bin/env python3
"""E1 section 1, the quotes against the raw record, second pass (E1b-01): what the 389 case-account strings that
quote-check-E1.json lists as missing from the room's corpus are. Reads quote-check-E1.json; prints JSON.

    python3 out/audit-E1/case_missing_read.py > out/audit-E1/case_missing_read.json

The rule, declared before the run (E1b-01):
- Each string is compared lower-cased, with curly quotes made straight, single quotes inside it taken as the
  record's double quotes, white space collapsed and the end's punctuation trimmed; an ellipsis or a bracketed
  insertion splits it into parts that must all be found in one text.
- It takes the first of these that holds it, in this order:
  (1) "coded passage": a concept text of the room (the raw check missed it on punctuation or marks);
  (2) "coder's label": a second-order theme or concept label of the room (themes.jsonl second_order, codes.jsonl
      first_order and second_order), or a label held the other way round (the string holds the whole label);
  (3) "thread title": a title of the room's threads (package/store/threads.jsonl);
  (4) "coder's brief": the room's brief.md;
  (5) "forest item": the room's forest (trees/<sub>.md; item text there is clipped);
  (6) "another room's concept": a concept text of another room;
  (7) "near quote": a difflib ratio of 0.85 or more against a window of the room's concept texts (words changed);
  (8) "read by hand": none of these.
- The file lists at most ten missing strings for a room; the rooms where it lists fewer than case_quotes minus
  case_found are named, so the 389 against 548 is explained, not assumed.
"""
import collections, difflib, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SPLIT = re.compile(r"\.\.\.|…|\[[^\]]*\]")


def low(s):
    for a in ("“", "”", "‘", "’", '"', "'", "\\"):
        s = s.replace(a, "")
    return " ".join(s.split()).lower().strip(" ,.;:!?()")


def parts(s):
    return [low(p) for p in SPLIT.split(s) if low(p)]


def held(s, texts):
    ps = parts(s)
    if not ps:
        return False
    for t in texts:
        if all(p in t for p in ps):
            return True
    return False


def held_back(s, labels):
    ls = low(s)
    return any(l and len(l) >= 12 and l in ls for l in labels)


def ratio(s, texts):
    s = low(s)
    n, best = len(s), 0.0
    for t in texts:
        for i in range(0, max(1, len(t) - n + 1), max(1, n // 4)):
            w = t[i:i + n]
            m = difflib.SequenceMatcher(None, s, w)
            if m.quick_ratio() > best:
                best = max(best, m.ratio())
    return round(best, 3)


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    qc = json.load(open(os.path.join(ROOT, "quote-check-E1.json"), encoding="utf-8"))
    codes = jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
    by_sub = collections.defaultdict(list)
    for c in codes:
        by_sub[c["sub"]].append(c)
    titles = collections.defaultdict(list)
    for t in jl(os.path.join(ROOT, "package", "store", "threads.jsonl")):
        titles[t["sub"]].append(low(t.get("title") or ""))
    rows, capped = [], []
    for room in qc["rooms"]:
        sub = room["sub"]
        miss = room["case_missing"]
        if len(miss) < room["case_quotes"] - room["case_found"]:
            capped.append({"sub": sub, "missing_by_count": room["case_quotes"] - room["case_found"], "listed": len(miss)})
        if not miss:
            continue
        own = [low(c.get("text") or "") for c in by_sub[sub]]
        labels = [low(c.get(f) or "") for c in by_sub[sub] for f in ("first_order", "second_order")]
        tp = os.path.join(ROOT, "package", sub, "themes.jsonl")
        labels += [low(t.get("second_order") or "") for t in jl(tp)] if os.path.exists(tp) else []
        bp = os.path.join(ROOT, "package", sub, "brief.md")
        brief = [low(open(bp, encoding="utf-8").read())] if os.path.exists(bp) else []
        fp = os.path.join(ROOT, "trees", sub + ".md")
        forest = [low(open(fp, encoding="utf-8", errors="replace").read())] if os.path.exists(fp) else []
        for s in miss:
            if held(s, own):
                k = "coded passage"
            elif held(s, labels) or held_back(s, labels):
                k = "coder's label"
            elif held(s, titles[sub]):
                k = "thread title"
            elif held(s, brief):
                k = "coder's brief"
            elif held(s, forest):
                k = "forest item"
            else:
                k = None
            r = {"sub": sub, "string": s, "class": k}
            rows.append(r)
    pend = [r for r in rows if r["class"] is None]
    others = [(c["sub"], low(c.get("text") or "")) for c in codes]
    for r in pend:
        ps = parts(r["string"])
        hit = [sub for sub, t in others if sub != r["sub"] and ps and all(p in t for p in ps)]
        if hit:
            r["class"], r["other_room"] = "another room's concept", hit[0]
            continue
        b = ratio(r["string"], [low(c.get("text") or "") for c in by_sub[r["sub"]]])
        r["ratio"] = b
        r["class"] = "near quote" if b >= 0.85 else "read by hand"
    cnt = collections.Counter(r["class"] for r in rows)
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01):")[1].strip(),
                      "listed": len(rows), "by_class": dict(cnt.most_common()),
                      "missing_by_count": sum(r["case_quotes"] - r["case_found"] for r in qc["rooms"]),
                      "capped_rooms": capped,
                      "listed_in_capped_rooms": sum(c["listed"] for c in capped),
                      "missing_in_capped_rooms": sum(c["missing_by_count"] for c in capped),
                      "rows": rows}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
