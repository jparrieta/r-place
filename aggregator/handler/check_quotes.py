"""Handler-side, before stage E1: do the coders' quotes stand in the record?
For a seeded sample of rooms, every code's `text` is looked for in its item's words in the room's
coder corpus (the record the coder read), exactly at its offsets and anywhere in the item; and
every quoted string of 25+ characters in case.md is looked for anywhere in the room's corpus.
Reads the corpus from aggregator/input/raw/ (build_raw_record.py) first. Writes RUN/DROPS/E1/quote-check-E1.json, which stage E1 reads.
  python3 check_quotes.py [--rooms 80] [--seed 13]
"""
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from paths import P
import json, os, random, re, sys, unicodedata
R, W = P("run"), P("work")
Y = P("yard_rooms")
L = W + "/legacy"
F = P("input") + "/coders/rooms"
args = sys.argv[1:]
n = int(args[args.index("--rooms") + 1]) if "--rooms" in args else 80
seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 13
def norm(s):
    s = unicodedata.normalize("NFKC", s or "").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()
RAW = P("input") + "/raw"      # build_raw_record.py: every frame room's coder corpus, kept in the run (2026-09-30)
def corpus(sub):
    import gzip
    for p in (os.path.join(RAW, sub, "coder_corpus.jsonl.gz"), os.path.join(L, sub, "coder_corpus.jsonl"),
              os.path.join(Y, sub, "run", "coder_corpus.jsonl")):
        if os.path.exists(p) and not (sub == "Dorset" and p.startswith(L)):
            op = gzip.open if p.endswith(".gz") else open
            rows = [json.loads(l) for l in op(p, "rt", encoding="utf-8") if l.strip()][1:]
            return {r["id"]: " ".join(x for x in (r.get("title"), r.get("selftext"), r.get("body")) if x) for r in rows if r.get("id")}
    return None
subs = sorted(d for d in os.listdir(F) if os.path.isdir(os.path.join(F, d)))
rnd = random.Random(seed); sample = sorted(rnd.sample(subs, min(n, len(subs))))
tot = dict(codes=0, exact=0, inside=0, absent=0, item_missing=0, case_quotes=0, case_found=0)
rooms = []
for s in sample:
    C = corpus(s)
    if C is None:
        rooms.append({"sub": s, "note": "no corpus held"}); continue
    Cn = {k: norm(v) for k, v in C.items()}
    allc = " ".join(Cn.values())
    r = dict(sub=s, codes=0, exact=0, inside=0, absent=[], case_quotes=0, case_found=0)
    for l in open(os.path.join(F, s, "codes.jsonl"), encoding="utf-8"):
        if not l.strip(): continue
        c = json.loads(l)
        if c.get("retracted"): continue
        t = c.get("text") or ""; it = C.get(c.get("item_id"))
        r["codes"] += 1
        if it is None:
            tot["item_missing"] += 1; r["absent"].append(c["code_id"]); continue
        st, en = c.get("start"), c.get("end")
        if isinstance(st, int) and isinstance(en, int) and it[st:en] == t:
            r["exact"] += 1
        elif norm(t) and norm(t) in Cn[c["item_id"]]:
            r["inside"] += 1
        else:
            r["absent"].append(c["code_id"])
    cm = os.path.join(F, s, "case.md")
    if os.path.exists(cm):
        txt = open(cm, encoding="utf-8").read()
        quotes = [x or y for x, y in re.findall(r'(?:(?<![\w])"([^"\n]{25,400})"(?![\w]))|(?:“([^”\n]{25,400})”)', txt)]
        for q in quotes:
            r["case_quotes"] += 1
            parts = [p for p in re.split(r"\s*(?:…|\.\.\.|\[[^\]]*\])\s*", q) if len(p) > 12]
            if norm(q) in allc or (parts and all(norm(p) in allc for p in parts)):
                r["case_found"] += 1
            else:
                r.setdefault("case_missing", []).append(q[:120])
    for k in ("codes", "exact", "inside", "case_quotes", "case_found"): tot[k] += r[k]
    tot["absent"] += len(r["absent"]); r["absent"] = r["absent"][:20]
    r["case_missing"] = r.get("case_missing", [])[:10]
    rooms.append(r)
res = {"seed": seed, "rooms_sampled": len(sample), "totals": tot,
       "code_quote_found_share": round((tot["exact"] + tot["inside"]) / max(1, tot["codes"]), 4),
       "case_quote_found_share": round(tot["case_found"] / max(1, tot["case_quotes"]), 4),
       "method": "code text at its offsets in the item, else anywhere in the item after normalising case, quotes and white space; case.md strings of 25+ characters opened and closed by double quotes on one line, anywhere in the room's corpus; an ellipsis or bracketed insertion splits a string into parts that must each be found",
       "rooms": rooms}
os.makedirs(R + "/DROPS/E1", exist_ok=True)
json.dump(res, open(R + "/DROPS/E1/quote-check-E1.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rooms"}, indent=1))
