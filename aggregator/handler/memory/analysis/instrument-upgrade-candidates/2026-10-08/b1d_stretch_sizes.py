"""B1d: the chosen rooms not yet reread, in the seeded order, with their sizes, to declare a stretch.

usage: python3 out/_analysis/b1d_stretch_sizes.py [--n 30]

Sizes from `mem.py room <sub> --size`: forest, codes and second-order themes in bytes. The running total
counts codes plus second-order themes (the stretch's measure, as at B1b) and, beside it, the forest.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, "tools")
import saturation as S  # noqa: E402

n_max = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 30

listing = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                         capture_output=True, text=True).stdout
order = [(int(ln.split("\t")[0]), ln.split("\t")[1]) for ln in listing.splitlines() if "\t" in ln]
st = S.store(".")
an = S.analysed(".", "out", st)
chosen = S.read_chosen("out", an) or []
done = set()
p = os.path.join("out", "pass2-B1.jsonl")
if os.path.exists(p):
    for line in open(p, encoding="utf-8"):
        if line.strip():
            done.add(json.loads(line).get("sub"))

tot = forest_tot = 0
k = 0
print("order\tsub\tforest\tcodes\tthemes\tcodes+themes\trunning\trunning_forest")
for pos, sub in order:
    if sub not in chosen or sub in done:
        continue
    out = subprocess.run(["python3", "tools/mem.py", "room", sub, "--size"], capture_output=True, text=True).stdout
    m = re.search(r"forest (\d+)\s+codes (\d+)\s+second-order themes (\d+)", out)
    f, c, t = (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (0, 0, 0)
    tot += c + t
    forest_tot += f
    k += 1
    print("%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d" % (pos, sub, f, c, t, c + t, tot, forest_tot))
    if k >= n_max:
        break
print("chosen %d, reread %d" % (len(chosen), len([s for s in chosen if s in done])))
