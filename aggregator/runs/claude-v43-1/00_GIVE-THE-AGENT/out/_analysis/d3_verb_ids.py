#!/usr/bin/env python3
"""D3: list the ids the verb `mem.py adaptations --element <id>` returns, page by page, and report repeats and the
total, to explain a difference between the verb's count and the helpers' count. Writes nothing.

    python3 out/_analysis/d3_verb_ids.py --element P18
"""
import argparse, collections, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
a = ap.parse_args()
ids, offset = [], 0
while True:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "adaptations", "--element", a.element,
                        "--offset", str(offset), "--limit", "100"], cwd=ROOT, capture_output=True, text=True)
    page = [l for l in r.stdout.splitlines() if l and not l.startswith(("[", " ", "#")) and len(l.split()) > 2]
    if not page:
        break
    ids.extend((l.split()[0], l.split()[1]) for l in page)
    offset += 100
count = collections.Counter(i for i, _ in ids)
print("%s: %d verb lines, %d distinct ids" % (a.element, len(ids), len(count)))
for i, n in count.items():
    if n > 1:
        print("repeated: %s x%d, ops %s" % (i, n, [op for j, op in ids if j == i]))
print("ops:", dict(collections.Counter(op for _, op in ids)))
