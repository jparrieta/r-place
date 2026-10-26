#!/usr/bin/env python3
"""D4a-08: name the five carried room forms as moves, one at a time: print the tier_history line (flushed), log the
move through mem.py log --kind move, then snap it. Subprocess output goes to stderr only.

    python3 out/_analysis/d4a08_moves.py --start 295 >> out/tier_history.jsonl
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
T = json.load(open(os.path.join(AN, "d4a08e_forms.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a08_names.json"), encoding="utf-8"))["5"]
ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, required=True)
a = ap.parse_args()
C = T["cuts"]["5"]
n = a.start
for f in sorted(C["forms"]):
    line = subprocess.run([sys.executable, os.path.join(AN, "d4a08_write.py"), "--what", "tier", "--form", f, "--move-no", str(n)],
                          capture_output=True, text=True, check=True).stdout.strip()
    print(line, flush=True)
    rec = json.loads(line)
    sig = "; ".join("%s in %.0f per cent of defining members" % (d["name"], 100 * d["presence"]) for d in C["forms"][f]["sig_T4"][:3]) or "no change signature"
    text = ("move %d (merging): room form %s of D4a-08 named, '%s' (%d defining rooms by Ward, %d placed by the whole mix of both "
            "blocks; %s; %s). Ground: the rooms' selected changes and coded concepts; no canvas, verdict or branch. tier_history "
            "line appended; snap follows." % (n, f, NAMES[f][0], C["forms"][f]["ward_n"], rec["members_n"], sig, NAMES[f][2]))
    lg = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", text, "--kind", "move", "--ids", "D4a08-" + f],
                        capture_output=True, text=True, cwd=ROOT)
    sys.stderr.write(lg.stdout)
    if lg.returncode:
        sys.exit("log failed at %s: %s" % (f, lg.stderr[-300:]))
    sn = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "D4", "move-merging-%d" % n],
                        capture_output=True, text=True, cwd=ROOT)
    sys.stderr.write(sn.stdout[-200:])
    if sn.returncode:
        sys.exit("snap failed at %s" % f)
    n += 1
sys.stderr.write("moves made: %d, last move %d\n" % (len(C["forms"]), n - 1))
