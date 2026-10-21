#!/usr/bin/env python3
"""D3a-47: check that every id a guard list names is named in a logged reading of the rule. The diary is read through
`mem.py diary --grep "<rule>'s readings"`; an id counts as named when its room-and-number appears in an entry's text.
Prints the ids not named. Writes nothing.

  python3 out/_analysis/d3_guard_named.py --rule G52 --ids AyyMD-050 Fez-053 ...
"""
import argparse
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--rule", required=True)
ap.add_argument("--ids", nargs="+", required=True)
a = ap.parse_args()
out = subprocess.run(["python3", "tools/mem.py", "diary", "--grep", "%s's readings" % a.rule],
                     capture_output=True, text=True).stdout
text = "\n".join(l for l in out.splitlines() if "%s's readings" % a.rule in l)
missing = [i for i in a.ids if i not in text]
print("ids checked: %d; named in a reading: %d; not named: %d" % (len(a.ids), len(a.ids) - len(missing), len(missing)))
for i in missing:
    print("  " + i)
