#!/usr/bin/env python3
"""build_neighbours.py, v38: stage 00, who neighbours whom, on the canvas and in the coders' record.

    python3 tools/build_neighbours.py --root <run>/00_GIVE-THE-AGENT --atlas <atlas_2017.json>

Handler side, at build (build.sh runs it when INPUT/canvas/atlas_2017.json exists). Reads the
atlas polygons (placeAtlas 2017, every `path` of every entry), package/canvas/artworks.jsonl
(artwork id -> the rooms of this frame it links), package/store/rooms.jsonl (the frame) and
package/store/relations.jsonl (the mention graph). Writes package/store/neighbours.jsonl, one
line per ordered pair of rooms in the frame that touch in any of three ways:

    {"sub", "other",
     "shared_artworks": [ids],   artworks the atlas links to both rooms (a joint build, or one
                                 room's work inside the other's)
     "border_px": n,             pixels of one room's artworks that touch (4-neighbour) a pixel
                                 of the other's, counted over artwork pairs
     "overlap_px": n,            pixels covered by an artwork of each (regions overlap)
     "mention": null | {"label", "n", "reciprocal", "direction"}}   the coders' record:
                                 direction is names, named-by or both

Both directions are written, so `grep '"sub": "netherlands"'` finds every neighbour. And
package/store/_README-neighbours.md with the counts.

**The limits.** The atlas polygons are one annotator's outline at one time (the path keys),
drawn after the event; a border is where two outlines meet, not a negotiation. Pixels are
counted on the atlas outline, not recounted from the placement log. A mention is a pointer a
coder recorded (relations.py's limit applies). Rooms with no artwork in the atlas have no
canvas neighbours, which says nothing about where they built.
"""
import argparse, collections, json, os, sys

import numpy as np

W = H = 1000


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def mask(poly):
    """Flat pixel indices whose centres fall inside the polygon (even-odd rule)."""
    P = np.asarray(poly, dtype=float)
    if len(P) < 3:
        return np.zeros(0, dtype=np.int64)
    x0, y0 = max(int(np.floor(P[:, 0].min())), 0), max(int(np.floor(P[:, 1].min())), 0)
    x1, y1 = min(int(np.ceil(P[:, 0].max())), W - 1), min(int(np.ceil(P[:, 1].max())), H - 1)
    if x1 < x0 or y1 < y0:
        return np.zeros(0, dtype=np.int64)
    xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
    xs, ys = xs.ravel(), ys.ravel()
    inside = np.zeros(xs.shape, dtype=bool)
    xj, yj = P[-1]
    for xi, yi in P:
        cross = ((yi > ys) != (yj > ys)) & (xs < (xj - xi) * (ys - yi) / ((yj - yi) if yj != yi else 1e-12) + xi)
        inside ^= cross
        xj, yj = xi, yi
    px = (ys[inside] - 0.5).astype(np.int64) * W + (xs[inside] - 0.5).astype(np.int64)
    return px


