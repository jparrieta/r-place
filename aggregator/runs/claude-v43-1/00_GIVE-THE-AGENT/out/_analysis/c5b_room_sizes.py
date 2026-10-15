#!/usr/bin/env python3
"""C5b: the facts the three readers' rooms are drawn from (stage C5 section 8), by query and never by opening notes.
For every pass 5 story room and every room on either side of the onset contrast (contrast.md: early, first coded
turn after hour 0 and before hour 3; late, after hour 48), print its side, its story verdict if any, whether
account.md cites or names it, and the bytes of its forest (`mem.py room <sub> --size`). Also counts the rooms
account.md visits on each side. Writes out/_analysis/c5b_room_sizes.json; draws nothing.

    python3 out/_analysis/c5b_room_sizes.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
rooms = {}
for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        rooms[r["sub"]] = r


def side(sub):
    h = rooms.get(sub, {}).get("onset_first_code_hour")
    if h is None:
        return None
    if 0 < h < 3:
        return "early"
    if h > 48:
        return "late"
    return "neither"


acc = open(os.path.join(OUT, "account.md"), encoding="utf-8").read()
cited = set(re.findall(r"\[([A-Za-z0-9_]+)/c\d{4}", acc))
named = {s for s in rooms if re.search(r"(?<![A-Za-z0-9_/])%s(?![A-Za-z0-9_])" % re.escape(s), acc)}
visited = cited | named
story = [json.loads(l) for l in open(os.path.join(OUT, "story_rooms-p5.jsonl"), encoding="utf-8") if l.strip()]
story = {r["sub"]: r for r in story if r.get("sub")}


def forest_bytes(sub):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "room", sub, "--size"],
                       capture_output=True, text=True, cwd=ROOT)
    m = re.search(r"forest (\d+)", p.stdout)
    return int(m.group(1)) if m else None


want = set(story) | {s for s in rooms if side(s) in ("early", "late")}
rows = []
for s in sorted(want):
    rows.append({"sub": s, "side": side(s), "onset": rooms.get(s, {}).get("onset_first_code_hour"),
                 "items_in_window": rooms.get(s, {}).get("items_in_window"),
                 "story": (story.get(s) or {}).get("verdict"), "in_account": s in visited,
                 "forest_bytes": forest_bytes(s)})
vis = {"early": sorted(s for s in visited if side(s) == "early"), "late": sorted(s for s in visited if side(s) == "late"),
       "neither": sorted(s for s in visited if side(s) == "neither")}
json.dump({"visited_by_side": vis, "rows": rows}, open(os.path.join(OUT, "_analysis", "c5b_room_sizes.json"), "w"),
          indent=1)
print("account.md visits: early %d, late %d, neither %d" % (len(vis["early"]), len(vis["late"]), len(vis["neither"])))
print("early:", ", ".join(vis["early"]))
print("late:", ", ".join(vis["late"]))
for r in rows:
    if r["story"]:
        print("story %-24s %-17s side %-7s forest %6s  in_account %s" % (r["sub"], r["story"], r["side"],
                                                                          r["forest_bytes"], r["in_account"]))
for sd in ("early", "late"):
    fb = sorted(r["forest_bytes"] for r in rows if r["side"] == sd and r["forest_bytes"] is not None)
    print("%s side: %d rooms; forest bytes min %s median %s max %s; <= 4000: %d" % (
        sd, len(fb), fb[0], fb[len(fb) // 2], fb[-1], sum(1 for b in fb if b <= 4000)))
