## 3. What it does differently

The branch shares one key: add-step on K01 at the third-order theme T3-032, under Keying (T4-001). D4's sentence for it: "Within F01, members object to the play and police the licence: they set limits on taste and repetition, demand labels, deletion, restoration or better jokes, and dispute when the licence ends." 15 current-ledger lines carry the key; 11 members hold one line and 2 hold two.

I read the 15 `how` sentences and sorted each by what the objection was about (`out/_analysis/d5a04_F04_reading.json`, counted by `out/_analysis/d5_facets.py`; a line may show more than one). This is my reading, not a key.

- **The joke judged for effort, repetition or timeliness: 6 members.** r/magictcg: "Participants judge effort, repetition and timeliness separately from the technical plausibility of fabricated images." r/canucks: "Members criticize duplicate or deteriorating jokes and request deletion without thereby objecting to a canvas recruitment flood." Also r/anime_irl, r/elitedangerous, r/nbaspurs and r/ultrahardcore.
- **The licence's end or duration disputed: 4 members.** r/bindingofisaac: "Participants dispute the end of the temporary joke by answering a one-day explanation with reports of continuing posts." r/chelseafc: "Members demand restoration and dispute the prank's duration without establishing completed restoration." Also r/dankmemes and r/monstercat.
- **The play or its compulsory rules objected to: 4 members.** r/monstercat: "Members contest compulsory joke participation and defend its temporary duration while the moderator explains its intended stupidity." r/dankmemes: "Recognizing the prank does not end resistance to its rules or make continued performance acceptable." Also r/nbaspurs and r/ultrahardcore.
- **A limit of taste or harm set: 3 members.** r/stargate: "Participants contest the prank's acceptability and propose explicitly fictional alternatives rather than accepting a common license to deceive." r/nbaspurs: "Readers can demand consequences for the painful prank's maker and switch off the host styling." Also r/bostonceltics.
- **Labels or deletion demanded: 2 members.** r/AMD: "Members seek labels or deletion because lingering pranks contaminate later searches and make genuine leaks harder to judge." Also r/canucks.
- **Moderators enforcing a limit: 1 member.** r/elitedangerous: "Moderators enforce duplication and relevance limits during the joke licence, distinct from deciding canvas leadership or policing offensive wording."

6 of 13 members show two or more of these.

K01 gives the play a one-day licence. It does not say that the licence has limits, that members set them, or that its end is argued over. In these rooms members set three kinds of limit: on taste (no jokes about a death or a team's worst day), on quality (no stale or repeated jokes) and on time (the day ends at a set hour). They addressed the limits to the host: they asked the moderators to remove a post, to restore the sub, or to take a moderator's fan card away. In 12 of the 13 members' lines it is members who object; in one, a moderator enforces.

**What the claim rests on.** The shared key is a pattern across rooms: 13 rooms and 15 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). What members objected to, and to whom, is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "the licence policed: objections to the play, its limits and its end". The strongest argument that it names the key and not the rooms: "policed" says that someone enforced the limits, and in 12 of 13 members the lines show members objecting, not anyone enforcing. Only r/elitedangerous shows enforcement, by a moderator. A reader who suspected the name would look for a sanction that followed an objection. The lines record demands (remove it, restore the sub, take the fan card), and the quotes record a few answers (a sidebar "fixed" [nbaspurs/c0006], an apology [stargate/c0007]). They record no sanction on a member. The second half of the name, "objections to the play, its limits and its end", holds for every member. I propose a renaming in `notes-D5.md`: "the licence contested: objections to the play, its limits and its end".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **Taste.** r/bostonceltics: "its just a tasteless April fools joke" [bostonceltics/c0012].
- **Quality.** r/nbaspurs: "I have a decent sense of humor, but putting a photo up of a shitty time in Spurs history takes 0 creativity." [nbaspurs/c0011]. r/anime_irl: "{Calendar_irl was a mistake}" [anime_irl/c0167].
- **The play objected to.** r/monstercat: "i didn't really want to take part in the lame mcatDab joke" [monstercat/c0147]. r/bindingofisaac: "when you dont like egg but the whole reddit is full of it" [bindingofisaac/c0192].
- **The end.** r/monstercat: "inb4 people rejoice that it's over" [monstercat/c0144].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 13 members, 4 compose, 9 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return. The share with residue, 9 of 13, is higher here than in F01 (49 of 103), F02 (15 of 33) or F03 (9 of 18).

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 13 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (13 rooms, 15 lines), and members' words show the objections. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a K01 that holds the limits, and the host's answers appear only in the quotes of a few members. A verdict of composes with residue on the original model is not a current local or shared failure.
