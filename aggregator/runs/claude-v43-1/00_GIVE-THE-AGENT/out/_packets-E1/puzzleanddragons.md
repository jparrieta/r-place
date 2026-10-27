# Reconstruction packet

Score, claim by claim of the coder's account below, whether the skeleton accounts for it, with the element id or `none`, one line per claim in the form the return specification gives. State unresolved evidence or stale versions in each affected claim reason. Pending or rejected lines are not asserted support; silence is not negative evidence. Report unresolved claim counts separately from contradiction. Reproduce the skeleton current model version and local status in the summary.

## The skeleton (the global model with supported local adaptations and explicit uncertainty)

# r/puzzleanddragons rebuilt from the global model (46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525) plus 75 adjudicated re-check lines

Adapted-local status: unresolved; grade: composes-with-residue; version status: current.
Return model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525; current model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525.
Unresolved adaptations: 0 (not asserted support).

[P01] The room calls its own members, and kindred subs, to come and place for a work: to start it, build it, finish it or hold it.  (['D01']; applies here: yes)
   instantiate   t01              The organizer asks for all available help building the shared mascot.  [c0001,c0003]

[P02] The room settles what its mark will show of it: a member proposes a picture, the room argues its design, makes its land's flag or emblems the mark, signs it or leaves it unsigned, claims a mark others made, adds to it or enlarges it, or adds a personal piece to a shared mark.  (['D02']; applies here: yes)
   instantiate   t08              Members debate lettering, sprite revisions, eggs, and game-specific details after announcing completed work.  [c0082,c0083,c0119,c0135,c0151,c0155]
   link          t06              A completed-territory announcement receives new design proposals, making completion a milestone that can reopen construction.  [c0130,c0131,c0133]

[P03] The room builds its mark, and members report its state to the thread: what is placed, done or missing, and where.  (['D02']; applies here: yes)
   instantiate   t01              Placement reports and later rebuilding reports expose the changing state of the picture in the thread.  [c0008,c0015,c0034,c0112]
   link          t03              New rebuild coordinates are followed by completion reports, returning organizing from relocation to shared construction.  [c0031,c0034,c0090,c0091]

[P04] Members circulate a template that lays out the mark pixel by pixel, or coordinates that locate it, ask for them, and ask strays to keep to them.  (['D02']; applies here: yes)
   instantiate   t01              Helpers circulate maps, revised sprites, corner counts, and coordinates for their shared target.  [c0002,c0009,c0033,c0139,c0140]
   add-step      t03              A helper requests replacement of the organizing post's reference image and the organizer acknowledges completing the update.  [c0022,c0023]

[P05] The room keeps its placed work against erosion: members watch it and repair changed pixels, and the room rallies to defend it under attack, covers the night, hardens its shape and puts upkeep before growth. Repair restores the form the keepers know. A change the room has planned or agreed (P02) is therefore repaired away as damage until its keepers are told of it, and it is lost or given up where the telling does not reach them.  (['D03']; applies here: contested)
   instantiate   t02              Members defend completed work, correct stray colors, and seek a lost template while attempting repairs.  [c0007,c0093,c0113,c0160]
   instantiate   t08              Helpers restore the earlier background and require notice that apparent vandalism is an authorized initiative, supporting repair to a familiar form.  [c0025,c0122,c0125,c0126]
   restrict      t08              Uncertain keepers can avoid disputed repairs instead of restoring an assumed form, so missing instructions do not necessarily entail erasure or abandonment.  [c0120,c0148,c0149,c0160]
   add-step      t02              Members revise threat assessments after raising alarms, while different responses do not establish a collective decision to defend or surrender.  [c0156,c0157,c0158,c0164,c0166]

[P06] Members work out who changed their work and why: they trace placers and rooms, find friendly fire or their own mistake, blame officers, or disown placers acting in their name.  (['D03']; applies here: yes)
   instantiate   t08              The organizer directly corrects a vandalism attribution by identifying the changes as the shared initiative.  [c0121,c0122]

[P07] Rooms spare their neighbours' work, rein in their own attackers, apologise for damage and appeal to attackers to stop.  (['D04']; applies here: yes)
   instantiate   t03              Visitors report moving their overlapping logo and apologize for destructive expansion.  [c0074,c0107,c0110]
   link          t03              Visitors frame rebuilding assistance as repair for damage their side caused, alongside the separate bargain exchanging labor.  [c0107,c0108,c0110,c0185]

[P08] Rooms propose, settle and contest borders, truces and deals with neighbours by talk, through envoys, and hold each other to them.  (['D04']; applies here: yes)
   instantiate   t03              Participants report a treaty and describe negotiating space through an exchange of work.  [c0021,c0086,c0097]
   link          t02              A treaty announcement answers a defensive fight call, connecting defense with diplomacy without requiring an offensive raid.  [c0018,c0021]

