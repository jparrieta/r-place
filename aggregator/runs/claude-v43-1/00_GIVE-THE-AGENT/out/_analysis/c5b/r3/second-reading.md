# The second reading

## The rule

Written before the declarations were amended. The rule was first written for the fourth-order themes; the paragraph after it extends it to the dimensions.

**What the rule reads.** In each of the 28 construct blocks in `fourth/fourth.jsonl`, the rule reads every sentence of the `prose`, `changed` and `mistaken_for` fields that says something about these rooms or their members. A sentence about a source construct, saying what Gieryn or Mintzberg holds, is about the literature. It is read only for its mark, verified or recalled.

**Which sentences are in question.** A sentence is in question when it is:
- **universal:** every, all, no one, nothing, never, always, any, only;
- **comparative:** more, most, less, fewer, strongest, than, as much as;
- **causal:** because, so, makes, brings, turns into, leads to, keeps alive, why, explains, or a verb that gives one act as the cause of another;
- **cyclic:** again, each time, returns, renews, a loop.

**When a sentence in question stands.** It stands only if one of these supports it:
- an order count in `model/arrows.jsonl` that beats its null;
- a line in `findings.jsonl`;
- a count in `structure-C4.md` (rule 5's three numbers, or the rooms carrying a theme);
- a fact of the setting as the contract states it. The setting facts are: one pixel per interval for each account; anyone may change any pixel; placement stopped at hour 73; no one holds authority over another's placing.

**Otherwise the sentence is rewritten.** The new sentence says what members did, in how many rooms, in the members' own terms. Each act it names must be shown by at least one member's quote. The quotes are the exemplars and material in `structure-C4.md`, and for the first four declarations a further seeded draw through `cite.py`.

**The scope.** The declaration prose rule above now also reads the eight dimension declarations in `dimensions.jsonl`. It reads every sentence of the `construct` block's `changed` and `mistaken_for` fields that says something about these rooms or their members. The `question` and `predicate` fields define what the dimension gathers. They are read only for a claim about the rooms stated as fact.

## The sentences in question

Each sentence below is quoted from an amended declaration and holds a word from the rule's lists. The field it comes from is in brackets.

**T4-007 Stigmergy**
- (prose) The record does not show whether placers who never wrote followed the canvas.
- (mistaken_for) Here any member may post a template (Standardization of output, 237 rooms), and no one can make placers follow it.

**T4-008 Standardization of output**
- (changed) Here anyone may post a template, and no one can make a placer follow it.
- (mistaken_for) A template here is posted for anyone to follow, and no one can order a placer to follow it.

**T4-009 Workarounds**
- (changed) Here the workaround evades the rate limit that applies to every account, and members in 80 rooms argue whether scripts are fair.

**T4-013 Repair work**
- (prose) Anyone could change any pixel.
- (prose) They defend it against attackers (392 rooms), watch it and repair changed pixels (293), choose upkeep over expansion (43), concentrate effort on fewer pieces (29), cover the night shift (24) and reshape the mark against tampering (20): 'Remember to maintain, not just expand!' [greenlattice/c0215]. 526 of 705 rooms carry at least one of these, gated on the rooms with a work of their own.

**T4-014 Territoriality**
- (prose) In seven rooms or fewer each, hosts vet others' requests to build, members dispute who may approve a spot, and a room relies on a bigger neighbour. 288 of 705 rooms carry at least one of these: 'Well, we were here first.
- (mistaken_for) Property rights or possession: nothing here is owned, only claimed.

**T4-022 Flagging the nation**
- (prose) In five rooms or fewer each, they weigh the room against nations, dispute national belonging, debate friendship with historic enemies or argue the nation's historical record. 62 of 705 rooms carry at least one of these: 'We did it again after 1965 and 1971, now at r/Place.' [pakistan/c0240].
- (prose) Membership carried in does not come before the attack more often than chance (F-011).

**D04 Order without law**
- (mistaken_for) There is no common pool to manage here, only adjacent works.

**D05 Collective identity**
- (changed) Membership carried in does not come before the attack more often than chance (F-011).
- (mistaken_for) The emblem is what the room chooses to show; identity is the membership the work carries, which can exist before any emblem is chosen.

**D07 Imprinting**
- (changed) Most rooms existed before the canvas; 78 of 705 have no posts in the week before it.

## The records to code

**The codes.**
- **M, the trace or a marker.** The member reports the state of the work to the thread (what is placed, done, missing, or where). Or the member says they acted on what the canvas showed. Or the member points others to the canvas's state.
- **MP, a proposal grounded in the trace.** The record proposes an addition and names, in the same record, the state of the canvas that prompts it. It counts with M, since the trace is "an opportunity for advancement" (Heylighen 2016, p. 8).
- **P, a proposal or request.** The member proposes, asks, invites or instructs other members or another room about what to add, where or how. The record names no state of the canvas that prompts it.
- **O, other.** A celebration, a call for hands, upkeep, a joke, or talk off the work.

The records below are drawn from the record at random. Each is a member's words, verbatim, with its citation and its hour since the canvas opened.

- [Slovakia/c0038] h69.29: "I've almost finished a new one at 605, 772. Help me maintain it?"
- [TransFlagPlace/c0253] h61.22: "CAN I PLEASE BUILD "DONATE BLOOD""
- [TransFlagPlace/c0230] h58.74: "Trans Avocado Idea Proposed"
- [rainbowgrid/c0007] h64.61: "center block of the black outline is 496,414"
- [TransFlagPlace/c0274] h66.50: "help adding the genderfluid flag"
- [TransFlagPlace/c0136] h38.77: "Might be a good place to start a new TransFlag, is all I'm saying."
- [TransFlagPlace/c0259] h62.42: "Watch The Throne Cover"
- [TransFlagPlace/c0226] h58.30: "Donate blood"
- [bangtan/c0055] h48.67: "I added a little something for my bias"
- [AvoArmy/c0006] h13.94: "people are making and protecting avos without sub coordination"
- [italy/c0177] h44.83: "Ma magari avessero uno script. In realtà hanno fatto tutto a mano. C'è chi era sveglio alle 4 per contrastare i griefer."
- [Slovakia/c0017] h43.75: "Don't destroy the drop next to our flag!"
- [AvoArmy/c0075] h36.17: "It's hard to fill in the space while trying to maintain because of the vandalism"
- [TransFlagPlace/c0264] h63.83: "Trying to add RHPS to the flag"
- [AvoArmy/c0121] h61.39: "I would like to revert them to the green, natural, almost erotic avocado color"
- [TransFlagPlace/c0229] h58.61: "where should we attempt again"
- [AvoArmy/c0045] h29.68: "idk if we can direct the avomind *that* meticulously."
- [AvoArmy/c0187] h73.15: "I'm conceding on my effort to transmute your sign to say anarchy. Good fight, avocado people."
- [TransFlagPlace/c0086] h28.17: "I couldn't help but notice the demiboy flag here."
- [TransFlagPlace/c0175] h43.58: "I tried to make it again, but there are at least 3 separate factions fighting for that heart, and I'm an army of 1."
- [Slovakia/c0019] h44.29: "I started turning 1 of the hearts into Slovak, need some help."
- [TransFlagPlace/c0103] h32.52: "Already started on it, come help along!"
- [AvoArmy/c0100] h68.79: "I'm very much in favour of a bi-avo."
- [rainbowgrid/c0009] h65.07: "oh ok so like right in the middle of what's ETP territory right now?? i'm not that good at place coordinates, like how do you make one of those links to a place, i should learn that :)"
