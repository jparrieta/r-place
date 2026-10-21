#!/usr/bin/env python3
"""D3a-57: write out/recheck-scope.json (stage section 5). Every analysed room is affected, since the scope is
uncertain for the rooms that rely on no rewritten element (the candidates enter every room's vocabulary). The
file names, for each room, how it was found: the elements its accepted lines rely on (d3_recheck_scope.py's
rule), or none, as a contrasting case. Refuses if the file exists or the sets do not partition the corpus.

    python3 out/_analysis/d3_recheck_scope_write.py [--write]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
sys.argv = [sys.argv[0]]
spec = {}
src = open(os.path.join(OUT, "_analysis", "d3_recheck_scope.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(OUT, "_analysis", "d3_recheck_scope.py"), "__name__": "scope"}
import io, contextlib  # noqa: E402
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src, "d3_recheck_scope.py", "exec"), ns)
rooms, why = ns["rooms"], ns["why"]
affected = sorted(rooms)
relying = {s: sorted(why[s]) for s in rooms if why.get(s)}
contrast = sorted(s for s in rooms if not why.get(s))
scope = {
    "affected_rooms": affected,
    "unaffected_rooms": {},
    "reason": ("All %d analysed rooms are re-checked against the revised model (version from VERSION). %d rooms "
               "rely on an element stage D3 rewrote, bounded, moved to standing or entered: an accepted or modified "
               "non-absent ledger line on R01 or P05 (revised), on P21, P22 or A21 (the field's entries, now "
               "standing), or on P06, R02, K03, K04 or P19 (candidates now standing); an accepted propose line in "
               "the group of one of the fifteen new candidates (P23 to P34, K05 to K07); or a verdict ruling whose "
               "residue names a candidate. %d rooms rely on none of these and are re-checked as contrasting cases: "
               "the candidates enter every room's vocabulary, so whether such a room's record shows a candidate's "
               "act cannot be told before its labeler reads the revised model, and the stage says to re-check all "
               "rooms where the scope is uncertain. Found by out/_analysis/d3_recheck_scope.py at D3a-57."
               % (len(rooms), len(relying), len(contrast))),
    "relying": relying,
    "contrasting_cases": contrast,
    "identified_by": "out/_analysis/d3_recheck_scope.py (D3a-57)",
}
ok = set(scope["affected_rooms"]) | set(scope["unaffected_rooms"]) == set(rooms) and not (
    set(scope["affected_rooms"]) & set(scope["unaffected_rooms"]))
print("rooms %d; affected %d (relying %d, contrasting %d); unaffected %d; partition %s" % (
    len(rooms), len(affected), len(relying), len(contrast), len(scope["unaffected_rooms"]), ok))
if not ok:
    sys.exit("refused: the sets do not partition the analysed corpus")
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
p = os.path.join(OUT, "recheck-scope.json")
if os.path.exists(p):
    sys.exit("refused: %s exists; never overwrite" % p)
json.dump(scope, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", p)
