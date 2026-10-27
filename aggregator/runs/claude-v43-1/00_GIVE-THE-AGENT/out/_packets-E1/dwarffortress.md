# Reconstruction packet

Score, claim by claim of the coder's account below, whether the skeleton accounts for it, with the element id or `none`, one line per claim in the form the return specification gives. State unresolved evidence or stale versions in each affected claim reason. Pending or rejected lines are not asserted support; silence is not negative evidence. Report unresolved claim counts separately from contradiction. Reproduce the skeleton current model version and local status in the summary.

## The skeleton (the global model with supported local adaptations and explicit uncertainty)

# r/dwarffortress rebuilt from the global model (46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525) plus 75 adjudicated re-check lines

Adapted-local status: unresolved; grade: composes-with-residue; version status: current.
Return model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525; current model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525.
Unresolved adaptations: 0 (not asserted support).

[P01] The room calls its own members, and kindred subs, to come and place for a work: to start it, build it, finish it or hold it.  (['D01']; applies here: yes)
   instantiate   t01              Members recruit fellow dwarves and request help with particular additions to the shared display.  [c0002,c0049,c0058,c0082]

[P02] The room settles what its mark will show of it: a member proposes a picture, the room argues its design, makes its land's flag or emblems the mark, signs it or leaves it unsigned, claims a mark others made, adds to it or enlarges it, or adds a personal piece to a shared mark.  (['D02']; applies here: yes)
   instantiate   t02              Contributors revise figures, assign professions, change priorities, and drop a proposal in favor of work already underway.  [c0016,c0031,c0032,c0053,c0060,c0125]
   instantiate   t04              Members choose between a short redirect name and the full subreddit name for identifying the work.  [c0061,c0071,c0072,c0084]

[P03] The room builds its mark, and members report its state to the thread: what is placed, done or missing, and where.  (['D02']; applies here: yes)
   instantiate   t02              Members report completed parts and individual progress, including a mug, one lettering pixel, and an unfinished sign.  [c0016,c0017,c0063]

[P04] Members circulate a template that lays out the mark pixel by pixel, or coordinates that locate it, ask for them, and ask strays to keep to them.  (['D02']; applies here: yes)
   instantiate   t04              Anchor coordinates, a proposed grid, and visible goal images make contributions locatable and comparable.  [c0003,c0006,c0140,c0146]
   add-condition t04              Changed targets must reach relevant placers through accessible public images when the planning chat is unavailable.  [c0140,c0141,c0145,c0146]

[P05] The room keeps its placed work against erosion: members watch it and repair changed pixels, and the room rallies to defend it under attack, covers the night, hardens its shape and puts upkeep before growth. Repair restores the form the keepers know. A change the room has planned or agreed (P02) is therefore repaired away as damage until its keepers are told of it, and it is lost or given up where the telling does not reach them.  (['D03']; applies here: contested)
   link          t04              Repairers need a visible revised goal to distinguish intended changes from an invasion they would otherwise repair away.  [c0145,c0146,c0153,c0154]
   instantiate   t03              Members clean, repair, and defend figures against changed colors, encroachment, and the Void.  [c0005,c0026,c0064,c0120]
   instantiate   t03              The revised known-form mechanism fits a repairer undoing an intended edit after mistaking it for invasion.  [c0144,c0145]
   restrict      t04              Apply demonstrated mistaken restoration without inferring eventual loss or abandonment when unreached keepers' outcomes remain unobserved.  [c0141,c0142,c0145,c0146,c0154,c0155]
   add-condition t03              Independent visual maintenance can continue without participation in any coordination channel.  [c0101]

[P06] Members work out who changed their work and why: they trace placers and rooms, find friendly fire or their own mistake, blame officers, or disown placers acting in their name.  (['D03']; applies here: yes)
   instantiate   t03              Participants identify friendly fire and mistakes when apparently hostile pixels belong to an intended design.  [c0041,c0042,c0145]

[P07] Rooms spare their neighbours' work, rein in their own attackers, apologise for damage and appeal to attackers to stop.  (['D04']; applies here: yes)
   instantiate   t05              Members welcome neighbors, remind placers to respect agreements, urge returning disputed art, and stop repairing an intended recoloring.  [c0012,c0030,c0070,c0153,c0154]

[P08] Rooms propose, settle and contest borders, truces and deals with neighbours by talk, through envoys, and hold each other to them.  (['D04']; applies here: yes)
   instantiate   t05              Neighbors negotiate reciprocal noninterference, conditional borders, truces, and proposed relocation or rebuilding.  [c0011,c0062,c0067,c0094]

