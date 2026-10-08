"""Write each named room's concept dump (b1_room_codes.py) to <dir>/<prefix><sub>.txt, so that
b1_shared_many.py can compare one room with many partners in one call.

usage: python3 out/_analysis/b1_dump_rooms.py <dir> <prefix> <sub> [<sub> ...]
"""
import os
import subprocess
import sys

folder, prefix = sys.argv[1], sys.argv[2]
for sub in sys.argv[3:]:
    out = subprocess.run(["python3", "out/_analysis/b1_room_codes.py", sub],
                         capture_output=True, text=True).stdout
    with open(os.path.join(folder, prefix + sub + ".txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
print("wrote %d dumps" % (len(sys.argv) - 3))
