"""Handler-side: case_facts_outcome.jsonl, the six canvas fields per room of the frame.
Input: the placeAtlas 2017 file (github.com/placeAtlas/atlas-2017, web/atlas.json; sha256
40a93f67dc55287812b66c0b3cdf2fb93980e2232fb0b3631e744a3550903b26 when this was run, 2026-09-25).
  python3 build_outcome.py ATLAS.json ROOMS.tsv OUT.jsonl
  (the runs' atlas is aggregator/input/canvas/atlas_2017.json)
Rules, reproduced against the 300 rows of Layer Fork/ASSETS/canvas (all 300 identical):
  entries  atlas entries whose subreddit links name the room (case-insensitive; four aliases)
  area_px  sum of the entries' polygon areas (shoelace), not a raster count
  centre   the atlas centre of the largest entry
  ring     distance of the centre from (500, 500): under 150 centre, under 333 middle, else edge
  artwork  the entries' names joined with ' | '; source: the provenance sentence, verbatim
"""
import json, collections, math, sys
atlas, rooms_tsv, out = sys.argv[1:4]
A = json.load(open(atlas))
subs = [l.split("\t")[0] for l in open(rooms_tsv).read().splitlines()[1:] if l.strip()]
ALIAS = {"hyperlightdrifer": "hyperlightdrifter", "r2007scape": "2007scape", "protectthet": "ockytop", "chelsea": "chelseafc"}
poly = lambda e: e if "_area" in e else next(iter(e["path"].values())); ctr = lambda e: next(iter(e["center"].values()))
shoe_ = lambda p: abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2
shoe = lambda p: p["_area"] if isinstance(p, dict) else shoe_(p)
by = collections.defaultdict(list)
for e in A:
    for s in (e.get("links") or {}).get("subreddit", []) or []:
        s = s.strip().strip("/").lower(); s = s[2:] if s.startswith("r/") else s
        by[ALIAS.get(s, s)].append(e)
# artworks credited by the canvas or a description, not by a link (data/atlas/README.md)
import csv, os
CR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "atlas", "credits_beyond_links.csv")
ids = {str(e["id"]): e for e in A}
DR = os.path.join(os.path.dirname(CR), "derived_regions.json")
derived = json.load(open(DR, encoding="utf-8")) if os.path.exists(DR) else {}
for r in (csv.DictReader(open(CR, encoding="utf-8")) if os.path.exists(CR) else []):
    if not r["atlas_id"]:   # a region drawn from the pixel record: its pixels are counted, not a polygon's area
        g = derived[r["region"]]; xs = [p[0] for p in g["pixels"]]; ys = [p[1] for p in g["pixels"]]
        c = [round(sum(xs) / len(xs)), round(sum(ys) / len(ys))]
        by[r["sub"].lower()].append({"name": g["name"], "path": {"derived": [[c[0], c[1]]]}, "center": {"derived": c},
                                      "_area": len(g["pixels"])})
        continue
    if ids[str(r["atlas_id"])] not in by[r["sub"].lower()]:
        by[r["sub"].lower()].append(ids[str(r["atlas_id"])])
def ring(c):
    d = math.hypot(c[0] - 500, c[1] - 500)
    return "centre" if d < 150 else ("middle" if d < 333 else "edge")
SRC = ("placeAtlas 2017 (github.com/placeAtlas/atlas-2017), 1473 entries; the area is the atlas polygon, "
       "not a recount from the pixel log. This is the one measure in this package not made of a community's "
       "own words \u2014 treat it as an outcome, never as evidence of intent.")
with open(out, "w") as f:
    for s in subs:
        es = by.get(s.lower(), [])
        if not es:   # a room no atlas entry covers (r/tenma): no artwork, no area
            f.write(json.dumps({"sub": s, "canvas_artwork": "", "canvas_source": SRC, "canvas_centre": None,
                                "canvas_entries": 0, "canvas_area_px": 0, "canvas_ring": None}, ensure_ascii=False) + "\n")
            continue
        big = max(es, key=lambda e: shoe(poly(e)))
        src = SRC + (" Here one region has no atlas outline: it is drawn from the pixel record (data/atlas/derived_regions.json)."
                     if any("_area" in e for e in es) else "")
        f.write(json.dumps({"sub": s, "canvas_artwork": " | ".join(e["name"] for e in es), "canvas_source": src,
                            "canvas_centre": list(ctr(big)), "canvas_entries": len(es),
                            "canvas_area_px": sum(shoe(poly(e)) for e in es), "canvas_ring": ring(ctr(big))},
                           ensure_ascii=False) + "\n")
