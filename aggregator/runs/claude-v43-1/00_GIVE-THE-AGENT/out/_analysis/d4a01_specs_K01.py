#!/usr/bin/env python3
"""D4a-01: write the specs of F01's five subforms (cut rule R3), from my reading of F01's lines by level-3 node
(_analysis/d4a01_lines_K01_addstep.txt). Each subform's key is add-step:K01:<T3>, a child of F01's key; its lines
state a narrower change than F01's. Two level-3 groups are set aside, with their reasons, in tree-D4.md: T3-001
(staging April Fools fake news, 37 rooms) and T3-048 (reacting to official April Fools, 14 rooms), whose lines state
several different steps. Writes out/_analysis/d4a01_cut_F02.json to F06.json; never overwrites.

    python3 out/_analysis/d4a01_specs_K01.py
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
COMMON = ("Cut rule R3 (tree-D4.md): a level-3 child of F01's key, held by 5 or more of F01's members, whose lines "
          "(read whole in _analysis/d4a01_lines_K01_addstep.txt) state a narrower change than F01's. ")
SPECS = [
    ("F02", "add-step:K01:T3-023", "the takeover run as a temporary regime",
     "Within F01, a takeover's play becomes a temporary regime: its rules are enforced by real removals, bans and "
     "bots, members perform and test them, its styling is made usable or switched off, and its end is set.",
     "The lines under T3-023 (running an April Fools takeover) state this: 'Fictional commandments are enforced "
     "through real removals and approvals' (battlecats); 'A temporary joke becomes a case-sensitive participation "
     "rule enforced by automated messages' (monstercat); 'Moderators settle the prank's cutoff by timezone' "
     "(warframe); 'Restoring ordinary rules and styling ends the license' (MMA)."),
    ("F03", "add-step:K01:T3-095", "the joke tested: members check a claim's truth",
     "Within F01, members test whether a claim is a joke before they act on it: by its date, its source, its "
     "plausibility or its marks, and they repair a literal reading.",
     "The lines under T3-095 (testing others' April Fools claims) state this in most rooms: 'Participants "
     "authenticate purported previews through stamps, typography, artist attribution and collector numbers' "
     "(magictcg); 'Participants repair a literal reading of the fake takeover by invoking the date' (mariokart); "
     "'Recipients actively test authenticity' (streetfighter). In three rooms the test leads into practical "
     "repair or advice (terraria, warframe, zelda); they share the step that tests the claim."),
    ("F04", "add-step:K01:T3-032", "the licence policed: objections to the play, its limits and its end",
     "Within F01, members object to the play and police the licence: they set limits on taste and repetition, "
     "demand labels, deletion, restoration or better jokes, and dispute when the licence ends.",
     "The lines under T3-032 (objecting to April Fools posts) state this: 'Participants police the scope of "
     "licensed joking' (bostonceltics); 'Members dispute when the temporary licence ends' (dankmemes); 'Members "
     "demand restoration and dispute the prank's duration' (chelseafc); 'Moderators enforce duplication and "
     "relevance limits during the joke licence' (elitedangerous)."),
    ("F05", "add-step:K01:T3-097", "the styling ended: ordinary use restored",
     "Within F01, members and moderators end the prank's styling and restore ordinary use: they switch styles "
     "off, ask whether the sub has switched back, and clear what the prank left.",
     "The lines under T3-097 (switching off the prank styling) state this: 'Readers restore usable access by "
     "disabling prank styling' (minecraft); 'Users escape prank styling locally by disabling styles' "
     "(pcmasterrace); 'A moderator publicly ends the local joke period' (popheads); 'Ending the theme swap "
     "includes a later reminder to remove its leftover page title' (NieR)."),
    ("F06", "add-step:K01:T3-100", "the joke kept: a request that its change last",
     "Within F01, members ask that a joke's change outlast the day: a temporary feature, mode, flair, banner or "
     "board is to become permanent, or a joke activity real.",
     "The lines under T3-100 (keeping April Fools changes afterwards) state this: 'Members seek permanence for a "
     "temporary joke game mode' (starcraft); 'Members turn appreciation of temporary styling into a request for "
     "permanent optional flair' (mls); 'Participants explicitly convert an apparent joke poll into a real "
     "continuing activity' (kanye); 'Calls to retain merged boards' (4chan)."),
]
for fid, key, name, wic, why in SPECS:
    p = os.path.join(AN, "d4a01_cut_%s.json" % fid)
    if os.path.exists(p):
        raise SystemExit("refusing to overwrite %s" % p)
    json.dump({"id": fid, "parent": "F01", "level": "third", "keys": [key], "name": name, "what_it_changes": wic,
               "move": "splitting", "why": COMMON + why + " These are the labelers' how sentences.",
               "ground": "keys"}, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", os.path.basename(p))
