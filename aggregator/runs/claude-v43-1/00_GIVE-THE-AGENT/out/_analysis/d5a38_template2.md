# Room form C, the design and its marking: the form account

Written at D5a-38, 27 October 2026. The model is the version frozen at D3 (46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525). Form C is one of the six room forms of the cut J ruled at D4a-08 (`room-forms-D4a08c.*`); how every room reaches its form is in `room-forms-allocation.md`. It holds 125 of the 705 analysed rooms. 96 are defining rooms: rooms with 5 or more selected changes, which shaped the form. 27 are thin rooms (1 to 4 selected changes) and 2 are core rooms (no selected change), placed afterwards. Thin and core rooms weigh less: every share, signature, theme count, representative choice and split below is read on the 96 defining rooms, and the thin and core rooms are named in section 15.

A room form is not a branch: it gathers rooms by the whole mix of their changes (two thirds) and their codes (one third), and the 35 branches are the level below it (section 12). The form is a pole of a continuum: 28 of its 96 defining rooms lie nearer another form's centre (section 13). This file sits beside the room-forms files, not in `forms/`, because the stage's close-check reads every account in `forms/` as a branch account (`departures.jsonl` line 18). Hours are counted from the start of the event (h+).

## 1. How these rooms organized, as a narrative

In these 125 subreddits much of the talk was about what the mark should show. Members proposed a picture, argued its colours and its size, held polls, and changed the design while they built it. The design was seldom settled for good. When a part was finished, someone proposed the next.

The work began with a proposal. "Lets get r/cubers into the pixel art going on at r/place. How about this design?" [cubers/c0018]. The design had to fit the hands the room had. A r/bardmains member wrote, "since we don't have THAT many people, I think something small like this is okay." [bardmains/c0006]. A r/esperanto member found the room had gone too big: "Yup. Seems like we went too big. This subreddit doesn't have enough people to do this properly :/" [esperanto/c0013]. It had to fit the canvas too. A r/hongkong member wrote, "removed 3 rows to not have to overwrite FREEUAB to the north. Now a 29 width x 26 height rectangle." [hongkong/c0030].

Members argued over details, and some tried to settle them by vote. In r/AMD: "Stop changing the color of the arrow! There is a strawpoll. Let's settle this and all get on one page." [AMD/c0277]. A r/aggies member was told to decide quickly, "because it is really ambiguous whether this is an attack by trolls/takeover." [aggies/c0132]. The organiser decided for the night: "Im just going to make it a white line get people unified and if they hate it it can be discussed tomorrow." [aggies/c0134]. Some choices were made by what was already on the canvas. Asked about a darker orange, the member who had started the r/bardmains mask answered, "Way too late to switch colors. We stayed with yellow just because there was a preexisting yellow blob when we started." [bardmains/c0015]. Members planned the order of the work so the design would hold while it changed: "Maybe if we change the letters to white first, so it still contrasts, then switch the black to blue." [sheffield/c0041].

A change to the design met the room's own keepers. In r/cubers a member proposed a wider cube, "Let's upgrade!" [cubers/c0169]. A builder found that "people think I'm just messing with it" [cubers/c0172], and gave up: "Yeah I gave up. I think some people like the newer design, but others are happy with the way it is, so I guess it stays." [cubers/c0173]. In r/trees: "Trying to get a bigger pattern going on the pineapple, but everyone keeps 'fixing' it" [trees/c0351]. In r/vegan a member saw new pixels removed "because some will think it's sabotage, so for now let's just aim for the 3-pixel G." [vegan/c0190]. Not every keeper who undid a change was uninformed. A r/FlaggyFlag member had seen the change and reversed it: "I tried this a little while ago, and it doesn't look good with the white part, so I started changing it back to blue." [FlaggyFlag/c0008]. A r/uvic member, asked whether to change the logo, answered, "I like what we have right now. I think it should stick" [uvic/c0052].

When the work was up, the rooms marked it, and often started again. "We built one logo. What does r/factorio do when we finish a build? We make a new one twice as big!" [factorio/c0058]. A r/gatech member celebrated, "We Did It Guys! /r/Place will Forever have our Mark!" [gatech/c0070], and the next reply proposed more: "Now let's write r/gatech above it" [gatech/c0071]. At the close a r/bardmains member wrote, "It ended and someone put a red point in Bard's eye so we can't fix it *face palm*" [bardmains/c0072]. Another answered, "Still proud of what we made together though!" [bardmains/c0075].

