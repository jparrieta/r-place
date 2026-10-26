## 3. What it does differently

The branch shares one key: add-step on P11 (marking the work) at the third-order theme T3-043 (credit for the work), under T4-026 (Completion ritual). 14 current-ledger lines carry the key, one per member. They are the same 14 lines that place these rooms in F17 at this theme. D4's sentence for the subform: "Within F17, members dispute and correct who made the work while it is still being placed: accusations, denials, competing labour claims and corrected omissions."

I read the 14 `how` sentences and sorted each by what the crediting did (`out/_analysis/d5a19_F19_reading.json`, counted by `out/_analysis/d5_facets.py`). This is my reading, not a key.

- **Who made the work disputed: between members, between rooms, or over who started it: 8 members.** r/Okami: "Attribution includes disputes about authentic makers, first arrival and proof during ongoing work." r/wine: "Reporting maintenance can provoke an ownership accusation that the maintainer explicitly denies." Also r/afip, r/anime, r/freedomplanet, r/luciomains, r/opticgaming and r/yogscast.
- **A claimant's standing checked: nationality, account age, how active they were: 3 members.** r/azerbaijan: "Acknowledging the contribution includes asking whether its maker is Azeri or Turkish and receiving the maker's national self-identification." Also r/opticgaming and r/yogscast.
- **A list of helpers made, and omissions in it corrected: 3 members.** r/Moondye7: "Crediting includes correcting omissions, teasing sufficient activity and requesting symbolic moderator rewards for helpers." Also r/SwissNeutralityZone and r/vocaloid.
- **An attempt or unfinished work credited: 2 members.** r/aeon: "Crediting attempted participation after closure acknowledges effort even when the intended mark remains unfinished." r/rocketbeans: "Participants also recognised the project's communal value while its construction remained unfinished."
- **A reward or a proof asked for or offered with the credit: 2 members** (r/Moondye7 and r/yogscast).

Most members show one of these: 11 show one, 2 show two and 1 shows three. Nine members contest credit, by a dispute over who made the work or a check on a claimant. By the earliest hour each line cites, 9 of 14 lines begin before placement stopped and 5 after. Of the 9 that contest credit, 7 begin before the close.

P11 says the room "credits makers and helpers". The model also names, in P02, a room that "claims a mark others made", and in P24, members explaining "whose mark a picture is". None of these says that a claim to credit can be refused. In these rooms it was. Members denied a fellow member's part, a political sub's share in a flag, and their own sub's claim to pictures others had made. Two groups claimed one wolf. Claimants were checked: their account's age, their nationality, how active they had been. And keeping the work was heard as claiming it (r/wine), so a member who repaired a picture had to deny owning it. Credit here was a claim others could contest, not a thanks the room handed out.

**What the claim rests on.** The shared key is a pattern across rooms: 14 rooms and 14 lines in the ledger, cut at D4 on keys alone as a subform of F17. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). Who claimed and who denied is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines and my dating of them are readings of the coders' sentences and cited concepts, not counts the ledger makes.

**Stage D4's name, read against the members.** The name is "credit contested during the work". Credit is contested in 9 of 14 members, and the line begins during the work in 9; both hold in 7. The other members credit attempts, make lists of helpers, or correct a bot's attribution, without a dispute, and most of these come after the close. The strongest argument that the name names the key: it restates D4's sentence, "while it is still being placed", and the contest falls during the work in half the members. A reader who suspected so would set the contests beside their hours and find the lists and the thanks after the close. I propose a renaming in `notes-D5.md`: "credit claimed, checked and corrected: makers disputed, claimants checked, lists of helpers mended, mostly while the work stood".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **The idea here, the work elsewhere.** r/luciomains: "Was coordinated from the main subreddit, not from here. Still cool!" [luciomains/c0010].
- **Cleanup counted against a claim.** r/freedomplanet: "no you were not I had to clean up your mess twice" [freedomplanet/c0045]. Another reframed it: "bonding experience clean up others messes" [freedomplanet/c0047].
- **Activity weighed.** r/opticgaming: "i was more active than you were so idk where you are coming from" [opticgaming/c0144].
- **No sole credit.** r/afip: "neither group deserves sole credit we are all doing it as Americans." [afip/c0074].
- **A name for the memorial.** r/SwissNeutralityZone: "Count me in too. I fought the void for our flag and mountains." [SwissNeutralityZone/c0106].
- **A bot corrected.** r/vocaloid: "I'm giving credit where credit is due Mr. Bot." [vocaloid/c0068].
- **Credit before the goal.** r/rocketbeans: "auch wenn wir aktuell noch nicht am ziel angekommen sind, hats spass gemacht und die community wieder bisschen zum leben erweckt" [rocketbeans/c0043] (even though we have not reached the goal yet, it was fun and brought the community back to life a little).
- **A symbolic reward.** r/Moondye7: "der Post ist jetzt komplett (denke ich), kannst ja dem Rest auch noch Scheinmod geben" [Moondye7/c0067] (the post is complete now, I think; you can give the rest a sham moderator title too).

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 14 members, 6 compose, 7 compose with residue, 0 do not compose and 1 cannot tell, r/azerbaijan. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 14 members are unresolved, r/azerbaijan among them; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (14 rooms, 14 lines), and members' words show each way credit was claimed and checked. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a P11 that holds this step, and five members credit without a contest. A verdict of composes with residue or cannot tell on the original model is not a current local or shared failure.