[P09] Rooms attack others' work by the recurring moves the canvas affords: erasing, encroaching, converting a sign, raiding on a streamer's call, planting a script, altering a work as a joke.  (['D08']; applies here: yes)
   link          t10              Host posting irritation is explicitly offered as a reason for helping destructive canvas action.  [c0161]
   instantiate   t07              Members call a joint strike against a neighboring flag, while a separate participant admits a joke alteration.  [c0092,c0044]

[P10] After the work is erased or overrun, the room weighs fighting for the spot against moving, and moves: a new spot, a smaller version, a fresh start.  (['D04']; applies here: not-testable)
   absent                         Movement and rebuilding proposals do not establish both triggering erasure and a completed collective relocation.  [c0075,c0094,c0126]

[P11] When a work is up, the room marks it: announces it, celebrates it, credits makers and helpers, reports members' own parts and says what working with strangers meant.  (['D07']; applies here: yes)
   instantiate   t11              Participants announce completion, thank contributors, and name the finished work.  [c0155,c0151,c0156]

[P12] The room records what happened to its work and to the canvas around it: screenshots and timelapses, reports of its fate, mourning, imagined art, atlas entries, the end marked.  (['D07']; applies here: yes)
   instantiate   t11              Participants share a timelapse and recount conflicts, treaties, concessions, and the finished display.  [c0100,c0157,c0158,c0156]
   add-condition t05              A post-close report of contributed pixels records earlier assistance rather than demonstrating new placement after the stop.  [c0159]

[P13] Near the close and after it, the room decides what of its temporary effort to keep: a later canvas, a new purpose for its canvas sub, the mark in its banner, ties with other rooms, the work remade elsewhere.  (['D07']; applies here: not-testable)
   absent                         A pre-close welcome does not establish a later decision or durable outcome about retaining the temporary effort.  [c0148]

[P14] Members add placements with scripts, bots and spare accounts, and the room argues over these machine hands and adjusts them.  (['D02']; applies here: yes)
   instantiate   t06              Members recruit script users, propose defensive adjustments, and debate automation's fun and usefulness during sleep.  [c0130,c0138,c0110,c0111]

[P15] A member answers a call or proposal in one line that joins, assents, reports a part done or thanks, and the line asks for nothing back.  ([]; applies here: yes)
   instantiate   t08              A request for help on the dead goblin receives a brief acceptance framed as a reassigned task.  [c0049,c0050]

[K01] The host sub is keyed as play for April Fools: members post fakes and takeovers under the one-day licence, and a claim in it, a call to the canvas included, may be a joke.  (['D06']; applies here: unobserved)
   absent                         A canvas joke and a temporary posting rule do not establish deceptive host-wide April Fools framing.  [c0044,c0085]

[K02] The room judges that it has too few hands or too little room for the work it wants: doubt, a canvas judged too full, a work judged absent or outclassed.  (['D01']; applies here: yes)
   instantiate   t02              Members judge available space, coordination, and defensible scale insufficient for some proposed extensions.  [c0035,c0036,c0096]

[C01] Most rooms worked on their marks without deciding how they were organized: a decided element of order (a leader, a vote, an oath, a sanction, a division of the work) is coded in 46 of 705 rooms (F-006).  (['D02']; applies here: not-testable)
   absent                         Reported decisions in one room cannot test the stated cross-room prevalence of decided order.  [c0055,c0079]

[R01] The starter: a member who proposes the mark, maps it or begins placing it. Others joining is not part of the role: it is the answer to the room's call (P15), in the order A02 and A01 state.  (['D02']; applies here: yes)
   instantiate   t02              Members initiate work by setting an anchor, carving out a corner, and proposing profession-colored figures.  [c0003,c0013,c0053]

[R02] The envoy: a member who acts for a room toward another room, carrying a proposal between threads or chats.  (['D04']; applies here: yes)
   instantiate   t05              A member reports carrying a conditional border agreement back from another group's thread.  [c0062]

[P16] Rooms help one another's works and trade help: they give pixels to a neighbour's mark, ask other rooms for help, barter help for space or repair, thank their allies, greet them, and turn requests away.  (['D04']; applies here: yes)
   instantiate   t05              Neighbors offer joint defense, barter construction help for preserved pixels, and ask for help for nearby allies.  [c0021,c0022,c0043,c0104,c0160]

[P17] Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred rooms in a hub, tally kindred rooms' works and make joint marks.  (['D04']; applies here: yes)
   instantiate   t06              An alliance inquiry, reported collaboration, and an ally-colored plan show cooperation through named partners and shared designs.  [c0056,c0129,c0150]