## 2. What the form does

These elements are instantiated in 80 per cent of the defining members or more (`_analysis/d5f_model.py`, current ledger, particular lines included). The model's prose says them so.

{{INSTANTIATED}}

The model has the room settle what its mark shows (P02), circulate a template (P04) that settles the design in a thread (A11), build it (P03), keep it (P05) and mark it when it is up (P11). These rooms do all of it. The difference is not in which elements they hold: P02 is instantiated in all 96 defining members, and in 99.5 per cent of the 558. It is in what they change.

## 3. What it does differently, element by element and arrow by arrow

**The change signature.** The form's defining members change one fourth-order theme more than the defining population does (at 1.5 times its share or more, in a third of the members or more): Collective representation, the theme of what the mark shows. 97.9 per cent of them change it, against 52.7 per cent of the 558 (share ratio 2.63). It is the clearest single lean of any form so far.

**Element by element and arrow by arrow.** The table gives every element or arrow and op that 14 defining members or more change, at 1.2 times the defining population's share or more (`_analysis/d5f_facts.py`). A selected line specifies the model (add-condition, add-step), restricts it (restrict), connects two of its parts (link) or contradicts it. The kind of a line is not relied on (J: kappa 0.08).

{{ELEMENTS}}

{{CONTRADICT}}, so these rooms replace nothing in the model. I read the lines behind the table whole (`_analysis/d5f_dump.py`: 113 lines on the design, keeping and templates).

- **P02, the design: specified (add-step 21 members, 22 per cent against 11) and connected (link 19).** The added steps are how a room settles a design for now: a poll, a provisional choice made overnight, a design sequenced so it holds while it changes, a design sized to the hands. r/aggies: "An organizer fixes a provisional design overnight and defers reconsideration instead of waiting for a completed vote." r/bitcoin: "The work is sequenced into logo, lettering and background to reduce simultaneous pixel demands." The links run from a finished part back to design. r/factorio: "A finished mark explicitly warrants making another larger one, returning completion to design and planning rather than only toward preservation." r/criticalrole: "Celebrating completed lettering is followed by d20 and logo proposals, so a finished stage can reopen design work."
- **P05, keeping: restricted (46 members, 48 per cent against 37).** Nearly every one of these lines restricts P05's telling clause: a change the room planned is repaired away until its keepers are told of it. Two things recur. Informed members disagreed with the change, so telling them would not have settled it. r/hentai: "Telling keepers about a redesign cannot alone secure it when informed participants explicitly oppose the temporary change's risk." r/calvinandhobbes: "Conflicting repair cannot be attributed solely to uninformed keepers when participants explicitly disagree about the intended design." Or the record does not show what the keepers knew. r/earthbound: "The information-deficit mechanism requires evidence of keeper knowledge because different repair targets alone cannot distinguish ignorance, dissent, or behaviour after an instruction."
- **A11, from design talk to a template that settles it: restricted (58 members, 60 per cent against 48).** Section 7 reads these lines: the template did not settle the design.
- **P04, the template: specified (add-step 22 members).** Keeping the template current: retiring old posts, reconciling rival corrections, messaging those who overwrite. r/tf2: "Standardization includes retiring outdated posts, announcing changed locations and stopping work on obsolete outlines."
- **P01, the call: connected (link 14 members).** A call returns after a finished part or a move.

**What the model would not predict.** The model has a template settle a design in a thread, and keeping restore the form the keepers know until they are told of a change. In these rooms the design is settled for a time and then reopened, often after each finish. And the telling clause meets disagreement as well as ignorance: some keepers knew of the change and did not want it. Each of the 46 lines that restrict P05 restricts its telling clause, and none of them shows a change lost only because its keepers were not told; they say that telling was not enough, or that the record cannot tell ignorance from dissent.

The rooms that show the form best, by the rule in section 11, are r/cubers and r/PUBATTLEGROUNDS; the one that shows it least well is r/kuwait.

**What the claim rests on.** The form is a cut of the allocation (changes two thirds, codes one third, Ward's method, six forms by J's ruling). Its stability on matched subsamples is about 0.21, and 28 of its 96 defining rooms lie nearer another form's centre. The table's counts are the ledger's. That members argued, settled and reopened their designs, and that keepers knew of changes they undid, is a claim on their words, through `cite.py`, in sections 1, 4 and 11.

