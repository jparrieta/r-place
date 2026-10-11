# Confusions, B1e

Written at stage B1, leg B1e, 2026-10-11. Stage B2 scores it.

## How the pairs were ranked

The ranking rests on three records.

- Rule 0 lines in `multiplacement_log.jsonl`. A line puts two themes on one second-order theme and says which one is primary.
- Bag lines, which keep one theme and name the kinds a fourth placement would need.
- The gate questions the second pass left for B1e.

A pair often placed together is a pair where a reader must choose which theme carries the second-order theme. When both directions are common, readers have already chosen differently. Balance is the smaller direction over the larger. The script is `out/_analysis/b1e_confusions.py`; the shared-member counts come from `out/_analysis/b1e_pair_overlap.py`. Each exposing second-order theme is a seeded pick among the pair's rule 0 lines, except in pairs 16 and 17, where it was chosen by hand.

## The ranked pairs

1. **T3-005 defending the work against attackers / T3-021 watching and repairing the work** (both G09). The confusion will look like this: a theme where members watch the logo, fix changed pixels and fight off a raid in one stretch. One reader places it as defence, another as repair. 655 second-order themes sit on either theme and 131 on both. Rule 0 lines: 126, with T3-005 primary in 60 and T3-021 primary in 66. Bag lines: 61. Expose it with GreenCorner t03, "defending, repairing, and retaking the corner". The separating question: is an attacker fought (T3-005), or are changed pixels found and fixed (T3-021)?

2. **T3-010 settling borders with neighbours / T3-149 agreeing truces with rival rooms** (G14 and G15). The confusion: neighbours who skirmished then agree a line. One reader sees a border, another a truce. Rule 0 lines: 38 (33 with T3-010 primary, 5 with T3-149). Bag lines that keep T3-010 and name T3-149: 151. Expose it with anarcho_capitalism t12, "negotiating truces, logos, and borders". The separating question: had a fight begun between rooms already in contact (T3-149), or is space shared where no fight began (T3-010)? The two themes are in different families, so a reader holding G14 alone sees T3-149 only through T3-010's discriminator.

3. **T3-001 staging April Fools fake news / T3-023 running an April Fools takeover** (both G01). The confusion: moderators switch the sub's look and members post fake news inside it. Rule 0 lines: 31 (16 and 15), balance 0.94. Expose it with AyyMD t08, "pulling the subreddit's own April Fools switch". The separating question: are fakes posted by members (T3-001), or is the sub itself taken over (T3-023)?

4. **T3-028 running scripts for the work / T3-070 sharing coordinates, templates and how-to** (G11 and G05). The confusion: a post gives the template and the overlay script in one breath. Rule 0 lines: 29 (16 and 13), balance 0.81. Expose it with england t03, "using scripts, images and coordinates to build a flag". The separating question: is the work placed by a script (T3-028), or are placers given what to place by hand (T3-070)?

5. **T3-004 settling the mark's design / T3-020 choosing a canvas spot** (both G07). The confusion: one thread settles what to draw and where. Rule 0 lines: 42 (24 and 18), balance 0.75. Expose it with nyu t01, "setting the torch's shape and place".

6. **T3-002 calling members in to place / T3-033 proposing the room's mark** (G04 and G07). The confusion: a post proposes a picture and asks everyone to help make it. Rule 0 lines: 47 (28 and 19), balance 0.68. Expose it with dofus t01, "making the Dofus Emerald together".

7. **T3-015 routing canvas posts into megathreads / T3-075 objecting to the canvas flood** (both G02). The confusion: members complain about the flood and moderators answer with a megathread. Rule 0 lines: 38 (15 and 23), balance 0.65. Expose it with trees t13, "arguing over r/place taking over r/trees".

8. **T3-004 settling the mark's design / T3-070 sharing coordinates, templates and how-to** (G07 and G05). The confusion: the design is settled by posting the template. Rule 0 lines: 40 (25 and 15), balance 0.60. Expose it with naruto t01, "making a Konoha mark workable".

9. **T3-009 celebrating the finished work / T3-073 reporting how the work fared** (both G21). The confusion: an end-of-canvas post that celebrates and tells what survived. Rule 0 lines: 40 (26 and 14), balance 0.54. Expose it with flashtv t13, "marking the finished canvas and recounting what survived".

10. **T3-004 settling the mark's design / T3-038 building and reporting the mark** (G07 and G08). The confusion: the design changes while it is being placed. Rule 0 lines: 18 (6 and 12), balance 0.50. Expose it with signal t01, "getting r/signal onto r/place together".

