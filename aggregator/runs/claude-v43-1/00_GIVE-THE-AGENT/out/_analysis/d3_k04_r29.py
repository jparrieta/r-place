#!/usr/bin/env python3
"""D3a-52: apply G56's reading 29 backwards to K04's instantiate rows. Reads K04-inst-spec-v2.txt and
K04-tags-inst-v2.txt, and writes new files beside them (the v2 files stay): K04-inst-spec-v3.txt, with furry_irl-033
moved from SHOW to a paired elaboration, since its CU rested on a pun on the corrupted name, born on the canvas;
K04-tags-inst-v3.txt, with furry_irl-033 tagged OE,BE and kuwait-029's OE made VE (c0026 is by the visiting member who
wrote c0023). Each row to change must be found exactly once.

  python3 out/_analysis/d3_k04_r29.py
"""
R = "out/_analysis/d3_rulings/"
SPEC = {
    "furry_irl-033": ("SHOW", "ELAB",
                      "c0146 'It may say furay_irl' (h+73.16) holds to the room's name, 'furry_irl in my heart', against "
                      "the lettering the canvas changed, belonging to a body that is not a nation voiced through the "
                      "canvas; c0022 '/r/forry_irl' (h+22.04) is a pun on the corrupted name, born on the canvas (BE; "
                      "readings 2 and 29)|auburn-029"),
}
TAGS = {"furry_irl-033": ("OE,CU,BE", "OE,BE"), "kuwait-029": ("OE,NA,AC", "VE,NA,AC")}

rows, seen = [], set()
for l in open(R + "K04-inst-spec-v2.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, rest = l.rstrip("\n").split("|", 2)
    if aid in SPEC:
        assert cls == SPEC[aid][0] and aid not in seen, (aid, cls)
        rows.append("%s|%s|%s" % (aid, SPEC[aid][1], SPEC[aid][2]))
        seen.add(aid)
    else:
        rows.append(l.rstrip("\n"))
assert seen == set(SPEC), set(SPEC) - seen
open(R + "K04-inst-spec-v3.txt", "w", encoding="utf-8").write("\n".join(rows) + "\n")

tags, changed = [], set()
for l in open(R + "K04-tags-inst-v2.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, t = l.strip().split("|")
    if aid in TAGS:
        assert t == TAGS[aid][0] and aid not in changed, (aid, t)
        t = TAGS[aid][1]
        changed.add(aid)
    tags.append("%s|%s" % (aid, t))
assert changed == set(TAGS), set(TAGS) - changed
open(R + "K04-tags-inst-v3.txt", "w", encoding="utf-8").write("\n".join(tags) + "\n")
print("spec v3: %d rows, %d changed; tags v3: %d rows, %d changed" % (len(rows), len(seen), len(tags), len(changed)))