**The name, read against the members.** The name is "the design and its marking". The strongest argument that it names the cut rather than what the rooms did: the form has one signature, collective representation, and the name restates it. A reader who suspected the name would look for members whose record is not about the design. The least fitting member, r/kuwait, is about where to put a flag, not what it shows (section 11). But 97.9 per cent of the defining members change the design's theme, and the marking appears in the links from a finished part back to design. The name holds. I make no renaming proposal. One sharpening goes to `notes-D5.md`: the design settled for a time and reopened.

## 4. The concepts it employs

First-order concepts for each change the form leans to, through `cite.py`:

- **The design proposed and sized.** "I'm not an excellent pixel artist, and since we don't have THAT many people, I think something small like this is okay." [bardmains/c0006].
- **The design settled for now.** "Im just going to make it a white line get people unified and if they hate it it can be discussed tomorrow." [aggies/c0134]. "We're heading in this direction unless people are opposed." [bardmains/c0084].
- **The design reopened after a finish.** "We did it Reddit! (Again)" [factorio/c0071]. "Now let's write r/gatech above it" [gatech/c0071].
- **A change repaired away.** "Tried to do the same, but people think I'm just messing with it" [cubers/c0172].
- **A change refused by those who knew of it.** "supposedly we had agreed to with Bulgaria. I even posed a mockup but then at least one person was like "we don't want it like that" so I gave up and deleted the posts." [cubers/c0309].
- **The template kept current.** "this post is out of date, follow the design of the stickied post or visit the discord" [tf2/c0297].

## 5. Composition here

Three judgments are kept apart.

**The original global model (historical).** `verdicts-D.jsonl`, by the last analyst ruling or else the readers' agreement. All 125 members: {{VERDICTS}}. The 96 defining members: {{VERDICTS_DEF}}. The two that cannot tell are thin rooms, r/bigbang (2 selected changes, 3 coded concepts) and r/watchmen (1, 2). These verdicts describe the unadapted model at the first return.

**The adapted local accounts.** By `adaptation-returns.jsonl` and the current model hash (46384686), as `vlib.local_return_states` reads them, all 125 members are unresolved; none is validated and none has insufficient evidence. The limit D3 named is the same for each: the labelers marked every local account unresolved, and prior.md section 3's measure of local validation was not computed (J after the D3c interview). The unresolved members are:

{{UNRESOLVED}}

**The shared form explanation: supported as a lean, unresolved as an explanation.** One change binds nearly every defining member: 97.9 per cent change collective representation, the most uniform signature of the six forms so far. The changes say what the model does not: the design is settled for a time and reopened, and keepers undo changes they know of as well as changes they do not. But the same changes are frequent in the population (52.7 per cent), 28 of the 96 defining members lie nearer another form's centre, and every member's own adapted account is unresolved. A verdict of composes with residue on the original model is not a current local or shared failure.

## 6. How the model runs here

Counts are of defining members with a current-ledger line, particular lines included (`_analysis/d5f_model.py`); they count any line of an op.

**The elements that do the work.** The elements of section 2. P27, choosing the spot before any loss, is instantiated in 76 of 96 (79 per cent), against 72; P06, working out who changed the work, in 90 (94 per cent), against 87.

**The elements that sit idle.** P34 is absent in 95 of 96 defining members, P30 in 90, P33 in 88, P28 in 81, P29 in 80, K07 in 74, A21 in 73 and K03 in 68. They are idle in the population too, and their idleness does not mark the form.

**The elements that fit less here.** P22, contesting which version of the canvas is kept after the close, is instantiated in 20 of 96 (21 per cent), against 32 per cent of the 558. These rooms argued their design during the work more than after it.

**What these rooms do that the model has no place for.** 33 of 96 defining members carry 62 propose lines, against 210 of the 558 defining rooms. The propose lines are not part of the form's lean.

**Where the room models and my reading disagree.** They agree. r/cubers' model keeps the condition that "communication alone cannot secure implementation", and r/bardmains' model holds that its "strengthened claim that uninformed keepers erase an agreed change remains unresolved". My reading of the members' lines is the same.

**The held proposals (QD4-001; never served to any room, not re-checked).** The model above is the frozen version. J ruled that both held proposals are stated in full wherever the model is reported. They are, as the tree file states them:

