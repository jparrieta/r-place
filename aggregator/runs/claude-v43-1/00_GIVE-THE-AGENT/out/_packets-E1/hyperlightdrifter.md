# Reconstruction packet

Score, claim by claim of the coder's account below, whether the skeleton accounts for it, with the element id or `none`, one line per claim in the form the return specification gives. State unresolved evidence or stale versions in each affected claim reason. Pending or rejected lines are not asserted support; silence is not negative evidence. Report unresolved claim counts separately from contradiction. Reproduce the skeleton current model version and local status in the summary.

## The skeleton (the global model with supported local adaptations and explicit uncertainty)

# r/hyperlightdrifter rebuilt from the global model (46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525) plus 67 adjudicated re-check lines

Adapted-local status: unresolved; grade: composes-with-residue; version status: current.
Return model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525; current model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525.
Unresolved adaptations: 0 (not asserted support).

[P01] The room calls its own members, and kindred subs, to come and place for a work: to start it, build it, finish it or hold it.  (['D01']; applies here: yes)
   instantiate   t01              Members invite help completing the figure and showing their pixel art on the canvas.  [c0001,c0009]

[P02] The room settles what its mark will show of it: a member proposes a picture, the room argues its design, makes its land's flag or emblems the mark, signs it or leaves it unsigned, claims a mark others made, adds to it or enlarges it, or adds a personal piece to a shared mark.  (['D02']; applies here: yes)
   instantiate   t07              Members debate whether the available pink matches the game or orange better preserves its recognizable promotional appearance.  [c0033,c0042,c0044,c0046]

[P03] The room builds its mark, and members report its state to the thread: what is placed, done or missing, and where.  (['D02']; applies here: yes)
   instantiate   t01              Contributors report starting a figure and finishing its face and eyes.  [c0007,c0008]
   add-step      t01              Contributors merge duplicate starts by explicitly choosing to help an image that is further along or already beside them.  [c0011,c0014]
   link          t04              Seeking and announcing approval occur during construction before the figure is declared complete.  [c0015,c0021,c0031]

[P04] Members circulate a template that lays out the mark pixel by pixel, or coordinates that locate it, ask for them, and ask strays to keep to them.  (['D02']; applies here: yes)
   instantiate   t03              A grid makes the picture usable by helpers unfamiliar with pixel art.  [c0016]
   add-step      t03              An alliance guide standardizes help across neighboring pictures by identifying accepted details that helpers might otherwise change.  [c0051,c0052]

[P05] The room keeps its placed work against erosion: members watch it and repair changed pixels, and the room rallies to defend it under attack, covers the night, hardens its shape and puts upkeep before growth. Repair restores the form the keepers know. A change the room has planned or agreed (P02) is therefore repaired away as damage until its keepers are told of it, and it is lost or given up where the telling does not reach them.  (['D03']; applies here: contested)
   instantiate   t06              Completion redirects effort toward keeping the figure alive, locating it, and repairing recurring random pixels.  [c0031,c0036,c0039,c0040]
   restrict      t07              Known proposals can be opposed for fidelity and competing effort, so informed disagreement must be distinguished from uninformed repair before explaining why a change fails.  [c0041,c0042,c0045,c0046]

[P06] Members work out who changed their work and why: they trace placers and rooms, find friendly fire or their own mistake, blame officers, or disown placers acting in their name.  (['D03']; applies here: yes)
   instantiate   t07              Recoloring participants identify themselves and clarify that their changes are friendly rather than destructive.  [c0041]

[P07] Rooms spare their neighbours' work, rein in their own attackers, apologise for damage and appeal to attackers to stop.  (['D04']; applies here: yes)
   instantiate   t06              Participants explicitly omit the figure's legs so the logo below can remain.  [c0031]

[P08] Rooms propose, settle and contest borders, truces and deals with neighbours by talk, through envoys, and hold each other to them.  (['D04']; applies here: yes)
   instantiate   t04              Participants seek approval and negotiate whether the figure can extend into a neighboring logo.  [c0015,c0021,c0022,c0023,c0025]
   add-condition t04              Negotiation takes place under unequal capacity to defend claimed space, which members can challenge while accepting cooperation.  [c0020,c0073,c0074]

