"""B1e: quote chosen concepts through cite.py, one line each, for copying into the scheme's exemplars.

usage: python3 out/_analysis/b1e_cite.py sub/c0012 sub/c0040 ...
"""
import subprocess
import sys

for a in sys.argv[1:]:
    sub, code = a.split("/")
    out = subprocess.run(["python3", "tools/cite.py", "--room", sub, "--code", code, "--stage", "B1"],
                         capture_output=True, text=True).stdout
    q = [x for x in out.splitlines() if x.startswith('"')]
    print(q[0] if q else "NONE %s" % a)
