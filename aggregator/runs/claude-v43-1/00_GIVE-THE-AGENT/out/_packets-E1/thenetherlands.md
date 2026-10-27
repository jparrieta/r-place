# Reconstruction packet

Score, claim by claim of the coder's account below, whether the skeleton accounts for it, with the element id or `none`, one line per claim in the form the return specification gives. State unresolved evidence or stale versions in each affected claim reason. Pending or rejected lines are not asserted support; silence is not negative evidence. Report unresolved claim counts separately from contradiction. Reproduce the skeleton current model version and local status in the summary.

## The skeleton (the global model with supported local adaptations and explicit uncertainty)

# r/thenetherlands rebuilt from the global model (46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525) plus 67 adjudicated re-check lines

Adapted-local status: unresolved; grade: composes-with-residue; version status: current.
Return model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525; current model version: 46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525.
Unresolved adaptations: 0 (not asserted support).

[P01] The room calls its own members, and kindred subs, to come and place for a work: to start it, build it, finish it or hold it.  (['D01']; applies here: yes)
   instantiate   t03              Calls invite members to shared work and make the invitation actionable through coordinates and a planning destination.  [c0305,c0306,c0307]

[P02] The room settles what its mark will show of it: a member proposes a picture, the room argues its design, makes its land's flag or emblems the mark, signs it or leaves it unsigned, claims a mark others made, adds to it or enlarges it, or adds a personal piece to a shared mark.  (['D02']; applies here: yes)
   instantiate   t02              Participants propose national and regional marks and debate royal and anthem imagery as their representation.  [c0052,c0007,c0083,c0314,c0315]

[P03] The room builds its mark, and members report its state to the thread: what is placed, done or missing, and where.  (['D02']; applies here: yes)
   instantiate   t05              Participants report enlarging the flag and later announce anthem completion.  [c0070,c0236]

[P04] Members circulate a template that lays out the mark pixel by pixel, or coordinates that locate it, ask for them, and ask strays to keep to them.  (['D02']; applies here: yes)
   instantiate   t03              Coordinates direct helpers and a layout request seeks to prevent participants from overwriting one another.  [c0306,c0232]

[P05] The room keeps its placed work against erosion: members watch it and repair changed pixels, and the room rallies to defend it under attack, covers the night, hardens its shape and puts upkeep before growth. Repair restores the form the keepers know. A change the room has planned or agreed (P02) is therefore repaired away as damage until its keepers are told of it, and it is lost or given up where the telling does not reach them.  (['D03']; applies here: yes)
   instantiate   t04              Cleaning and night watch instantiate maintenance, while a self-overwriting complaint leaves the revised agreed-change and notification mechanism unresolved.  [c0072,c0238,c0394,c0232]

[P06] Members work out who changed their work and why: they trace placers and rooms, find friendly fire or their own mistake, blame officers, or disown placers acting in their name.  (['D03']; applies here: yes)
   instantiate   t03              A layout request attributes interference to self-overwriting rather than automatically treating changed pixels as hostile.  [c0232]

[P07] Rooms spare their neighbours' work, rein in their own attackers, apologise for damage and appeal to attackers to stop.  (['D04']; applies here: contested)
   instantiate   t07              Participants urge restraint because encroachment risks vandalism and useful work remains elsewhere.  [c0076,c0233,c0274,c0276]
   restrict      t11              Retrospective criticism of expansion is moral accounting, not by itself evidence that attackers were restrained while placement remained possible.  [c0391,c0395,c0396]

[P08] Rooms propose, settle and contest borders, truces and deals with neighbours by talk, through envoys, and hold each other to them.  (['D04']; applies here: yes)
   instantiate   t07              Visitors propose reciprocal limits and non-aggression while other approaches receive conditional refusal.  [c0077,c0080,c0241]
   add-condition t07              A truce refusal explicitly makes prior discussion in the planning chat relevant to receiving leniency.  [c0241]

[P09] Rooms attack others' work by the recurring moves the canvas affords: erasing, encroaching, converting a sign, raiding on a streamer's call, planting a script, altering a work as a joke.  (['D08']; applies here: yes)
   instantiate   t05              Calls seek flag conversion, reclaimed territory and removal of another community's flag without proving that each requested attack was executed.  [c0059,c0282,c0379]