{{HELD}}

Both held proposals bear on this form. The A11 proposal would withdraw the arrow these rooms restrict most (section 7). The P05 proposal would bound the telling clause these rooms restrict in 46 members.

## 7. The restrict lines: the arrow fails here, or the record cannot show it

**The rule, logged at D5a-36 before reading, unchanged.** I read every restrict line on an arrow held by a defining member, 301 lines, and sorted each `how` sentence (`_analysis/d5f_restricts.py`; my sort in `d5a38_sort_1.json` to `d5a38_sort_4.json`, joined in `d5a38_restrict_sorted.json`). *The arrow fails here*: the line says the consequent came without the antecedent, from another source or in another order, or that the antecedent did not lead to it. *The record cannot show it*: the line says the order, the link or the step is not visible, not dated or not established in the record. *Both*, where it says both. *Neither*, where it states a condition or a scope, or says that the two acts coincide or overlap. This is one reader's sort, mine; no second coder read it (J: no readers for the rest of the run).

{{RESTRICTS}}

**The form's own arrow: A11, the template that settles the design.** In 40 of its 58 restrict lines here the arrow fails: the template did not settle the design. Members went on disputing details, revised the template, or settled the design another way. r/eve: "Templates do not settle collective agreement while helpers lack the model, letters require revision and members oppose the corner design." r/PUBATTLEGROUNDS: "Design disagreement is settled by choosing an already circulated image under space constraints rather than necessarily posting a new pixel template." In 16 more the line states a condition: the template settles the design only for placers who recognize its current version. r/trees: "Posting a template settles design only for informed participants, since helpers unaware of the revision keep restoring the previous version." That is P05's telling clause again, met at the template. A11's mechanism uses the word "settled", and the held A11 proposal would withdraw the arrow on these grounds; this form holds the largest share of its restrict lines among the forms read so far.

**The arrows every form restricts.** A10 (judging too few hands, then the move) fails here in 28 of 36 lines; A13 (keeping under strain, then help) in 20 of 30, where help came from spare capacity or reciprocity; A04 (keeping, then border talk) in 18 of 21, where talk came during building.

**Where the record cannot show it.** The record cannot show that celebration caused the record of the work (A08, 10 of 19 lines), that help was delivered (A14, 7 of 9), or that a call turned members against a rival (A15, 6 of 9).

**So the two readings divide by kind, as in forms A and B.** Where the line concerns the order of two acts the rooms report (a design and its template, keeping and talk, a shortage and a move), it mostly says the arrow fails as stated. Where it concerns cause (celebration and record, help delivered), it mostly says the record cannot show it. Across all 301 lines: the arrow fails here in 172, the record cannot show it in 68, both in 13, neither in 48.

## 8. The one relationship that runs differently here

A11 runs from P02 (the design) to P04 (the template). Its connection: "in a room carrying both, the first design talk comes before the first template (tested, not beaten: 0.556 against a null mean of 0.557)". Its mechanism: "Design talk in a thread is settled by someone posting a template that lays out the agreed design pixel by pixel."

In r/PUBATTLEGROUNDS a posted image settled a dispute. Two members disagreed over the logo's G. One pointed to a posted image and to the space the room had: "Yea, but even AWM said that [this](http://i.imgur.com/NHCXwr1l.png) was the one we should go for. AWM was the one who posted that pic if you look down a bit, plus we are cramped for space in both vertical and horizontal directions." [PUBATTLEGROUNDS/c0103]. The other agreed: "Oh alright" [PUBATTLEGROUNDS/c0104]. The image was already in circulation; it settled the dispute when the room pointed back to it.

In r/cubers a posted design did not settle the work. A member posted a wider design, "Let's upgrade!" [cubers/c0169]. Builders began, "I'm starting on the yellow face at the bottom. Let's do that and work our way up." [cubers/c0171]. Keepers took the change for damage, and the builder gave up because the room was divided: "I think some people like the newer design, but others are happy with the way it is, so I guess it stays." [cubers/c0173].

In 58 of 96 defining members a current-ledger line restricts A11, against 47.7 per cent of the 558. What runs differently here is that the design does not end at the template. It is settled by a poll, an organiser's choice, the space or the existing pixels, and it reopens.

