"""Print chosen concepts of a room (id, theme, hour, writer, label), read from its full concept
listing, so ids cited in an episode line can be checked against the store before writing.

usage: python3 out/_analysis/b1_show_codes.py <sub> c0001,c0002,...
"""
import subprocess
import sys

sub, wanted = sys.argv[1], set(sys.argv[2].split(","))
out = subprocess.run(["python3", "out/_analysis/b1_room_codes.py", sub],
                     capture_output=True, text=True).stdout
seen = set()
for line in out.splitlines():
    cid = line.split()[0] if line.strip() else ""
    if cid in wanted:
        seen.add(cid)
        print(line[:170])
missing = sorted(wanted - seen)
if missing:
    print("NOT FOUND in %s: %s" % (sub, ", ".join(missing)))
