"""Print every concept of a room, paging mem.py codes --sub past its 80-line limit.

usage: python3 out/_analysis/b1_room_codes.py <sub> > $TMPDIR/<sub>_codes.txt
"""
import re
import subprocess
import sys

sub = sys.argv[1]
first = subprocess.run(["python3", "tools/mem.py", "codes", "--sub", sub],
                       capture_output=True, text=True).stdout
m = re.search(r"(\d+) concepts in", first)
total = int(m.group(1)) if m else 0
seen = 0
offset = 0
while offset < total + 80:
    out = first if offset == 0 else subprocess.run(
        ["python3", "tools/mem.py", "codes", "--sub", sub, "--offset", str(offset)],
        capture_output=True, text=True).stdout
    for line in out.splitlines():
        if re.match(r"^c\d{4}", line):
            print(line)
            seen += 1
    offset += 80
sys.stderr.write("%s: %d of %d concepts printed\n" % (sub, seen, total))
