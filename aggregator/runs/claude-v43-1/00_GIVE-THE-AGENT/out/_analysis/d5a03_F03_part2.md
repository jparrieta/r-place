## 3. What it does differently

The branch shares one key: add-step on K01 at the third-order theme T3-095, under Keying (T4-001). D4's sentence for it: "Within F01, members test whether a claim is a joke before they act on it: by its date, its source, its plausibility or its marks, and they repair a literal reading." 18 current-ledger lines carry the key, one in each member.

I read the 18 `how` sentences and sorted each by what the test used or led to (`out/_analysis/d5a03_F03_reading.json`, counted by `out/_analysis/d5_facets.py`; a line may show two). This is my reading, not a key.

- **The claim checked by its source, marks or plausibility: 8 members.** r/magictcg: "Participants authenticate purported previews through stamps, typography, artist attribution and collector numbers rather than simply playing along." r/AMD: "Readers test hardware plausibility and inspect disclaimers instead of treating April Fools as enough to settle each claim." Also r/canucks, r/denverbroncos, r/hunterxhunter, r/PUBATTLEGROUNDS, r/streetfighter and r/yugioh.
- **The date named: 5 members.** r/mariokart: "Participants repair a literal reading of the fake takeover by invoking the date and receiving explicit recognition." Also r/canucks, r/dankmemes, r/ontario and r/yugioh.
- **A literal reading repaired: 5 members.** r/drumcorps: "Participants distinguish deliberate joking from an earnest mistake when a challenged poster admits the error." Also r/dankmemes, r/mariokart, r/minecraft and r/ontario.
- **The prank's effects troubleshot: 3 members.** r/terraria: "Testing suspected prank interference becomes practical troubleshooting through resetting controls and identifying a mod as the source." r/warframe: "Members repair disruptive prank styling and offer compensation for its reported practical costs." Also r/minecraft.
- **The test turned into a sincere or ordinary exchange: 3 members.** r/reddevils: "Prank uncertainty reached practical ticket exchange, where the seller promised proof that an ordinary offer was genuine." r/zelda: "A subject-swap joke brings a visitor into sincere cross-game recommendation and another participant decides to try the other game." Also r/planetside.
- **The frame rejected: 1 member.** r/PUBATTLEGROUNDS: "Participants test and reject the prank frame by citing blocked access and cheat advertising as signs of unauthorized control."

7 of 18 members show two of these. The most common pair is the date with a repaired reading (r/dankmemes, r/mariokart, r/ontario).

K01 says that a claim may be a joke. It does not say that members check, what they check it by, or what follows. In these rooms the check used the date, the source and the marks of the thing claimed. A failed check sent a member away and a correction brought them back (r/ontario). A check could read what looked like a joke as a hack of the sub (r/PUBATTLEGROUNDS), and it reached sincere offers that had to prove they were not jokes (r/reddevils).

**What the claim rests on.** The shared key is a pattern across rooms: 18 rooms, 18 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). What members did when they tested a claim is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "the joke tested: members check a claim's truth". The strongest argument that it names the key and not the rooms: in 3 members the line is not a check of truth. r/planetside turned a rumour into "an absurd performance and collective ratings rather than only authentication", r/zelda's swap led to sincere recommendations, and r/warframe's members repaired styling. A reader who suspected the name would look for lines with no question of true or false in them. They would find these three, and r/terraria, where the check became troubleshooting. In the other 14 members someone asked whether a claim was true or a joke. I defend the name from the members and make no renaming proposal.

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **The claim checked.** r/canucks: "You're supposed to do something *different* for April 1st." [canucks/c0022]. r/drumcorps: "This is not another April Fools shitpost." [drumcorps/c0056].
- **A literal reading met.** r/mariokart: "What? How does this make any sense?" [mariokart/c0006]. r/dankmemes: "April fools pal" [dankmemes/c0253]; "I was being sarcastic" [dankmemes/c0254].
- **The effects troubleshot.** r/minecraft: "Going out on a limb, I *think* it's the text going blurry. I *think*." [minecraft/c0024]. r/warframe: "Personally, I didn't mind the comic sans....The spinning images is goddamned infuriating." [warframe/c0026].
- **The test turned sincere.** r/zelda: "I can't say anything about how it compares to Zelda (only here because of the April fools joke) but it's easily in my top 5 all time video games." [zelda/c0086].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 18 members, 9 compose, 9 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 18 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (18 rooms, 18 lines), and members' words show the testing. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a K01 that holds the test, and each member holds a single line. A verdict of composes with residue on the original model is not a current local or shared failure.
