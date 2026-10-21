#!/usr/bin/env python3
"""D3a-52: apply G56a backwards to K04's instantiate rulings. Reads K04-inst-spec.txt and K04-tags-inst.txt, and
writes new files beside them (the first files stay): K04-inst-spec-v2.txt, with the five lines whose only form was a
member's outside colour allegiance (CX) moved to NOT with new evidence; K04-tags-inst-v2.txt, without those five tag
rows and with CO made CX in the two lines that also show CU. Each row to change must be found exactly once.

  python3 out/_analysis/d3_k04_g56a.py
"""
R = "out/_analysis/d3_rulings/"
NEW = {
    "borussiadortmund-031": "c0018 'oh shit I just realized being a bluecorner member may have been a mistake' (h+13.17) speaks as one member of an outside colour faction, in a room that is not that faction (CX; G56a)",
    "diablo-026": "c0032 'join the void and only the void. the void has no political beliefs' (h+70.18), c0034 (h+71.04) and c0035 'The Void is great.' (h+71.21) voice two members' own allegiance to an outside colour faction, in a room that is not that faction, beside a game joke proposed as a picture in c0005 (h+40.49) (CX; G56a)",
    "minecraft-063": "c0033 'ALL HAIL BLUE CORNER!' (h+10.33) and c0034 'PURPLE CORNER WILL RISE' (h+10.91) voice two members' own allegiances to rival outside colour factions, in a room that is not either faction (CX; G56a)",
    "twentyonepilots-037": "c0091 'NO! ALL HAIL THE BLUE CORNER!' (h+58.06) refuses the room's logo call for one member's own outside colour faction (CX; G56a)",
    "winnipegjets-061": "c0003 'I added to the sexy blue corner. No regerts' (h+12.70) reports one member's own work for an outside colour faction (CX; G56a)",
}
CX = {"cubers-047", "h3h3productions-028"}

rows, seen = [], set()
for l in open(R + "K04-inst-spec.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, rest = l.rstrip("\n").split("|", 2)
    if aid in NEW:
        assert cls == "SHOW", (aid, cls)
        rows.append("%s|NOT|%s" % (aid, NEW[aid]))
        seen.add(aid)
    else:
        rows.append(l.rstrip("\n"))
assert seen == set(NEW), set(NEW) - seen
open(R + "K04-inst-spec-v2.txt", "w", encoding="utf-8").write("\n".join(rows) + "\n")

tags, dropped, changed = [], set(), set()
for l in open(R + "K04-tags-inst.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, t = l.strip().split("|")
    if aid in NEW:
        dropped.add(aid)
        continue
    if aid in CX:
        parts = t.split(",")
        assert parts.count("CO") == 1, (aid, t)
        t = ",".join("CX" if p == "CO" else p for p in parts)
        changed.add(aid)
    tags.append("%s|%s" % (aid, t))
assert dropped == set(NEW) and changed == CX, (dropped, changed)
open(R + "K04-tags-inst-v2.txt", "w", encoding="utf-8").write("\n".join(tags) + "\n")
print("spec v2: %d rows, %d moved to NOT; tags v2: %d rows, %d dropped, %d with CO made CX"
      % (len(rows), len(seen), len(tags), len(dropped), len(changed)))