[P09] Rooms attack others' work by the recurring moves the canvas affords: erasing, encroaching, converting a sign, raiding on a streamer's call, planting a script, altering a work as a joke.  (['D08']; applies here: unobserved)
   absent                         Fight calls defend an overwritten mascot without specifying an offensive raid or destruction of another room's separate work.  [c0017,c0018]

[P10] After the work is erased or overrun, the room weighs fighting for the spot against moving, and moves: a new spot, a smaller version, a fresh start.  (['D04']; applies here: yes)
   instantiate   t03              After displacement, participants publish new rebuild coordinates and report the move completed.  [c0029,c0031,c0090,c0091,c0098]
   link          t03              A visitor offers to rebuild overrun art and the organizer answers with new coordinates, joining relocation to outside repair in one exchange.  [c0030,c0031]

[P11] When a work is up, the room marks it: announces it, celebrates it, credits makers and helpers, reports members' own parts and says what working with strangers meant.  (['D07']; applies here: yes)
   instantiate   t06              Members celebrate successive completions, credit helpers, and describe pride in their own contribution.  [c0006,c0130,c0143,c0175,c0177,c0182]

[P12] The room records what happened to its work and to the canvas around it: screenshots and timelapses, reports of its fate, mourning, imagined art, atlas entries, the end marked.  (['D07']; applies here: yes)
   instantiate   t06              Members share a timelapse, preserve a threatened final image, and recount repeated rebuilding after placement ends.  [c0094,c0174,c0184,c0185]
   link          t02              A warning calls for pictures before loss and a moderator reports preserving the final image, supporting a threat-to-recording route.  [c0168,c0174]

[P13] Near the close and after it, the room decides what of its temporary effort to keep: a later canvas, a new purpose for its canvas sub, the mark in its banner, ties with other rooms, the work remade elsewhere.  (['D07']; applies here: yes)
   instantiate   t06              The canvas picture becomes the subreddit header before the live work stops being vulnerable.  [c0154,c0174]

[P14] Members add placements with scripts, bots and spare accounts, and the room argues over these machine hands and adjusts them.  (['D02']; applies here: unobserved)
   absent                         Manual timed contributions and repair reports do not decide whether scripts, bots, or spare accounts were also used.  [c0016,c0093,c0149]

[P15] A member answers a call or proposal in one line that joins, assents, reports a part done or thanks, and the line asks for nothing back.  ([]; applies here: yes)
   instantiate   t01              Members answer the call with brief reports of placing a pixel or doing their part.  [c0008,c0016]

[K01] The host sub is keyed as play for April Fools: members post fakes and takeovers under the one-day licence, and a claim in it, a call to the canvas included, may be a joke.  (['D06']; applies here: yes)
   instantiate   t05              Members invent PAD news, expose edited images, invoke the date, and warn that announcements may be pranks.  [c0042,c0045,c0047,c0052,c0190]

[K02] The room judges that it has too few hands or too little room for the work it wants: doubt, a canvas judged too full, a work judged absent or outclassed.  (['D01']; applies here: yes)
   instantiate   t02              The organizer doubts that a proposed alternative site can be completed before stronger placers overwhelm it.  [c0011,c0012,c0014]

[C01] Most rooms worked on their marks without deciding how they were organized: a decided element of order (a leader, a vote, an oath, a sanction, a division of the work) is coded in 46 of 705 rooms (F-006).  (['D02']; applies here: not-testable)
   absent                         Instructions enforcing a shared stage show local ordering but cannot test an aggregate frequency or reveal how authority was selected.  [c0123,c0124,c0125]

[R01] The starter: a member who proposes the mark, maps it or begins placing it. Others joining is not part of the role: it is the answer to the room's call (P15), in the order A02 and A01 state.  (['D02']; applies here: yes)
   instantiate   t01              The proposer supplies a mascot and map, while subsequent joining is separately evidenced in members' placement reports.  [c0001,c0002,c0008,c0016]

[R02] The envoy: a member who acts for a room toward another room, carrying a proposal between threads or chats.  (['D04']; applies here: yes)
   instantiate   t04              A neighbouring member carries a joint-defense appeal into the room and accepts directions to its painters.  [c0132,c0136,c0137]

[P16] Rooms help one another's works and trade help: they give pixels to a neighbour's mark, ask other rooms for help, barter help for space or repair, thank their allies, greet them, and turn requests away.  (['D04']; applies here: yes)
   instantiate   t03              Members trade logo movement for help finishing the mascot and later promise repairs to both pictures.  [c0024,c0086,c0087,c0109]
   instantiate   t04              Neighbours request joint defense, report a help post, and receive directions to available painters.  [c0037,c0132,c0136,c0169]

