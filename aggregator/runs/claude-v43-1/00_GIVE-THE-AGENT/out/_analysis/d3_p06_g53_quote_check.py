#!/usr/bin/env python3
"""D3a-48: check every single-quoted segment in notes-D3.md's G53 paragraph against P06's element record
(out/model/elements.jsonl) and the history lines naming P06. Prints each segment with FOUND or NOT FOUND. Writes nothing.

  python3 out/_analysis/d3_p06_g53_quote_check.py
"""
import json
import re

notes = open("out/notes-D3.md", encoding="utf-8").read()
g53 = notes.split("- **G53 (logged at D3a-48")[1].split("## Where the mass is")[0]
el = next(json.loads(l) for l in open("out/model/elements.jsonl", encoding="utf-8")
          if l.strip() and json.loads(l)["id"] == "P06")
texts = [v if isinstance(v, str) else json.dumps(v, ensure_ascii=False) for v in el.values()]
texts += [l for l in open("out/model/history.jsonl", encoding="utf-8") if "P06" in l]
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(g53)
miss = 0
for s in segs:
    ok = any(s in t for t in texts)
    miss += not ok
    print("%s: '%s'" % ("FOUND" if ok else "NOT FOUND", s))
print("segments %d; not found %d" % (len(segs), miss))
