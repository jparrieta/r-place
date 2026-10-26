## 3. What it does differently

The branch shares one key: restrict on P05 at the fourth-order theme T4-006 (Collective representation). Every member holds one line on it, 59 lines in all; most lift through the third-order theme T3-004. D4's sentence for it: "P05's added clause says that a planned change is repaired away until its keepers are told. In these rooms the lines limit the clause where the design is settled." D4 read two halves in the lines. F07 is one of three branches that restrict P05 at different nodes; F26 and F27 are the others, and they meet F07 only at the dimension.

I read the 59 `how` sentences and sorted each by what it says about the clause (`out/_analysis/d5a07_F07_reading.json`, counted by `out/_analysis/d5_facets.py`; a line may show more than one). This is my reading, not a key.

- **Informed members reject the change: repair enforces a competing design, and telling does not settle it: 31 members.** r/megaman: "Communicating a planned alteration cannot secure its acceptance when keepers knowingly reject the change as defacement." r/AyyMD: "Informing keepers of an agreed colour does not secure acceptance when a participant explicitly rejects the vote after being told its result." r/fivenightsatfreddys: "Telling keepers a revised plan is insufficient where informed factions dispute its legitimacy rather than merely misrecognizing the change as damage." r/katawashoujo: "Distinguish builder rejection from repair through ignorance: purple was proposed and partly placed, but original builders explicitly wanted black for contrast." The others are r/AMD, r/archlinux, r/calvinandhobbes, r/edboxes, r/eve, r/farmcarrots, r/FlaggyFlag, r/flashtv, r/hentai, r/hongkong, r/hyperlightdrifter, r/luciomains, r/metalgearsolid, r/morrowind, r/muse, r/newzealand, r/OnePiece, r/polska, r/porterrobinson, r/Rainbow6, r/seahawks, r/sheffield, r/shield, r/TheHulk, r/TsundereSharks, r/unitedkingdom and r/uvic. In 20 of the 31 the same line names no evidence limit.
- **The record does not show the agreed change, the untold keepers, the failed telling or the loss: 36 members.** r/twitch: "Cancelled recolouring warrants the revised uninformed-keepers mechanism only with evidence of an agreed change, keeper identity, and failed communication, which these concepts do not supply." r/coldplay: "The information-failure explanation requires evidence of an agreed change, reversal, and failed communication that the retained clarification and unexplained abandonment do not establish." 11 of the 36 are among the 31 above.
- **Mistaken repair or misrecognition of a friendly change is seen in part: 7 members.** r/czech: "Friendly misrepair and correcting plan knowledge are evidenced, but erased lettering alone does not identify uninformed keepers or establish abandonment caused by failed notification." r/timbers: "Recognition of friendly redesign is documented, but explicit notification and permanent loss of an intended change remain unresolved." Also r/chicago, r/eve, r/satania, r/sheffield and r/tampabaylightning.
- **A change the keepers welcome becomes part of the defended work: 2 members.** r/pusheen: "Apply restoring-the-known-form only to changes treated as damage, since an explicitly welcomed unplanned addition can become part of the defended work." Also r/luciomains.
- **Upkeep does not always come before new work: 1 member.** r/indieheads: "Upkeep does not invariably outrank creation when an organiser prefers replacing documented images to defending them indefinitely."
- **Uncertain keepers hold back from repair: 1 member.** r/puzzleanddragons: "Uncertain keepers can avoid disputed repairs instead of restoring an assumed form, so missing instructions do not necessarily entail erasure or abandonment."

P05's clause names one reason a planned change is undone: the keepers were not told. It predicts that telling them ends the repair. In about half of these rooms the keepers knew and did not accept the change. The repair then carried one version of the design against another, and telling did not end it. In the other half the coders found repair and argument but not the evidence the clause needs, so the clause is untested there. A room of this branch does not show the clause failing for lack of telling; it shows the design still open while the room keeps the work.

This is a claim the branch bounds, and it is written as finding F-025 under rule 14 (`findings.jsonl`). It narrows the clause to changes the keepers would accept once told. It changes no word of P05; the model stays frozen, and F-024's two routes are not touched.

**What the claim rests on.** The shared key is a pattern across rooms: 59 rooms, 59 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of a restrict line is not used (J: kappa 0.08). That members knew of a change and rejected it is a claim on their words, through `cite.py`, in sections 1, 4 and 10, and F-025 cites them. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "the telling clause not shown at the design: informed members reject the planned change". The strongest argument that it names the key and not the rooms: its second half says informed members reject the change, and 28 of 59 members' lines say no such thing. A reader who suspected the name would count the lines with no rejection in them; by my reading they are 28, most of them lines in which the evidence the clause needs is missing. The first half, "the telling clause not shown", holds for every member. I propose a renaming in `notes-D5.md`: "the telling clause limited: informed members reject the change, or the record cannot show the clause".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **A change rejected.** r/megaman: "Except the phrygian cap just looks bad. You can't say you're protecting him when you're now just trying to change it completely." [megaman/c0025].
- **A change offered, with an offer to stop.** r/katawashoujo: "Heyo, every once in a while I'm continuing to place purple around the heart. I will stop if you want me to" [katawashoujo/c0036].
- **A change undone.** r/uvic: "Oh no, now it's off center!" [uvic/c0011]. r/archlinux: "I was trying to anti-alias the text too, but it kept getting erased." [archlinux/c0228].
- **Deciding before changing.** r/uvic: "Before attempting anything we should decide if we actually want to make the change shown in the picture. Comment what you guys think!" [uvic/c0051].
- **Going along.** r/FlaggyFlag: "I'll go along with it, but I would still rather have the blue border." [FlaggyFlag/c0009].
- **Enforcing a version.** r/fivenightsatfreddys: "anyone caught putting black pixels on Fredbear's hat will be banned unironically for a week" [fivenightsatfreddys/c0538].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 59 members, 21 compose, 38 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 59 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (59 rooms, 59 lines), and members' words show the rejection in several rooms. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a P05 that holds the bound, and the lines split between rejection and missing evidence. The bound itself is a finding (F-025), resting on cases. A verdict of composes with residue on the original model is not a current local or shared failure.
