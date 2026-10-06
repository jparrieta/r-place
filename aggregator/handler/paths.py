"""paths.py: where the handler's scripts find things, in one place.

Each key is resolved in this order: the environment variable RPLACE_<KEY> (upper case), then
aggregator/handler/paths.json, then the defaults below. Every path is relative: a relative value is
read from the repository root, and no default names a machine. The instrument's own folders sit
inside the repository. The other keys name sources outside it (the coding yard, Layer A's records,
the v37 package); their defaults are the places they sit beside the repository on the author's
machines, tried in order, the first that exists winning. Set yours in paths.json (copy
paths.example.json) before running a script that needs them.

    python3 aggregator/handler/paths.py          # print every key, its value, where it came from, and whether it exists
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))                 # the repository root (this file is in aggregator/handler/)
DEFAULTS = {                                                        # relative to the repository root
    "run": ["aggregator/runs/claude-v43-1"],                                # the aggregator's run, built by handler/claude/build.sh; RPLACE_RUN picks another
    "input": ["aggregator/input"],                                          # the shared input: coders/, canvas/, raw/ (restructure 2026-10-02)
    "work": ["aggregator/handler/_work"],                                   # the handler's scratch: legacy rooms, lineage (not committed)
    "yard_rooms": ["../../Obsidian/Research/Claude/rPlace/Layer A/50_coding_runs/yard_v30/rooms",  # the full coding yard's rooms
                   "../../rPlace/Layer A/50_coding_runs/yard_v30/rooms"],
    "layer_a": ["../../Obsidian/Research/Claude/rPlace/Layer A",            # coder_version.csv, the batch archives
                "../../rPlace/Layer A"],
    "c5_data": ["data/pixels-per-artwork/data"],                             # the pixel record per artwork, built by data/pixels-per-artwork/run_all.sh
    "hourly_pixels": ["data/pixels-hourly/pixels.csv"],                      # the hourly series, built by data/pixels-hourly/build_pixels.py
    "v37_package": ["aggregator/handler/_work/sources/v37-package",           # copied in 2026-10-02; earlier rooms' mentions, facts, threads
                    "../gioia-j-sonnet-v37-20260908/00_GIVE-THE-AGENT/package"],
}


def _abs(v):
    """A relative value is read from the repository root; ~ is expanded for a user's own setting."""
    v = os.path.expanduser(v)
    return v if os.path.isabs(v) else os.path.normpath(os.path.join(REPO_ROOT, v))


def _load():
    p = os.path.join(HERE, "paths.json")
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    except ValueError:
        sys.exit("aggregator/handler/paths.json is not valid JSON")


def get(key):
    env = os.environ.get("RPLACE_" + key.upper())
    if env:
        return _abs(env), "environment"
    cfg = _load()
    if key in cfg:
        return _abs(cfg[key]), "paths.json"
    cands = [_abs(c) for c in DEFAULTS[key]]
    for c in cands:
        if os.path.exists(c):
            return c, "default"
    return cands[0], "default"

def P(key):
    return get(key)[0]


if __name__ == "__main__":
    for k in DEFAULTS:
        v, src = get(k)
        print("%-12s %-11s %s %s" % (k, src, "ok     " if os.path.exists(v) else "MISSING", os.path.relpath(v, REPO_ROOT)))