[P10] After the work is erased or overrun, the room weighs fighting for the spot against moving, and moves: a new spot, a smaller version, a fresh start.  (['D04']; applies here: unobserved)
   absent                         Shifting toward one shared flag is proposed, but relocation after an overrun is not established by that suggestion.  [c0071,c0078]

[P11] When a work is up, the room marks it: announces it, celebrates it, credits makers and helpers, reports members' own parts and says what working with strangers meant.  (['D07']; applies here: yes)
   instantiate   t09              Participants celebrate anthem completion, present the final territory and take pride in shared contributions.  [c0236,c0380,c0387]

[P12] The room records what happened to its work and to the canvas around it: screenshots and timelapses, reports of its fate, mourning, imagined art, atlas entries, the end marked.  (['D07']; applies here: yes)
   instantiate   t09              An inventory and a timelapse preserve the final territory and its collective performance.  [c0383,c0393]

[P13] Near the close and after it, the room decides what of its temporary effort to keep: a later canvas, a new purpose for its canvas sub, the mark in its banner, ties with other rooms, the work remade elsewhere.  (['D07']; applies here: contested)
   instantiate   t10              Participants propose banner reuse and announce a new banner while placement is still underway.  [c0316,c0351]
   restrict      t10              Keeping the work can start during active placement rather than only near the close or afterward.  [c0316,c0351,c0380]
   add-step      t12              The museum plan requires turning the canvas into a specially printed and framed physical object rather than merely saving its pixels.  [c0412,c0413]
   add-condition t12              Physical reuse depends on personal funds and specialist printing, while a destination and completed exhibition remain unresolved.  [c0413,c0414]

[P14] Members add placements with scripts, bots and spare accounts, and the room argues over these machine hands and adjusts them.  (['D02']; applies here: yes)
   instantiate   t11              One retrospective contributor reports writing a bot to deploy alternate accounts after judging manual effort hopeless.  [c0398]

[P15] A member answers a call or proposal in one line that joins, assents, reports a part done or thanks, and the line asks for nothing back.  ([]; applies here: yes)
   instantiate   t03              A nested one-line promise to help accepts participation without asking for anything back.  [c0053]

[K01] The host sub is keyed as play for April Fools: members post fakes and takeovers under the one-day licence, and a claim in it, a call to the canvas included, may be a joke.  (['D06']; applies here: yes)
   instantiate   t01              A temporary positivity rule makes friendliness enforced conduct as well as play before moderators explicitly close the performance.  [c0029,c0004,c0256]
   instantiate   t06              Participants recognize, compare and object to other April Fools jokes beyond the moderator positivity rule.  [c0138,c0295,c0296]
   add-step      t01              A peer reminder to be kind elicits an apology, showing participants enforcing the temporary frame in replies.  [c0048,c0049,c0050]

[K02] The room judges that it has too few hands or too little room for the work it wants: doubt, a canvas judged too full, a work judged absent or outclassed.  (['D01']; applies here: yes)
   instantiate   t03              Repeated corrections consume effort needed to advance purple text, prompting a request for helpers rather than establishing collective defeat.  [c0074]

[C01] Most rooms worked on their marks without deciding how they were organized: a decided element of order (a leader, a vote, an oath, a sanction, a division of the work) is coded in 46 of 705 rooms (F-006).  (['D02']; applies here: unstated)

[R01] The starter: a member who proposes the mark, maps it or begins placing it. Others joining is not part of the role: it is the answer to the room's call (P15), in the order A02 and A01 state.  (['D02']; applies here: yes)
   instantiate   t02              A member proposes the Dutch flag, instantiating the starter independently of the later commitment to help.  [c0052]

[R02] The envoy: a member who acts for a room toward another room, carrying a proposal between threads or chats.  (['D04']; applies here: yes)
   instantiate   t07              A visitor explicitly represents Armenia while requesting a border and possible alliance.  [c0308]

[P16] Rooms help one another's works and trade help: they give pixels to a neighbour's mark, ask other rooms for help, barter help for space or repair, thank their allies, greet them, and turn requests away.  (['D04']; applies here: yes)
   instantiate   t07              Cross-border aid appears as promises, reported repair, requests and thanks without requiring every approach to succeed.  [c0234,c0240,c0266,c0309]
   link          t01              An aid appeal explicitly invokes the friendly day as its reason without documenting that aid was delivered.  [c0029,c0179]