This is description, not a test. A11's expectation in form C is 0.355 (2 within-case datings over 705 rooms, times 125), so A11 is not-testable-here (section 10).

## 9. Fourth-order themes over- and under-represented

The rule was logged at D5a-01 before it ran (`_analysis/d5_themes.py`), and it is applied here to the defining members' codes (`_analysis/d5f_facts.py`). A member's coded concepts are counted by the fourth-order themes of their second-order theme's placements, and the form's pooled share on a theme is set against the pooled share over all 705 rooms. Over-represented: a ratio of 1.5 or more, with the theme present in 5 members or more. Under-represented: a ratio of 0.67 or less, with a population share of 1 per cent or more. These are shares of what the coders coded in these rooms, never a property of the rooms (contract section 5).

**Over-represented (2).**

{{OVER}}

In the rooms' words, from members holding the largest share on each theme (`_analysis/d5f_theme_quotes.py`): Collective representation, "removed 3 rows to not have to overwrite FREEUAB to the north. Now a 29 width x 26 height rectangle." [hongkong/c0030]. Collective efficacy, "Trolls threaten to destroy the still being made shield logo. Anyone want to help stop them?" [shield/c0070].

**Under-represented (3):** {{UNDER}}.

Collective representation is the form's change signature, so its excess in the codes partly restates the cut. The coders coded less rivalry and fewer tribes here than in the population. These rooms talked about their own picture more than about their rivals.

## 10. Arrows present, absent or not-testable-here

Section 1's arithmetic, declared at D5a-01: an arrow's expectation in a form is its within-case datings (its `subs`, counted over the 705 analysed rooms) over 705, times the form's n, here 125. Below one the arrow is not-testable-here, and no absence, boundary condition or failed proposition may be written from it. In form C the expectations run from {{ARROW_MIN}} to {{ARROW_MAX}}:

{{ARROWS}}

**Present: none. Absent: none. Not-testable-here: all 21.** Members' current-ledger lines on an arrow (sections 7 and 8) are description only. Members among an arrow's within-case datings: {{IN_SUBS}}. That is arithmetic about the model's own evidence, and it tests nothing in the form.

**Propositions.** {{PROPS}}. Every proposition is not testable here; none holds and none fails against a real expectation. No `findings.jsonl` line is bounded from this form.

## 11. How representative members do the work

**The rule, logged at D5a-36 before it ran, unchanged** (`_analysis/d5f_facts.py`). Fit is a defining member's distance to the form's centre in the allocation's 892 columns. The best two are the nearest members whose selected changes and coded concepts are at or above the form's defining medians (10 changes, 119.5 concepts). The least well is the farthest defining member. The member read at length is, among the ten nearest, the one with the most selected changes not read at length earlier in stage D5.

**Best fit: r/cubers** (distance 0.741; 12 selected changes; 320 coded concepts; first-return verdict composes, re-check grade composes with residue; in F11 and F12). Its members built a puzzle cube. The design was proposed in the first post (section 1). A neighbour offered terms on the design itself: "How about you change your colors to be more like this http://imgur.com/GpMEXP6 and we move out of the way and even help you with the cube?" [cubers/c0032]. The starter agreed: "I'm good with this compromise. Better than trying to run you off into the Black Sea. :)" [cubers/c0034]. When the cube was up, a member wrote, "We did it guys! Now just keep it!" [cubers/c0072]. Later a wider design was proposed and repaired away (section 8). A member proposed telling the room's chat "to reduce infighting" [cubers/c0204]. Another design was turned down because the keepers could not hold it: "too hard to do without reference, makes protecting it hard" [cubers/c0187]. Its maker answered, "Oh, I havent thought about that, lol. Was just going for the looks :/" [cubers/c0188]. After the close a member recalled a design agreed with a neighbour and refused by a member of the room (section 4).

**Second best fit: r/PUBATTLEGROUNDS** (distance 0.742; 14 selected changes; 161 coded concepts; first-return verdict composes with residue, re-check grade composes with residue; in F01, F03 and F07). Its members built a game's logo letter by letter. When the first spot failed, they moved and reused what they had: "Yeah, we can re-purpose the B and G into P U and go from there." [PUBATTLEGROUNDS/c0087]. One letter took hours: "However is changing the G is making me lose my mind. Been trying to make the proper g for 2 hours. Lemme handle the g fam" [PUBATTLEGROUNDS/c0097]. The dispute over it was settled by pointing to a posted image (section 8). When a member proposed building on a neighbour's corner, another refused for the neighbour's work: "Leave top left alone, that Runescape connection lost is great" [PUBATTLEGROUNDS/c0121].