[P18] Rooms carry a contest with a rival room in talk: they trade taunts, flood the rival's threads, claim victory, salute the rival after the fight and blame attackers after the close.  (['D08']; applies here: yes)
   instantiate   t08              Insults, marching imagery, and a claimed memorial to an opponent's defeat carry conflict into talk.  [c0112,c0114,c0117]

[K03] The community carries a quarrel from before the canvas into it: a rival sub, a sports or national rivalry, an old dispute.  (['D05']; applies here: unobserved)
   absent                         Territorial conflict and fandom insults do not establish an earlier quarrel with the same neighbors.  [c0090,c0112]

[P20] The host sub draws a line around canvas talk: moderators gather it into a megathread, remove canvas posts by rule, change posting rules, pause the sub's usual events or disown the work; members open a canvas sub, object to the flood or argue the canvas's worth.  (['D06']; applies here: yes)
   instantiate   t10              Temporary permission, megathread proposals, spam complaints, defenses of relevance, and unsubscribing contest the host's boundary around canvas talk.  [c0085,c0086,c0068,c0123,c0163,c0164]

[K04] The room acts as a body it was before the canvas, or as a faith in a colour: it argues the nation's history, belonging and politics beyond its flag, carries in the sub's quarrel, lore, jokes or ideology, or professes and spreads a colour.  (['D05']; applies here: yes)
   instantiate   t08              Game language supplies forms for recruitment, arrival, task acceptance, restraint, and calls to defend the work.  [c0002,c0029,c0050,c0074,c0128]

[P19] One room's work lives on another room's mark or territory under the host's rule: guests ask for space or protection, hosts rule on requests, and both sides dispute who may approve.  (['D04']; applies here: unstated)

