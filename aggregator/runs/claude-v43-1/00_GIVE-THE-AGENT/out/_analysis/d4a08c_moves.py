#!/usr/bin/env python3
"""D4a-08c: name the six forms (the cut recommended for the appendix) as moves, one at a time: print the tier_history
line (flushed), log the move, snap it. Subprocess output goes to stderr only.

    python3 out/_analysis/d4a08c_moves.py --start 308 >> out/tier_history.jsonl
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, required=True)
a = ap.parse_args()
n = a.start
for f in "ABCDEF":
    line = subprocess.run([sys.executable, os.path.join(AN, "d4a08c_write.py"), "--what", "tier", "--form", f, "--move-no", str(n)],
                          capture_output=True, text=True, check=True).stdout.strip()
    print(line, flush=True)
    rec = json.loads(line)
    text = ("move %d (merging): room form %s of D4a-08c named, '%s' (%d rooms, core rooms placed by their codes); %s. Ground: the "
            "rooms' selected changes and coded concepts; no canvas, verdict or branch. tier_history line appended; snap follows."
            % (n, f, rec["name"], rec["members_n"], rec["why"]))
    lg = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", text, "--kind", "move", "--ids", "D4a08c-" + f],
                        capture_output=True, text=True, cwd=ROOT)
    sys.stderr.write(lg.stdout)
    if lg.returncode:
        sys.exit("log failed at %s" % f)
    sn = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "D4", "move-merging-%d" % n], capture_output=True, text=True, cwd=ROOT)
    sys.stderr.write(sn.stdout[-200:])
    if sn.returncode:
        sys.exit("snap failed at %s" % f)
    n += 1
sys.stderr.write("moves made: 6, last move %d\n" % (n - 1))
