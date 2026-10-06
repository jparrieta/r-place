"""For the lexicon: the item of first use of each term in one room, through cite.py (logged).

python3 out/_analysis/lex.py <sub> "term one" "term two" ...
Prints one line per term: the term, the room, the item id and hour of its earliest coded use, the code id.
"""
import json, subprocess, sys

sub, terms = sys.argv[1], sys.argv[2:]
for t in terms:
    r = subprocess.run([sys.executable, "-W", "ignore", "tools/cite.py", "--room", sub, "--grep", t, "--n", "2000",
                        "--json", "--stage", "A1"], capture_output=True, text=True)
    try:
        qs = json.loads(r.stdout)["quotes"]
    except Exception:
        print(f"{t}\t{sub}\tNOT FOUND"); continue
    if not qs:
        print(f"{t}\t{sub}\tNOT FOUND"); continue
    q = min(qs, key=lambda q: q.get("created_utc") or 0)
    h = (q["created_utc"] - 1490976000) / 3600
    print(f"{t}\t{sub}\t{q['item_id']}\th{h:+.2f}\t{q['code_id']}")
