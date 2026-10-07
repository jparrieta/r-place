"""Print every member of a third-order theme with its second-order theme note and concept labels,
through out/_analysis/b1_room.py (which reads through mem.py). Read-only.
usage: python3 out/_analysis/b1_theme_members.py T3-010 [--from N] [--to M]
  --from/--to select members by their position in the theme (1-based), to print in parts."""
import json, subprocess, sys

tid = sys.argv[1]
a = sys.argv[2:]
lo = int(a[a.index("--from") + 1]) if "--from" in a else 1
hi = int(a[a.index("--to") + 1]) if "--to" in a else 10**6
for line in open("out/scheme/scheme_current.jsonl"):
    d = json.loads(line)
    if d["theme"] != tid:
        continue
    members = d["members"]
    print("%s %s: %d members" % (tid, d["label"], len(members)))
    for i, m in enumerate(members, 1):
        if i < lo or i > hi:
            continue
        r = subprocess.run(["python3", "out/_analysis/b1_room.py", m["sub"], m["theme_id"]],
                           capture_output=True, text=True)
        out = [l for l in r.stdout.splitlines() if not l.startswith("note: placements")]
        print("#%d" % i)
        print("\n".join(out))