[P09] Rooms attack others' work by the recurring moves the canvas affords: erasing, encroaching, converting a sign, raiding on a streamer's call, planting a script, altering a work as a joke.  (['D08']; applies here: unobserved)
   absent                         A takeover question and defensive-force alternative do not establish an adopted attack against a rival.  [c0017,c0026,c0031]

[P10] After the work is erased or overrun, the room weighs fighting for the spot against moving, and moves: a new spot, a smaller version, a fresh start.  (['D04']; applies here: unobserved)
   absent                         The recorded coordinate change does not establish an erased work or rebuilding after a loss.  [c0053,c0054,c0055,c0056]

[P11] When a work is up, the room marks it: announces it, celebrates it, credits makers and helpers, reports members' own parts and says what working with strangers meant.  (['D07']; applies here: yes)
   instantiate   t09              Members celebrate intact survival, thank supporters, and express pride in the small community's achievement.  [c0059,c0060,c0061,c0063,c0068,c0070,c0071]

[P12] The room records what happened to its work and to the canvas around it: screenshots and timelapses, reports of its fate, mourning, imagined art, atlas entries, the end marked.  (['D07']; applies here: yes)
   instantiate   t08              A participant records chat growth, completion, and the addition of a companion in a retrospective account.  [c0062]

[P13] Near the close and after it, the room decides what of its temporary effort to keep: a later canvas, a new purpose for its canvas sub, the mark in its banner, ties with other rooms, the work remade elsewhere.  (['D07']; applies here: unobserved)
   absent                         Celebrating permanence in the final canvas does not establish a decision to continue collective activity or reuse the work.  [c0059,c0061]

[P14] Members add placements with scripts, bots and spare accounts, and the room argues over these machine hands and adjusts them.  (['D02']; applies here: contested)
   restrict      t02              The local evidence establishes script requests, conditional account lending, and instructions, while claims of added placements require confirmation of actual execution.  [c0004,c0005,c0057,c0058]
   add-step      t02              Requesting a script and offering an account conditionally are recruitment steps distinguishable from running the supplied script.  [c0004,c0005,c0058]

[P15] A member answers a call or proposal in one line that joins, assents, reports a part done or thanks, and the line asks for nothing back.  ([]; applies here: yes)
   instantiate   t01              A portrait invitation receives a bare affirmative answer without a request in return.  [c0009,c0010]

[K01] The host sub is keyed as play for April Fools: members post fakes and takeovers under the one-day licence, and a claim in it, a call to the canvas included, may be a joke.  (['D06']; applies here: unobserved)
   absent                         The coded project invitation does not establish host-level parody or its absence elsewhere in the room.  [c0001]

[K02] The room judges that it has too few hands or too little room for the work it wants: doubt, a canvas judged too full, a work judged absent or outclassed.  (['D01']; applies here: yes)
   instantiate   t01              A participant doubts the feasibility of a contested corner and proposes another location.  [c0006]

[C01] Most rooms worked on their marks without deciding how they were organized: a decided element of order (a leader, a vote, an oath, a sanction, a division of the work) is coded in 46 of 705 rooms (F-006).  (['D02']; applies here: not-testable)
   absent                         A single room cannot test aggregate prevalence, and informal voting language cannot reveal decision rules adopted inside the unavailable chat.  [c0043,c0048,c0062]

[R01] The starter: a member who proposes the mark, maps it or begins placing it. Others joining is not part of the role: it is the answer to the room's call (P15), in the order A02 and A01 state.  (['D02']; applies here: yes)
   instantiate   t01              The first caller reports placing a first pixel while asking others to complete the picture, fitting starting without implying command.  [c0001]

[R02] The envoy: a member who acts for a room toward another room, carrying a proposal between threads or chats.  (['D04']; applies here: yes)
   instantiate   t04              A participant offers negotiation on behalf of a neighboring community without evidence of formal appointment.  [c0023]

[P16] Rooms help one another's works and trade help: they give pixels to a neighbour's mark, ask other rooms for help, barter help for space or repair, thank their allies, greet them, and turn requests away.  (['D04']; applies here: yes)
   instantiate   t05              Neighbors offer reciprocal cleaning and the direct reply promises returned upkeep after the builders finish their own figure.  [c0027,c0032]

