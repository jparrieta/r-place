"""Print one room's second-order themes for B1 reading: header, theme note and every concept
label (with hour), through mem.py so that every read is logged (rule 1).

usage: python3 out/_analysis/b1_room.py <sub> [tNN ...] [--words]
  --words also prints the first 90 characters of the participant's words for each concept.
"""
import re
import subprocess
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
words = "--words" in sys.argv
sub = args[0]
want = args[1:]


def mem(*a):
    r = subprocess.run(["python3", "tools/mem.py", *a, "--stage", "B1"], capture_output=True, text=True)
    return r.stdout


ids = []
for line in mem("themes", "--rooms", sub).splitlines():
    m = re.match(r"\s+%s/(t\d+)\s" % re.escape(sub), line)
    if m:
        ids.append(m.group(1))
if want:
    ids = [i for i in ids if i in want]

for tid in ids:
    out = mem("theme", "%s/%s" % (sub, tid), "--limit", "3000")
    for line in out.splitlines():
        if line.startswith("r/"):
            print("\n" + line[:150])
        elif line.startswith("placed:"):
            print(line[:200])
        elif line.startswith("note:"):
            print(line[:520])
        elif re.match(r"c\d{4}", line):
            parts = line.split("|")
            m = re.search(r"h\s*([+-]?\d+\.\d+)", parts[0])
            hour = m.group(1) if m else "?"
            cid = line[:5]
            label = parts[1].strip()[:100] if len(parts) > 1 else ""
            text = (" || " + parts[2].strip()[:90]) if words and len(parts) > 2 else ""
            print("  %s %7s %s%s" % (cid, hour, label, text))
