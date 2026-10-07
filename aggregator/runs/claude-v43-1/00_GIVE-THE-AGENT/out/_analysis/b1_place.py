"""Place a room's second-order themes through mem.py place, in the order given (the verb writes
scheme_current.jsonl and kinds-B1.jsonl; this only calls it). Stops at the first refusal.

usage: python3 out/_analysis/b1_place.py <sub> t01=T3-002 t02=T3-004,T3-103 ...
  a comma puts the theme in several third-order themes, the first being the primary.
"""
import subprocess
import sys

sub = sys.argv[1]
for arg in sys.argv[2:]:
    tid, themes = arg.split("=")
    for t in themes.split(","):
        r = subprocess.run(["python3", "tools/mem.py", "place", "%s:%s" % (sub, tid), "--theme", t, "--stage", "B1"],
                           capture_output=True, text=True)
        line = [l for l in r.stdout.splitlines() if l.startswith("placed")]
        print(line[0] if line else "REFUSED %s:%s %s %s" % (sub, tid, t, (r.stdout + r.stderr).strip()[-300:]))
        if not line:
            sys.exit(1)
