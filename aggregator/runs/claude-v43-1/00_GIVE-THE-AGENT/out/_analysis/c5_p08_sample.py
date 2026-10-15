#!/usr/bin/env python3
"""C5a-02, the P08 test (rules in notes-C5.md): run c2_first_concepts.py for P05:P08 over the rooms where A04's order
fails, save its whole output once to c5_p08_fails.txt, draw 40 rooms with seed 20261015, save the sample to
c5_p08_sample.json, and print for each sampled room its first P08 concept and its first P05 concept, whole. Refuses to
redraw an existing sample; --print reprints it.

    python3 out/_analysis/c5_p08_sample.py [--print]
"""
import json, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "out", "_analysis")
TXT, SJ = os.path.join(A, "c5_p08_fails.txt"), os.path.join(A, "c5_p08_sample.json")
if "--print" not in sys.argv:
    if os.path.exists(SJ):
        sys.exit("the sample exists; run with --print")
    p = subprocess.run([sys.executable, os.path.join(A, "c2_first_concepts.py"), "--elements", "c2_elements_p4.json",
                        "--pair", "P05:P08", "--rooms", "BOTH", "--fails", "--n", "1"], cwd=ROOT, capture_output=True,
                       text=True)
    open(TXT, "w", encoding="utf-8").write(p.stdout)
    blocks = re.split(r"^== ", p.stdout, flags=re.M)
    head, rooms = blocks[0], {}
    for b in blocks[1:]:
        name = b.splitlines()[0].strip()
        p05 = re.search(r"first P05:\n(.*?)(?=\n  first P08:|\Z)", b, re.S)
        p08 = re.search(r"first P08:\n(.*?)(?=\n== |\Z)", b, re.S)
        rooms[name] = {"P05": p05.group(1).strip() if p05 else "", "P08": p08.group(1).strip() if p08 else ""}
    pick = sorted(random.Random(20261015).sample(sorted(rooms), min(40, len(rooms))))
    json.dump({"header": head.strip(), "n_rooms": len(rooms), "drawn": {k: rooms[k] for k in pick}},
              open(SJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.load(open(SJ, encoding="utf-8"))
print(s["header"])
print("rooms parsed: %d; drawn: %d" % (s["n_rooms"], len(s["drawn"])))
for i, (k, v) in enumerate(s["drawn"].items(), 1):
    print("%02d %s\n   P08: %s\n   P05: %s" % (i, k, v["P08"], v["P05"]))
