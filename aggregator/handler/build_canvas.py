"""Handler-side: the canvas files every run joins at build, in aggregator/input/canvas/.
  artworks.jsonl  every atlas artwork (1,473): id, name, linked subreddits, pixels its polygon
                  covers, centre, placements and distinct placers in all and in its smallest-polygon
                  pixels, first and last placement hour, and the placements per hour, hours 0 to 96
  pixels.csv      the per-room hourly series (px_in_region_any, px_by_pre_members,
                  px_by_window_members), the frame's rooms only
case_facts_outcome.jsonl (the six fields per room) is computed from the atlas polygons elsewhere and
placed beside these; build.sh copies the three into package/ and joins the six fields.
"""
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from paths import P
import csv, gzip, json, os, collections
C5 = P("c5_data")
OUT = P("input") + "/canvas"
os.makedirs(OUT, exist_ok=True)
ROOMS = P("input") + "/coders/ROOMS.tsv"
PIX = P("hourly_pixels")
OPEN_MS = 1490976000000
frame = {l.split("\t")[0] for l in open(ROOMS).read().splitlines()[1:] if l.strip()}
hourly = collections.defaultdict(lambda: [0] * 97)
with gzip.open(C5 + "/panel_30min.csv.gz", "rt") as f:
    for r in csv.DictReader(f):
        h = int(float(r["hours_from_open"]))
        if 0 <= h <= 96:
            hourly[int(r["artwork_id"])][h] += int(r["placements"])
from paths import REPO_ROOT as REPO_
CR = REPO_ + "/data/atlas/credits_beyond_links.csv"   # credits by the canvas or a description (data/atlas/README.md)
# artwork_id is the entry's position in the atlas list, not its atlas id
pos = {str(e["id"]): k for k, e in enumerate(json.load(open(OUT + "/atlas_2017.json", encoding="utf-8")))}
extra = collections.defaultdict(list)
for r in (csv.DictReader(open(CR, encoding="utf-8")) if os.path.exists(CR) else []):
    if r["atlas_id"]:
        extra[pos[str(r["atlas_id"])]].append(r["sub"])
n = 0
with open(OUT + "/artworks.jsonl", "w", encoding="utf-8") as fo:
    for r in csv.DictReader(open(C5 + "/artworks_index.csv")):
        i = int(r["artwork_id"]); subs = [s for s in r["subreddits"].split("|") if s]
        credited = [s for s in extra.get(i, []) if s not in subs]
        x, y = (int(v) for v in r["center"].split())
        hr = lambda ms: round((int(ms) - OPEN_MS) / 3600000.0, 2) if ms else None
        fo.write(json.dumps({"artwork_id": i, "name": r["name"], "subreddits": subs,
            "subreddits_in_frame": sorted(s for s in subs + credited if s in frame or s.lower() in {f.lower() for f in frame}),
            "credited_beyond_links": credited,
            "pixels_covered": int(r["area_px"]), "centre": [x, y], "placements": int(r["placements"]),
            "placements_smallest_polygon": int(r["placements_primary"]), "distinct_placers": int(r["distinct_placers"]),
            "first_hour": hr(r["first_ts_ms"]), "last_hour": hr(r["last_ts_ms"]),
            "placements_by_hour_0_96": hourly[i]}, ensure_ascii=False) + "\n"); n += 1
low = {s.lower(): s for s in frame}
rows = 0
with open(PIX, newline="") as fi, open(OUT + "/pixels.csv", "w", newline="") as fo:
    rd = csv.reader(fi); w = csv.writer(fo); w.writerow(next(rd))
    for r in rd:
        if r[0].lower() in low:
            w.writerow([low[r[0].lower()]] + r[1:]); rows += 1
# the files a run needs beside these, when a run is built from nothing: the atlas, the canvas manifest,
# and stage D4's activity table, cut to the frame
REPO = REPO_
import shutil
for src, dst in ((REPO + "/data/atlas/atlas_2017.json", OUT + "/atlas_2017.json"),
                 (REPO + "/data/atlas/derived_regions.json", OUT + "/derived_regions.json"),
                 (OUT + "/DATA-manifest-canvas.md", OUT + "/DATA-manifest-canvas.md")):
    if not os.path.exists(dst) and os.path.exists(src):
        shutil.copyfile(src, dst); print("copied", os.path.basename(dst))
ACT = REPO + "/data/pixels-hourly/activity-week-before.csv"
if os.path.exists(ACT):
    D4 = OUT + "/D4"; os.makedirs(D4, exist_ok=True)   # build.sh copies it into each run's DROPS/D4/data
    with open(ACT, newline="") as fi, open(D4 + "/activity-week-before.csv", "w", newline="") as fo:
        rd = csv.reader(fi); w = csv.writer(fo); w.writerow(next(rd))
        for r in rd:
            if r[0] in frame or r[0].lower() in low:
                w.writerow(r)
    shutil.copyfile(REPO + "/data/pixels-hourly/README-activity.md", D4 + "/README-activity.md")
    print("stage D4's activity table written")
print("artworks", n, "pixel rows", rows, "rooms", len({l.split(',')[0] for l in open(OUT + '/pixels.csv').read().splitlines()[1:]}))
