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

**T4-002 Boundary work**
- (prose) Most rooms were standing communities before the canvas opened, with their own subject and rules, and the canvas arrived as a flood of posts about something else.
- (mistaken_for) Moderation or gatekeeping as such: removals belong here only when they draw the line between the sub's business and the event.

**T4-010 Backstage decision-making**
- (prose) They announce in the thread what the chat decided (33 rooms): 'Over in the discord we've decided not to expand south any farther.' [dwarffortress/c0079].
- (prose) What a chat decided reaches the record only when a member brings it back to the thread.

**T4-011 Decided order**
- (prose) The form pass, which counted nothing, found the question who leads almost never asked.
- (changed) Here a decided leader or vote binds no placer who does not choose to follow, since no one can order another to place.

**T4-018 Meta-organization**
- (prose) Members form alliances between rooms (91 rooms), meet other rooms in a chat (31), make joint marks (27), gather kindred rooms in a hub (13) and tally kindred rooms' works (6): 'Hi all - trying to help with team logos. /r/nbaplace has been created to coordinate different team subs' [lakers/c0155]. 146 of 705 rooms carry at least one of these.

**T4-024 Symbolic boundaries**
- (prose) Anyone could place any pixel.

**T4-025 Visibility returns**
- (prose) The theme was never tested as an element; at pass 5 it was the residue of six story rooms.
- (changed) Coined, this corpus's: nothing was borrowed to change.

**D02 Coordination without command**
- (changed) It names the set of ways a room aligned many hands on one picture when no one could give an order that bound anyone.

**D03 Maintenance**
- (mistaken_for) Defence is one act inside it; resilience names an outcome, the work surviving, which this study reads from the record and never from the canvas.

## The records to code

**The codes.**
- **M, the trace or a marker.** The member reports the state of the work to the thread (what is placed, done, missing, or where). Or the member says they acted on what the canvas showed. Or the member points others to the canvas's state.
- **MP, a proposal grounded in the trace.** The record proposes an addition and names, in the same record, the state of the canvas that prompts it. It counts with M, since the trace is "an opportunity for advancement" (Heylighen 2016, p. 8).
- **P, a proposal or request.** The member proposes, asks, invites or instructs other members or another room about what to add, where or how. The record names no state of the canvas that prompts it.
- **O, other.** A celebration, a call for hands, upkeep, a joke, or talk off the work.

The records below are drawn from the record at random. Each is a member's words, verbatim, with its citation and its hour since the canvas opened.

- [wildhockey/c0022] h38.63: "Edit: Nevermind, didn't refresh the page..."
- [starcraft/c0150] h69.92: "[place] Defend the little zergling! The Dutch are invading it!"
- [2007scape/c0840] h48.41: "I don't think we have the man power to uphold the GE and the Connection Lost image and the image is not correctly scaled as it will take 4x the amount of squares proposed"
- [pathofexile/c0086] h26.54: "Currently working on removing all the weird pixels randomers are adding. I choose to believe they're all butthurt Diablo 3 players. (that's a joke)"
- [dota2/c0084] h8.02: "NEED HELP"
- [thesilphroad/c0135] h22.19: "If we decide on a spot I'll help but we need to all decide on the same spot. Don't want to split efforts."
- [fireemblem/c0150] h27.55: "Yo, are we doing Great Lord Hector or Lord Hector?  Lord Hector would match with the other two sprites."
- [torontoraptors/c0128] h62.47: "Make sure to go contribute to the Raptors Logo on /r/Place, Co-ordinates are (729,670)"
- [placeDE/c0090] h48.94: "Der blaue Startpunkt ist auf 528, 859."
- [physical_removal/c0012] h23.51: "Hat is done, moving onto outline and glasses now. Some ancaps are unknowingly building over the snek in order to expand the flag the commies took over though =("
- [ufl/c0032] h60.21: "Help me expand the UF logo on /r/place"
- [donaldglover/c0070] h39.68: "BTI Album Cover on /r/place"
- [gameattack/c0031] h48.33: "Good job mate, I had to go to sleep after the first half of the border was made and was pleasantly surprised when i woke up to it was nearly complete."
- [bangtan/c0008] h30.63: "Would like to help if a spot is settled on"
- [factorio/c0027] h15.63: "added location in original post"
- [vinesauce/c0011] h14.92: "(404, 711)"
- [prequelmemes/c0130] h12.37: "Everyone go to place and help contribute to Place and make sure that the tale of Darth Plagueis the Wise is told to all!"
- [EraseThePlace/c0092] h12.37: "CALL TO ACTION! Center being invaded by a subreddit tag! Need immediate backup!"
- [dota2/c0063] h2.69: "Can we make the dota logo on /r/place?  I feel like we should"
- [2007scape/c0720] h51.76: "It usually is but it's being brigaded."
- [cfb/c0032] h14.44: "we need more help as well.  Can't mods sticky this?"
- [cfb/c0334] h43.12: "holding down the late/early shift"
- [uoft/c0091] h53.76: "You should probably make a separate thread for the Skule logo otherwise it's gonna get trampled. There seems to be three of us working on it right now. I'm currently using incognito with another account to help out too."
- [starcitizen/c0330] h69.84: "It looks like the gridref (600,456) is wrong. It should be (600,482)."
