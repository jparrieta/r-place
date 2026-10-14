#!/usr/bin/env python3
"""C3c: append findings F-016 (the four universal problems put to the structure: the mapping) and F-017 (the goal) to
findings.jsonl. Counts are those printed by c3c_mapping_check.py, c3c_rooms_per_theme.py, c3c_goal_counts.py and
c3c_hours.py at C3c; the script re-reads the mapping's per-problem theme counts from mapping-C3.jsonl and refuses to
write if an id already exists.

    python3 out/_analysis/c3c_findings.py
"""
import collections, datetime, json, os, sys

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out")
path = os.path.join(OUT, "findings.jsonl")
have = {json.loads(l)["id"] for l in open(path, encoding="utf-8") if l.strip()}
if have & {"F-016", "F-017"}:
    sys.exit("F-016 or F-017 already in findings.jsonl; nothing written")
mp = [json.loads(l) for l in open(os.path.join(OUT, "mapping-C3.jsonl"), encoding="utf-8") if l.strip()]
n = collections.Counter(m["problem"] for m in mp)
assert (n["division"], n["allocation"], n["reward"], n["information"], n["none"]) == (1, 2, 2, 4, 19), n
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

f16 = {
    "stage": "C3", "leg": "C3c", "id": "F-016", "tier": "fourth", "warrant": "inferred", "status": "standing", "t": t,
    "statement": (
        "Nine of the 28 fourth-order themes are ways of handling one of the four universal problems, and 19 are not. "
        "Information provision: 4 themes (Sensemaking, Stigmergy, Backstage decision-making, Attribution), 555 of 705 "
        "rooms. Reward provision: 2 (Completion ritual, by construction; Visibility returns), 543 rooms, nearly all of "
        "it credit and celebration after the work; a reward offered before the work appears in 9 rooms (prizes 7, a "
        "tile as payment 2). Task allocation: 2 (Mobilization, by construction; Decided order), 394 rooms; by "
        "self-selection to calls in 361 (calling members 345, recruiting kindred subs 44, timing a mass placement 2), "
        "by decision in 46. Task division: 1 (Standardization of output), 237 rooms, by coordinates and templates "
        "(207); division among teams in 5. The remainder of 19 holds 7 themes between rooms (a change of level), 6 "
        "that make the boundary and membership the frame takes as given, 3 different mechanisms (making the goal, "
        "sizing it, multiplying hands under the rate limit), the work itself (repair), and 2 after the clock."),
    "evidence": ["out/mapping-C3.jsonl", "out/_analysis/c3c_mapping_check.py", "out/_analysis/c3c_rooms_per_theme.py",
                 "out/_analysis/c3c_rule5_members.py", "Pigifs:c0036", "paydaytheheist:c0010",
                 "indieheads:c0144", "AmericanFlaginPlace:c0396"],
    "bound": (
        "The mapping is the analyst's reading of the declarations as they stood, one reader. The counts are rooms "
        "whose coded talk sits under a theme, not rooms that solved a problem: the evidence is talk in public and "
        "there is no denominator of groups (contract section 5). Two mappings are by construction (Mobilization, "
        "Completion ritual) and rest on the declarations, not on the rooms showing that a call allocated or that "
        "credit induced anyone to place. Every claim that a problem is absent or thin is about small rooms writing in "
        "public and is marked weak."),
    "refuted_by": ["a second reader mapping the 28 declarations and placing most of the remainder under one of the four",
                   "records of the chats showing that most rooms assigned parts or promised rewards where the threads "
                   "are silent"],
    "literature": ["Puranam, Alexy and Reitzig 2014"],
    "why": "stage C3c, section 5: the contract's section 1 claim put to the structure as it stands, not revised to fit",
}

f17 = {
    "stage": "C3", "leg": "C3c", "id": "F-017", "tier": "fourth", "warrant": "inferred", "status": "standing", "t": t,
    "statement": (
        "The rooms' goals were made on the clock, mostly from a sign the room already had, proposed by one member and "
        "argued in its design rather than chosen between; a vote was rare; loss changed the goal. A member proposes "
        "the room's mark in 166 of 705 rooms (median first hour 12.7). The design is argued in 281 rooms and put to a "
        "vote in 18 (median first vote at hour 42.4; 7 of 18 before hour 24). The goal is inherited in 152 rooms: the "
        "homeland's flag 96, national emblems 39, the room's mark found already placed 43, a sign others began "
        "adopted 6. It is contested in 152, mostly over whether the canvas belongs in the host sub at all (arguing the "
        "canvas's worth 76, objecting to the canvas flood 72). It is "
        "changed in 190: relocating 116, upkeep chosen over expansion 43, fewer pieces 29, quitting 20, weighing "
        "fight against move 17. The structure places the making of the goal in Collective representation (T4-006) "
        "and the model in the room settling its mark (P02) and the starter (R01), outside the four problems, which "
        "take the goal as given. The goal is a picture, so one artifact can state it and divide it (A11, "
        "theorised); at room level an argued design goes with shared coordinates only slightly more often "
        "(94 of 281 rooms, against 113 of the other 424; not held to size)."),
    "evidence": ["out/_analysis/c3c_goal_counts.py", "out/_analysis/c3c_hours.py",
                 "out/_analysis/c3c_rooms_per_theme.py", "anime:c0177", "2007scape:c0230", "argentina:c0525",
                 "GreenCorner:c0107", "raocow:c0027"],
    "bound": (
        "The four modes are the analyst's placement of third-order themes by their names; the theme a record sits "
        "under does not track its stance, so the counts are of rooms whose coded talk sits under a theme, not of "
        "rooms read for how they chose. The modes overlap (a room can inherit a flag and argue its design). Counts "
        "are not held to size. A goal set in a chat or before the canvas is invisible here, and the claim that goals "
        "were rarely chosen between rivals is an absence claim, marked weak."),
    "refuted_by": ["a read of the rooms' first proposals showing that most goals were chosen against a rival "
                   "proposal, or set by a body outside the room"],
    "literature": ["Felin and Zenger 2016", "Felin and Zenger 2017", "Puranam, Alexy and Reitzig 2014"],
    "why": "stage C3c, section 5, part 5: whether each room inherited, negotiated, contested or changed its goal, "
           "the question C3a left open from Felin and Zenger",
}

with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(f16, ensure_ascii=False) + "\n")
    f.write(json.dumps(f17, ensure_ascii=False) + "\n")
print("appended F-016, F-017")