[P17] Rooms join other rooms in coalitions: they meet in shared chats, form alliances, gather kindred rooms in a hub, tally kindred rooms' works and make joint marks.  (['D04']; applies here: yes)
   instantiate   t03              Organizing through a kindred subreddit and crediting related communities support a hub form of joint work without proving that every international alliance offer was accepted.  [c0213,c0318,c0353]

[P18] Rooms carry a contest with a rival room in talk: they trade taunts, flood the rival's threads, claim victory, salute the rival after the fight and blame attackers after the close.  (['D08']; applies here: yes)
   instantiate   t07              A visitor promises not to forget, while a banner announcement frames the work through opponents' blood and tears.  [c0288,c0351]

[K03] The community carries a quarrel from before the canvas into it: a rival sub, a sports or national rivalry, an old dispute.  (['D05']; applies here: unobserved)
   absent                         Canvas competition and exasperation about Germany do not independently establish a pre-event quarrel carried into the canvas.  [c0127,c0206]

[P20] The host sub draws a line around canvas talk: moderators gather it into a megathread, remove canvas posts by rule, change posting rules, pause the sub's usual events or disown the work; members open a canvas sub, object to the flood or argue the canvas's worth.  (['D06']; applies here: yes)
   instantiate   t08              Moderators redirect canvas requests and later posts to preserve ordinary subreddit use.  [c0349,c0406,c0410]

[K04] The room acts as a body it was before the canvas, or as a faith in a colour: it argues the nation's history, belonging and politics beyond its flag, carries in the sub's quarrel, lore, jokes or ideology, or professes and spreads a colour.  (['D05']; applies here: yes)
   instantiate   t10              Participants debate national self-presentation through royal and anthem imagery rather than only filling a national flag.  [c0314,c0315]

[P19] One room's work lives on another room's mark or territory under the host's rule: guests ask for space or protection, hosts rule on requests, and both sides dispute who may approve.  (['D04']; applies here: yes)
   instantiate   t07              Requests to place a guest name above the anthem elicit warnings and clarification, supporting the request-stage range rather than demonstrating installation.  [c0358,c0359,c0360,c0361]
   instantiate   t09              A retrospective account reports goodboye integrated into the canvas and describes help on its left dog as a compromise.  [c0387,c0389]