[C02] In some rooms, a tie the room had before the canvas (a league or school rivalry, a nation's history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack.  (['D08', 'D05']; applies here: contested)
   restrict      t08              Applying inherited lore to a canvas opponent does not establish a pre-canvas relationship that selected that opponent.  [c0112,c0114,c0108]

[P21] Members dispute, or state the limits of, who may commit the room to an agreement with other rooms: they say that one member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another group for a leader to deal with.  (['D04']; applies here: unobserved)
   absent                         Agreement reports and access objections show no explicit disclaimer of standing, refusal to be bound, or request for an authorized representative.  [c0062,c0079,c0140]

[P22] After placement ends, members contest which version of the canvas and of the event is kept: they ask a cleanup of a shared copy to fix their work, take part in it, argue that the cleanup should keep the damage as history, and correct accounts of the event that describe their group wrongly.  (['D07']; applies here: unobserved)
   absent                         Final naming, war recollections, and a concession report do not establish contested cleanup or correction of the room's public history.  [c0156,c0157,c0158]

[P23] Members move the room's planning into a chat, an existing server or a new one, and invite helpers to it. They bring the chat's designs, decisions and warnings back to the thread. They argue which chat to use, whether a chat is needed or secure, whether it is official, and whether it may decide for the work or bind placers.  (['D02']; applies here: yes)
   instantiate   t06              Planning moves into chat and returns through reported decisions, expansion limits, diplomatic invitations, and ally-colored targets.  [c0054,c0055,c0079,c0103,c0150]
   add-step      t06              A member also asks the public thread to carry a relocation proposal into chat, making the relay bidirectional.  [c0126,c0150]
   add-condition t04              Chat coordination reaches willing contributors only when its goals also become accessible to people unable to use the chat.  [c0140,c0141,c0146,c0149]

[P24] Members ask what the canvas is, how to place, what a call or a name means and what a picture shows, and others explain the rule, the timer, the controls, whose mark a picture is and what happened. They ask before, during and after the close, and some questions get no answer.  (['D01']; applies here: yes)
   instantiate   t01              Willing novices ask how to draw and contribute, and others explain choosing a color and placing it.  [c0027,c0028,c0051,c0052]
   instantiate   t09              A notice explains the changed five-minute interval without establishing its effect on participation.  [c0066]

[P25] The room's work brings people into the room. A viewer finds the sub through the mark or through a sign written to that end, a member of an ally comes through joint work, and a lapsed member returns. Members welcome them, explain the room's subject, take them into its usual activity, count the new subscribers and argue how to receive them.  (['D07']; applies here: adapted)
   add-step      t04              A short redirect is created to make the game findable, while actual discovery through that route remains unmeasured.  [c0061]
   add-condition t06              Distinguish reported event-channel arrivals from artwork-driven subreddit discovery and lasting membership conversion.  [c0148,c0061]

[P26] Members make new jokes out of the canvas work, its mistakes, its damage and its neighbours: puns on the mark, mock names and titles for a figure, and jokes about attackers and bots. The room takes the jokes up, and some members want a joke kept in the work.  (['D05']; applies here: yes)
   instantiate   t08              An admitted joke alteration is bargained over, while a canvas collision becomes a game-style engraving.  [c0044,c0043,c0069]

[P27] Before any loss, the room chooses where to put its work and changes the spot while it builds. It looks for open room, weighs a crowded or contested place, shrinks or moves the design ahead of a neighbour or the void, restarts a misplaced start, and refuses to move once enough pixels are in.  (['D04']; applies here: yes)
   instantiate   t02              Members locate initial work, try coordinates, propose shifting a row, and seek uses for small remaining spaces without establishing prior destruction.  [c0003,c0046,c0075,c0097]

[P28] A room forms for the canvas around a mark. Members open a sub or a chat for a pattern or a figure and set it up. They invite the people seen building or copying the mark, give it a meaning its followers share, gather its repeaters into a group that can negotiate, and move or split the room.  (['D05', 'D06']; applies here: unobserved)
   absent                         Creating a short redirect for an existing community does not establish a new collective formed around a mark.  [c0061]

[P29] Members argue whether a joke, a taunt or a word in canvas talk offends, and they refuse slurs and hate symbols. They object, correct, apologise, remove the words or tell the speaker to leave, and they cover swastikas or refuse to draw them.  (['D05']; applies here: unobserved)
   absent                         A hostile term's presence does not establish an objection to that term or collective policing of offensive language.  [c0112]

[P30] The room turns its work toward people outside the canvas whom the mark shows or addresses: the creators, the team, the streamer, a company or the press. It shows them the work, hopes for their notice, shares the coverage and celebrates their acknowledgement, or it keeps the work from troubling them.  (['D07']; applies here: unobserved)
   absent                         Finishing a figure for a game's deity does not demonstrate seeking acknowledgment from creators, teams, streamers, or press.  [c0008]

[P31] Members argue whether covering others' work is fair. Some call it betrayal, dirty or a cost to the room's name. Others answer that change is the canvas's point, that wiping makes room for new art, or that the canvas is a game of conquest. The argument runs during the work and after the close.  (['D04']; applies here: yes)
   instantiate   t08              A member justifies sparing other structures through a creators-rather-than-destroyers norm without establishing consensus.  [c0074]

[P32] A member steps away from the work under strain, or the room repairs a quarrel between members. The work turns stressful or personal, or a member is criticised or yelled at over a pixel or a proposal. Others rebuke the harsh speaker, the speaker apologises, or the member threatens to leave or leaves.  (['D01']; applies here: not-testable)
   absent                         A sharp coordination order receives an inclusion request, but neither personal withdrawal from pixel work nor completed quarrel repair is established.  [c0139,c0140,c0163]

[P33] Rooms keep their plans from rivals who read their threads, and they reach into rivals' venues. Members switch to their own language or write in code, move the plan to private messages, plant members in a rival's chat and warn of a snitch in their own.  (['D02', 'D08']; applies here: unobserved)
   absent                         Using a planning chat does not by itself establish secret plans, infiltration, or spying on rivals.  [c0054,c0103]

[P34] Members who object to the canvas posts in the sub turn against the room's own mark. One member says the posts make them tear down the logo, and one recruits trolls to ruin the flag.  (['D06']; applies here: yes)
   instantiate   t10              One participant explicitly attributes claimed destructive assistance to irritation with canvas posting in the host sub.  [c0161]
   add-condition t10              The evidence establishes a participant's stated motive and claimed assistance, without independent pixel measurement or evidence of collective host opposition.  [c0161,c0164]

[K05] Members place on their own time and with their own devices. They fit placing around sleep, study, exams, work and travel. They cannot place from a phone or while away, they leave when the wait is too long, they save pixels under the timer, they find the work addictive, and they report what it cost them.  (['D02', 'D07']; applies here: yes)
   instantiate   t10              Sleep is invoked to justify automated upkeep, while another contributor reports being pulled away after placing a few pixels.  [c0111,c0122]

[K06] The site sets what members can do, and members report its faults and pass on fixes. They report a blank or stale canvas, the site down, a vanished or faulty timer, glitches that seem to give extra pixels, captchas, the official app required and the site blocked in a country. They refresh, update, keep a separate window and test whether extra pixels reach the canvas.  (['D02']; applies here: yes)
   instantiate   t09              Members report a site-imposed wait and its later five-minute interval without demonstrating malfunction or extra-pixel exploitation.  [c0017,c0066]

[K07] Some members belong to both rooms in a contest or at a border. They say they are torn or proud of both, and the room reassures them or still counts them as its own.  (['D04']; applies here: unobserved)
   absent                         Choosing another project while wishing these builders well does not establish explicitly divided membership in a contest.  [c0024]

arrows in the model: 21

[A01] P01 -> P03 (order): The room's call brings members to the canvas, who then build the mark and say how far it has come.

[A02] R01 -> P01 (order): A member who proposes or begins a mark gives the room something to answer, and calls for hands gather around it.
   add-condition t02              Starting and calling can coincide in one opening rather than requiring distinct sequential turns.  [c0002,c0003]

[A03] P03 -> P05 (order): Once a mark stands on a surface anyone can change, keeping it becomes the work: a finished part is something to lose.
   instantiate   t03              An invitation to build and maintain a figure is followed by a stated need to concentrate on cleaning it.  [c0004,c0005]
   add-condition t02              Keeping existing pixels can overlap initial construction rather than wait for the entire display to be completed.  [c0004,c0005]

[A04] P05 -> P08 (order): Keeping a mark against erosion brings the room up against the neighbours whose pixels erode it, and the room turns to talk with them.
   instantiate   t05              A perceived neighboring threat receives an accommodation and joint-defense offer directly.  [c0020,c0021,c0022]

[A05] P08 -> P07 (order): A settled border gives the room a line to keep: members spare the neighbour's work by it and remind others of it.
   instantiate   t05              A reported agreement receives a direct welcome and later reminders to leave the neighboring logo alone.  [c0011,c0012,c0030]

[A06] P05 -> P14 (order): Upkeep under attack outruns what one pixel per interval can hold, and members turn to scripts and spare accounts to keep up.
   add-condition t10              Overnight coverage is an explicit automation rationale, while the proposed manual-capacity threshold remains unmeasured.  [c0110,c0111,c0130]

[A07] P03 -> P11 (order): A mark reported done gives the room a finished thing to point at, and the room marks it together: announcement, credit, pride.

[A08] P11 -> P12 (order): Marking the work together turns the room toward keeping it: members ask for the final image, the timelapse, the list of what changed.
   add-condition t11              Recording can accompany construction when a timelapse is shared before later pieces are completed.  [c0100,c0155]

[A09] P12 -> P13 (order): A record of the work gives the room something to carry: the image into the banner, the plan into the next canvas.
   absent                         The pre-close welcome is not linked to the timelapse or final accounts as the cause of a later retention decision.  [c0148,c0100,c0157]

[A10] K02 -> P10 (order): A room that judges it has too few hands to hold its spot stops fighting for it and moves.
   absent                         Capacity objections and relocation proposals do not establish that insufficient hands caused a completed collective move.  [c0096,c0094,c0126]

[A11] P02 -> P04 (transition): Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel.
   absent                         Design proposals, an anchor, and a grid proposal do not establish a template settling a preceding design dispute.  [c0003,c0006,c0053]

[A12] P01 -> P15 (transition): A call is the first part of a pair: posted to a thread, it makes an answer from each reader the next thing due, given in the thread or by placing. Joining is the answer the call prefers, so it comes bare, one line that commits and gives no reason ('I'm in'); declining is the dispreferred answer and, in conversation analysis, comes with a reason. In the written record a bare join is the ordinary way a call is accepted (25 of 31 read acceptances, F-023); a member can also accept by placing and write nothing, which the record cannot show.
   instantiate   t08              The dead-goblin help request receives a brief acceptance that asks for nothing back.  [c0049,c0050]
   add-condition t08              The observed assent supports a written response without testing normative obligation, refusal preferences, or silent placement answers.  [c0049,c0050]

[A13] P05 -> P16 (order): A room keeping its work under strain runs short of hands and turns to other rooms for help, and other rooms send it.
   absent                         Joint-defense offers and requests for neighbor help do not establish shortage of hands as their cause.  [c0022,c0104]

[A14] P08 -> P16 (order): Talk over a border opens a channel through which the two rooms then trade help: room for upkeep, pixels for protection.
   add-condition t05              Accommodation and offered help can occur in the same turn rather than as separately observed stages.  [c0021,c0022]

[A15] P01 -> P09 (order): A call brings members to the canvas, and some of them turn its hands against a rival's work instead of, or before, building the room's own.

[A16] P09 -> P07 (order): A call to attack makes an answer from the room due in its thread. Members who do not want the attack refuse it, rein in the attackers or apologise to the target; refusing is the dispreferred answer, so in written replies it usually comes with a reason (23 of 38 read pairs, F-014), and the reason states the room's norm or the attack's cost ('Nah, keep /r/place neutral.'; 'Why? That'll just cause them to want to attack us').

[A17] P09 -> P08 (order): A call to attack is met by the room's relations with its neighbours: the room invokes a truce, or proposes a deal instead.
   add-condition t05              Bargaining during conflict is visible, while separate attack posts cannot be assigned as the cause of those negotiations.  [c0067,c0092,c0094]

[A18] P09 -> P18 (order): An attack makes the rival a named party, and the contest is carried on in talk: taunts, chants, claims of victory, a salute after the fight.

[A19] P05 -> P17 (order): A room keeping its work against attack joins other rooms whose works face the same threat, and they defend each other's works together.
   add-condition t05              Joint defense is explicitly offered against shared threats, but the coalition's internal formation remains unseen.  [c0022,c0129]

[A20] P01 -> P20 (order): Calls to the canvas flood the host sub, and its moderators or members answer by drawing a line around canvas talk: one thread, removals, a canvas sub.
   add-condition t10              Host complaints concern event content broadly and do not isolate recruitment calls as the sole cause of the flood.  [c0002,c0085,c0164,c0152]

[A21] P08 -> P21 (order): An agreement made with another room in the room's name puts its members' compliance in question. Members who did not make it say that it does not bind them, or refuse it, or say that no one can bind every placer.
   absent                         The revised timing boundary cannot be tested because the coded passages show neither authority disclaimers during terms nor later refusals to be bound.  [c0055,c0062,c0103,c0140]

## The coder's account

## Chronology

The record opens with ordinary Dwarf Fortress life. In batch 01, from `62huml` to `62mcwf`, people ask and answer game questions, discuss chat venues, recount forts, and seek graphics help; no served window or complete short thread visibly turns that activity into canvas conduct. The first dedicated event post is `62n9hh` at d0 03-31 18:59. It asks, “Seen the canvas yet? Let's work together like good dwarves!”, gives a starting coordinate for “'S'laves to Armok,” and rallies “For the glory of the mountainhomes!”

The first building episode runs from `62n9hh` to `62ujis` across batches 02 and 03. People replace the initial lettering ambition with dwarf figures, an Armok shrine, “STRIKE THE EARTH,” a mug, a plump helmet, profession-colored Urists, and a dead goblin; alongside making them, they recruit helpers, teach people to choose a color, and clean overwritten pixels. At d1 04-01 18:33, `62ujis` says the goblin is “Starting to take shape,” then “complete,” and thanks contributors because it “took off really quickly.” [crosses 02|03]

As space tightened, building became border work. From `dfpc5ly` in batch 03 through `637l8b` in batch 04, participants report agreements with neighboring designs, argue about the Catalan flag and Indonesia, move diplomacy into Discord, defend against the Void, and revise figures to ease conflict. The positions vary sharply: `62ys9y` at d1 04-02 09:23 says Catalonia is “attempting to destroy our human,” while `dfq47ce` at d1 04-02 11:50 asks to “get the ball moving” on moving and rebuilding with five people ready to stop. Later, `637l8b` at d2 04-03 15:44 asks people not to fight an Indonesian-flag dwarf because the change is “to help ease tensions,” and `dfrw7wn` announces “WE DID IT!” ten minutes later. These are contrasting speakers and successive proposals, not evidence that the whole community changed its mind. [crosses 03|04]

Placement closes before the final account begins. The ending episode runs from `63845g` at d3 04-03 17:08 to `dfsh2ni` at d3 04-03 22:40, an instrument-measured 5.54 hours. `63845g` names the finished display “The dwarven fortress of Placemurdered at it's end”; `dfsbja9` recalls “Two wars,” “two peace treaties,” alliances, and a Minecraft collaboration, while `dfsh2ni` continues defending the BOPP diamond on allies' behalf. Ordinary discussion is already resuming: `638czu` asks for help getting into an intimidating game, and by `63ex4j` at d3 04-04 15:47 the room is again proposing game features, here a `[ROPE]` tag for strangling enemies.

## Relations — what set off what

An N64 neighbor's explicit bargain receives an explicit welcome. `dfoehfg` says “we came to an agreement”: N64 help will be traded for leaving the shrine alone. `dfoejeb` replies, “we'll welcome you into our taverns” and drain the drowning pits 1.4 minutes later. The words establish the bargain and acceptance; the reply position alone does not.

A defense call is redefined as mistaken damage. `dfp22fk` says “The dwarves must resist!”; `dfp26vj` answers 2.9 minutes later, “Friendly fire! You are destroying the golden tooth!” This supports a corrective response, not a claim that everyone accepted the tooth or that the correction ended the wider dispute.

Discord-first coordination visibly produces access and repair problems. In `6369ip`, `dfrmmu5` orders a mistaken defender to “go to the discord”; `dfrpsaw` answers 86.1 minutes later that not everyone has access and asks for “a picture of the end goal here.” In a separate thread, `dfrnfhp` apologizes for repairing a planned edit because “I thought that they were invading,” and `dfrpknr` asks for a goal “easily viewable for everyone,” calling the Discord assumption misguided. These passages support participants' own explanation that unseen plans led to mistaken repairs; they do not prove every mistaken repair had that cause.

The Indonesian-pattern dwarf is a supported response to conflict, but the broader reconciliation is only partly visible. `dfqv4bv` declares “Any peace is over”; 16.79 hours later, `637l8b` explicitly says the recoloring is “to help ease tensions about their flag.” That stated purpose supports the link across batches, while the interval and subsequent completion do not establish that tensions actually ended. [crosses 03|04]

Other sequences remain sequences. Calls to defend, later script recruitment, and the final “WE DID IT” posts follow one another, but the record does not identify which particular call caused which pixels. Likewise, retrospective claims of alliances and treaties are participant accounts of what happened, not direct observation of the other communities' decisions.

## Posts against comments

Posts foreground decisive acts: “Let's work together” in `62n9hh`, “A coordinated defense is needed!” in `62ys9y`, and “Final push” in `6349s2`. Comments expose the work underneath—cooldowns, grids, corrections, limited space, bargains, apologies, and missing access to Discord. Thus the layers agree that collaborative work occurred, while comments make it look more improvised and disputed than the rally posts do.

The sharpest descriptive contrast concerns conflict. The post `62ys9y` presents Catalonia as an aggressor trying to destroy the human and Factorio; the comment `dfq47ce` presents a move-and-rebuild proposal with five people ready to stop. These are incompatible positions from different speakers, not proof of a settled community reversal. Similarly, the post in `6369ip` treats the portal pattern as hostile, while `dfrnfhp` says the “invasion” was a planned edit they mistakenly repaired and `dfrpknr` asks for a public target image.

Completion claims also differ by layer. Edited posts `6349s2` and `dfrw7wn` announce “WE DID IT,” while comments such as `dfsbja9` supply the social account—wars, treaties, alliances, collaboration—and dissenting comments continue to call the local posts spam. The post layer marks an outcome; the comment layer shows both how participants explained it and who objected.

## Counter-reading

My reading is: r/dwarffortress turned familiar figures, language, and jokes into shared canvas work, using Reddit and Discord to recruit, build, repair, negotiate, and defend it, then thanked participants and recounted a finished Placemurdered, while objections contested flooding, access, and scripts rather than erasing the collaboration.

A plausible competing account is that the apparent collaboration was chiefly disconnected image posting plus off-platform or scripted action, with Reddit participants neither sharing the plan nor recognizing the claimed agreements or final success. If my reading were wrong, the record should contain people refusing collective maintenance, repudiating Discord decisions or scripts as illegitimate, reporting unrecognized or failed truces, and describing the end-state as failure.

I searched the complete supplied record through `find` for its own vocabulary around spam and flooding, scripts and fun, Discord access, peace/truces/agreements, and completion/failure, then read the relevant returned items through `read item`. The strongest contrary item is `dfrdrbb`: “Im helping the void, this kind of r-place spamming is triggering me.” It shows that objection sometimes became active opposition, not merely a complaint. `dfsghhi` likewise asks to stop “a flood of unrelated content,” and `dfra4w6` asks, “What's the fun in having a script automatically write pixel art?”

This changes the account by ruling out consensus: some participants rejected the posts, scripts, or the canvas work itself, and one said they aided its destruction. What survives is the narrower claim of visible collaborative practice. `63182q` reports correcting errant pixels without joining communications while praising “those that are doing the team work”; `dfpke6i` reports Discord decisions alongside completed figures; `6349s2` moves from “40% there” to “WE DID IT GUYS”; and `dfsbja9` attributes the end to “So many people” working together. The failure search found no event passage describing the final display as a failure. Its strongest ambiguity was `dfpx5q5`, “We did it! EDIT: Almost...”, and the deleted-body post `633kne`, “It was a good run”; neither outweighs later explicit completion reports. This null result is limited to the supplied, partly removed record and cannot establish what absent speakers or unseen Discord participants thought.

## Saturation

Practice-level saturation is strong by the final slice. The first eight themes—calling people in, drawing, repairing, keeping plans findable, bargaining, Discord/script coordination, attack calls, and Dwarf Fortress storytelling—first appear in batch 02. The five-minute-wait singleton, posting/tool dispute, and recounting themes first appear in batch 03. Batch 04 extends established practices and introduces no new theme, while adding the clearest end account. A second grouping review after the counter-reading kept these boundaries: common words such as “Discord,” “help,” or “reply” were not enough to merge distinct acts of moving decisions, making plans visible, bargaining, and recruiting.

Record-level saturation is limited. All 198 threads were disposed and the pooled checks passed, but no one reader held the whole week: four coders read arbitrary slices, there is no agreement measure, and relations crossing 02|03 or 03|04 are weaker than a continuous single-reader account. Discord carries deliberation the record cannot show; Reddit preserves invitations, target images, scripts, returned plans, and participant reports instead. Deleted and removed bodies hide several prompts, although surviving titles and replies preserve narrow acts. Later ordinary threads show the subreddit returning to game talk, but the 97-hour window cannot establish what happened afterward.

## Selection

As case lead I read the briefing and all openings before the gate, using them only to locate the week's shape; I coded and cited nothing from openings beyond readable titles. The gate assigned branch B. Each fleet coder worked in corpus order, retained threads whose visible windows touched r/place or the room's own conduct, read retained long threads in full, and excluded ordinary gameplay, tutorials, arena administration, streams, and unrelated images. All read out-of-scope threads at or above the citation threshold retain their exact exclusion passage. After pooling, I read codes slice-by-slice beside each slice case and only then searched raw items for the counter-reading.

## Other communities named

Neighbors appear through what r/dwarffortress participants say and do, not as independently verified partners. N64 is welcomed after `dfoehfg` reports a help-for-noninterference agreement. SquareSpiral shortens its sign to leave room and is treated as a neighbor in `dfouvsw`. r/placeportalpattern and BOPP move between border concern and alliance; at the end `dfsh2ni` says members defended the BOPP diamond, and `dfs6jth` thanks BOPP as “great neighbors.” Catalonia is attacked and negotiated with in `62ys9y` and `dfq47ce`. Indonesia is first cast as an enemy, then offered rebuilding help and represented in a dwarf “to help ease tensions” in `637l8b`. An r/MMA visitor requests room in `63256p`; Vaporwave reports a negotiated truce in `dfrxf87`; Minecraft supplies a joint pattern in `6349s2`; and Factorio is called a buddy needing help in `dfqq89v`. The short r/armok name is created to lead viewers back to Dwarf Fortress in `62ujp3`.

Discord is the principal off-platform venue. `dfqpw77` says efforts and diplomacy are coordinated in its placedwarf room, while `dfrpsaw` and `637a55` show that some people cannot or do not want to use it. What returns to Reddit—plans, scripts, invitations, and reported agreements—is visible; the deliberation inside is not.

## Absence

Removed or deleted bodies conceal some event proposals, assistance requests, and alerts. Their surviving titles support only narrow acts, and no missing body was reconstructed. Image and link contents were not treated as observed unless a participant described them in text. Automated bot summaries and routing notices are platform or moderator-tool setting rather than ordinary participant conduct.

The record nevertheless preserves direct human passages for building, maintaining, negotiating, dissenting, and recounting. Absence is most consequential for Discord decisions and for threads such as `633kne`, whose title says “It was a good run” while its body is deleted: the phrase cannot safely be turned into either defeat or celebration. The supplied record is therefore sufficient for a full verdict about visible practice, but not for consensus, complete off-platform process, or the fate of every design beyond the window.

## The room's second-order themes

- t01 calling people in and showing them how to place
- t02 drawing and revising dwarves, signs, and neighbors
- t03 cleaning, repairing, and defending the pixels
- t04 keeping the work findable outside Discord
- t05 bargaining over borders and helping neighbors
- t06 moving plans through Discord and scripts
- t07 calling attacks, war, and strikes
- t08 turning canvas events into Dwarf Fortress stories and jokes
- t09 announcing the five-minute wait
- t10 arguing over place posts and pixel-writing scripts
- t11 thanking, celebrating, and recounting what they made

This is the end of the packet. Confirm you reached it by returning your lines and then the end marker the return specification names. END OF PACKET
