## 3. What it does differently

The branch shares one key: add-step on P01 (the call) at the third-order theme T3-002 (calling members in to place), under T4-005 (Mobilization), the coders' theme for calls for hands. T3-002 is the coders' theme for "Members call the room's own members to come and place for its work: to start, build, finish or hold a picture, calls to placers who are not yet a group included." 18 current-ledger lines carry the key, one per member. D4's sentence for the branch: "P01 says the room calls members and kindred subs to place. In these rooms answering a call is an exchange: a willing member asks what to do, where to start or for backup, and the caller supplies instructions, location cues and visibility (a sticky, other venues), reaching people beyond the room."

I read the 18 `how` sentences with the codes each cites, and sorted each member into one of four groups (`out/_analysis/d5a35_F35_reading.json`, counted by `out/_analysis/d5_facets.py`). This is my reading, not a key.

- **A willing answer asks for the task, the place or the means: 5 members.** r/stargate: "Accepting participation can simultaneously request the coordinates or backup needed to make the commitment workable." r/polyamory: "An interested answer can return the next action to the caller by asking what to do, distinguishing expressed interest from commitment to a specified task." Also r/FlaggyFlag, r/mamamoo and r/seahawks.
- **A joining answer reports a part, explains itself or renews the call: 5 members.** r/starbound: "A participant reports doing their part and immediately recruits additional helpers so joining can renew the call". r/homestuck: "Joining shared work can include explaining earlier solo labor and identifying remaining needs rather than giving a bare acceptance". Also r/borussiadortmund, r/lebanon and r/TheHulk.
- **The caller widens or orients the call: 5 members.** r/littlewitchacademia: "Moderators increased a recruitment call's visibility by stickying it." r/raocow: "Recruitment reaches regular video readers by appending an invitation inside established posting formats." Also r/GuildWars2, r/hatsune and r/tenma.
- **The call redirected, divided or refused: 3 members.** r/wow: "Calls can receive bare refusals or disinterest rather than acceptance or a reason grounded in neighbour protection." r/purdue: "Calls for hands include an explicit division between adding and defense and a later proposal to assign guards to scripted areas." Also r/clashroyale.

The model says a call is answered in one line that asks for nothing back (P15), and that this bare answer follows the call in the same thread (A12). In these rooms the answer often asked for something: a starting place, coordinates, what to do. Or it reported a part done and called others in. A room of this branch does what the model would not predict: its willing members wait for a task, and its callers have to supply one. Where a call says only "come and place", the record shows members who wanted to help and did not know how.

Of the population's 48 add-step lines on P01, in 46 rooms, 18 lift to T3-002 and form this branch; the rest lift to other third-order themes (`out/_analysis/d5a35_checks.py`). One member, r/borussiadortmund, holds a second add-step line on P01 at another theme.

**What the claim rests on.** The shared key is a pattern across rooms: 18 rooms and 18 lines in the ledger, cut at D4 on keys alone. D4's comparison of rooms by composition did not survive a change of distance and sorted rooms by size, so the cut stands on the key. The kind of an add-step line is not used (J: kappa 0.08). That members asked for tasks, reported parts and widened calls is a claim on their words, through `cite.py`, in sections 1, 4 and 10; I read every key line's cited codes. My sorting of the lines into groups is a reading of the coders' sentences and the cited words, not a count the ledger makes.

**Stage D4's name, read against the members.** The name is "the call made workable: answers ask for a task, and callers supply it". "Answers ask for a task" holds for 5 members. "Callers supply it" holds, as visibility or a location cue, for 5 others, and as an instruction in r/FlaggyFlag and r/clashroyale. Five members' lines concern joiners who report and renew the call, and three concern calls redirected, divided or refused. The strongest argument that the name names the key and not the rooms: it restates D4's sentence, which joins two halves of an exchange that the record shows together in only two members. A reader who suspected so would look for a member whose question was answered with a task, and would find it in r/FlaggyFlag and r/clashroyale; elsewhere the question stands unanswered in the cited words, or the line concerns another part of calling. I propose a renaming in `notes-D5.md`: "the call answered beyond a bare yes: questions for a task, reports that renew the call, and calls made visible".

## 4. The concepts it employs

The branch has one shared key. First-order concepts for it, through `cite.py`:

- **Where is it?** r/mamamoo, to a call to protect a small corner: "where is that exactly though? its so tiny :(" [mamamoo/c0003].
- **A plan, please.** r/GuildWars2, answering a proposed logo: "Sure." [GuildWars2/c0079], and, in the same comment, "Can someone draw up a plan in paint or something?" [GuildWars2/c0080].
- **Asking other places for hands.** r/GuildWars2: "I've asked for some help on some discord servers I know, we'll need a lot of people for this !!" [GuildWars2/c0115].
- **An official campaign.** r/hatsune, a post title: "Official /r/hatsune /r/place campaign" [hatsune/c0038]. Under an earlier post: "If this isn't added already, please go ahead and add it." [hatsune/c0037].
- **Spare time on offer.** r/lebanon: "Drop me a DM if u need to lay down more pixels. I'm unemployed and got time on my hands." [lebanon/c0104].
- **The group found late.** r/lebanon: "I spent two hours yesterday trying to get a flag and you guys do it without me noticing" [lebanon/c0105].
- **Adding and defending, divided.** r/purdue: "I'm playing defense.. you guys keep adding" [purdue/c0061].
- **A welcome for the joiner.** r/TheHulk: "Imma join you guys cuz i like the hulk" [TheHulk/c0004]; the answer: "Welcome Hulkster!" [TheHulk/c0005].
- **Redirected to the current work.** r/clashroyale, to a new proposal: "We are already making a princess" [clashroyale/c0117]. Later: "either finish the princess first or organize it yourself" [clashroyale/c0347].
- **How do you do it?** r/clashroyale, to a call to make a wizard: "How do you do it?" [clashroyale/c0224]. The answer: "Go to r/place and place the pixels where you want them" [clashroyale/c0225].
- **Bringing the small corner forward.** r/mamamoo: "i was just about to post about maybe putting some mamamoo on r/place haha, lets make it big!!" [mamamoo/c0002].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement: of 18 members, 8 compose, 10 compose with residue, 0 do not compose and 0 cannot tell. These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 18 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

@@UNRESOLVED@@

**The shared branch explanation: unresolved.** The key is supported as a pattern (18 rooms, 18 lines), and members' words show answers that ask for a task, answers that renew the call, and calls made visible. The explanation the branch shares is not supported as one. Every member's local account is unresolved. No room was re-checked against a P01 that holds the step. And the exchange D4 names, a question answered with a task, is shown in two members' words (r/FlaggyFlag, r/clashroyale). A verdict of composes with residue on the original model is not a current local or shared failure.
