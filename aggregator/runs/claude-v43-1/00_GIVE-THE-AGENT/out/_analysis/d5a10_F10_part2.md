## 3. What it does differently

The branch shares one key: add-step on P08 (the deal) at the third-order theme T3-010, under T4-016 (Negotiated order). 39 current-ledger lines carry the key; 37 members hold one line and r/onepunchman holds two. D4's sentence for it: "P08 says rooms propose, settle and contest deals and hold each other to them. In these rooms a deal also takes work around it: members prepare it inside the room (local consensus, a contact, checks on the counterpart's credibility), and they carry it out by moving placed work, changing templates and bot targets, and relaying the terms to placers who do not know them."

I read the 39 `how` sentences and sorted each by the part of the deal's work it shows (`out/_analysis/d5a10_F10_reading.json`, counted by `out/_analysis/d5_facets.py`). This is my reading, not a key.

- **The deal carried out by moving placed work or changing templates or bot targets: 8 members.** r/msu: "A cooperative bargain can be implemented by moving existing lettering so the neighbour can finish, without that move being triggered by erasure." r/drumcorps: "Making accommodation effective requires contacting responsible bot operators and changing the target after permission is reported." Also r/49ers, r/coldplay, r/earthbound, r/phish, r/transformers and r/WPI.
- **The deal prepared inside the room: 7 members.** r/ohio: "Members seek local consensus before communicating a territorial proposal without thereby establishing a formal leader or voting rule." r/switzerland: "Participants verify a relocation request's consensus and credibility before treating it as a change to an existing pact." Also r/catalunya, r/drawhelix, r/mit, r/NewMexico and r/placetardis.
- **The terms relayed to placers, or the relay failing: 7 members.** r/skyrim: "Distributing an agreement to ordinary placers remains a separate task after organizers approve it." r/poland: "Agreement news must be transmitted beyond its negotiating venue, and participants explicitly describe that transmission as still incomplete." r/littlewitchacademia: "Accepting an apology preserved neighbourly goodwill after uncontrolled placers defeated the promised pixel allowance." Also r/earthbound, r/evex, r/FederationPlace and r/Moondye7.
- **An uneven, conditional or refused bargain: 7 members.** r/israel: "An artist accepts a compromise while conceding inability to win, making unequal bargaining power explicit within the deal." r/Dustforce: "Explains bilateral accommodation being made conditional on displacing a third group's pixels rather than ensuring every neighboring claimant is spared." Also r/korea, r/nascar, r/onepunchman, r/seolhyun and r/uofmn.
- **A channel or person to deal through: 6 members.** r/riskofrain: "Negotiation is directed to a linked chat where a prospective representative must ask for diplomatic status." Also r/drumcorps, r/fivenightsatfreddys, r/Moondye7, r/notredame and r/starlightstage.
- **Terms sought before any loss, or regretted for not being sought: 4 members.** r/linux: "Anticipated overlap can prompt a treaty request before demonstrated warfare or erosion." Also r/buffalobills, r/cavestory and r/kurdistan.
- **An appeal or apology turned into accommodation: 3 members** (r/faeria, r/hearthstone, r/littlewitchacademia).

Only 4 of 38 members show two of these parts.

P08 says rooms make deals and hold each other to them. It does not say what a deal costs the room that makes it. In these rooms the deal had three kinds of work beside the talk: agreeing inside the room before answering, moving the room's own placed work or its templates and scripts, and getting the terms to every placer. The last is the telling problem of P05, carried between rooms. A deal could be undone by the room's own placers, as in r/buffalobills and r/littlewitchacademia; whether those placers had heard of the deal, the record does not say (section 6). Where the model has P21 (members say no one can bind every placer), these rooms also tried to reach every placer, by telling.

**What the claim rests on.** The shared key is a pattern across rooms: 38 rooms and 39 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). What members did to make their deals is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "a deal carried out as work: prepared in the room, then implemented and relayed". The strongest argument that it names the key and not the rooms: it names three steps in order, and one member (r/earthbound) shows two of them; no member shows all three. A reader who suspected the name would look for a room where a deal was prepared, carried out and relayed. None is shown. Seven members' lines are about uneven or refused bargains, which the name does not cover. The first half, "a deal carried out as work", holds for the 21 members whose lines show preparing, carrying out or relaying. I propose a renaming in `notes-D5.md`: "the deal's work: preparing, carrying out and relaying the terms, or bargaining from weakness".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **Asking in advance.** r/linux: "We'd like to make a treaty before it becomes a war. Any propositions?" [linux/c0047].
- **A neighbour's leave, with a date.** r/drumcorps: "r/rust, they said they will let us build through it sometimes tomorrow" [drumcorps/c0110].
- **Making room for each other.** r/transformers: "I think that'll work fine, we're currently only working on raph so there shouldn't be any gripe from our side" [transformers/c0078].
- **Fitting two works together.** r/hearthstone: "I'll help, it will look better with one over the other than two just crashing into each other" [hearthstone/c0284].
- **Ceding space from boredom.** r/onepunchman: "I would do that, if the damn flag wasn't so complicated. Anyway just take it, I'm bored of it anyway" [onepunchman/c0054].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 38 members, 16 compose, 22 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 38 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (38 rooms, 39 lines), and members' words show each part of a deal's work. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a P08 that holds these steps, and the steps are shown in subsets of members, rarely together. A verdict of composes with residue on the original model is not a current local or shared failure.
