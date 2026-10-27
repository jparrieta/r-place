#!/usr/bin/env python3
"""E1 section 1, the quotes against the raw record: quote-check-E1.json (the handler's check, outside the session).

    python3 out/audit-E1/quote_check_raw.py > out/audit-E1/quote_check_raw.json

Reports both shares as the file gives them, its totals and method, and lists every missing case-account string with a
first sorting by script, declared before the run (E1a). The sorting only says where to look; what each string is (a
quote from outside the room's corpus, a paraphrase in quote marks, an invention) is read by hand in the audit section.
For each missing string, in the coded record (codes.jsonl `text`, which holds the coded passages, not the raw corpus):
  - in_room_codes: the string, lower-cased with end punctuation trimmed, is in one of the room's concepts;
  - in_other_codes: it is in a concept of another room (a quote from outside the room's corpus, if not in the room's);
  - best_ratio: the best difflib ratio of the string against any window of the room's concepts of the same length
    (0.85 or more suggests a near quote with words changed);
  - non_ascii_share: the share of letters outside ASCII (a sign of a translation or a non-English quote);
  - in_case_twice: the string occurs more than once in the case account.
Also: the listed strings against the file's own count of missing strings (case_quotes minus case_found).
"""
import collections, difflib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def low(s):
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return " ".join(s.split()).lower().strip(" ,.;:!?'\"()")


def best_ratio(s, texts):
    best = 0.0
    n = len(s)
    for t in texts:
        if abs(len(t) - n) < n * 0.5 and len(t) <= 3 * n:
            best = max(best, difflib.SequenceMatcher(None, s, t).ratio())
            continue
        step = max(1, n // 4)
        for i in range(0, max(1, len(t) - n + 1), step):
            r = difflib.SequenceMatcher(None, s, t[i:i + n]).quick_ratio()
            if r > best:
                best = max(best, difflib.SequenceMatcher(None, s, t[i:i + n]).ratio())
    return round(best, 3)


def main():
    q = json.load(open(os.path.join(ROOT, "quote-check-E1.json"), encoding="utf-8"))
    codes = [json.loads(l) for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8")]
    by_room = collections.defaultdict(list)
    for c in codes:
        by_room[c["sub"]].append(low(c.get("text") or ""))
    allcodes = "\x00".join(t for ts in by_room.values() for t in ts)
    rows = []
    for r in q["rooms"]:
        case = open(os.path.join(ROOT, "package", r["sub"], "case.md"), encoding="utf-8").read()
        for s in r["case_missing"]:
            ls = low(s)
            in_room = any(ls in t for t in by_room[r["sub"]])
            letters = [ch for ch in s if ch.isalpha()]
            rows.append({"sub": r["sub"], "string": s,
                         "in_room_codes": in_room,
                         "in_other_codes": (not in_room) and ls in allcodes,
                         "best_ratio": best_ratio(ls, by_room[r["sub"]]),
                         "non_ascii_share": round(sum(1 for ch in letters if ord(ch) > 127) / len(letters), 3) if letters else 0,
                         "in_case_twice": case.count(s.strip('"')) > 1})
    t = q["totals"]
    near = sum(1 for x in rows if not x["in_room_codes"] and x["best_ratio"] >= 0.85)
    print(json.dumps({
        "seed": q.get("seed"), "rooms_sampled": q.get("rooms_sampled"), "method": q.get("method"), "totals": t,
        "code_quote_found_share": q["code_quote_found_share"], "case_quote_found_share": q["case_quote_found_share"],
        "missing_by_count": t["case_quotes"] - t["case_found"], "missing_listed": len(rows),
        "rooms_with_missing": sum(1 for r in q["rooms"] if r["case_missing"]),
        "sorting": {"in_room_codes": sum(x["in_room_codes"] for x in rows),
                    "in_other_codes_only": sum(x["in_other_codes"] for x in rows),
                    "near_quote_0.85": near,
                    "non_ascii_over_0.2": sum(1 for x in rows if x["non_ascii_share"] > 0.2),
                    "none_of_these": sum(1 for x in rows if not x["in_room_codes"] and not x["in_other_codes"]
                                         and x["best_ratio"] < 0.85)},
        "rows": rows}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
