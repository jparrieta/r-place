#!/usr/bin/env python3
"""C2d-01, pass 4: the two fourth-order recuts declared in notes-C2.md (pass 4, declarations 1 and 2), made one at a
time (rule 11). Each rewrites fourth/fourth.jsonl in place for the two lines it touches and appends to
tier_history.jsonl one line per touched fourth-order theme (the old line as `was`) and one per moved third-order theme.
Members are found by name, never typed. Refuses a recut already made.

  --recut hosting  asking a host for space, disputing who approves a spot, relying on a bigger neighbour and vetting
                   others' requests to build move from Meta-organization to Territoriality (move: splitting off and
                   merging); Meta-organization's gloss, prose and question become the coalitions'.
  --recut flags    building the homeland's flag and drawing national emblems move from Flagging the nation to
                   Collective representation, by the rule written before it: a theme whose acts draw or settle what the
                   room's own mark shows goes with Collective representation.

    python3 out/_analysis/c2d_recut_p4.py --recut hosting|flags [--write]
"""
import argparse, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
FP = os.path.join(OUT, "fourth", "fourth.jsonl")
TH = os.path.join(OUT, "tier_history.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
ap = argparse.ArgumentParser()
ap.add_argument("--recut", required=True, choices=["hosting", "flags"])
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
t4 = dict((r["id"], r) for r in rows)
t3 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8") if l.strip()))


def by_name(name):
    hit = [k for k, r in t4.items() if r["name"] == name]
    if len(hit) != 1:
        sys.exit("fourth-order theme %r not found once" % name)
    return hit[0]


def t3_in(name, inside):
    hit = [k for k in t4[inside]["members"] if t3[k]["name"] == name]
    if len(hit) != 1:
        sys.exit("third-order theme %r not found once in %s (already moved?)" % (name, inside))
    return hit[0]


if a.recut == "hosting":
    src, dst = by_name("Meta-organization"), by_name("Territoriality")
    names = ["asking a host for space", "disputing who approves a spot", "relying on a bigger neighbour",
             "vetting others' requests to build"]
    move_src, move_dst = "splitting", "merging"
    new_src = {
        "gloss": "Reports are coming in that we might have Polish reinforcements!",
        "gloss_from": "physical_removal/c0046",
        "prose": ("Some organizing on the canvas had rooms, not people, as its members. What holds this bundle together is "
                  "a room joining other rooms as partners in a body of rooms: kindred hubs, named alliances, shared "
                  "councils and chats, tallies of kindred works, joint marks. It explains how small rooms held space they "
                  "could not have held alone, by defending one another's works. Hosting, where one room's work lives on "
                  "another's mark under the host's rule, left this theme at pass 4 for Territoriality: it is a claim on "
                  "space, not a partnership.")}
    new_dst = {
        "prose": ("The canvas is finite, and a mark needs a place. What holds this bundle together is the feeling and "
                  "expression of ownership over a place no one owns: a room's claim rests on having been there first and "
                  "having made something there, and others mostly treat the claim as real. Choosing a spot, holding it, "
                  "yielding it, granting part of it, letting another room's work live on one's mark under one's rule or "
                  "asking to live on another's, disputing who may approve a spot, weighing a fight for a lost spot against "
                  "a move, and moving all work on that claim. Territoriality is what turns a free canvas into a map of "
                  "holdings.")}
    why = ("pass 4 declaration 1: hosting follows no coalition, comes before one in 12 of 17 rooms, and hosts that give a "
           "ground rule on space or design (F-012); the reviewer's partition set hosting beside territory (C2c)")
else:
    src, dst = by_name("Flagging the nation"), by_name("Collective representation")
    names = ["building the homeland's flag", "drawing national emblems"]
    move_src, move_dst = "splitting", "merging"
    new_src = {
        "gloss": "Gentlemen it's been an honour serving with you for our country, flag and sub",
        "gloss_from": "turkey/c0252",
        "prose": ("Rooms named for a nation, state or region mostly made its flag; making the flag and its emblems is the "
                  "mark's content and sits with Collective representation from pass 4. What holds this bundle together is "
                  "the nation claimed beyond the mark: members felt national through the work, helped kin nations and "
                  "joined flags in friendship, cast canvas fights as historic wars, read politics into the pixels, argued "
                  "who belongs and the nation's record, weighed the room against nations, and mocked rival peoples. It "
                  "explains why a national room's fights could be told as its history: the membership was in place before "
                  "the canvas opened.")}
    new_dst = {
        "prose": ("Before a room can build, it must decide what it will show of itself. What holds this bundle together is "
                  "that the mark is the room's emblem: proposing it, designing it, signing it or leaving it unsigned, "
                  "honouring a creator or the dead through it, making the land's flag or its emblems the mark, and claiming "
                  "a mark that others made or began are all choices about what the room is, and members argue them as "
                  "such. The emblem is also what the room later defends, mourns and takes into its banner.")}
    why = ("pass 4 declaration 2, the rule written first: a theme whose acts draw or settle what the room's own mark shows "
           "goes with Collective representation; the two gates (scheme_v2.jsonl) make the land's flag or its emblems the "
           "mark; the other ten members claim, argue or narrate the nation beyond the mark; the reviewer's partition and "
           "pass 3's idiom rule read the same way")
moved = [t3_in(n, src) for n in names]
was_src, was_dst = json.loads(json.dumps(t4[src])), json.loads(json.dumps(t4[dst]))
t4[src]["members"] = [m for m in t4[src]["members"] if m not in moved]
t4[dst]["members"] = t4[dst]["members"] + moved
for k, mv, extra in ((src, move_src, new_src), (dst, move_dst, new_dst)):
    t4[k].update(extra)
    t4[k].update({"pass": 4, "leg": LEG, "move": mv, "t": T})
hist = [{"t": T, "stage": "C2", "leg": LEG, "tier": "fourth", "id": src, "move": move_src, "event": "members_changed",
         "was": was_src, "now": [{"id": src, "members": t4[src]["members"]}], "why": why},
        {"t": T, "stage": "C2", "leg": LEG, "tier": "fourth", "id": dst, "move": move_dst, "event": "members_changed",
         "was": was_dst, "now": [{"id": dst, "members": t4[dst]["members"]}], "why": why}]
hist += [{"t": T, "stage": "C2", "leg": LEG, "tier": "third", "id": m, "move": move_dst, "event": "fourth-order home changed",
          "was": {"fourth": src}, "now": [{"id": m, "fourth": dst}], "why": why} for m in moved]
print("%s: %s move from %s %s (%d left) to %s %s (%d now)" % (a.recut, ", ".join("%s %s" % (m, t3[m]["name"]) for m in moved),
      src, t4[src]["name"], len(t4[src]["members"]), dst, t4[dst]["name"], len(t4[dst]["members"])))
if a.write:
    with open(FP, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(TH, "a", encoding="utf-8") as f:
        for h in hist:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    print("fourth.jsonl rewritten (%d lines); %d tier_history lines appended" % (len(rows), len(hist)))
