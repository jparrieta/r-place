#!/usr/bin/env python3
"""D4a-05: make the room tree's moves in order, one at a time: print the move's tier_history line (flushed,
so the redirect has written it before the snap), log the move through mem.py log --kind move, then snap it
with tools/snap.py. Forms B to H first (A was move 238), then every sub-form depth-first. The subprocesses'
own output goes to stderr, never into the redirected file.

    python3 out/_analysis/d4a05_moves.py --start 239 >> out/tier_history.jsonl
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
T = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
NAMES = json.load(open(os.path.join(AN, "d4a05_names.json"), encoding="utf-8"))
ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, required=True)
a = ap.parse_args()
NODES = {n["id"]: n for n in T["nodes"]}


def parent_of(nid):
    return nid.rsplit(".", 1)[0] if "." in nid else None


def children(nid):
    return sorted((k for k in NODES if parent_of(k) == nid), key=lambda k: int(k.rsplit(".", 1)[1]))


order = [f for f in sorted(T["forms"]) if f != "A"]
for f in sorted(T["forms"]):
    stack = children(f)
    while stack:
        nid = stack.pop(0)
        order.append(nid)
        stack = children(nid) + stack
n = a.start
for nid in order:
    line = subprocess.run([sys.executable, os.path.join(AN, "d4a05_write.py"), "--what", "tier", "--node", nid,
                           "--move-no", str(n)], capture_output=True, text=True, check=True).stdout.strip()
    print(line, flush=True)
    rec = json.loads(line)
    node = NODES[nid]
    if nid in T["forms"]:
        sig = "; ".join("%s %s %.2f of members' changes, %.1f times the population, in %.0f per cent of members"
                        % (d["node"], d["name"], d["share"], d["ratio"], 100 * d["presence"]) for d in T["forms"][nid]["sig_T4"])
        text = ("move %d (merging): room form %s named, '%s' (%d rooms; %s). Ground: the rooms' selected changes; no "
                "canvas, verdict or branch. tier_history line appended; snap follows." % (n, nid, NAMES[nid][0], node["n"], sig))
    else:
        text = ("move %d (splitting): room sub-form %s declared under %s, '%s' (%d rooms; %s). Ground: the rooms' "
                "selected changes. tier_history line appended; snap follows." % (n, nid, parent_of(nid), NAMES[nid][0],
                                                                                 node["n"], rec["why"]))
    lg = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", text, "--kind", "move",
                         "--ids", nid], capture_output=True, text=True, cwd=ROOT)
    sys.stderr.write(lg.stdout + lg.stderr[-300:] if lg.returncode else lg.stdout)
    if lg.returncode:
        sys.exit("log failed at %s" % nid)
    sn = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "D4", "move-%s-%d" % (rec["move"], n)],
                        capture_output=True, text=True, cwd=ROOT)
    sys.stderr.write(sn.stdout[-200:])
    if sn.returncode:
        sys.exit("snap failed at %s" % nid)
    n += 1
sys.stderr.write("moves made: %d, last move %d\n" % (len(order), n - 1))
