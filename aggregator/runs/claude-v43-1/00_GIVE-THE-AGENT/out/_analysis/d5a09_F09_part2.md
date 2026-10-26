## 3. What it does differently

The branch shares one key: a link from P03 (building) at the fourth-order theme T4-014 (Territoriality). Every member holds a line on it, 55 lines in all; most lift through the third-order theme T3-022. D4's sentence for it: "The model runs from building to keeping and, after a loss, to the move (P10), but no arrow runs from the move back to building. In these rooms it does: after a relocation the room recruits, designs and builds again at the new spot, and members report the new work."

Every line states the same sequence: the room moved, then built again. I read the 55 `how` sentences for what else they say (`out/_analysis/d5a09_F09_reading.json`, counted by `out/_analysis/d5_facets.py`; a line may say more than one thing, and 6 members' lines say nothing beyond the sequence). This is my reading, not a key.

- **New coordinates, an anchor or a template for the new site: 14 members.** r/korea: "Returns an invaded attempt to construction through replacement coordinates, their acceptance, and an explicit report of joining there." r/UPenn: "The move returns directly to construction through use and correction of the new anchor." The others are r/adventuretime, r/bostonceltics, r/chibears, r/flashtv, r/giivasunner, r/malaysia, r/nyjets, r/rutgers, r/SquareSpiral, r/thepointing, r/turkey and r/uiuc.
- **A loss, erasure or taken spot named as what moved the room: 11 members.** r/msu: "The loss-triggered move immediately restarts construction with a different design, supplying a local return omitted by the standing arrows." Also r/animalcrossing, r/bostonceltics, r/FaroeIslands, r/freedomplanet, r/korea, r/SquareSpiral, r/stargate, r/Temple, r/toolband and r/utahjazz.
- **The rebuilt work reported complete or standing: 10 members.** r/day9: "An official relocation is followed by reported completion at the new location, documenting a local return to building without establishing its cause." Also r/anaheimducks, r/fivenightsatfreddys, r/formula1, r/jerma985, r/rush, r/seolhyun, r/stardewvalley, r/stargate and r/vinesauce.
- **The line claims a sequence, not a cause: 10 members.** r/buffalowizards: "Recovery and relocation return the thread to locating and reporting the work without establishing a causal rebuilding loop." Also r/chibears, r/day9, r/Dustforce, r/fivenightsatfreddys, r/indieheads, r/pusheen, r/rush, r/Temple and r/wildhockey.
- **The new site or help offered or permitted by others: 6 members.** r/berkeley: "Reported host permission supplies an authorised location for restarting construction, adding a return route from relocation to building." Also r/hyperlightdrifter, r/indieheads, r/nbaspurs, r/rush and r/stargate.
- **Renewed calls or helpers redirected: 6 members.** r/rwby: "Relocation reopens recruitment and building as helpers are redirected to a fresh site and a new letter is started for others to continue." Also r/adventuretime, r/jerma985, r/kingdomhearts, r/twitchplayspokemon and r/utahjazz.
- **Repeated moves: 5 members.** r/twitchplayspokemon: "Explains relocation renewing building and recruitment before another takeover prompts another search." Also r/kingdomhearts, r/stardewvalley, r/stargate and r/toolband.
- **A new or smaller design at the new site: 4 members.** r/seolhyun: "Relocation returns the effort to a revised design, placement guide and celebrated rebuilt result within the participant's edited account." Also r/greyblob, r/msu and r/stargate.
- **The move and the first new pixels in one turn: 3 members.** r/penguins: "Relocation can include rebuilding immediately because one turn reports both moving and placing the eye." Also r/pebble and r/twice.

The model would not predict that a room builds again after it moves. It has an arrow into the move (A10, from judging too few hands) and none out of it. In these rooms the move was not an end. It was one step in the work: the room found a site, often told its members new coordinates, and built. And the move seldom came from a judgment of too few hands. The lines name a loss or a taken spot, a site offered by another room, or a choice not to fight (section 7).

**What the claim rests on.** The shared key is a pattern across rooms: 54 rooms and 55 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of a link line is not relied on (J: kappa 0.08). That members moved and then built is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes. Ten lines say outright that they show a sequence and not a cause, and the account claims no more than they do.

**Stage D4's name, read against the members.** The name is "the move returns to building: relocation followed by renewed construction". The strongest argument that it names the key and not the rooms: it is the key, written in prose. A reader who suspected the name would look for members whose line shows no move followed by building. Three do not show it plainly: r/berserk's line is about making a relocation notice more visible, r/hyperlightdrifter's about approval sought during construction, and r/pebble's about moving while still building. In the other 51 the members moved and built again, in their words. I defend the name and make no renaming proposal.

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **The spot taken.** r/nbaspurs: "We might have to relocate, Manchester United is taking over the area :/ Any location ideas?" [nbaspurs/c0076]. r/chibears: "They're trying to put the pink floyd album cover there, we need a different spot" [chibears/c0039].
- **The work lost.** r/utahjazz: "Oh no that shit is gone already lol. It's been demolished." [utahjazz/c0049]. r/toolband: "I tried. Had something going for a while, but the corners are very prestigious, so it got consumed." [toolband/c0059].
- **A new site proposed.** r/malaysia: "I guess we can shift to one of the Romanian hearts, /u/djfoo000, what do you think of (653,760)?" [malaysia/c0107].
- **Starting again.** r/vinesauce: "I'm trying to start one in the red space under the German flag" [vinesauce/c0052]. r/penguins: "i moved over to the RA right under Pitt, gonna try to take that over. it has alot of black so itll be easier i think i just placed the eye" [penguins/c0087].
- **Help to move from the room that won.** r/seolhyun: "the Mass Effect community has overpowered us, but are willing to help us relocate and rebuild" [seolhyun/c0007].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 54 members, 22 compose, 32 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 54 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: supported, as a sequence.** One shared change explains this part of every member's history: after the move, the room built again. Every member carries a re-check line that states it, and members' words show it in the rooms cited here. That is what the contract asks of a shared level: a limited change that explains the members jointly. Two limits stay. The support is for a sequence, not a cause; ten lines say so, and none claims a cause. And every member's own adapted account is unresolved, so the branch explanation stands on the shared line, not on validated local models. A verdict of composes with residue on the original model is not a current local or shared failure.
