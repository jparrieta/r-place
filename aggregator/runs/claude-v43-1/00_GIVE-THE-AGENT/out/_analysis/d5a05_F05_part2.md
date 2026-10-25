## 3. What it does differently

The branch shares one key: add-step on K01 at the third-order theme T3-097, under Keying (T4-001). D4's sentence for it: "Within F01, members and moderators end the prank's styling and restore ordinary use: they switch styles off, ask whether the sub has switched back, and clear what the prank left." 13 current-ledger lines carry the key; 11 members hold one line and r/anime_irl holds two.

I read the 13 `how` sentences and sorted each by how the styling ended, or failed to (`out/_analysis/d5a05_F05_reading.json`, counted by `out/_analysis/d5_facets.py`; a line may show more than one). This is my reading, not a key.

- **The host ended the styling or restored the sub: 6 members.** r/popheads: "A moderator publicly ends the local joke period while later discussion evaluates its prominence." r/NieR: "Ending the theme swap includes a later reminder to remove its leftover page title and a moderator acknowledgment." Also r/dota2, r/furry_irl, r/miraculousladybug and r/nbaspurs.
- **Members complained about the styling or refused its rules: 4 members.** r/metalgearsolid: "The styling complaint identifies the prank and its readability cost without showing the styling being disabled or restored." r/anime_irl: "Participants contest changed rules and directly refuse title enforcement within the temporary takeover." Also r/miraculousladybug and r/nbaspurs.
- **Members switched the styling off for themselves: 3 members.** r/pcmasterrace: "Users escape prank styling locally by disabling styles or uninstalling the font rather than securing a room-wide reversal". r/minecraft: "Readers restore usable access by disabling prank styling and qualify which interface controls are available". Also r/schoolidolfestival.
- **Members asked what changed or whether the sub was back: 2 members.** r/ontario: "A later question asks whether the subreddit has switched back while leaving the changed feature and its restoration unresolved." Also r/miraculousladybug.
- **Leftovers of the play cleared or kept: 2 members.** r/furry_irl: "Recovery restores ordinary posting rules while preserving compliant prank posts with participation flair." Also r/NieR.
- **A member waited the play out: 1 member.** r/anime_irl: "A participant explicitly waits out the calendars before posting, documenting delayed participation rather than an implemented styling switch."

5 of 12 members show two or more of these.

K01 gives the play a one-day licence. It does not say that the play can block ordinary use of the sub, or that the day needs an end someone carries out. In these rooms the styling made pages hard to read, and members took one of two routes out. Some left at once on their own, with a browser setting or a tool, and needed no one. Others asked the host, and in 6 members the host ended the play. The end could leave traces: a page title, a flair, posts kept from the day.

**What the claim rests on.** The shared key is a pattern across rooms: 12 rooms and 13 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). What members did when the styling got in the way is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "the styling ended: ordinary use restored". The strongest argument that it names the key and not the rooms: the name claims an outcome, and half the lines do not show it. In r/pcmasterrace members escaped "rather than securing a room-wide reversal". In r/metalgearsolid the line shows the complaint "without showing the styling being disabled or restored", and in r/ontario the restoration is "unresolved". r/anime_irl waited and refused. A reader who suspected the name would count the lines in which the sub is restored: 6 of 12 by my reading. "The styling" names what every line concerns; "ended" and "restored" hold for half. I propose a renaming in `notes-D5.md`: "the styling escaped or ended: members switch it off, the host restores ordinary use".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **Refusing the play's rules.** r/anime_irl: "So we can just change the rules willy nilly now eh? Good to know." [anime_irl/c0069].
- **Waiting for the end.** r/anime_irl: "Has it finished yet?" [anime_irl/c0033].
- **Naming what changed.** r/miraculousladybug: "Hawkmoth themed" [miraculousladybug/c0016].
- **After the end.** r/popheads: "It's April 2nd here... so what now?" [popheads/c0253].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 12 members, 6 compose, 6 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 12 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (12 rooms, 13 lines), and members' words show the styling and its end. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a K01 that holds an end, and the end is shown in 6 members only. A verdict of composes with residue on the original model is not a current local or shared failure.