def ring(px):
    """4-neighbour pixels just outside a mask."""
    s = set(px.tolist())
    out = set()
    for p in s:
        x, y = p % W, p // W
        for q, ok in ((p - 1, x > 0), (p + 1, x < W - 1), (p - W, y > 0), (p + W, y < H - 1)):
            if ok and q not in s:
                out.add(q)
    return np.fromiter(out, dtype=np.int64, count=len(out))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--atlas", required=True)
    a = ap.parse_args(argv)
    st = os.path.join(a.root, "package", "store")
    frame = {r["sub"] for r in jl(os.path.join(st, "rooms.jsonl"))}
    low = {s.lower(): s for s in frame}
    rows = jl(os.path.join(a.root, "package", "canvas", "artworks.jsonl"))
    arts = {r["artwork_id"]: [low.get(x.lower()) for x in r.get("subreddits_in_frame") or [] if low.get(x.lower())]
            for r in rows}
    atlas = json.load(open(a.atlas, encoding="utf-8"))
    # artworks.jsonl numbers the artworks its own way; join each atlas entry to it by name and centre
    def centre(e):
        c = e.get("center") or {}
        v = next(iter(c.values()), None) if isinstance(c, dict) else c
        return tuple(int(round(x)) for x in v) if v else None
    by_key = {((r.get("name") or "").strip().lower(), tuple(r.get("centre") or ())): r["artwork_id"] for r in rows}
    by_name = collections.defaultdict(list)
    for r in rows:
        by_name[(r.get("name") or "").strip().lower()].append(r)
    masks, unjoined = {}, 0
    for e in atlas:
        nm = (e.get("name") or "").strip().lower()
        aid = by_key.get((nm, centre(e) or ()))
        if aid is None and len(by_name.get(nm, [])) == 1:
            aid = by_name[nm][0]["artwork_id"]
        if aid is None and by_name.get(nm) and centre(e):
            cx, cy = centre(e)
            aid = min(by_name[nm], key=lambda r: (r["centre"][0] - cx) ** 2 + (r["centre"][1] - cy) ** 2 if r.get("centre") else 1e12)["artwork_id"]
        if aid is None:
            unjoined += 1
            continue
        if not arts.get(aid):
            continue
        parts = [mask(poly) for poly in (e.get("path") or {}).values()]
        m = np.unique(np.concatenate(parts)) if parts else np.zeros(0, dtype=np.int64)
        if len(m):
            masks[aid] = np.unique(np.concatenate([masks[aid], m])) if aid in masks else m
    # regions no atlas entry outlines (derived_regions.json beside the atlas: the koi), each its own
    # negative id and the one room credited with it
    dr = os.path.join(os.path.dirname(a.atlas), "derived_regions.json")
    for k, (name, g) in enumerate(sorted((json.load(open(dr, encoding="utf-8")) if os.path.exists(dr) else {}).items())):
        s = low.get(g["sub"].lower())
        if s:
            arts[-1 - k] = [s]
            masks[-1 - k] = np.unique(np.array([y * W + x for x, y in g["pixels"]], dtype=np.int64))
    # pixel -> artworks, for overlaps and borders
    owner = collections.defaultdict(list)
    for aid, m in masks.items():
        for p in m.tolist():
            owner[p].append(aid)
    overlap = collections.Counter()
    for p, ids in owner.items():
        if len(ids) > 1:
            for i in ids:
                for j in ids:
                    if i != j:
                        overlap[(i, j)] += 1
    border = collections.Counter()
    for aid, m in masks.items():
        for p in ring(m).tolist():
            for j in owner.get(p, ()):
                if j != aid:
                    border[(aid, j)] += 1
    pairs = collections.defaultdict(lambda: {"shared_artworks": set(), "border_px": 0, "overlap_px": 0, "mention": None})
    for aid, rooms in arts.items():
        for s in rooms:
            for o in rooms:
                if s != o:
                    pairs[(s, o)]["shared_artworks"].add(aid)
    for (i, j), n in border.items():
        for s in arts.get(i, []):
            for o in arts.get(j, []):
                if s != o:
                    pairs[(s, o)]["border_px"] += n
                    pairs[(o, s)]["border_px"] += 0
    for (i, j), n in overlap.items():
        for s in arts.get(i, []):
            for o in arts.get(j, []):
                if s != o:
                    pairs[(s, o)]["overlap_px"] += n
    # borders are counted from each side's ring; make them symmetric (the larger of the two counts)
    for (s, o) in list(pairs):
        b = max(pairs[(s, o)]["border_px"], pairs[(o, s)]["border_px"] if (o, s) in pairs else 0)
        pairs[(s, o)]["border_px"] = b
        pairs[(o, s)]["border_px"] = b
    for r in jl(os.path.join(st, "relations.jsonl")):
        o = low.get((r.get("other") or "").lower())
        if not o or o == r["sub"] or not r.get("other_in_frame"):
            continue
        for (x, y, d) in ((r["sub"], o, "names"), (o, r["sub"], "named-by")):
            cur = pairs[(x, y)]["mention"]
            if cur is None:
                pairs[(x, y)]["mention"] = {"label": r.get("label"), "n": r.get("n"), "reciprocal": bool(r.get("reciprocal")),
                                            "direction": d}
            elif cur["direction"] != d:
                cur["direction"] = "both"
    out = os.path.join(st, "neighbours.jsonl")
    n = collections.Counter()
    with open(out, "w", encoding="utf-8") as f:
        for (s, o), v in sorted(pairs.items()):
            if not (v["shared_artworks"] or v["border_px"] or v["overlap_px"] or v["mention"]):
                continue
            line = {"sub": s, "other": o, "shared_artworks": sorted(v["shared_artworks"]), "border_px": v["border_px"],
                    "overlap_px": v["overlap_px"], "mention": v["mention"]}
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
            n["pairs"] += 1
            n["shared"] += bool(v["shared_artworks"])
            n["border"] += bool(v["border_px"])
            n["overlap"] += bool(v["overlap_px"])
            n["mention"] += bool(v["mention"])
            n["canvas_and_mention"] += bool(v["mention"]) and bool(v["border_px"] or v["overlap_px"] or v["shared_artworks"])
    rooms_with = len({s for (s, o) in pairs})
    with open(os.path.join(st, "_README-neighbours.md"), "w", encoding="utf-8") as f:
        f.write("## neighbours.jsonl\n\nOrdered room pairs that touch: %d (each pair written both ways). Sharing an "
                "artwork %d; bordering on the atlas outline %d; overlapping %d; named in the coders' record %d; "
                "both on the canvas and named %d. Rooms with at least one neighbour: %d of %d; artworks with an "
                "outline and a room of this frame: %d; atlas entries not joined to artworks.jsonl by name: %d.\n\nThe atlas outline is one annotator's, drawn after the event; "
                "a border is where two outlines meet, not a negotiation. A mention is a pointer a coder recorded.\n"
                % (n["pairs"], n["shared"], n["border"], n["overlap"], n["mention"], n["canvas_and_mention"],
                   rooms_with, len(frame), len(masks), unjoined))
    print("neighbours.jsonl: %d ordered pairs (shared %d, border %d, overlap %d, mention %d); %d rooms with a neighbour; "
          "%d atlas entries not joined by name" % (n["pairs"], n["shared"], n["border"], n["overlap"], n["mention"], rooms_with, unjoined))
    return 0


if __name__ == "__main__":
    sys.exit(main())
