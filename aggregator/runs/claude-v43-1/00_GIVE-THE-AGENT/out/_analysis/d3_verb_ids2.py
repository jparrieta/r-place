#!/usr/bin/env python3
"""D3: list the ids the verb `mem.py adaptations --element <id>` returns, page by page, and report repeats and the
total, to explain a difference between the verb's count and the helpers' count. Supersedes d3_verb_ids.py, which
did not stop at the end of the verb's pages: this version reads the total from the first page's footer
('[lines a-b of N') and stops there. Writes nothing.

    python3 out/_analysis/d3_verb_ids2.py --element P18
"""
import argparse, collections, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
a = ap.parse_args()


def page(offset):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "adaptations", "--element", a.element,
                        "--offset", str(offset), "--limit", "100"], cwd=ROOT, capture_output=True, text=True,
                       timeout=60)
    return r.stdout.splitlines()


first = page(0)
m = next((re.search(r"of (\d+)", l) for l in first if l.startswith("[lines")), None)
total = int(m.group(1)) if m else 0
ids, offset, lines = [], 0, first
while offset < total and offset < 5000:
    if offset:
        lines = page(offset)
    for l in lines:
        parts = l.split()
        if len(parts) > 2 and not l.startswith(("[", " ", "#")) and re.match(r"^[\w.-]+-\d{3}$", parts[0]):
            ids.append((parts[0], parts[1]))
    offset += 100
count = collections.Counter(i for i, _ in ids)
print("%s: verb total %d, %d lines read, %d distinct ids" % (a.element, total, len(ids), len(count)))
for i, n in count.items():
    if n > 1:
        print("repeated: %s x%d, ops %s" % (i, n, [op for j, op in ids if j == i]))
print("ops:", dict(collections.Counter(op for _, op in ids)))