[C02] In some rooms, a tie the room had before the canvas (a league or school rivalry, a nation's history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack.  (['D08', 'D05']; applies here: yes)
   instantiate   t02              The appeal to place MH17 on the Russian flag names a historical reference and a target together without explaining every canvas conflict.  [c0371]

[P21] Members dispute, or state the limits of, who may commit the room to an agreement with other rooms: they say that one member's agreement does not bind every placer, deny that a treaty speaks for them, or ask another group for a leader to deal with.  (['D04']; applies here: unobserved)
   absent                         Prior consultation is invoked in a truce refusal, but no cited item states limits on who may bind every placer.  [c0241,c0308]

[P22] After placement ends, members contest which version of the canvas and of the event is kept: they ask a cleanup of a shared copy to fix their work, take part in it, argue that the cleanup should keep the damage as history, and correct accounts of the event that describe their group wrongly.  (['D07']; applies here: yes)
   instantiate   t09              After closure, participants value imperfections as collective authorship and challenge a celebratory account by naming harm to other communities.  [c0390,c0387,c0395]

[P23] Members move the room's planning into a chat, an existing server or a new one, and invite helpers to it. They bring the chat's designs, decisions and warnings back to the thread. They argue which chat to use, whether a chat is needed or secure, whether it is official, and whether it may decide for the work or bind placers.  (['D02']; applies here: yes)
   instantiate   t03              Participants invite helpers into planning chats, report a chat plan and request the official server, without exposing the internal decision process.  [c0082,c0231,c0235,c0341]
   add-step      t08              A moderator routes fast discussion and diplomacy to different chat destinations, distinguishing operational functions from the right to post in the host.  [c0321,c0322,c0349]
   link          t03              Recruitment offers access to shared plans by directing helpers into the planning chat as part of the invitation.  [c0305,c0307,c0341]

[P24] Members ask what the canvas is, how to place, what a call or a name means and what a picture shows, and others explain the rule, the timer, the controls, whose mark a picture is and what happened. They ask before, during and after the close, and some questions get no answer.  (['D01']; applies here: yes)
   instantiate   t10              A question about the canvas receives an explanation of the five-minute pixel rule within the ordinary social thread.  [c0312,c0313]

[P25] The room's work brings people into the room. A viewer finds the sub through the mark or through a sign written to that end, a member of an ally comes through joint work, and a lapsed member returns. Members welcome them, explain the room's subject, take them into its usual activity, count the new subscribers and argue how to receive them.  (['D07']; applies here: unobserved)
   absent                         Visitor thanks do not identify canvas-driven arrival, subscription or return to the host community.  [c0319,c0309]

[P26] Members make new jokes out of the canvas work, its mistakes, its damage and its neighbours: puns on the mark, mock names and titles for a figure, and jokes about attackers and bots. The room takes the jokes up, and some members want a joke kept in the work.  (['D05']; applies here: yes)
   instantiate   t07              An invasion joke and a blood-sweat-tears banner turn canvas work and its neighbours into comic material.  [c0294,c0351]

[P27] Before any loss, the room chooses where to put its work and changes the spot while it builds. It looks for open room, weighs a crowded or contested place, shrinks or moves the design ahead of a neighbour or the void, restarts a misplaced start, and refuses to move once enough pixels are in.  (['D04']; applies here: yes)
   instantiate   t05              Participants identify open space, suggest shifting toward one shared flag and propose reducing its footprint without documenting relocation after defeat.  [c0276,c0071,c0335,c0336]

[P28] A room forms for the canvas around a mark. Members open a sub or a chat for a pattern or a figure and set it up. They invite the people seen building or copying the mark, give it a meaning its followers share, gather its repeaters into a group that can negotiate, and move or split the room.  (['D05', 'D06']; applies here: not-testable)
   absent                         Dedicated chat invitations and a faction-subreddit question establish destinations but not who founded a new mark-centered collective or how it formed.  [c0277,c0307,c0354]

[P29] Members argue whether a joke, a taunt or a word in canvas talk offends, and they refuse slurs and hate symbols. They object, correct, apologise, remove the words or tell the speaker to leave, and they cover swastikas or refuse to draw them.  (['D05']; applies here: unobserved)
   absent                         An unexplained request to remove the VOC logo and a host-language complaint do not establish a canvas-specific dispute about offensive words or hate symbols.  [c0242,c0259]

[P30] The room turns its work toward people outside the canvas whom the mark shows or addresses: the creators, the team, the streamer, a company or the press. It shows them the work, hopes for their notice, shares the coverage and celebrates their acknowledgement, or it keeps the work from troubling them.  (['D07']; applies here: unobserved)
   absent                         Imagined royal pride does not document outreach to, hoped-for notice by, or acknowledgement from the represented person.  [c0324]

[P31] Members argue whether covering others' work is fair. Some call it betrayal, dirty or a cost to the room's name. Others answer that change is the canvas's point, that wiping makes room for new art, or that the canvas is a game of conquest. The argument runs during the work and after the close.  (['D04']; applies here: yes)
   instantiate   t11              Participants oppose expansion, report harm to other communities and regret its consequences during work and retrospective moral accounting.  [c0240,c0395,c0397]

[P32] A member steps away from the work under strain, or the room repairs a quarrel between members. The work turns stressful or personal, or a member is criticised or yelled at over a pixel or a proposal. Others rebuke the harsh speaker, the speaker apologises, or the member threatens to leave or leaves.  (['D01']; applies here: unobserved)
   absent                         Correction strain and a separate host-kindness apology do not establish a canvas worker quitting or repairing a pixel-work quarrel.  [c0074,c0049,c0050]

[P33] Rooms keep their plans from rivals who read their threads, and they reach into rivals' venues. Members switch to their own language or write in code, move the plan to private messages, plant members in a rival's chat and warn of a snitch in their own.  (['D02', 'D08']; applies here: unstated)

[P34] Members who object to the canvas posts in the sub turn against the room's own mark. One member says the posts make them tear down the logo, and one recruits trolls to ruin the flag.  (['D06']; applies here: unobserved)
   absent                         Moderators redirect canvas traffic, but the cited items do not show members attacking their own mark because of that traffic.  [c0349,c0410]

[K05] Members place on their own time and with their own devices. They fit placing around sleep, study, exams, work and travel. They cannot place from a phone or while away, they leave when the wait is too long, they save pixels under the timer, they find the work addictive, and they report what it cost them.  (['D02', 'D07']; applies here: yes)
   instantiate   t10              Placing competes with studying and depends on members' availability, including overnight watch from another location.  [c0311,c0238,c0388]

[K06] The site sets what members can do, and members report its faults and pass on fixes. They report a blank or stale canvas, the site down, a vanished or faulty timer, glitches that seem to give extra pixels, captchas, the official app required and the site blocked in a country. They refresh, update, keep a separate window and test whether extra pixels reach the canvas.  (['D02']; applies here: unobserved)
   absent                         Explaining the ordinary five-minute timer does not establish a site fault or a corrective workaround.  [c0313]

[K07] Some members belong to both rooms in a contest or at a border. They say they are torn or proud of both, and the room reassures them or still counts them as its own.  (['D04']; applies here: unobserved)
   absent                         A coexistence request and friendly descriptions of neighboring groups do not establish a speaker belonging to both sides of a contest.  [c0302,c0268]

arrows in the model: 21

[A01] P01 -> P03 (order): The room's call brings members to the canvas, who then build the mark and say how far it has come.
   absent                         Recruitment and building reports occur, but the cited record does not trace which recruits built the work.  [c0305,c0070]

[A02] R01 -> P01 (order): A member who proposes or begins a mark gives the room something to answer, and calls for hands gather around it.
   instantiate   t02              The flag proposal supplies a shared object around which a later call directs continued red and blue expansion.  [c0052,c0057]

[A03] P03 -> P05 (order): Once a mark stands on a surface anyone can change, keeping it becomes the work: a finished part is something to lose.
   instantiate   t04              A report of enlarging the flag receives a reply describing continual cleaning as ongoing work.  [c0070,c0072]

[A04] P05 -> P08 (order): Keeping a mark against erosion brings the room up against the neighbours whose pixels erode it, and the room turns to talk with them.

[A05] P08 -> P07 (order): A settled border gives the room a line to keep: members spare the neighbour's work by it and remind others of it.

[A06] P05 -> P14 (order): Upkeep under attack outruns what one pixel per interval can hold, and members turn to scripts and spare accounts to keep up.
   absent                         An individual retrospective bot account does not establish upkeep as its specific trigger or automation as a cause of territorial success.  [c0398]

[A07] P03 -> P11 (order): A mark reported done gives the room a finished thing to point at, and the room marks it together: announcement, credit, pride.

[A08] P11 -> P12 (order): Marking the work together turns the room toward keeping it: members ask for the final image, the timelapse, the list of what changed.

[A09] P12 -> P13 (order): A record of the work gives the room something to carry: the image into the banner, the plan into the next canvas.
   absent                         Banner reuse begins during placement, but the cited proposals do not identify whether a saved image prompted it.  [c0316,c0351,c0380]

[A10] K02 -> P10 (order): A room that judges it has too few hands to hold its spot stops fighting for it and moves.
   absent                         Shifting toward one shared flag does not demonstrate shortage causing retreat and relocation after loss.  [c0071,c0074]

[A11] P02 -> P04 (transition): Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel.
   absent                         Coordinates and a layout request do not demonstrate a design argument settled by an agreed pixel template.  [c0306,c0232]

[A12] P01 -> P15 (transition): A call is the first part of a pair: posted to a thread, it makes an answer from each reader the next thing due, given in the thread or by placing. Joining is the answer the call prefers, so it comes bare, one line that commits and gives no reason ('I'm in'); declining is the dispreferred answer and, in conversation analysis, comes with a reason. In the written record a bare join is the ordinary way a call is accepted (25 of 31 read acceptances, F-023); a member can also accept by placing and write nothing, which the record cannot show.
   instantiate   t03              A bare promise to help answers a flag proposal within its reply tree without establishing the general preference or refusal claims.  [c0052,c0053]

[A13] P05 -> P16 (order): A room keeping its work under strain runs short of hands and turns to other rooms for help, and other rooms send it.
   absent                         Moral repair and a threatened artwork's help appeal do not establish Dutch defensive shortage causing reciprocal assistance that was actually sent.  [c0240,c0348,c0349]

[A14] P08 -> P16 (order): Talk over a border opens a channel through which the two rooms then trade help: room for upkeep, pixels for protection.
   absent                         Armenia's border request and later thanks are separate posts whose sequence does not establish negotiated exchange terms.  [c0308,c0309]

[A15] P01 -> P09 (order): A call brings members to the canvas, and some of them turn its hands against a rival's work instead of, or before, building the room's own.

[A16] P09 -> P07 (order): A call to attack makes an answer from the room due in its thread. Members who do not want the attack refuse it, rein in the attackers or apologise to the target; refusing is the dispreferred answer, so in written replies it usually comes with a reason (23 of 38 read pairs, F-014), and the reason states the room's norm or the attack's cost ('Nah, keep /r/place neutral.'; 'Why? That'll just cause them to want to attack us').

[A17] P09 -> P08 (order): A call to attack is met by the room's relations with its neighbours: the room invokes a truce, or proposes a deal instead.

[A18] P09 -> P18 (order): An attack makes the rival a named party, and the contest is carried on in talk: taunts, chants, claims of victory, a salute after the fight.

[A19] P05 -> P17 (order): A room keeping its work against attack joins other rooms whose works face the same threat, and they defend each other's works together.
   absent                         Kindred organizing and an alliance proposal do not establish a shared defensive threat causing coalition formation.  [c0213,c0318,c0353]

[A20] P01 -> P20 (order): Calls to the canvas flood the host sub, and its moderators or members answer by drawing a line around canvas talk: one thread, removals, a canvas sub.
   instantiate   t08              A canvas help request receives a moderator redirection to keep ordinary subreddit use possible.  [c0347,c0349]

[A21] P08 -> P21 (order): An agreement made with another room in the room's name puts its members' compliance in question. Members who did not make it say that it does not bind them, or refuse it, or say that no one can bind every placer.
   absent                         A truce refusal over prior consultation does not establish an agreement followed by a stated limit on who can bind all placers.  [c0241,c0308]

## The coder's account

## Chronology

The record opens with ordinary discussion already under way, then the community abruptly remakes its own room. At H+0.29 moderator potverdorie announces “Alleen maar heilzame content en positiviteit” in `62m6c1`; members answer with compliments, pets, hearts, “vriendo” language, mock enforcement and wordplay. This first episode runs from `62m6c1` to the moderators’ “terugkeert naar de orde van de dag” retrospective in `62totb`. It is an April Fools practice of the subreddit, not canvas work, and its opening and early enactment come from batches 01–04 while its explicit closure comes from batch 05.

Canvas work starts alongside that performance. At H+1.82 the post `62ms9a` proposes “een grote Nederlandse vlag”; by `62n832` participants are enlarging and cleaning a flag, writing the Wilhelmus, negotiating borders, watching threats and using Discord “om af te stemmen waar we eigenlijk mee bezig zijn” (`dfou5rc`). Across batches 02–05, the work broadens from flags and lettering into calls for an orange line, night watch, repair, expansion and arguments over Greece, Sweden, Denmark and Armenia. The episode’s visible bounds are `62ms9a` and the repair pledge `dfpa470`; the latter says energy spent fighting Greece is a waste and “ik ga ze ook helpen.”

After the moderators end the heilzaam day, r/place becomes one topic among the subreddit’s ordinary traffic. Batches 06–11 show recruiting, image proposals, border requests and short calls continuing while moderators increasingly route fast discussion, diplomacy and “these requests” to specialist subreddits and Discord. This middle episode runs from the recruiting and ordinary-talk cluster in `62w7hj` to the final active-canvas requests in `6377bs`. Slice cases, rather than one whole-week reading, supply this stretch; many posts survive only by title.

At H+73.16, after placement ended, `6384js` presents “Het Uiteindelijke Nederlandse Territorium.” The discussion celebrates maintenance, shared imperfections, posters and timelapses, but it also revises the triumphal account: `dfsja64` says “we hebben het ook voor enkele andere subreddits verkloot,” and `dft0s2e` describes an “out of control mob” that “just wanted to expand.” This retrospective episode runs from `6384js` through the alt-account bot account in `dftk7jt`.

The room then returns mostly to ordinary subreddit business. The event’s last development is not more pixel placement but a keepsake plan: in the monthly roundup `63d73s`, `dftcfkq` asks how the museum plan is going, `dftk6us` says specialist printing will take at least a month, and `dftkf3t` asks which museum. That unanswered question is the case’s final edge.

## Relations — what set off what

The moderator rule produces some later posts by explicit reference, not merely by order. Under a cute-image post, `dfnr09o` tells a critic “Lees de nieuwe regel even na ;)” and links back to `62m6c1`, 97.2 minutes after the announcement. The later passage identifies the rule it is enacting. [crosses 01|02]

The moderators also explicitly close that practice. `dfp2q0z` says that after 24 hours “we zijn weer back to business,” and `dfp3ksu` redirects a late “subreddit-Segel” to the closing thread. These turns answer continuing wordplay from the preceding slice rather than proving that every member stopped at once. [crosses 04|05]

Within the canvas work, participant explanations support local responses but not a single causal story for territorial growth. `dfp1wso` says “please stop invading Greece” and calls it unnecessary vandalism; `dfpa470` later says the fighting prompted them to help Greece. That is a participant’s stated reason for their own repair action, not evidence that the community as a whole reversed course. Conversely, separate expansion posts that merely follow one another are a sequence, not proof that one caused the next.

Moderation visibly redirects, rather than ends, coordination. `dfqdapo` calls on Dutch readers to restore a threatened artwork; 3.8 minutes later `dfqdgi8` answers “these requests” by directing them to r/PlaceNL, r/Cirkeltrek or Discord so the subreddit can be used normally. The wording supplies the link; the corpus does not show whether everyone complied.

The museum exchange is the clearest late call-and-answer. `dftcfkq` asks for progress, and 148.2 minutes later `dftk6us` answers “Duurt minstens een maand” and explains the cost and specialist printing. Four minutes later `dftkf3t` asks which museum. The first relation is supported by a direct answer; the final sequence remains open because no answer is recorded.

## Posts against comments

In batch 02, sweet post titles present uncomplicated wholesomeness, while comments also test it: `dfnqjeb` adds “Soa's ook” beneath “Verspreid de liefde.” The posts say positivity; the comments perform it, parody it and sometimes resist it. [batch 02]

Canvas posts commonly issue clean proposals—draw, expand, defend, finish—while comments contain the operational uncertainty and disagreement. The post `62ms9a` says to make a large Dutch flag; its comments supply dimensions, labour, threats and a later venue shift. In batch 05, expansion-oriented posts coexist with the comment `dfp1wso`, which calls the move into Greece “unnecessary vandalism,” and `dfpa470`, which promises repair. The layers therefore show competing positions, not a demonstrated change of collective mind. [batches 02 and 05]

Later posts keep soliciting action while moderator comments constrain where it belongs. `dfqdapo` asks for defence; `dfqdgi8` sends such requests elsewhere. Here the post layer recruits and the comment layer polices the venue. [batch 09]

The retrospective posts frame a finished national achievement—most plainly `6384js`, “Het Uiteindelijke Nederlandse Territorium.” Comments celebrate that achievement but also disclose costs and methods that the post layer does not: `dfsja64` names harm to other subreddits, `dft0s2e` describes uncontrolled expansion, and `dftk7jt` describes writing a bot to deploy alt accounts. [batch 12]

## Counter-reading

My reading is that this case is not simply a national flag project: participants alternated between remaking the subreddit as a one-day friendly space and coordinating, defending, expanding, negotiating, then commemorating Dutch canvas work.

Before searching, I specified the consequential competing account: the apparent cooperation and friendly self-presentation concealed a primarily aggressive, bot-assisted territorial project. If that account were stronger, the corpus would contain participants explicitly describing conquest, damage to smaller communities, bot use, or rejection of restraint as central rather than exceptional.

The strongest contrary item is `dft0s2e`. After consulting Discord logs, its author says organisers “just wanted to expand,” calls the result an “out of control mob,” and explains that nearby Puerto Rico “should NEVER have been attacked.” A targeted search for participants’ own terms—expansion, invasion, griefing, ruined subreddits, bots and alt accounts—also returned `dfosy98` (“Terugpakken en uitbreiden! ... VOC mentaliteit”), `dfsja64` (“voor enkele andere subreddits verkloot”) and `dftk7jt` (a bot deploying alt accounts). I read each returned item rather than treating matches as a result.

This evidence changes the weight of the account: aggression and automation were not just outsiders’ accusations, and territorial success depended partly on conduct some participants later regretted. It does not erase the separate heilzaam practice, the direct repair and restraint passages, the negotiations, or the moderator routing. The supported conclusion is coexistence and conflict among practices, not a claim that the community changed its mind. The targeted search found no new uncoded contrary practice; its scope was the case vocabulary above, not proof that other missing material would agree.

## Saturation

Thematically, later slices both repeated and extended the early practices. “Making the subreddit heilzaam for the day” and “putting Dutch and local marks on the canvas” first appear in batch 01; “joining and directing the shared pixel work,” “watching, cleaning and restoring the work,” “pushing the flag and orange line outward,” and “playing and spotting other 1 April jokes” first appear in batch 02; “making and answering requests across canvas borders” first appears in batch 03; “keeping place traffic within subreddit rules” first appears in batch 04; “celebrating and recounting what the canvas became” first appears in batch 05; “working r/place into ordinary subreddit talk” first appears in batch 06; “questioning expansion and accounting for harm” first appears in batch 12; and “carrying the finished canvas into a museum print” first appears in batch 14. Thus the main live-event practices settle early, but the late retrospective critique and museum follow-through are genuinely new practices rather than repetitions.

As a record, the census is broad but not venue-complete. Removed bodies and unavailable images make many short calls recoverable only from titles; Discord, r/cirkeltrek and r/PlaceNL are visible as chosen organising destinations, but their deliberations are not. The final retrospective thread continues late, and the museum question remains unanswered. In branch B no reader held the whole week, one coder read each arbitrary slice, and there is no agreement measure. Relations assembled across slices are therefore weaker than a single whole-case reading; the forest reveals reply order and intervals, but adjacency alone is not causation.

## Selection

The gate selected branch B, so I read the brief and openings before dispatch but did not code from the openings. Fourteen coders disposed whole-thread slices in corpus order. They retained explicit r/place conduct and the subreddit’s own April Fools practice, while excluding ordinary news, advice, politics and social threads unless the served text recruited them into either practice. After consolidation I read the pooled codes one slice at a time beside the slice cases, built themes incrementally, then used raw-item reading only for the counter-reading stage. Slice boundaries were arbitrary with respect to the material, and context openings could show an exchange to two coders without giving either the whole week.

## Other communities named

The community treats r/place as the work site and later as the source of the museum proposal. r/cirkeltrek, r/PlaceNL and several Discord channels become destinations for planning, fast discussion and diplomacy; Reddit retains invitations, redirects, plans and reports, but not the deliberation inside those venues. Sweden, Greece, Armenia and Denmark appear variously as neighbours, allies, requesters, targets and recipients of repair. Other named groups—including r/NintendoSwitch, r/Overwatch, r/goodboye and the Starry Knights—enter through claims about threats, protection, integration or damage. These are Dutch-side pointers and accounts, not reciprocal evidence from the named communities.

## Absence

Removal is substantial but patterned rather than total. Many small canvas posts lose bodies or linked images while titles still preserve narrow acts such as asking, proposing, expanding or thanking; surviving comments sometimes recover coordinates, disagreement, moderation or repair. Deleted material cannot establish the missing proposal details or outcomes. The most consequential gap is off-platform: `dfou5rc` explicitly says participants are coordinating on Discord, while later comments report Discord logs and singing, but the live decisions are unseen. The case therefore supports what returned to Reddit and what participants said about the move, not a reconstruction of the hidden venue.

## The room's second-order themes

- t01 making the subreddit heilzaam for the day
- t02 putting Dutch and local marks on the canvas
- t03 joining and directing the shared pixel work
- t04 watching, cleaning and restoring the work
- t05 pushing the flag and orange line outward
- t06 playing and spotting other 1 April jokes
- t07 making and answering requests across canvas borders
- t08 keeping place traffic within subreddit rules
- t09 celebrating and recounting what the canvas became
- t10 working r/place into ordinary subreddit talk
- t11 questioning expansion and accounting for harm
- t12 carrying the finished canvas into a museum print

This is the end of the packet. Confirm you reached it by returning your lines and then the end marker the return specification names. END OF PACKET