[P17] Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred rooms in a hub, tally kindred rooms' works and make joint marks.  (['D04']; applies here: yes)
   instantiate   t05              A documented alliance asks members whose own work is fine to protect neighbors who will return the help.  [c0050]

[P18] Rooms carry a contest with a rival room in talk: they trade taunts, flood the rival's threads, claim victory, salute the rival after the fight and blame attackers after the close.  (['D08']; applies here: unstated)

[K03] The community carries a quarrel from before the canvas into it: a rival sub, a sports or national rivalry, an old dispute.  (['D05']; applies here: unobserved)
   absent                         The dispute over current spatial power does not establish an inherited rivalry.  [c0073,c0074]

[P20] The host sub draws a line around canvas talk: moderators gather it into a megathread, remove canvas posts by rule, change posting rules, pause the sub's usual events or disown the work; members open a canvas sub, object to the flood or argue the canvas's worth.  (['D06']; applies here: unobserved)
   absent                         A chat-planning invitation does not establish a megathread, posting restriction, or objection to a canvas flood.  [c0043]

[K04] The room acts as a body it was before the canvas, or as a faith in a colour: it argues the nation's history, belonging and politics beyond its flag, carries in the sub's quarrel, lore, jokes or ideology, or professes and spreads a colour.  (['D05']; applies here: unobserved)
   absent                         Arguments over game colors do not by themselves establish inherited lore in canvas conduct, running jokes, ideology, or devotion to a color faction.  [c0044,c0046]

[P19] One room's work lives on another room's mark or territory under the host's rule: guests ask for space or protection, hosts rule on requests, and both sides dispute who may approve.  (['D04']; applies here: yes)
   instantiate   t04              Official approval within defended space and a challenge to the larger group's authority instantiate the standing host-rule relation.  [c0021,c0025,c0073,c0074]

