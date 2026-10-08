"""For each room-name search, the number of rooms `mem.py codes --grep <re> --by-room` lists, and
the read rooms past its first page of 80, so a search run on the first page only can be re-checked.

usage: python3 out/_analysis/b1_listing_pages.py <read_rooms_file> "<label>=<regex>" ...
"""
import re
import subprocess
import sys

read = {l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()}
for arg in sys.argv[2:]:
    label, rx = arg.split("=", 1)
    rooms = []
    offset = 0
    while True:
        cmd = ["python3", "tools/mem.py", "codes", "--grep", rx, "--by-room"]
        if offset:
            cmd += ["--offset", str(offset)]
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        page = [l.split()[0] for l in out.splitlines()
                if re.match(r"^\S+\s+\d+\s+h", l)]
        rooms += page
        m = re.search(r"\[(?:end: )?lines \d+-(\d+) of (\d+)", out)
        if not m or int(m.group(1)) >= int(m.group(2)) or not page:
            break
        offset += 80
    past = [r for r in rooms[80:] if r in read]
    print("%s\t%d rooms\tread rooms past 80: %s" % (label, len(rooms), ", ".join(past) or "none"))
