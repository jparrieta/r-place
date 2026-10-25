#!/usr/bin/env python3
"""D4: run several cuts in order through d4_cut.py, each a move. With --dry it runs each spec's dry run and prints the
members and the checks, writing nothing. With --write, for each spec in order: run d4_cut.py --write; only after it
reports the branch written, log the move with mem.py log --kind move --ids <id> (the move number, its name, the cut,
level, key, members, name, what it changes, ground), then snap it with snap.py D4 move-<stem>-<n>. Stops at the
first failure, so nothing is logged for a cut that was not written. Move numbers start at --first.

    python3 out/_analysis/d4_cut_batch.py --leg D4a-02 --first 208 --dry  out/_analysis/d4a02_cut_F07.json ...
    python3 out/_analysis/d4_cut_batch.py --leg D4a-02 --first 208 --write out/_analysis/d4a02_cut_F07.json ...
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--leg", required=True)
ap.add_argument("--first", type=int, required=True)
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--dry", action="store_true")
g.add_argument("--write", action="store_true")
ap.add_argument("specs", nargs="+")
a = ap.parse_args()
CUT = os.path.join(ROOT, "out", "_analysis", "d4_cut.py")


def run(args):
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=ROOT)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


n = a.first
for p in a.specs:
    spec = json.load(open(p, encoding="utf-8"))
    rc, out = run([CUT, "--spec", p, "--leg", a.leg] + (["--write"] if a.write else []))
    m = re.search(r"^members: (.*)$", out, re.M)
    members = m.group(1).split(", ") if m else []
    if rc != 0 or (a.write and "wrote branch" not in out):
        print("FAILED at %s:\n%s" % (spec["id"], out[-1500:]))
        sys.exit(1)
    if a.dry:
        print("%s (%s, %s, parent %s): %d members; %s" % (spec["id"], spec["keys"][0], spec["level"], spec["parent"],
                                                        len(members), [l for l in out.splitlines() if l.startswith("form:")][0]))
        continue
    kindtxt = "subform %s of %s" % (spec["id"], spec["parent"]) if spec["parent"] else "branch %s named" % spec["id"]
    text = ("move %d (%s), %s: %s at the %s order, key %s, %d members (read from the level matrix by d4_cut.py). "
            "Name: %s. What it changes: %s Ground: %s." % (n, spec["move"], a.leg, kindtxt, spec["level"],
                                                          ", ".join(spec["keys"]), len(members), spec["name"],
                                                          spec["what_it_changes"], spec["ground"]))
    rc2, out2 = run([os.path.join(ROOT, "tools", "mem.py"), "log", text, "--kind", "move", "--ids", spec["id"]])
    if rc2 != 0:
        print("LOG FAILED at %s:\n%s" % (spec["id"], out2[-800:]))
        sys.exit(1)
    stem = spec["move"].split()[0]
    rc3, out3 = run([os.path.join(ROOT, "tools", "snap.py"), "D4", "move-%s-%d" % (stem, n)])
    snapline = [l for l in out3.splitlines() if l.startswith("snap ")]
    if rc3 != 0 or not snapline:
        print("SNAP FAILED at %s:\n%s" % (spec["id"], out3[-800:]))
        sys.exit(1)
    print("%s written (%d members); move %d logged; %s" % (spec["id"], len(members), n, snapline[0][:90]))
    n += 1