[C02] In some rooms, a tie the room had before the canvas (a league or school rivalry, a nation's history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack.  (['D08', 'D05']; applies here: not-testable)
   absent                         No coded attack names an inherited rival to test the tie-to-attack mechanism.  [c0026,c0031]

[P21] Members dispute, or state the limits of, who may commit the room to an agreement with other rooms: they say that one member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another group for a leader to deal with.  (['D04']; applies here: unobserved)
   absent                         Disputing a larger group's territorial authority does not establish limits on who can bind one's own placers to an agreement.  [c0021,c0073,c0074]

[P22] After placement ends, members contest which version of the canvas and of the event is kept: they ask a cleanup of a shared copy to fix their work, take part in it, argue that the cleanup should keep the damage as history, and correct accounts of the event that describe their group wrongly.  (['D07']; applies here: unobserved)
   absent                         A live color dispute and later intact-finish celebration do not establish contest over a post-event retained version or historical account.  [c0033,c0041,c0060,c0071]

[P23] Members move the room's planning into a chat, an existing server or a new one, and invite helpers to it. They bring the chat's designs, decisions and warnings back to the thread. They argue which chat to use, whether a chat is needed or secure, whether it is official, and whether it may decide for the work or bind placers.  (['D02']; applies here: yes)
   instantiate   t08              The candidate now covers invitations to plan in chat and retrospective reports of its membership, completion, and additions.  [c0043,c0062]
   add-step      t08              Planning develops with uneven awareness, and later invitations to read chat history reconnect participants while others contribute without entering it.  [c0047,c0048,c0049,c0069]

[P24] Members ask what the canvas is, how to place, what a call or a name means and what a picture shows, and others explain the rule, the timer, the controls, whose mark a picture is and what happened. They ask before, during and after the close, and some questions get no answer.  (['D01']; applies here: yes)
   instantiate   t06              The candidate applies narrowly when a late arrival asks how to help and receives an explanation of the completed figure's defense needs.  [c0035,c0036]

[P25] The room's work brings people into the room. A viewer finds the sub through the mark or through a sign written to that end, a member of an ally comes through joint work, and a lapsed member returns. Members welcome them, explain the room's subject, take them into its usual activity, count the new subscribers and argue how to receive them.  (['D07']; applies here: unstated)

[P26] Members make new jokes out of the canvas work, its mistakes, its damage and its neighbours: puns on the mark, mock names and titles for a figure, and jokes about attackers and bots. The room takes the jokes up, and some members want a joke kept in the work.  (['D05']; applies here: unobserved)
   absent                         Calling the figure the Hero or Drifter does not establish a new joke taken up by the room.  [c0031,c0059]

[P27] Before any loss, the room chooses where to put its work and changes the spot while it builds. It looks for open room, weighs a crowded or contested place, shrinks or moves the design ahead of a neighbour or the void, restarts a misplaced start, and refuses to move once enough pixels are in.  (['D04']; applies here: yes)
   instantiate   t01              The candidate also covers proposing another location because the original corner looks difficult to use.  [c0006]

[P28] A room forms for the canvas around a mark. Members open a sub or a chat for a pattern or a figure and set it up. They invite the people seen building or copying the mark, give it a meaning its followers share, gather its repeaters into a group that can negotiate, and move or split the room.  (['D05', 'D06']; applies here: unobserved)
   absent                         Chat planning within the fandom effort does not demonstrate a new room forming around a copied pattern or mark.  [c0043,c0062]

[P29] Members argue whether a joke, a taunt or a word in canvas talk offends, and they refuse slurs and hate symbols. They object, correct, apologise, remove the words or tell the speaker to leave, and they cover swastikas or refuse to draw them.  (['D05']; applies here: unobserved)
   absent                         Challenging a larger group's authority does not establish correction of offensive jokes, slurs, or hate symbols.  [c0074]

[P30] The room turns its work toward people outside the canvas whom the mark shows or addresses: the creators, the team, the streamer, a company or the press. It shows them the work, hopes for their notice, shares the coverage and celebrates their acknowledgement, or it keeps the work from troubling them.  (['D07']; applies here: unobserved)
   absent                         Recognizable promotional colors and closing celebration do not establish outreach to creators, companies, or the press.  [c0046,c0071]

[P31] Members argue whether covering others' work is fair. Some call it betrayal, dirty or a cost to the room's name. Others answer that change is the canvas's point, that wiping makes room for new art, or that the canvas is a game of conquest. The argument runs during the work and after the close.  (['D04']; applies here: unobserved)
   absent                         Asking about takeover and proposing joining forces do not establish a broader argument about whether covering others is fair.  [c0017,c0018]

[P32] A member steps away from the work under strain, or the room repairs a quarrel between members. The work turns stressful or personal, or a member is criticised or yelled at over a pixel or a proposal. Others rebuke the harsh speaker, the speaker apologises, or the member threatens to leave or leaves.  (['D01']; applies here: unobserved)
   absent                         Conditional concession over available effort does not establish withdrawal under stress or a repaired personal quarrel.  [c0045]

[P33] Rooms keep their plans from rivals who read their threads, and they reach into rivals' venues. Members switch to their own language or write in code, move the plan to private messages, plant members in a rival's chat and warn of a snitch in their own.  (['D02', 'D08']; applies here: unobserved)
   absent                         A public chat invitation and retrospective reading invitation do not establish secrecy, infiltration, or hidden plans.  [c0043,c0048]

[P34] Members who object to the canvas posts in the sub turn against the room's own mark. One member says the posts make them tear down the logo, and one recruits trolls to ruin the flag.  (['D06']; applies here: unobserved)
   absent                         Explaining that recoloring is friendly does not establish attacking one's own mark because of disliked canvas posts.  [c0041]

[K05] Members place on their own time and with their own devices. They fit placing around sleep, study, exams, work and travel. They cannot place from a phone or while away, they leave when the wait is too long, they save pixels under the timer, they find the work addictive, and they report what it cost them.  (['D02', 'D07']; applies here: yes)
   instantiate   t09              Participants recount time spent struggling and work continuing across sleep, showing personal time costs without measuring total collective labor.  [c0066,c0062]

[K06] The site sets what members can do, and members report its faults and pass on fixes. They report a blank or stale canvas, the site down, a vanished or faulty timer, glitches that seem to give extra pixels, captchas, the official app required and the site blocked in a country. They refresh, update, keep a separate window and test whether extra pixels reach the canvas.  (['D02']; applies here: unobserved)
   absent                         Routine refresh instructions do not establish a site fault, stale canvas, or a tested platform workaround.  [c0058]

[K07] Some members belong to both rooms in a contest or at a border. They say they are torn or proud of both, and the room reassures them or still counts them as its own.  (['D04']; applies here: yes)
   instantiate   t05              A participant identifies with both neighboring fandoms and receives reciprocal appreciation, showing shared attachment without divided loyalty.  [c0065,c0067]

arrows in the model: 21

[A01] P01 -> P03 (order): The room's call brings members to the canvas, who then build the mark and say how far it has come.

[A02] R01 -> P01 (order): A member who proposes or begins a mark gives the room something to answer, and calls for hands gather around it.
   instantiate   t01              Reporting a first pixel and asking for hands are combined in one turn rather than demonstrated as separate temporal phases.  [c0001]

[A03] P03 -> P05 (order): Once a mark stands on a surface anyone can change, keeping it becomes the work: a finished part is something to lose.
   instantiate   t06              The completion announcement explicitly makes keeping the figure alive the next task.  [c0031,c0036]

[A04] P05 -> P08 (order): Keeping a mark against erosion brings the room up against the neighbours whose pixels erode it, and the room turns to talk with them.
   restrict      t04              Negotiation begins during construction before reported maintenance, so upkeep cannot supply the exclusive initiating stage.  [c0015,c0021,c0029,c0031]

[A05] P08 -> P07 (order): A settled border gives the room a line to keep: members spare the neighbour's work by it and remind others of it.
   absent                         An offer to negotiate and subsequent restraint do not demonstrate a settled bilateral treaty causing that restraint.  [c0023,c0024,c0031]

[A06] P05 -> P14 (order): Upkeep under attack outruns what one pixel per interval can hold, and members turn to scripts and spare accounts to keep up.
   restrict      t02              Early script requests precede reported upkeep, while later instructions leave actual execution and its supposed cause in maintenance strain unresolved.  [c0004,c0005,c0029,c0058]

[A07] P03 -> P11 (order): A mark reported done gives the room a finished thing to point at, and the room marks it together: announcement, credit, pride.

[A08] P11 -> P12 (order): Marking the work together turns the room toward keeping it: members ask for the final image, the timelapse, the list of what changed.
   restrict      t09              Fate-reporting and celebration occur together in the closing account, so a directional causal explanation requires evidence beyond their co-occurrence.  [c0059,c0061,c0062]

[A09] P12 -> P13 (order): A record of the work gives the room something to carry: the image into the banner, the plan into the next canvas.
   absent                         The final-canvas record does not reveal whether recording generated a plan for future collective activity.  [c0059,c0061]

[A10] K02 -> P10 (order): A room that judges it has too few hands to hold its spot stops fighting for it and moves.
   absent                         The Guardian move has no coded shortage explanation or preceding loss, and a different build's location concerns cannot supply one.  [c0006,c0053,c0054,c0056]

[A11] P02 -> P04 (transition): Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel.
   restrict      t07              The grid predates the later color disagreement, whose recorded accommodation concerns competing effort rather than settlement through an agreed template.  [c0016,c0044,c0045,c0046]

[A12] P01 -> P15 (transition): A call is the first part of a pair: posted to a thread, it makes an answer from each reader the next thing due, given in the thread or by placing. Joining is the answer the call prefers, so it comes bare, one line that commits and gives no reason ('I'm in'); declining is the dispreferred answer and, in conversation analysis, comes with a reason. In the written record a bare join is the ordinary way a call is accepted (25 of 31 read acceptances, F-023); a member can also accept by placing and write nothing, which the record cannot show.
   instantiate   t01              A bare affirmative answer directly follows the portrait invitation without demonstrating anything about silent readers.  [c0009,c0010]

[A13] P05 -> P16 (order): A room keeping its work under strain runs short of hands and turns to other rooms for help, and other rooms send it.
   restrict      t05              The directly stated condition for reciprocal upkeep is having one's own work finished or fine, rather than a demonstrated shortage causing solicitation.  [c0027,c0032,c0050]

[A14] P08 -> P16 (order): Talk over a border opens a channel through which the two rooms then trade help: room for upkeep, pixels for protection.

[A15] P01 -> P09 (order): A call brings members to the canvas, and some of them turn its hands against a rival's work instead of, or before, building the room's own.
   absent                         The build call and takeover question do not establish recruited hands turning into an adopted attack.  [c0001,c0017,c0031]

[A16] P09 -> P07 (order): A call to attack makes an answer from the room due in its thread. Members who do not want the attack refuse it, rein in the attackers or apologise to the target; refusing is the dispreferred answer, so in written replies it usually comes with a reason (23 of 38 read pairs, F-014), and the reason states the room's norm or the attack's cost ('Nah, keep /r/place neutral.'; 'Why? That'll just cause them to want to attack us').
   absent                         The explicit instruction to spare the lower logo has no coded attack call established as its trigger.  [c0031]

[A17] P09 -> P08 (order): A call to attack is met by the room's relations with its neighbours: the room invokes a truce, or proposes a deal instead.
   absent                         Negotiation and defensive alternatives do not establish an attack call as the cause of border talk.  [c0015,c0026]

[A18] P09 -> P18 (order): An attack makes the rival a named party, and the contest is carried on in talk: taunts, chants, claims of victory, a salute after the fight.
   absent                         The authority argument lacks a coded attack that could establish the proposed attack-to-rivalry mechanism.  [c0026,c0074]

[A19] P05 -> P17 (order): A room keeping its work against attack joins other rooms whose works face the same threat, and they defend each other's works together.

[A20] P01 -> P20 (order): Calls to the canvas flood the host sub, and its moderators or members answer by drawing a line around canvas talk: one thread, removals, a canvas sub.
   absent                         The build call and chat invitation do not establish a flood causing host restrictions.  [c0001,c0043]

[A21] P08 -> P21 (order): An agreement made with another room in the room's name puts its members' compliance in question. Members who did not make it say that it does not bind them, or refuse it, or say that no one can bind every placer.
   absent                         Approval and a spatial-authority challenge do not demonstrate an agreement causing a commitment disclaimer or refusal under the revised bound.  [c0021,c0074]

## The coder's account

## Chronology

The room's r/place work first appears at H24.55, `d1 04-01 16:33`, after an ordinary first day dominated by the game's anniversary and physical edition. The opening episode runs from `62trzb` to `dfpyljv`: one participant says they have “placed the first pixel” and asks others to “leave our mark,” while replies ask where to help, request a script, propose safer coordinates, and report completing a face and eyes. A second invitation at H35.16, `62xgfy`, asks whether members want to show r/place “some real pixel art.” These are parallel attempts, not evidence that one caused the other.

At H44.34 the main construction episode begins at `62zcq4` and extends through the defense report at `dfrwrm3`. Participants abandon duplicate starts to help the further-along image (`dfq9h4b`), supply a grid (`dfqlpib`), add a frame (`dfqmltj`), and propose the floating partner (`dfqpfp4`). They also work out boundaries. An early warning says GreenLattice “might try fighting back” (`dfq9vfa`), but a later edited comment says “We're allied now” and calls them “super diplomatic” (`dfqq4ug`); another announces official approval (`dfqq8ff`). With the logo below, participants discuss negotiation (`dfqrizh`, `dfqrw69`) and accept omitting the legs (`dfqs09r`). At `dfqvww8` they say “We've done it,” leave the neighboring logo in place, and turn to keeping the figure alive.

The maintenance and design episode runs from `632zh0` to `dfsopwb`. The post says “now we just need to maintain it” (`632zh0`); a brief fear that it is gone (`dfqwxnv`) is answered four minutes and forty-two seconds later with “still going strong” and a call to fight griefing (`dfqx5p1`). Participants then dispute orange versus pink. One side says pink is closer to the in-game color (`dfqxwoh`); the other says orange is more recognizable from the promo art (`dfqy074`). The pro-pink participant says they may concede if effort is better spent elsewhere (`dfqxyjl`). This is a descriptive disagreement and accommodation, not a community-wide change of mind.

During the same stretch, participants formalize help beyond the image. At H55.89, `633704` records an alliance in which neighbors keep one another's art clean and publishes a guide intended to prevent helpers making things worse. A separate Guardian attempt from `dfr3v07` to `dfrb4kd` changes coordinates twice and meets requests to move because another group is already building there. At H60.38, `634kbf` recruits “every helping hand” to paste and refresh a Guardian script. These episodes follow the main Drifter's completion; the text does not establish that completion caused either effort.

After placement closes, the final episode runs from `63847u` to `dft5ga7`. At `d3 04-03 17:08`, the first post thanks helpers for creating a Hero that will remain in the final canvas (`63847u`). Replies call it unblemished (`dfrzw32`) and immortalized (`dfs1zx2`). One participant recounts two people joining Discord, the figure being completed, the Discord growing to roughly ten, and the floating buddy being added (`dfs36e1`). The recounting is the participant's own explanation of how the work developed, not an independently observed causal test. A second post ten minutes later says the Drifter “survived and ended fully intact” (`63870m`), and a later reply simply says it “Looks awesome” (`dft5ga7`).

## Relations — what set off what

Several reply pairs support local relations because the later words answer the earlier ones. A claim that the work might already be gone (`dfqwxnv`) receives “Nope, still going strong” and a maintenance instruction (`dfqx5p1`) after 4 minutes 42 seconds. A proposal to recolor orange as pink (`dfqxnqj`) receives an argument to keep orange because it is closer and already present (`dfqxt98`) after 3 minutes 24 seconds; replies then supply competing image-based reasons (`dfqxwoh`, `dfqy074`). These are supported answer relations, not inferences from adjacency alone.

The GreenLattice sequence also contains an explicit development. The earlier comment anticipates fighting (`dfq9vfa`); the same participant later edits their stance to “We're allied now” after calling the other group diplomatic (`dfqq4ug`). Official approval is separately reported at `dfqq8ff`, and the Google doc is named as proof at `dfqsomq`. The participant's edited words support a change in that speaker's account from anticipated conflict to alliance. They do not establish that the whole community changed its mind.

Reciprocal help is stated rather than inferred. OnePiece offers to keep the Drifter clean if its own picture is fine (`dfqtgix`), and a later reply says, “We've finished ours now, so we'll help you maintain yours as well” (`dfqvxqo`). The alliance guide likewise tells members to help neighbors because “they will do the same” (`633704`).

Discord is linked to development by participants' own reports. Reddit invites members to “Join the Discord server so we can plan” (`dfqxv4k`); later, a participant says two more people joined it “and we got him done,” then found about ten people and a floating buddy the next day (`dfs36e1`). That supports their explanation of an observed sequence and credited contribution. Because the Discord itself is absent, it does not support a stronger causal claim about which decisions produced the final image.

Other episodes only follow one another. The portrait invitation at H35.16 (`62xgfy`) follows the first build call at H24.55 (`62trzb`), and the alliance guide at H55.89 (`633704`) follows the main construction post at H44.34 (`62zcq4`). The corpus contains no passage saying either later post was prompted by the earlier one.

## Posts against comments

Posts present concise calls and outcomes; comments reveal the contested work underneath them. “HELP! place” (`62zcq4`) provides coordinates and an image, while comments contain duplicate starts, design aids, approval claims, boundary negotiation, mutual help, and defense. The layers are complementary, but the post alone would make the effort look much simpler than the comment layer does.

The maintenance post says “Great job everyone, now we just need to maintain it!” (`632zh0`), while one comment says “I think it's already gone” (`dfqwxnv`). The comment layer immediately disputes that claim with “still going strong” (`dfqx5p1`). This is a momentary contradiction inside the comments, not evidence that the post's maintenance framing failed.

The Guardian material shows a sharper contrast. One post recruits help for a script (`634kbf`), whereas comments on the separate Guardian location thread report that Minnesota Wild is already building there (`dfr6usy`) and ask the builders to move (`dfrb4kd`). The post layer frames expansion as available work; the comment layer shows that available space was socially claimed.

The closing posts say the Hero will remain in the final canvas (`63847u`) and the Drifter ended intact (`63870m`). Their comments reinforce rather than contradict those claims: “without a single blemish” (`dfrzw32`), “immortalized” (`dfs1zx2`), and “standing intact” (`dft8ton`).

## Counter-reading

My reading is that this small community converged scattered starts into a shared Drifter, kept it through negotiation and reciprocal help as well as defense, moved some planning to Discord, and then celebrated an intact finish.

If that reading were wrong, the corpus would instead contain sustained calls to attack or take over neighbors, unresolved rival builds, or end-of-event reports that the shared image had been lost or abandoned.

I searched the case vocabulary for attack, destruction, taking over, sheer force, fighting, griefing, larger groups, manpower, moderation of space, and moving elsewhere, then read every returned item. The strongest contrary item is `dfqs5k7`: “Because we have the manpower to defend it :/,” a direct justification of control by force. The reply `dfqsf0e` challenges that logic as “because we said so and we're bigger?” This changes the account by making power asymmetry explicit: cooperation was not free of coercion, and “negotiation” sometimes occurred where a larger group could defend its claim. The main reading survives because the same record also contains an edited alliance report (`dfqq4ug`), approval (`dfqq8ff`), reciprocal maintenance (`dfqvxqo`), and intact closing accounts (`63847u`, `63870m`).

The search also found “sheer force” as one of two options (`dfqtdr2`), an initial fear that the image was gone (`dfqwxnv`), and requests to relocate a Guardian (`dfr6usy`). None became a sustained attack program or final loss. The two apparent “attack” hits outside retained threads concerned gameplay attacks (`dfnc28m`, `dfnk2qi`), so they do not bear on the competing account. Within the 170 in-window items and the searched vocabulary, I found no report that the final Drifter was abandoned or destroyed. That null result is limited by the partial record and by organizing that moved to Discord.

## Saturation

The practice account did not saturate early. The main construction thread supplied joining, design, negotiation, and maintenance; later threads added a formal multi-neighbor guide, a contested Guardian relocation, scripted assistance, Discord retrospection, and post-event credit. Later material therefore introduced new practice as well as repeating settled maintenance and alliance work.

The record is not complete enough to treat silence as absence. Planning moved to Discord (`dfqxv4k`, `dfs36e1`), approval was checked through a Google doc (`dfqsomq`), and the Guardian automation depended on a Pastebin script (`634kbf`). Reddit carries reports back from those venues but not their decisions or full contents. The header also reports that only 93 of 96 in-record reply parents are present and five bodies are deleted or removed. The event threads themselves were read whole, and no retained thread was truncated by triage, but off-platform movement and missing bodies limit claims about how decisions were made.

## Selection

I read `openings.md` before triage to locate the event within the room's week. I then followed the corpus in order, reading 30 threads in full and triaging two long, plainly non-event threads from their windows. Nine threads were retained because they recruited, coordinated, negotiated, maintained, automated, or recounted the community's r/place work. Threads about ordinary gameplay, merchandise, fan art, and videos were excluded. Every retained thread was read in full before coding.

## Other communities named

GreenLattice appears first as a possible opponent (`dfq9vfa`), then as an approving and allied neighbor (`dfqq4ug`, `dfqq8ff`) credited for “diplomacy and cooperation” after the event (`dfs36e1`). Gamindustri offers negotiation over the lower logo (`dfqrw69`), and the Drifter group accepts leaving off the legs (`dfqs09r`). OnePiece offers reciprocal cleaning (`dfqtgix`) and later describes pleasure at having the art beside its flag (`dfsewoi`). The alliance guide also names Naruto and Funhaus alongside OnePiece and Gamindustri (`633704`). Furry appears through one participant's report that they had been defending its art (`dfqugt8`). Wildhockey appears as a group asking the separate Guardian attempt to move (`dfrb4kd`). These are this community's recorded relations and reports; the corpus does not provide the other groups' complete accounts.

## Absence

The retained main thread contains a deleted comment at `dfqxcd8`; nothing in its surviving neighbors permits reconstruction. The opening-only thread `5wwc7n` is also only a deleted reply to a parent outside the record and was excluded. No moderator-distinguished intervention appears in the retained event exchanges. Surviving comments still show participants themselves handling design disputes, boundaries, approval, upkeep, and thanks, but the missing bodies and three unresolved parents mean absence of further disagreement cannot be established.

## The room's second-order themes

- t01 starting and joining Drifter builds
- t02 asking for and running scripts
- t03 making the picture easier to build correctly
- t04 negotiating room and boundaries
- t05 helping neighbors keep each other's art
- t06 finishing and keeping the hero alive
- t07 arguing whether the coat should be orange or pink
- t08 moving planning to Discord and bringing the story back
- t09 thanking helpers and celebrating an intact finish

This is the end of the packet. Confirm you reached it by returning your lines and then the end marker the return specification names. END OF PACKET
