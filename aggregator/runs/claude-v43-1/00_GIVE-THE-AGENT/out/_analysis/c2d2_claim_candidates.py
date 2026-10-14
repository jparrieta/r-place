#!/usr/bin/env python3
"""C2d-02, pass 5, declaration 3: list the candidate turns for the claim C02 (a tie the members had before the canvas
names the rival in the same turn that calls or carries out the attack). Candidates are the concepts cited in the
`residue` field of the story-room verdict lines, passes 1 to 4, for the rooms whose residue says membership or a
colour faith names the rival. Each candidate's text, hour and second-order theme are printed through cite.py, so the
three checks (a) attack called or carried out, (b) rival named, (c) the tie named or rested on can be read.
Writes out/_analysis/c2d2_claim_candidates.txt.

    python3 out/_analysis/c2d2_claim_candidates.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c2d2_claim_candidates.txt")
ROOMS = ["sweden", "unitedkingdom", "anarcho_capitalism", "completeanarchy", "epublica", "CKCrusaders", "texans",
         "starcitizen", "lakers", "rpi", "cardinals", "totallynotrobots", "greenlattice", "purplecorner",
         "orderofthebluecorner", "thebluecorner"]
codes = dict((s, []) for s in ROOMS)
for i in (1, 2, 3, 4):
    p = os.path.join(OUT, "story_rooms-p%d.jsonl" % i)
    rows = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()][1:]
    for r in rows:
        if r.get("sub") in codes:
            res = r.get("residue") or ""
            got = re.findall(r"c\d{4}", res)
            for a, b in re.findall(r"c(\d{4}) to c(\d{4})", res):
                got += ["c%04d" % n for n in range(int(a), int(b) + 1)]
            for c in got:
                if c not in codes[r["sub"]]:
                    codes[r["sub"]].append(c)
lines = []
for s in ROOMS:
    lines.append("== %s (%d candidates)" % (s, len(codes[s])))
    for c in sorted(codes[s]):
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", s, "--code", c],
                           cwd=ROOT, capture_output=True, text=True)
        got = [l for l in p.stdout.splitlines() if "[%s/%s]" % (s, c) in l]
        lines.append(got[0] if got else "%s/%s: not found by cite.py" % (s, c))
open(DEST, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
print("candidates: %d in %d rooms; written %s" % (sum(len(v) for v in codes.values()), len(ROOMS), os.path.relpath(DEST, ROOT)))