[P17] Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred rooms in a hub, tally kindred rooms' works and make joint marks.  (['D04']; applies here: unobserved)
   absent                         Joint-defense appeals and a chat referral do not establish that a coalition formed or defended together.  [c0037,c0132,c0136,c0137]

[P18] Rooms carry a contest with a rival room in talk: they trade taunts, flood the rival's threads, claim victory, salute the rival after the fight and blame attackers after the close.  (['D08']; applies here: yes)
   instantiate   t02              Members use hostile names and retrospective survival rhetoric about opponents without establishing reciprocal taunts.  [c0018,c0178,c0181]

[K03] The community carries a quarrel from before the canvas into it: a rival sub, a sports or national rivalry, an old dispute.  (['D05']; applies here: unobserved)
   absent                         Naming an encroaching neighbour as an opponent does not establish a quarrel carried over from before the canvas.  [c0018,c0065]

[P20] The host sub draws a line around canvas talk: moderators gather it into a megathread, remove canvas posts by rule, change posting rules, pause the sub's usual events or disown the work; members open a canvas sub, object to the flood or argue the canvas's worth.  (['D06']; applies here: unobserved)
   absent                         A prankster apologizes for misusing a help tag, but this does not establish a host rule containing canvas talk.  [c0057,c0126]

[K04] The room acts as a body it was before the canvas, or as a faith in a colour: it argues the nation's history, belonging and politics beyond its flag, carries in the sub's quarrel, lore, jokes or ideology, or professes and spreads a colour.  (['D05']; applies here: unstated)

[P19] One room's work lives on another room's mark or territory under the host's rule: guests ask for space or protection, hosts rule on requests, and both sides dispute who may approve.  (['D04']; applies here: unstated)

