#!/usr/bin/env python3
"""C5c-12, the fold-in: bring prose-test-C5.md up to the serial findings. Each change replaces one exact passage, which
must occur once; additions are dated 'At C5c-12' or name the leg that changed the name. The file before is kept as
prose-test-C5-p14.md. Refuses if the copy exists.

    python3 out/_analysis/c5c12_prose_test.py            check
    python3 out/_analysis/c5c12_prose_test.py --write    keep the copy and write
"""
import os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, "out", "prose-test-C5.md")
KEEP = os.path.join(ROOT, "out", "prose-test-C5-p14.md")
t = open(P, encoding="utf-8").read()
CH = [
 ("Four names need their difference from a construct they may be mistaken for stated in the account: Stigmergy, Decided order, Completion ritual and Live and let live. The account of pass 1 states none of the four differences; the account of pass 2 (C5a-02) states all four.",
  "Four names need their difference from a construct they may be mistaken for stated in the account: Stigmergy, Decided order, Completion ritual and Live and let live. The account of pass 1 states none of the four differences; the account of pass 2 (C5a-02) states all four.\n\n**At C5c-12 (pass 15), after the serial work.** Stigmergy is renamed Direct information sharing (C5c-10), and the account states its difference from stigmergy. Three of the four flagged names now have read evidence for their mechanisms: Collective efficacy (F-019), Live and let live (F-020) and Reciprocity (F-020). Critical mass stays flagged. Territoriality and Meta-organization name things rooms do, since C5c-08 restored the room as their actor. Every name still passes."),
 ("7. **Stigmergy (T4-007).** Because the half-built mark was a trace on a medium every member could see, a member could see what was missing and place there without being told. Passes.",
  "7. **Direct information sharing (T4-007; Stigmergy until C5c-10).** Because members posted the state of the mark to the thread, the room could see what was placed and what was missing without anyone directing the work. Passes. The name is Okhuysen and Bechky's (2009, p. 474) and claims only the posts the record holds. The account states its difference from stigmergy, in which the work itself channels later work: the record holds the posts, not the placing that would answer them. *Before C5c-10:* Because the half-built mark was a trace on a medium every member could see, a member could see what was missing and place there without being told. Passed then."),
 ("Passes, flagged. The name implies a belief shared by the room; the record holds single members' judgments, and A10 is thin.",
  "Passes, flagged. The name implies a belief shared by the room; the record holds single members' judgments, and A10 is thin. **At C5c-12:** read whole, the judgment came before a move after a loss in 10 of the 20 rooms that moved, voiced for the room in 7 (F-019), and in 11 more rooms the judgment ended in giving the work up. The flag stays on the shared belief, which no count tests."),
 ("14. **Territoriality (T4-014).** Because members claimed the spot as territory, a neighbour's growth into it could be disputed as encroachment. Passes.",
  "14. **Territoriality (T4-014).** Because the room claimed the spot as territory, a neighbour's growth into it could be disputed as encroachment. Passes. Since C5c-08 the declaration names the room as the claimant ('Well, we were here first.' [utahjazz/c0030])."),
 ("Passes, flagged. The return the name implies is not counted. The account must state its difference from an explicit truce.",
  "Passes, flagged. The return the name implies is not counted. The account must state its difference from an explicit truce. **At C5c-12:** read whole, the first sparing names no border, truce, deal or agreement in 107 of 124 rooms and mostly states the room's own norm (F-020). The tacit part of the name is shown. Its return shows in a few records ('let's not touch minecraft, they've done nothing to us' [indonesia/c0019]) and is not counted, so the flag stays on the return."),
 ("Passes, flagged. No count tests whether rooms that helped were helped in return.",
  "Passes, flagged. No count tests whether rooms that helped were helped in return. **At C5c-12:** read whole, the first help between rooms names a deal, an exchange or a return of help in 86 of 194 rooms ('they put their flag underneath our oryx when we asked them to, so at least we should return the favour' [rotmg/c0098]; F-020). The exchange shows in the members' words. Whether help was returned is still not counted, so the flag stays on the return."),
 ("18. **Meta-organization (T4-018).** Because rooms formed a body of rooms, the hands of other member rooms could defend one member room's work. Passes.",
  "18. **Meta-organization (T4-018).** Because rooms formed a body of rooms, the hands of other member rooms could defend one member room's work. Passes. Since C5c-08 the declaration says rooms announced the alliances and hubs, with rooms as their members, so the name does its work on rooms."),
 ("2. **Coordination without command (D02).** Because the room coordinated without command, a template or the trace could align a picture while no one could give an order. Passes.",
  "2. **Coordination without command (D02).** Because the room coordinated without command, a template or posted reports of the work's state could align a picture while no one could give an order. Passes. Since C5c-10 the declaration says the room aligned many hands where its record reports a work up after the first call (233 of 370 rooms with calls; F-021), and tried in the rest."),
]
for old, new in CH:
    if t.count(old) != 1:
        sys.exit("found %d times: %r" % (t.count(old), old[:70]))
    t = t.replace(old, new)
print("%d changes check" % len(CH))
if "--write" in sys.argv:
    if os.path.exists(KEEP):
        sys.exit("%s exists" % KEEP)
    shutil.copyfile(P, KEEP)
    open(P, "w", encoding="utf-8").write(t)
    print("prose-test-C5.md written; the file before kept as prose-test-C5-p14.md")
