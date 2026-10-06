#!/usr/bin/env python3
"""build_all.py — build every room of the census that has a raw24 file, resumably.

    python3 _tools/build_all.py --raw24 <dir> --census <_window97_recount_740.json> \
        --briefs <store/briefs dir> --instrument _instrument/v31 [--seconds 150] [--only a,b]

Rooms are built smallest first; a room whose STATE.json says built is skipped, so the script
can be run again and again until it prints "all built". --seconds stops after that many
seconds so a call with a time limit ends cleanly.
"""
import argparse, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw24", required=True)
    ap.add_argument("--census", required=True)
    ap.add_argument("--briefs", required=True)
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--rooms", default="rooms")
    ap.add_argument("--seconds", type=int, default=150)
    ap.add_argument("--only")
    ap.add_argument("--min-items", type=int, default=1)
    a = ap.parse_args()
    d = json.load(open(a.census))
    subs = [(s, v["in97"]) for s, v in d.items() if os.path.exists(os.path.join(a.raw24, s + ".jsonl"))]
    subs = [x for x in subs if x[1] >= a.min_items]
    if a.only:
        want = set(a.only.split(","))
        subs = [x for x in subs if x[0] in want]
    subs.sort(key=lambda x: (x[1], x[0]))
    t0 = time.time()
    built = skipped = failed = 0
    for s, n in subs:
        out = os.path.join(a.rooms, s)
        sp = os.path.join(out, "STATE.json")
        if os.path.exists(sp) and json.load(open(sp)).get("built"):
            skipped += 1
            continue
        if time.time() - t0 > a.seconds:
            print("time budget reached; built %d, skipped %d, failed %d, remaining %d"
                  % (built, skipped, failed, len(subs) - built - skipped - failed))
            return 2
        brief = os.path.join(a.briefs, s + ".md")
        cmd = ["python3", os.path.join(HERE, "build_room.py"), "--sub", s,
               "--raw", os.path.join(a.raw24, s + ".jsonl"), "--out", out,
               "--instrument", a.instrument]
        if os.path.exists(brief):
            cmd += ["--brief", brief, "--brief-source", "Gioia v36 store, the room's earlier run"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            failed += 1
            print("FAILED", s, r.stderr[-400:])
            open(os.path.join(a.rooms, "_build_failures.log"), "a").write("%s\n%s\n" % (s, r.stderr[-2000:]))
        else:
            built += 1
            print(r.stdout.strip())
    print("all built: built %d, skipped %d, failed %d" % (built, skipped, failed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