[C02] In some rooms, a tie the room had before the canvas (a league or school rivalry, a nation's history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack.  (['D08', 'D05']; applies here: not-testable)
   absent                         Defensive fight calls identify immediate encroachment without establishing an inherited tie selecting an offensive target.  [c0017,c0018]

[P21] Members dispute, or state the limits of, who may commit the room to an agreement with other rooms: they say that one member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another group for a leader to deal with.  (['D04']; applies here: unobserved)
   absent                         A moderator referral identifies a contact without showing disputed standing, stated limits on representation, or refusal to be bound by an agreement.  [c0089,c0021,c0097]

[P22] After placement ends, members contest which version of the canvas and of the event is kept: they ask a cleanup of a shared copy to fix their work, take part in it, argue that the cleanup should keep the damage as history, and correct accounts of the event that describe their group wrongly.  (['D07']; applies here: unobserved)
   absent                         Retrospective repair reports and differing survival explanations do not demonstrate cleanup of a shared copy or explicit correction of a false historical account.  [c0147,c0161,c0178,c0180,c0181]

[P23] Members move the room's planning into a chat, an existing server or a new one, and invite helpers to it. They bring the chat's designs, decisions and warnings back to the thread. They argue which chat to use, whether a chat is needed or secure, whether it is official, and whether it may decide for the work or bind placers.  (['D02']; applies here: yes)
   instantiate   t08              Painters are sent to Discord for the current egg initiative while instructions and requests not to revert return to Reddit.  [c0123,c0125,c0126]
   instantiate   t04              A neighbour seeking rapid help is directed to the chat holding active painters and agrees to return there if the threat resumes.  [c0136,c0137,c0138]
   link          t04              The need for rapid response directs a neighbour toward active painters in chat while preserving Reddit as an acceptable slower contact point.  [c0132,c0136,c0137,c0138]

[P24] Members ask what the canvas is, how to place, what a call or a name means and what a picture shows, and others explain the rule, the timer, the controls, whose mark a picture is and what happened. They ask before, during and after the close, and some questions get no answer.  (['D01']; applies here: yes)
   instantiate   t02              Confused readers ask about the canvas during late warnings and receive explanations of pixels, subreddit representation, and the Void.  [c0165,c0167,c0170,c0171,c0172]
   link          t02              A late protection warning receives a question about the event and an explanatory answer, keeping sensemaking available after construction.  [c0162,c0165,c0167]

[P25] The room's work brings people into the room. A viewer finds the sub through the mark or through a sign written to that end, a member of an ally comes through joint work, and a lapsed member returns. Members welcome them, explain the room's subject, take them into its usual activity, count the new subscribers and argue how to receive them.  (['D07']; applies here: unstated)

[P26] Members make new jokes out of the canvas work, its mistakes, its damage and its neighbours: puns on the mark, mock names and titles for a figure, and jokes about attackers and bots. The room takes the jokes up, and some members want a joke kept in the work.  (['D05']; applies here: yes)
   instantiate   t06              A member makes a new joke comparing collective max-plussing of the canvas mascot with their slower progress improving in-game monsters.  [c0144]

[P27] Before any loss, the room chooses where to put its work and changes the spot while it builds. It looks for open room, weighs a crowded or contested place, shrinks or moves the design ahead of a neighbour or the void, restarts a misplaced start, and refuses to move once enough pixels are in.  (['D04']; applies here: yes)
   instantiate   t02              Before a documented loss, participants consider moving the partly built outline and reject the proposed site as dangerous.  [c0011,c0012,c0013,c0014]

[P28] A room forms for the canvas around a mark. Members open a sub or a chat for a pattern or a figure and set it up. They invite the people seen building or copying the mark, give it a meaning its followers share, gather its repeaters into a group that can negotiate, and move or split the room.  (['D05', 'D06']; applies here: unobserved)
   absent                         A shared mascot and directions to the existing community chat do not establish formation of a new canvas room.  [c0001,c0125]

[P29] Members argue whether a joke, a taunt or a word in canvas talk offends, and they refuse slurs and hate symbols. They object, correct, apologise, remove the words or tell the speaker to leave, and they cover swastikas or refuse to draw them.  (['D05']; applies here: unobserved)
   absent                         Hostile naming and objections to unilateral replacement do not establish a dispute over offensive language or hate symbols.  [c0018,c0104]

[P30] The room turns its work toward people outside the canvas whom the mark shows or addresses: the creators, the team, the streamer, a company or the press. It shows them the work, hopes for their notice, shares the coverage and celebrates their acknowledgement, or it keeps the work from troubling them.  (['D07']; applies here: yes)
   instantiate   t06              A wish for company rewards receives a suggestion to post a screenshot on Facebook, supporting proposed external address rather than completed outreach.  [c0179,c0189]

[P31] Members argue whether covering others' work is fair. Some call it betrayal, dirty or a cost to the room's name. Others answer that change is the canvas's point, that wiping makes room for new art, or that the canvas is a game of conquest. The argument runs during the work and after the close.  (['D04']; applies here: yes)
   instantiate   t02              Members rebuke outsiders for proposing destruction without asking and contest unilateral replacement of their shared icon.  [c0100,c0104]

[P32] A member steps away from the work under strain, or the room repairs a quarrel between members. The work turns stressful or personal, or a member is criticised or yelled at over a pixel or a proposal. Others rebuke the harsh speaker, the speaker apologises, or the member threatens to leave or leaves.  (['D01']; applies here: unobserved)
   absent                         A directive to stop edits and a preference to surrender do not establish stressful withdrawal or repair of a personal quarrel.  [c0124,c0166]

[P33] Rooms keep their plans from rivals who read their threads, and they reach into rivals' venues. Members switch to their own language or write in code, move the plan to private messages, plant members in a rival's chat and warn of a snitch in their own.  (['D02', 'D08']; applies here: unobserved)
   absent                         A reported threatening visitor in Discord does not establish spying, concealed plans, or infiltration for strategic information.  [c0181,c0125]

[P34] Members who object to the canvas posts in the sub turn against the room's own mark. One member says the posts make them tear down the logo, and one recruits trolls to ruin the flag.  (['D06']; applies here: unobserved)
   absent                         A member preferring surrender after having fun does not report attacking the room's mark in resentment of canvas posts.  [c0166]

[K05] Members place on their own time and with their own devices. They fit placing around sleep, study, exams, work and travel. They cannot place from a phone or while away, they leave when the wait is too long, they save pixels under the timer, they find the work addictive, and they report what it cost them.  (['D02', 'D07']; applies here: yes)
   instantiate   t01              Members describe placement as repeated timed contributions rather than continuous unrestricted work.  [c0008,c0016]
   instantiate   t02              A defense reply jokes about conflict with an early class and the warner subsequently worries about costing the defender sleep.  [c0157,c0158]

[K06] The site sets what members can do, and members report its faults and pass on fixes. They report a blank or stale canvas, the site down, a vanished or faulty timer, glitches that seem to give extra pixels, captchas, the official app required and the site blocked in a country. They refresh, update, keep a separate window and test whether extra pixels reach the canvas.  (['D02']; applies here: yes)
   instantiate   t08              Participants test an egg design against the site's available palette and space, showing technical constraints without establishing a malfunction.  [c0153,c0155]

[K07] Some members belong to both rooms in a contest or at a border. They say they are torn or proud of both, and the room reassures them or still counts them as its own.  (['D04']; applies here: unobserved)
   absent                         Helping several pictures and denying membership in a neighbouring subreddit do not establish dual membership or divided allegiance.  [c0111,c0183]

proposed by this room:
   t07  An April Fools invitation elicits monster requests and tailored verse, extending holiday participation beyond deceptive announcements, takeovers, or canvas jokes.  [c0059,c0060,c0061]

arrows in the model: 21

[A01] P01 -> P03 (order): The room's call brings members to the canvas, who then build the mark and say how far it has come.
   instantiate   t01              The call receives a placement report eighteen minutes later, supporting recruitment into reported building.  [c0001,c0003,c0008]

[A02] R01 -> P01 (order): A member who proposes or begins a mark gives the room something to answer, and calls for hands gather around it.

[A03] P03 -> P05 (order): Once a mark stands on a surface anyone can change, keeping it becomes the work: a finished part is something to lose.
   instantiate   t02              The edited opening explicitly couples a completed picture with a continuing request for defense.  [c0006,c0007]

[A04] P05 -> P08 (order): Keeping a mark against erosion brings the room up against the neighbours whose pixels erode it, and the room turns to talk with them.
   instantiate   t03              Reported invasion and a defensive fight call are answered by coordination and a treaty report.  [c0004,c0005,c0018,c0021]

[A05] P08 -> P07 (order): A settled border gives the room a line to keep: members spare the neighbour's work by it and remind others of it.
   absent                         Treaty and repair reports do not isolate a settled border as the cause of restraint.  [c0021,c0074,c0110]

[A06] P05 -> P14 (order): Upkeep under attack outruns what one pixel per interval can hold, and members turn to scripts and spare accounts to keep up.
   absent                         Maintenance is visible but the record does not show its proposed transition from strain to automated or additional-account placement.  [c0007,c0093,c0160]

[A07] P03 -> P11 (order): A mark reported done gives the room a finished thing to point at, and the room marks it together: announcement, credit, pride.

[A08] P11 -> P12 (order): Marking the work together turns the room toward keeping it: members ask for the final image, the timelapse, the list of what changed.

[A09] P12 -> P13 (order): A record of the work gives the room something to carry: the image into the banner, the plan into the next canvas.
   absent                         Saving and header reuse are reported together without establishing that recording preceded or caused the decision to retain the image.  [c0154,c0174]

[A10] K02 -> P10 (order): A room that judges it has too few hands to hold its spot stops fighting for it and moves.
   absent                         The explicit weakness judgment concerns a proposed destination, whereas later relocation follows overwriting without a coded current-site manpower assessment.  [c0012,c0014,c0029,c0090]

[A11] P02 -> P04 (transition): Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel.
   restrict      t08              A template settles only a recognized current task; outdated references and unrecognized design stages can make helpers undo one another.  [c0025,c0123,c0124,c0125,c0148,c0149]

[A12] P01 -> P15 (transition): A call is the first part of a pair: posted to a thread, it makes an answer from each reader the next thing due, given in the thread or by placing. Joining is the answer the call prefers, so it comes bare, one line that commits and gives no reason ('I'm in'); declining is the dispreferred answer and, in conversation analysis, comes with a reason. In the written record a bare join is the ordinary way a call is accepted (25 of 31 read acceptances, F-023); a member can also accept by placing and write nothing, which the record cannot show.
   instantiate   t01              A brief placement report directly answers the call without showing what every reader did or whether each felt obliged to answer.  [c0003,c0008]

[A13] P05 -> P16 (order): A room keeping its work under strain runs short of hands and turns to other rooms for help, and other rooms send it.
   absent                         Assistance accompanies threatened upkeep, but its coded explanations name exchange and responsibility for damage rather than a demonstrated shortage of hands.  [c0086,c0107,c0108]

[A14] P08 -> P16 (order): Talk over a border opens a channel through which the two rooms then trade help: room for upkeep, pixels for protection.

[A15] P01 -> P09 (order): A call brings members to the canvas, and some of them turn its hands against a rival's work instead of, or before, building the room's own.
   absent                         The recruitment call is followed by defensive fight language without a coded redirection toward an offensive raid.  [c0003,c0017,c0018]

[A16] P09 -> P07 (order): A call to attack makes an answer from the room due in its thread. Members who do not want the attack refuse it, rein in the attackers or apologise to the target; refusing is the dispreferred answer, so in written replies it usually comes with a reason (23 of 38 read pairs, F-014), and the reason states the room's norm or the attack's cost ('Nah, keep /r/place neutral.'; 'Why? That'll just cause them to want to attack us').
   absent                         Visitors' apologies are visible but their originating attack calls are outside these coded passages, leaving the refusal mechanism untested.  [c0074,c0110]

[A17] P09 -> P08 (order): A call to attack is met by the room's relations with its neighbours: the room invokes a truce, or proposes a deal instead.
   absent                         A treaty answers a fight call but an offensive attack antecedent is not established.  [c0018,c0021]

[A18] P09 -> P18 (order): An attack makes the rival a named party, and the contest is carried on in talk: taunts, chants, claims of victory, a salute after the fight.
   absent                         Hostile language and retrospective threats do not establish that an offensive raid initiated reciprocal verbal contention.  [c0018,c0178,c0181]

[A19] P05 -> P17 (order): A room keeping its work against attack joins other rooms whose works face the same threat, and they defend each other's works together.
   absent                         The threat produces an alliance appeal, but its passing before further contact leaves actual coalition formation untested.  [c0132,c0136,c0137]

[A20] P01 -> P20 (order): Calls to the canvas flood the host sub, and its moderators or members answer by drawing a line around canvas talk: one thread, removals, a canvas sub.
   absent                         Calls for canvas help and organizing instructions do not establish a flood that caused the host to impose posting boundaries.  [c0003,c0066,c0126]

[A21] P08 -> P21 (order): An agreement made with another room in the room's name puts its members' compliance in question. Members who did not make it say that it does not bind them, or refuse it, or say that no one can bind every placer.
   absent                         Neither post-agreement refusal nor a disclaimer during negotiation is established by the treaty report and moderator referral.  [c0021,c0089,c0097]

## The coder's account

## Chronology

The week opens, in batches 01 and 02, on ordinary Puzzle & Dragons play: team questions, friend searches, achievements, and game news. Before the canvas project appears, the room also begins its own April Fools activity. The clearest early example asks members to invent “the most brutal April Fools prank” GungHo could pull (`62mfvh`); later posts stage fake announcements and images, while a separate exchange requests and supplies deliberately bad monster poems.

The first canvas episode runs from `62q1xx` to `dfp4a66`. At 02:35 UTC on 1 April, the opening post calls “Let's get our boy Tama in there!”, supplies a “Planned pixel map” and asks for “ALL HELP” (`62q1xx`). Eighteen minutes later, a commenter reports, “Placed a pixel there” (`dfogcbn`). The same post's updates then describe Mass Effect invading, ask people to finish quickly, and say the organizer has coordinated a leftward move of the other logo (`62q1xx`). A Mass Effect visitor apologizes for what happened to the design and proposes that both groups keep working during that move (`dfp1mes`); just over an hour later, another participant reports that “a treaty has been established” (`dfp4a66`). The post calls Tama “finalized and finished,” but also asks people to defend it from “griefers” (`62q1xx`): completion is a milestone, not an end to work.

The next episode runs from `dfq0r13` to `dfq4xs8`. On 2 April, an r/2007scape participant says, “we are helping to rebuild your work since we kinda bulldozed through everything” (`dfq0r13`). Four hours later, a participant reports, “N7 and Tama are both rebuilt” and credits r/2007scape (`dfq4xs8`). Between those endpoints the slice cases record contested relocation, new coordinates and reciprocal help. The evidence supports the sequence and the speakers' own explanation of why rebuilding occurred; linked images do not independently verify the canvas state.

By 18:20 UTC on 2 April, participants announce “The third step of the tamadra,” direct painters to a sticky, and ask them not to delete unfamiliar changes (`6318vp`). At 22:44 a post declares “Completed /r/pad territory” (`632tgz`), yet 44 minutes later a reply asks for a magic stone in the corner (`dfqwjuy`). Later discussion adds and revises +297, eggs, borders and lettering. This episode, from `6318vp` to `dfs66ei`, ends with a participant reporting that an incomplete plus “was fixed by the time /r/place closed” (`dfs66ei`). It therefore shows repeated participant-declared completions followed by further design and repair, not a community reversing a settled position.

The final live-canvas episode runs from `dfrfttq` to `dfrhm2t`. At 07:09 UTC on 3 April, a warning says the Void is “getting closer to your piece” (`dfrfttq`); one direct reply says an 8 a.m. class must wait to “protect ur child” (`dfrfuhm`). Parallel warning posts do not produce consensus: one commenter says the Void is “leaving us alone” (`dfrhxjr`), while another would “put it all to the void” (`dfrlcan`). A moderator preserves an image on the subreddit header “so even if we lose it” the final product can be posted (`dfrhm2t`). At 17:17 UTC, `6386r2` announces, “Place has ended but Tama lives unblemished.” A later answer describes Tama as “Remade 3 times,” says problems “got solved peacefully,” and credits Mass Effect and RuneScape with rebuilding help (`dfsjgq8`). Those are participants' retrospective explanations, not independently observed causes.

After that closing thread, batch 10 returns to ordinary game questions, friend matching, reset news, achievements and team planning. The event-close post precedes that return; the corpus does not show that the close caused it.

## Relations — what set off what

The planned map produces a directly described placement: `62q1xx` gives the map and location, and the reply `dfogcbn` says, “Placed a pixel there.” The reply arrived 18.4 minutes after the post. This is a map-to-placement response, not an inference from adjacency alone.

Mass Effect's damage is answered first with negotiation and then offered repair. The visitor `dfp1mes` names “what has happened to your design,” apologizes, and asks both sides to keep working while N7 moves. In the following slice, `62ux03` says N7 has nearly moved “off of your Tamadra design” and asks for the design so its members can “assist you in rebuilding.” The later post names the earlier problem and proposed remedy; the evidence does not show every internal decision made by either subreddit. [crosses 03|04]

The r/2007scape rebuilding relation is stated by the actor rather than inferred from timing: `dfq0r13` says they are rebuilding “since we kinda bulldozed through everything.” The subsequent report `dfq4xs8` that N7 and Tama are rebuilt follows four hours later. The first passage supports the destruction-to-repair relation; the second supports only the reported outcome.

Calling the territory complete sets off further proposals. The post `632tgz` says “Completed /r/pad territory,” and its direct reply `dfqwjuy`, 44 minutes later, asks, “Any way for a magic stone.” Later comments dispute sprite edits and name an established initiative: `dfqi62f` calls the timing too late, `dfqia5t` answers that the apparent vandalism is “our new initiative,” and `dfqirdr` directs people to “step three” in the sticky. These passages support a completion-to-revision sequence and explicit responses about legitimacy; they do not establish that the community as a whole changed its mind.

Void warnings set off mixed responses rather than one collective defense. `dfrfttq` warns that the Void is approaching and `dfrfuhm` explicitly answers with a promise to protect “ur child.” In the nearby warning thread, `635866` calls “Help protect it!”, but `dfrlcan` later says to give it to the Void. The record supports contrasting positions among speakers, not a shift from defense to surrender.

The close directly sets off celebration: `6386r2` announces that Place ended with Tama intact, and the replies praise the run and recount participation. The later explanation `dfsjgq8` answers a request to explain and attributes the repeated rebuilding to peaceful problem-solving and help from Mass Effect and RuneScape. That attribution is the participant's explanation; the earlier apology, coordination and rebuilding passages make it consistent with the record, but unseen off-platform action prevents a stronger causal claim.

## Posts against comments

In batch 03, the main post says Tama is “finalized and finished” (`62q1xx`); its comment layer shows disputed relocation, overwriting, treaties, destruction, rebuilding and a later Void warning. The posts say completion; the comments say completion remains vulnerable and revisable.

In batch 04, the moderator post frames Tamadra as being “slaughtered by r/MassEffect” (`62ted7`); comments say Mass Effect participants are working on the sabotage, and `62ux03` offers a move and rebuilding help. The posts supply the alarm, while the comments and later neighbour post complicate a simple attacker story.

In batch 05, the surviving title says “STOP DEFENDING THE IMAGE - REBUILD TO THE RIGHT” (`62yh1q`); the comment layer rebukes outsiders for announcing a replacement without asking. Because the post body is deleted, the title/comment tension cannot reveal the original rationale.

In batch 06, posts repeatedly announce a completed territory or finished +297 (`632tgz`, `633rkz`); comments propose more additions, reject some color schemes, repair trolls and recover a lost template. The posts mark milestones; the comments expose continuing design government and maintenance.

In batch 07, warning posts say the Void is approaching (`635866`, `635arj`); comments range from protection and neighbour help to “leaving us alone” (`dfrhxjr`) and surrender (`dfrlcan`). The posts say danger; the comment layer shows disagreement over its severity and the appropriate response.

In batch 09, the post says Tama ended unblemished (`6386r2`), and the comments agree while adding the story of repeated rebuilding, allies and threats. Here the layers differ in detail, not outcome.

## Counter-reading

My one-sentence reading is: the room made a small shared Tama through mapped pixel work, repeatedly answered displacement through bargaining and reciprocal rebuilding, and treated each completion as provisional through additions, defense, preservation and retrospective celebration.

The strongest competing account is that this was primarily a self-contained defensive fight and that neighbourly bargaining or returned help was incidental or merely retrospective. If my reading were wrong, the record should contain participants rejecting outside help or treaties, insisting on fighting alone, or denying that neighbours helped rebuild.

The strongest contrary item already in the cases is `62yh1q`, whose surviving title commands “STOP DEFENDING” and says to rebuild to the right. It changes the defense claim: participants did not uniformly defend the existing location, and relocation could displace holding ground. It does not overturn the broader reading, because the alternative it names is coordinated rebuilding, not solitary fighting. `dfrlcan` is a second qualification: one speaker was ready to give everything to the Void after having fun.

The strict search for fighting alone, refusing help or denying a treaty returned no hits. A broader search for this case's contrary phrases returned `62yh1q`, `dfrhxjr`, and one irrelevant pre-window gameplay item; all were read. A second help-denial search returned only an irrelevant pre-window gameplay item. These null event results are scoped to the supplied Reddit record and these phrases: they cannot establish agreement, especially because Discord coordination and other communities' deliberations are only partially visible.

The separate completeness search for the batch-02 warning returned `62mfvh` and the already-coded `62s5fw`; both were read, and the whole `62mfvh` thread was opened because it had previously been triaged. Its prompt and replies collectively invent hypothetical GungHo April Fools pranks, so a late code was added to the existing April Fools theme. This expands that practice earlier in the week but does not alter the canvas reading. Its earlier out-of-scope disposition remains visible under the append-only rule.

## Saturation

The themes appear early. The late search moves “staging and spotting PAD April Fools jokes” back to batch 02. Batch 03 first supplies assembling Tama from a shared map, responding to threats, bargaining and rebuilding with neighbours, answering a neighbour's joint-defense call, and celebrating the picture. Batch 04 first supplies the bad-poem performance and revising or adding to the finished picture. Batches 05 through 09 deepen those practices—especially relocation, step-three changes, Void responses, preservation and retrospective credit—but introduce no further practice group; batches 08 and 10 add no event code.

The Reddit record is sufficient for this practice-level account but is not whole. The forest shows substantial uncoded stretches inside coded items, deleted bodies narrow several important claims, and linked images cannot verify visual outcomes. Discord is itself part of the conduct: painters are sent there to coordinate and neighbours are directed there for rapid response. What happened inside that venue is unavailable; only instructions and retrospective reports return to Reddit. The r/2007scape help post, the other subreddits' deliberations, and a proposed Facebook screenshot are likewise unseen.

No one reader held the whole week. One coder read each arbitrary whole-thread slice, there is no agreement measure, and the forest makes sequences inspectable without giving the lead a single-reader account of every thread. Cross-slice relations are therefore weaker; the Mass Effect damage-to-repair relation above is carried across batches 03 and 04 only because the later post explicitly names moving N7 off Tama and helping rebuild. Long ordinary threads stopped at triage, including the batch-08 friend megathread, limit absence findings to the served windows.

## Selection

The lead read the briefing and complete openings table before the branch gate, using them only to orient the week. Branch B then assigned every whole thread to one of ten corpus-order slices. Each coder disposed every owned thread, read event-touching threads in full, and retained the room's own April Fools conduct separately from canvas conduct. Ordinary team advice, friend searches, pulls, dungeon talk, game news and achievements were excluded; every read exclusion with ten or more in-window items carries its exact instrument citation.

After collection, the lead read pooled codes beside each slice case in order, built themes incrementally, then used the permitted counter-reading search. The search changed one completeness decision: `62mfvh` remained append-only as out of scope but received a late code after its whole thread showed collective prank invention.

## Other communities named

r/MassEffect is first described as overwriting Tama, then appears through apology, negotiated movement, a treaty and offers of repair. r/runescape and r/2007scape are described as destroying space and then apologizing, relocating or rebuilding; these are claims and interactions preserved in this room, not independent accounts of those communities. r/mindcrack asks for joint defense against Dutch expansion, while an r/2007scape visitor later says they made a help post for threatened neighbours. r/touhou appears through one visitor proposing a larger image.

r/place is the canvas venue. Discord becomes a coordination venue for active painters and rapid response, with only fragments returning to Reddit. Imgur and a Discord-hosted template carry visual references the text record does not preserve as evidence. Facebook is only proposed as a destination for a screenshot; the corpus does not show the post occurring.

## Absence

Deleted post bodies matter most where titles alone survive: the general r/place invitation, several fake-news jokes, the border PSA, praise and finish posts, and especially `62yh1q`. Their surviving titles support narrow claims, while comments can show responses but cannot reconstruct the missing proposals. Deleted comments also interrupt some relocation and retrospective exchanges.

The supplied record does not show the images themselves, the internal Discord discussion, other communities' decision-making, or whether the proposed Facebook post occurred. The lack of a search hit rejecting allies is therefore only a bounded absence. What survives does show mapped placement, explicit apologies and bargains, participant-reported rebuilding, contested additions, mixed reactions to threats, preservation, and post-close remembrance.

## The room's second-order themes

- t01 assembling Tama from a shared pixel map
- t02 responding when Tama is threatened
- t03 bargaining, relocating, and rebuilding with neighbours
- t04 answering neighbours' calls for joint defence
- t05 staging and spotting PAD April Fools jokes
- t06 celebrating, preserving, and remembering Tama
- t07 requesting and writing bad monster poems
- t08 revising and adding to the finished picture

This is the end of the packet. Confirm you reached it by returning your lines and then the end marker the return specification names. END OF PACKET