11. **T3-010 settling borders with neighbours / T3-151 bartering help with neighbours** (G14 and G15). The confusion: a deal trades space for help. Rule 0 lines: 61 (56 and 5); bag lines: 114. Expose it with rocketbeans t06, "negotiating a place in the taskbar".

12. **T3-010 settling borders with neighbours / T3-150 forming alliances between rooms** (G14 and G15). The confusion: a border deal grows into a defence pact. Rule 0 lines: 42 (40 and 2); bag lines: 122. Expose it with AMD t13, "negotiating borders and peace with Polish neighbours".

13. **T3-010 settling borders with neighbours / T3-024 refusing to cover others' work** (G14 and G13). The confusion: the room spares a neighbour's art. Is that its own choice, or a term of a deal? Rule 0 lines: 43 (36 and 7); bag lines: 70. Expose it with 4chan t07, "negotiating borders and making peace with neighbours".

14. **T3-009 celebrating the finished work / T3-043 crediting who made the work** (both G21). Rule 0 lines: 78, with T3-009 primary in 75. Readers will agree which theme leads. They will disagree on whether the credit has concepts of its own and earns the second placement. Expose it with stardustcrusaders t19, "thanking people for the JoJo spot".

15. **T3-001 staging April Fools fake news / T3-095 testing others' April Fools claims** (both G01). Rule 0 lines: 83, with T3-001 primary in 78. The confusion: members test the room's own fakes, which stays T3-001, and test a claim made by someone else, which is T3-095. Expose it with donaldglover t04, "pulling and answering April Fools jokes".

16. **T3-188 disowning placers outside the plan / T3-087 tracing who changed the work** (both G10). The two share few members (2 of 228). The second pass met T3-188's doing many times as single concepts inside other themes. Readers will place a room's denial ("those were not our people") as tracing. Expose it with megaman t11, "arguing over who is attacking and who controls the beam", or denmark t13, "arguing over rogue placements, promises, and responsibility". The separating question: does an organised room say it does not control placers acting in its name (T3-188), or does a room try to find out who did the damage (T3-087)?

17. **T3-044 recruiting canvas visitors / T3-082 finding the room's mark placed** (G04 and G08). The confusion: a post shows where the mark is. Is it for outsiders who found it, or for members who did not know of it? Expose it with DevonUK t02, "finding and showing where the flag is". The separating question: whose eyes find the mark? Outsiders led to the sub are T3-044; the room's own members are T3-082.

## A family boundary to test

Pairs 2, 11, 12 and 13 share one structure. T3-010 is in G14, while truces, alliances, bartering and the room's own restraint are in G15 and G13. Second-order themes about dealing with neighbours often hold four or more of these kinds, which is why the bag lines cluster on T3-010. A reader at stage B2 who holds G14 alone has those neighbours only through T3-010's discriminators. B2 should test whether such a reader files truces and alliances under T3-010. If so, the remedy is to merge the G14 and G15 index pages, not to change the themes.

## The hardest pair, with an estimate

The hardest pair is T3-005 against T3-021. Of the 655 second-order themes on either theme, 131 (20%) hold both acts. For these, the record splits nearly evenly on which theme is primary (60 against 66). I expect two fresh readers to disagree on the primary placement in about 45% of the both-acts themes. I expect them to disagree in about 10% of the themes that hold one act, where the line is between watching for damage and fighting a raid. Across all 655, that gives an estimated disagreement of 15 to 20% on which of the two themes carries the second-order theme. The estimate is a judgment from the direction split. No reader has been tested.

## Two sibling pairs added at B2a-r1, before any reader

Stage B2 asks that at least half the pairs the pilot tests be sibling pairs inside one family. Pairs 1 to 17 hold eight. These two were added from the same rule 0 record, ranked after the seventeen, so that ten of nineteen are siblings.

18. **T3-014 moving planning into a chat / T3-152 announcing what the chat decided** (both G03). Rule 0 lines: 43, with T3-014 primary in 42. The confusion: a thread that moves the talk to Discord and later posts what Discord decided. Readers will agree on the move and differ on whether the relay earns a second placement. Expose it with floridagators t09, "moving coordination to Discord and bringing plans back".

19. **T3-015 routing canvas posts into megathreads / T3-063 removing canvas posts by rule** (both G02). Rule 0 lines: 36 (28 and 8). The confusion: a moderator who removes canvas posts and points them to one megathread. Expose it with quebec t13, "asking to consolidate the flood and enforcing a megathread".

In the round-1 packet, five nominated items render over 2,500 bytes and were replaced by seeded picks from their pairs: pair 7 by korea t15, pair 8 by furry t10, pair 11 by acecombat t05, pair 12 by parabola t02, and pair 19 by darksouls t13 (`out/_analysis/b2_hardset_r1.tsv`).
