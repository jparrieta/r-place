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

**T4-004 Frame bridging**
- (mistaken_for) In-group humour, or culture as such: the construct holds only the traffic between a frame the room had and the new episode.

**T4-005 Mobilization**
- (prose) Each account could place one pixel per interval, and no one could order another to place.
- (prose) The form pass found such lines and never counted them.
- (changed) Here no one could hold a member's time or assign it.
- (mistaken_for) The calls here rarely offer anything beyond the work: a reward offered before the work appears in 9 of 705 rooms (F-016), for example 'As an insentive, for every person who joins in and comments below I will post 5 pig gifs!

**T4-006 Collective representation**
- (prose) In six rooms or fewer each, they adopt a sign others began, make a tribute alone, build memorials to the dead, leave the work unsigned, plan a mark that moves in the timelapse or follow the creator's wishes. 483 of 705 rooms carry at least one of these: 'Does it bother anyone else that the logo is off center.....' [smite/c0348].

**T4-015 Live and let live**
- (prose) Two rooms or fewer each defy the call for restraint, mourn art the room covered, place rival marks together or urge repair over retaliation. 205 of 705 rooms carry at least one of these: 'We mean you no harm!

**T4-016 Negotiated order**
- (prose) In six rooms or fewer each, a room stays neutral, members negotiate across a language gap, argue whether cooperation is surrender or trade away another room's work. 467 of 705 rooms carry at least one of these.
- (prose) Members say themselves that an agreement does not bind every placer: 'Their group has agreed to not mess with our space but there will always be those individuals who don't listen / care' [hentai/c0105].

**T4-019 Attribution**
- (prose) Members work out who changed their work and why.

**T4-020 Repertoire of contention**
- (prose) In three rooms or fewer each, members plant disguised scripts on rivals, brigade one person off Reddit or relay a streamer's call to attack. 231 of 705 rooms carry at least one of these.

**T4-021 Rivalry**
- (changed) In some rooms, a tie from before the canvas names the rival in the same turn as the attack (C02, untested for order; F-013: 10 turns in 7 story rooms), and membership carried in does not come before the attack more often than chance (F-011).

**D06 Host framing**
- (mistaken_for) Frame analysis would cover every interpretation in the corpus; this names only the host community's handling of its own space during the event.

## The records to code

**The codes.**
- **M, the trace or a marker.** The member reports the state of the work to the thread (what is placed, done, missing, or where). Or the member says they acted on what the canvas showed. Or the member points others to the canvas's state.
- **MP, a proposal grounded in the trace.** The record proposes an addition and names, in the same record, the state of the canvas that prompts it. It counts with M, since the trace is "an opportunity for advancement" (Heylighen 2016, p. 8).
- **P, a proposal or request.** The member proposes, asks, invites or instructs other members or another room about what to add, where or how. The record names no state of the canvas that prompts it.
- **O, other.** A celebration, a call for hands, upkeep, a joke, or talk off the work.

The records below are drawn from the record at random. Each is a member's words, verbatim, with its citation and its hour since the canvas opened.

- [afip/c0007] h37.41: "We have plenty of space below the flag, lets just build a giant MURICA! there, rather than the scrappy shit we currently have at the top."
- [twice/c0057] h51.32: "I'm helping protect it :) We can try to write Knock Knock/Cheer Up/Ooh-Ahh under it!"
- [rickandmorty/c0010] h5.52: "Come help draw a Rick over at r/place while you wait for Season 3!"
- [southafrica/c0142] h51.13: "We are currently trying to do this:"
- [prequelmemes/c0542] h61.44: "What happened to our glorious Darth Sidious and his lightning in the corner of our banner?"
- [monsterhunter/c0118] h40.48: "Lets make this in r/place"
- [denmark/c0218] h45.67: "Aktion kl. 18 for at udvide det danske flag!!"
- [placestart/c0177] h49.81: "It doesn't get more Win95 than WEEZER"
- [furry/c0151] h36.74: "I will help."
- [halo/c0153] h39.34: "What's that square in r/place master chief's mouthpiece, it looks bad"
- [placestart/c0099] h46.74: "Where's clippy?"
- [prequelmemes/c0252] h39.58: "There's too many of them, what do we do?"
- [tinytardis/c0003] h35.07: "The Tiny TARDIS"
- [opticgaming/c0120] h48.24: "This is how i feel we should hold our territory in the area provided we should hold a 4x2 green brick wall, however we must avoid the major arts if possible!"
- [denmark/c0189] h45.42: "Den nyeste mission: Vi angriber New Zealands kiwi-flag og skifter det ud med Andrea!"
- [factorio/c0059] h22.40: "Everyone ready to start working on a big one?"
- [monsterhunter/c0103] h34.95: "Hey there! I say we keep expanding and create a Mizutsune icon!"
- [teamcube/c0036] h70.89: "496, 419 New Cube."
- [southafrica/c0107] h41.27: "Suggestion: Table Mountain or Mandela Silhouette on /r/place?"
- [coldplay/c0062] h73.50: "Next time we'll be ready for more!"
- [suomi/c0059] h17.55: "rakennetaan r/paikassa suomen lipun alle "TORILLE""
- [warriors/c0119] h56.60: "takes too much space"
- [ainbowroad/c0807] h29.79: "(362, 528) We are being built over by a pornhub logo. How shall we react?"
- [bindingofisaac/c0071] h20.05: "Pls"
