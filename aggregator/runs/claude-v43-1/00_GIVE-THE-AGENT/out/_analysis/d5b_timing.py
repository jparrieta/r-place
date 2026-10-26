#!/usr/bin/env python3
"""D5b, section 4: the narratives' dated changes against the members' placements by hour.

The rule is in the diary (D5b, 'D5b timing rule'). Each act names the branches whose narrative
dates it, the room, the hour, the implied direction (rise, fall, continue) and the act in brief.
Prints JSON, one row per act.

    python3 out/_analysis/d5b_timing.py
"""
import collections, csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKG = os.path.join(ROOT, "package")
ACTS = [
    ("F11 F12", "clubpenguin", 36.0, "fall", "a member moved the penguin to another site because it was damaged"),
    ("F23 F25", "thebluecorner", 39.0, "continue", "members called to a copy of the canvas while they wait for the cooldown"),
    ("F27 F32", "OnePiece", 51.18, "continue", "finally perfect, then kept"),
    ("F27", "hawks", 61.14, "rise", "adding the colour detail to the feathers"),
    ("F29", "jerma985", 56.11, "rise", "the chat decided to work on the Jerm and the logo now"),
    ("F29", "tagpro", 25.41, "rise", "voted in the chat to get rid of the bomb"),
    ("F31", "faeria", 29.15, "rise", "safe pasture secured for the yak on the Bolivian flag"),
    ("F32", "japan", 64.57, "continue", "we did it, but we need to protect the flag now"),
    ("F32", "httyd", 52.45, "continue", "we did it"),
    ("F32", "vim", 61.9, "continue", "we did it reddit"),
    ("F32", "ockytop", 35.56, "continue", "we did it guys"),
    ("F32", "newzealand", 34.13, "continue", "we did it, then new damage"),
    ("F32", "unturned", 37.45, "continue", "off by a pixel or two but we did it"),
    ("F32", "clg", 39.16, "fall", "the logo posted in its perfect form; members cannot keep defending as zealously"),
    ("F33", "paragon", 62.85, "rise", "the text made white on black"),
    ("F33", "feedthebeast", 46.57, "rise", "making the background blue from the bottom"),
    ("F33", "wine", 55.46, "rise", "shifting everything across one to fit an r"),
    ("F33", "india", 11.74, "rise", "an 18 by 27 flag being made at a set corner"),
    ("F33", "gatech", 52.55, "continue", "maintaining the logo by the most recent design"),
    ("F35", "stargate", 51.56, "continue", "two pixels down"),
    ("F35", "starbound", 59.68, "continue", "doing my part right now"),
    ("F17", "swordartonline", 40.19, "continue", "good job everyone: the mark made"),
    ("F18", "bostonceltics", 71.0, "continue", "the mark made after several setbacks"),
    ("F20", "chibears", 72.99, "rise", "the logo covered; we must replace it"),
    ("F27", "cowchop", 73.11, "continue", "the final logo posted, with the holes"),
]
series = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(PKG, "pixels.csv"), encoding="utf-8")):
    series[r["sub"]][int(float(r["hour_since_open"]))] = (int(float(r["px_by_window_members"] or 0)),
                                                           int(float(r["px_in_region_any"] or 0)))
LAST = 72
rows = []
for br, sub, h, implied, act in ACTS:
    row = {"branches": br, "sub": sub, "hour": h, "implied": implied, "act": act}
    hb = int(h)
    if h > LAST:
        row["result"] = "not checkable: after the series ends"
        rows.append(row)
        continue
    s = series.get(sub, {})
    before = [hb - k for k in (4, 3, 2, 1) if hb - k in s]
    after = [hb + k for k in (0, 1, 2, 3) if hb + k <= LAST and hb + k in s]
    wb, wa = sum(s[x][0] for x in before), sum(s[x][0] for x in after)
    ab, aa = sum(s[x][1] for x in before), sum(s[x][1] for x in after)
    # per-bin rates, so a short window at the series' end compares fairly
    rb, ra = (wb / len(before) if before else 0), (wa / len(after) if after else 0)
    ratio = (ra / rb) if rb else (float("inf") if ra else None)
    big = max(wb, wa) >= 10
    move = "rise" if (ratio is not None and ratio >= 1.5 and big) else (
        "fall" if (ratio is not None and ratio <= 0.67 and big) else "none")
    if implied == "continue":
        result = "contradicted" if move == "fall" else "corroborated"
    elif move == implied:
        result = "corroborated"
    elif move == "none":
        result = "not shown"
    else:
        result = "contradicted"
    row.update({"bins_before": before, "bins_after": after, "members_before": wb, "members_after": wa,
                "any_before": ab, "any_after": aa,
                "ratio": None if ratio is None else (round(ratio, 2) if ratio != float("inf") else "inf"),
                "move": move, "result": result,
                "members_by_hour": {x: s[x][0] for x in range(max(-16, hb - 6), min(LAST, hb + 6) + 1) if x in s}})
    rows.append(row)
print(json.dumps(rows, ensure_ascii=False))
