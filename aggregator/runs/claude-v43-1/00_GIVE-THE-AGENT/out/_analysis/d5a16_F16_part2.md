## 3. What it does differently

The branch shares one key: add-step on P23 (the chat) at the third-order theme T3-014, under T4-010 (Backstage decision-making). 35 current-ledger lines carry the key, one per member. D4's sentence for it: "P23 (a candidate) says members move planning into a chat and invite helpers. In these rooms the chat's access is upkeep: members replace expired invitations and broken links, screen who comes in, and relay decisions back to the thread for those outside."

I read the 35 `how` sentences and sorted each by the kind of upkeep it shows (`out/_analysis/d5a16_F16_reading.json`, counted by `out/_analysis/d5_facets.py`). This is my reading, not a key.

- **An expired or broken invitation reported and replaced: 15 members.** r/berserk: "Replacing an expired invitation restores access to the advertised planning venue." r/pcmasterrace: "Access to the planning venue requires replacing expired invitations and responding when the replacement expires again" Also r/AprilKnights, r/darksouls, r/GranColombia, r/lakers, r/lithuania, r/mcgill, r/monalisaclan, r/montenegro, r/mylittlepony, r/OrderOfTheKoi, r/redhotchilipeppers, r/spain and r/ssbpm.
- **Decisions and news carried between the chat and the thread, or to members outside the chat: 11 members.** r/theexpanse: "Returning decisions to accessible threads lets people without chat access follow design and alliance changes." r/dwarffortress: "A member also asks the public thread to carry a relocation proposal into chat, making the relay bidirectional." Also r/cavestory, r/esperanto, r/forsen, r/freedomplanet, r/hyperlightdrifter, r/ik_ihe, r/linux, r/monero and r/poland.
- **Entry to the chat controlled: 5 members.** r/stevenuniverse: "Organizers screened applicants and shared invitations privately to exclude ill-intentioned entrants and spam." r/TransFlagPlace: "Admission to the planning venue can require showing pixels already worked on, distinguishing entry screening from merely circulating an invitation." Also r/eve, r/monalisaclan and r/PurplePixels.
- **The chat named as where the plan lives: 4 members.** r/de: "An alliance coordinator must catch up on decisions, assignments and timing made while working elsewhere." r/kilian: "A takeover proposal receives a referral to chat, making access to the current plan part of how an alternative tactic is answered." Also r/metalgearsolid and r/spongebob.
- **A way kept open for those who will not or cannot enter the chat: 4 members.** r/starryknights: "Public templates permit participation without chat entry and provide a fallback when the coordinating chat is raided." Also r/darksouls, r/hyperlightdrifter and r/theexpanse.

Most members show one kind of upkeep: 31 show one and 4 show two. No member shows renewal, screening and relaying together.

P23 says members move planning into a chat, invite helpers, and bring the chat's decisions back to the thread. It treats the invitation as one act. In these rooms the invitation decayed. Links expired, on one server every thirty minutes, and members reported and replaced them again and again. Access was continuous work. P23 also names arguments over whether a chat is secure. Five rooms acted on it: they screened applicants, kept links private, divided channels by role, and banned members. Last, the chat split the room into members inside it and members outside. Some members outside followed a public template and worked anyway (r/starryknights, r/theexpanse). Others learned of the chat only after the event (r/hyperlightdrifter). P23's relay assumes someone carries decisions back; the lines show the people on both sides of it.

**What the claim rests on.** The shared key is a pattern across rooms: 35 rooms and 35 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). What members did to keep their chats usable is a claim on their words, through `cite.py`, in sections 1, 4 and 10. My sorting of the lines is a reading of the coders' sentences, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "the chat kept open: invitations renewed, entrants screened, outcomes relayed to the thread". Each clause holds for a subset: renewal in 15 members, relaying in 11, screening in 5. The strongest argument that it names the key and not the rooms: it lists three kinds of upkeep as if one room did all three, and no member's line shows all three. "Kept open" also sits badly beside screening, since five rooms narrowed the door on purpose. A reader who suspected the name would look for a room that renewed, screened and relayed; none is shown. I propose a renaming in `notes-D5.md`: "the chat's access kept up: invitations renewed, entry controlled, decisions carried back, each in different rooms".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **A dead link.** r/lakers: "It expired, can you post a new link?" [lakers/c0120].
- **A door by role.** r/PurplePixels: "Anyone can chat in #general. Those with a purple role can chat in #lounge." [PurplePixels/c0173].
- **Links kept private.** r/stevenuniverse: "We have an official Discord, pm me to receive the link. We're trying to avoid public links so we don't get spammed with trolls." [stevenuniverse/c0419].
- **The thread kept for news.** r/monero: "Major updates will be posted here, but until then join us in Freenode IRC #monero-offtopic" [monero/c0092].
- **The plan held in the chat.** r/metalgearsolid: "Cheers mate. You can chip in on the subreddit name if that works for you. Template is in the discord." [metalgearsolid/c0126].
- **Working without the chat.** r/theexpanse: "Can't get on Discord but I am working on the lettering." [theexpanse/c0104].
- **The chat raided.** r/starryknights: "Our Discord is currently being raided by the VOID. So just follow this template if you want to help. Thanks!" [starryknights/c0074].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 35 members, 13 compose, 22 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 35 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (35 rooms, 35 lines), and members' words show each kind of upkeep. The explanation the branch shares is not supported as one: every member's local account is unresolved, no room was re-checked against a P23 that holds this upkeep, and the kinds of upkeep fall in different members. The element itself is a candidate entered at D3. A verdict of composes with residue on the original model is not a current local or shared failure.