**Least well: r/kuwait** (distance 1.221; 10 selected changes; 26 coded concepts; first-return verdict composes; in F33; its point lies nearer form B's centre). Its record is about where to put the flag and whether helpers could find it. A member found a spot and was told, "We tried that, the rainbow people just quickly delete it." [kuwait/c0009]. Another gave coordinates: "Here: https://www.reddit.com/r/place#x=454&y=619 Help with the red line as it will make the bottom border and the red stripe of our flag." [kuwait/c0011]. A helper on a phone could not find it: "i can't really find it where the flag would be, i'm on mobile." [kuwait/c0020]. A neighbour asked for help and thanked the room: "Yes we did Al7mdlillah. 💪😎 thanks! GCC for life <3" [kuwait/c0026]. Its lines place a flag; they do not argue its design. It is in form C because Ward's method put it there.

**Read at length: r/bardmains** (distance 0.733; 16 selected changes; 85 coded concepts; first-return verdict composes with residue, re-check grade composes with residue; in F07, F23 and F34). The rule chose it: among the ten nearest it has the most selected changes and was not read at length earlier. Its members, players of one game character, built a small mask. The design was sized to the hands (section 1) and kept to the colour already on the canvas (section 1). Lettering went down rough, to hold the space: "Yeah I kinda fucked it up already, but I'm just getting it there before someone fills it with something else." [bardmains/c0043]. The design stayed open to the room: "We're heading in this direction unless people are opposed." [bardmains/c0084]; "We can let the masses decide." [bardmains/c0067]. Members could not always tell a change from damage: "Some people are trying to change the 3 brown parts to the yellowish thing, that's not us doing that, is it?" [bardmains/c0028]. A neighbour's beam crossed the mask, and a member settled the design with the neighbour: "I'm okay with you kinda going through us, I think this laser beam is a funny idea, but want to keep our bardmask somewhat intact. Thank you!" [bardmains/c0064]. The room marked the work, "GJ guys! Bard is just about done!" [bardmains/c0021], and at the close regretted the last pixel (section 1). A member started again on another canvas, "I started on the Bard mask and this time we can maybe aim for a full body? maybe chimes & meeps!" [bardmains/c0082], and was told, "Place is dead, let it go." [bardmains/c0083]. What is unrepresentative about it: its record is small, 85 coded concepts against the form's defining median of 119.5, so its design talk is short. It is a member of F07 and F34 both, the two design branches that lean to this form.

## 12. The branches its rooms come from

J asked that stage D6 build on the forms with the 35 branches as the level below. The branches do not nest in the forms: a branch was cut on one shared key, a form gathers rooms by the whole mix of their changes and codes. The table gives, for every branch, how many of its rooms are in form C, and the branch's share in C against C's share of the 705 rooms (125 of 705, 0.177). A ratio of 1 is what a branch would show if its rooms fell in the forms at random.

{{BRANCHES}}

**What the table shows.** Four branches lean to form C at 1.5 times its share or more. Three are branches of the design:
- F07, the telling clause not shown at the design: informed members reject the planned change: 34 of 59.
- F33, the plan kept current while the design settles: 12 of 23.
- F34, the design sized to the hands: 11 of 22.
- F14, the mark adopted as the room's emblem while it is still placed: 3 of 7.

F07 is the largest share any branch has in any form read so far, 0.576: more than half its rooms are here. So the branch of informed members rejecting a planned change is, more than any other, a branch of this form. 6 of the 103 rooms of F01, the April Fools play, are in form C.

**Rooms in no branch.** {{NOBRANCH}}.

## 13. The nearest form and what separates them

**The nearest form is B**, the work behind the thread. The distances between form C's centre and the others are {{CENTRES}}. In the tree, C joins B at five forms, and the two join A at three. C and B are separated by what the rooms changed: C's members change the design, B's the chat, the scripts and attack calls.

**The rooms between forms.** {{NEARER}}: these are the forms whose centres lie nearer than C's to its defining members, 28 rooms in all. The room that could have gone either way, the defining member with the smallest margin to another centre, is r/overwatch (23 selected changes, 1,198 coded concepts, in no branch). Its point lies nearer form E's centre, the April Fools play.

## 14. The split below the form

**The split rule, logged at D5a-36 before it ran, unchanged** (`_analysis/d5f_split.py`, on `room-forms-tree-rooms.tsv`). A split reads as a split when both parts hold 10 defining rooms or more and each part has a fourth-order change column (a node or a link) at 1.5 times the parent's defining share or more, held by a third of the part or more and by fewer in the other part. The walk descends only while splits read.

{{SPLIT}}

**Form C's first split, at eleven forms, does not read as a split.** C.2 (15 defining rooms, 37 in all) leans to collective representation, held by every one of its defining rooms against 97.5 per cent of C.1. That is a lean on a theme the whole form already holds. C.1 (81 defining rooms, 88 in all) has no column of its own. The share of defining rooms holding the signature theme in each part: {{SPLIT_SIG}}. C.2 holds more placed rooms than defining ones: 22 of its 37 are thin or core rooms. The walk stops at the form, and I write no subform candidate. Form C is one pattern with variation.

## 15. The thin and core rooms placed here

**Thin rooms (27),** placed by the whole mix of their changes and codes at the nearest form centre: {{THIN}}.

Their selected lines weigh less and enter no share above. The most frequent are {{THIN_LINES}}. They lean the same way as the defining members, to the design (P02 add-condition, link and add-step).

**Core rooms (2),** with no selected change, placed by their codes alone at the nearest centre in the code columns: {{CORE}}. Their placement rests on 3 and 4 coded concepts and is weak.

## 16. The form test

**The constructs.** P02 (the design), P04 (the template) and P05 (keeping), at the fourth-order theme T4-006 (Collective representation), with the arrow A11 and P05's telling clause.

**The relations.** The room settles its design for a time, by a poll, an organiser's choice, the space or the pixels already placed, and reopens it after each finish. A template does not end the design: it settles it only for the placers who recognize its current version. Keeping restores the known form, so a change is repaired away, by keepers who do not know of it and by keepers who know of it and do not want it.

**Is it falsifiable?** Yes. A room whose design was fixed by its first template and never reopened, or whose keepers undid changes only when uninformed, would fall outside the relations. Such rooms could be looked for in the population, among rooms with as much design talk; I have not looked for them here. A11's two within-case datings (r/udub, r/wallstreetbets) show only that design talk came before the template, not that the design stayed fixed.

**The four organizing problems.** The form binds information provision: the current design must reach the keepers. And it shows the limit of information: some keepers know the design and refuse it, so the form also touches the division of authority over the design (polls, an organiser's overnight choice), which the four problems treat as a matter of task division. It leaves the allocation of members to tasks and reward free. A remainder is supported: the design is never finished. The rooms treat a finished part as the start of the next, and none of the four problems names that.

**What varies among members.** How the design is settled for now (a poll, an organiser, the space, the pixels already there), and whether the room's keepers refused or only missed a change. The tree finds no split that reads. The variation is accommodated by the form.

**Result: a form, in a narrow sense.** The form binds constructs of canvas organizing and states their relations, and nearly every defining member's lines show its one lean. Its relations add to the model what it does not say: the design is reopened, and telling is not enough where keepers disagree. Two limits stay. The changes are frequent in the population, and a quarter of the defining rooms (28 of 96) lie nearer another centre. And the claim rests on my reading of the lines and the members' words, with every local account unresolved.

## 17. What would make you doubt this is a form at all

Three things.

First, the base rate. Collective representation is changed by 52.7 per cent of the 558 defining rooms. Form C may be the rooms where design talk was most of the record, not rooms that did the design differently. The ratio (2.63) says they changed it more; it does not say they changed it in another way.

Second, my sort of the restrict lines. One reader sorted 301 lines. And the line between "the template did not settle the design" and "it settles only for those who recognize it" is a judgement in many A11 lines.

Third, the survival figures, from the record, never from the canvas. The median organizing end is hour 71.66 for the 123 members with one, and the mean aftermath share is 0.0164. The coded `work_remained` field says kept in 71 members, lost in 36 and silent in 18. These figures are not compared here, and nothing in this account rests on them.

What would undo the form: rooms outside it with as much design talk whose designs were settled once and kept; or a reading of the members' threads in which the keepers who undid changes were, after all, uninformed.
