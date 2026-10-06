# r/place and the data we hold

*Kind of page: explanation, with a worked example.*

This page says what r/place was, what records of it the study holds, what those records let us see, and how to read one community's coded threads. It ends with a worked case: the Dutch push into the Armenian flag.

The canvas record can be joined to Reddit usernames; see the [terms of use](data-and-collection.md#terms-of-use) before publishing anything drawn from it.

## What r/place was

On 31 March 2017 at 16:00 UTC, Reddit opened a blank square of 1000 by 1000 pixels to its users. Any registered account could set one pixel to one of sixteen colours and then had to wait 300 seconds before it could set another. There was no undo, no ownership and no way to reserve space. Every account had the same rate of action. Reddit called it an April Fools joke and gave it no goal, no score and no teams.

Placement stopped on 3 April at 17:00 UTC; the last pixel landed at 16:58:54. The sources call this 72 hours. The study cuts it into 73 hourly bins and calls the open period the "during" window of 73 hours, so both figures appear in the project. The sources also warn that the common phrase "April 1 to 3" is editorial and does not fit the clock.

In that time 1,166,924 accounts made 16,559,897 placements, and 997,633 of the million pixels were written at least once. Nothing in the rules made a community. By the freeze the board carried flags, mascots, memorials and borders that only organised groups could have made.

## The data we hold

### Three records

| record | what it is | size |
|---|---|---|
| the canvas record | Reddit's log of every placement: time, x, y, colour, and a hash of the placer's username | 16,559,897 placements by 1,166,924 accounts |
| the text record | what the communities and the placers wrote on Reddit over 24 days, from a week before the opening to two weeks after the freeze | 67,296,426 records in 24,101 community archives; a separate placer-only corpus of 18,615,238 records in 50,936 venues |
| the atlas | a participant-built index of the final image: a polygon, a name and usually a claiming community for each artwork | 1,473 artworks, 1,236 naming a subreddit, about 775 communities |

**The canvas record** is in time order at one-second resolution, so the state of the board at any moment can be rebuilt. It has 3,256 rows outside the board (x or y equal to 1000); these are dropped, which leaves 16,556,641 placements.

**The text record** was built from both ends. From the people: every placer's hash was resolved to a username where possible, and everything that account wrote was fetched. From the canvas: every community the atlas names was swept whole. During the 73 hours, 347,915 of the resolved accounts wrote anything at all, 31.6 per cent of them.

**The atlas** covers 956,741 pixels, 95.7 per cent of the canvas, and holds 97.5 per cent of all placements. It indexes the final image, so it sees what survived. On the sources' life table about 31 per cent of artworks ended below half fidelity to the colours they were built with (22 to 37 per cent across gates). It credits artwork, so it misses communities whose job was to organise building elsewhere. 1,164 of its artworks credit a community the study codes; [the other 309](artworks-outside-the-population.md) are details of credited work, groups that organised off Reddit, individuals, and unsigned symbols.

### What the study built from them

**The frame of communities.** A room is one subreddit, read as a case. The census counts 706 rooms as the population; the v43 run reads a frame of 705 of them (4 October 2026), r/the_donald, the room with the most text, not coded (contract §5): communities an atlas artwork names (and four whose names are written on the canvas, and nine an atlas description credits), that wrote about the event during the 73 hours the canvas was open. [The census page](census.md) gives each step from 1,473 artworks to 706 communities, and the judgements behind them: 777 communities have a venue record and 71 fall out, r/place among them as the field, modelled apart. The frame the analyst receives is every census room coded when the copy was taken: 696 on 28 September 2026, 700 on 2 October, 705 on 4 October ([the numbers](numbers.md)).

**The coders' work per community.** One coder reads one room, with no other case, no atlas and no web. Each room leaves the same six files: `brief.md`, `case.md` (the coder's account of the week), `codes.jsonl` (first-order codes: the coder's label, the participant's words, the item and thread), `themes.jsonl` (the room's second-order themes), `threads.jsonl` (every thread in the window and what was done with it) and `pointers.jsonl`. A forest file, `trees/<room>.md`, shows each coded thread as its reply tree. Every quoted fragment was checked byte for byte against the corpus.

**The joined store.** A script joins the rooms into `package/store/`. It holds the first-order codes, the second-order themes, every thread, and the transitions (a transition is a coded turn that answers a coded turn, with the interval between them); `neighbours.jsonl` holds the pairs of rooms that share an artwork, border each other, overlap on the atlas outline, or are named in the coders' record. A pair can carry more than one tie. The counts change as rooms are added: [the numbers](numbers.md) read them from the files.

### What has been coded so far

The figures come from builds made on different dates, and they differ.

- The setting draft (31 August 2026) counts 318 rooms coded, 287 of them positive, and an analysis package of 300 cases with 27,933 first-order codes and 2,703 case themes. Those 300 cases carry 330 artworks, 18.4 per cent of the canvas and 19.5 per cent of all placing.
- The current frame holds 705 rooms (4 October 2026), and the store above is built from it.

Two cautions travel with these counts. Code counts grow with a room's text, so the contract bars reporting them across rooms as a property of the rooms. And the frame is built from artworks that survived: a room that organised and was overwritten before the freeze has no row.

## What the data let us do

The records share one clock. A thread's time and every code's `created_utc` come from Reddit, and every placement's `ts_ms` comes from the canvas log. Both are put on time since the opening, written as hours and minutes: H43:37 is 43 hours and 37 minutes after 16:00 UTC on 31 March. So a coded thread can be laid over the placements inside an artwork with no alignment step.

That is the core of the design. We can read what a room said it would do, and see on the board whether and when it happened. The sources report that hourly coded canvas talk and hourly placements correlate at 0.93 on a log scale, while all the placers' writing correlates with placements at 0.11. The volume of writing tracks Reddit's daily cycle. What people wrote about tracks the event, and only reading tells the two apart.

**The bridge.** The canvas log stores the placer as an unsalted SHA1 of the username, in base64. The same account always gives the same hash, so hashing a collected username joins the person's writing to the person's pixels. The hash is case sensitive. Of 1,166,924 placers, 1,101,801 resolved (94.4 per cent), and they made 99.5 per cent of placements.

What the bridge allows:

- classify every overwrite and every repair by the tie between the two accounts. Within an artwork, who destroys a pixel is close to a random placer (lift 1.05); who repairs it is not (lift 1.47, and 2.19 for placers tied to one community);
- say which communities' members placed in which artwork, as the Dutch study below does.

What it does not allow:

- The 65,123 hashes that never resolved are the lightest placers, about 1.3 placements each.
- Most placers wrote nothing while the canvas was open, so reading reaches the organisers and misses most of the crowd.
- The record holds pixels and public Reddit text only. Discord, private messages and off-site tools carried much of the coordination and are absent; coders see them only as pointers.
- The forest shows that one turn came after another. It does not show that the first caused the second.

## A worked case: Armenia and the Netherlands

The project's Dutch study (built 21 September 2026 in the project's working folders; not in this repository) names eighteen Dutch artworks in the atlas. The largest, *Entire Dutch Area*, covers 33,760 pixels. 90,920 accounts placed in a Dutch artwork. The bridge holds for 98.6 per cent of them, but only 34,713 wrote anything inside the 73 hours, so the sources put the reading ceiling at 38.7 per cent. Three Dutch rooms stand at or near saturation: PlaceNL, the organiser built for the event; thenetherlands, the standing national community; and cirkeltrek, the Dutch circlejerk. The study sets eight episodes where threads and pixels can be read against each other. Four bear on Armenia.

**Greece falls (H23:30 to H30:12).** r/greece had posted its flag at (558,13) at H06:26, inside what became the Dutch flag. Early in its own record r/armenia made an alliance with r/greece; a coded comment reads "They will help us and we will help them." A ceasefire with Greece was declared in cirkeltrek at H24:02 and held about two and a half hours. At H26:55 r/greece wrote "GUYS WE'RE GETTING INVADED BY THE NETHERLANDS", and at H27:05 r/armenia rallied to defend it. PlaceNL was founded at H27:40, inside the episode. Between H27 and H30 the Greek site flipped to red and orange. At H28:50 r/armenia posted the thread shown below: Greece has all but fallen, "WE ARE NEXT".

**Armenia holds, then the east closes.** Armenia announced its flag at (526,34) at H23:14. It built through H28 to H32, and at H34:01 a post read "Great work Armenia!!! We did it!!". Meanwhile the Dutch planned a lion in the east. At H41:41 cirkeltrek petitioned for a pact with Goodboye, and at H42:57 PlaceNL set the terms: a border around Goodboye, and otherwise hands off. With the east closed, cirkeltrek wrote at H43:01 that the Dutch lion would not be stopped by a cat. The cat was GreyBlob's, beside the Armenian flag.

**Armenia falls (H44:18 to H48:48).** cirkeltrek posted "Plan of attack on the left Wing" at H44:19. r/armenia asked at H44:50 "What is going on in the East? Are the Dutch invading?". At H45:43 PlaceNL's new plan said not to widen the flag but to fill the left with orange. Dutch posters then came into r/armenia itself: "INPOLDEREN" at H45:49, "Zweer trouw aan uw nieuwe Koninkrijk!" at H45:50, the Wilhelmus at H45:53. On the canvas, between H45:00 and H47:00, the Armenian site went from 39 per cent dark blue to 74 per cent orange. The coat-of-arms polygon took 8,912 placements at 75 per cent overwrites, and the lion was drawn by H48:30. The atlas credits that coat of arms to no subreddit. The sources say three parties built on that ground before the lion did.

**Armenia moves.** At H46:16 r/armenia posted a new site above the Turkish flag. Its case account says the room then moved above India with permission, finished a replacement flag, and after the freeze thanked India for the space. In the same record, members argued down a call for revenge on Turkey: "Why do we have to ruin someone else's flag because the Dutch ruined ours?", then "Pixels not politics!".

The same event shows up from the Dutch side of the bridge. Of r/armenia's 191 placers in the 73 hours, 146 (76.4 per cent) placed in Dutch artworks, and 65 per cent of r/armenia's placers placed in the coat of arms (79 per cent of GreyBlob's). The sources trace the polygon's first burst, H28 to H32, to Armenia building its own flag on that ground.

## A thread tree and its codes

The thread is `62ve2r`, from r/armenia at H28:50, as Greece falls. The forest header gives it 63 items, 18 coded and 34 dropped. This excerpt shows its first ten replies, as they appear in the room's forest, [`trees/armenia.md`](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/trees/armenia.md):

```
=== THREAD 62ve2r: "NEW UPDATE: GREECE HAS ALL BUT FALLEN FALLEN TO THE DUTCH, THEIR DEMISE IS IMMINENT AND WE ARE NEXT, EXPAND TO THE WEST AS QUICKLY AS POSSIBLE AND AT ALL COSTS OR ELSE WE WILL MEET THE SAME FATE AS GREECE" (H28.84)  items 63, coded 18, dropped 34 ===
[0] OP (CrazedZombie ⟨Armenian in California⟩) ↑21 -> [na c0022 na] ordering westward expansion at all costs
|-- [1] (Dutch-Ghost-Dance | +10.1m) ↑6 [edited] -> [na] "I'm very sorry some of my Dutch people.."
|   \-- [1.1] (CrazedZombie ⟨Armenian in California⟩ | +1.8m) ↑3 -> [na c0024] hoping to find peace with Dutch participants
|-- [2] (Mr-Major | +11.3m) ↑8 -> [na c0023 na] advising Armenia to extend left and abandon the east
|   \-- [2.1] (Idontknowmuch | +2.2h) ↑3 [edited] -> [na] "> but a lot of Dutchmen have gone hayw.."
|       \-- [2.1.1] (Mr-Major | +1.5h) ↑3 -> [na] "They deserve that"
|           \-- [2.1.1.1] (Idontknowmuch | +20.9m) ↑2 -> [c0032] suggesting Dutch participants help make the Armenian flag
|-- [3] (nzhdeh | +20.1m) ↑4 -> [na] "Okay, sounds good, I'll start expandin.."
|   \-- [3.1] (CrazedZombie ⟨Armenian in California⟩ | +15.8m) ↑1 -> [na c0025] rallying support from other subreddits
|-- [4] (RubberDong | +48.7m) ↑6 -> [na] "Greek here. Help us brothers. Help us .."
|   \-- [4.1] (Greybol3 | +2.4h) ↑2 -> [na c0031] promising to help Greece rebuild after the war
|-- [5] (vartanm ⟨Armenia⟩ | +1.1h) ↑1 [moderator] [sticky@retrieval] [edited] -> [na c0026] joking that small westward flags make another diaspora
|-- [6] (artin2 | +1.6h) ↑6 -> [c0165] urging Armenia to take over Turkey
|-- [7] (Lighthat | +1.8h) ↑4 -> [c0027] proposing Turkish-flag territory as a new home
|-- [8] (Parskastan | +1.9h) ↑3 -> [c0028] refusing to give up westward expansion
|-- [9] (Darkfizch | +2.8h) ↑2 -> [c0029] asking Armenia to spare Nehalennia while relaying Cirkeltrek intentions
|   \-- [9.1] (ThatGuyGaren ⟨Armed Forces⟩ | +10.6m) ↑3 -> [c0030] making Armenian expansion conditional on Dutch restraint
```

### How to read it

The forest file's own header explains most of the notation.

- **The thread line** gives the thread id, its title, the hour since the opening in decimal (H28.84 is H28:50), and the counts of items, coded items and dropped items.
- **Coordinates** are Dewey numbers. `[0]` is the submission, marked OP. `[2.1.1]` is a reply to `[2.1]`, which replies to `[2]`. Depth is the number of segments. The `|--` and `\--` lines draw the tree.
- **The author** comes next, with their flair in this room in `⟨…⟩`. `[moderator]` marks a distinguished item.
- **The time offset**, such as `+10.1m`, `+2.2h` or `+55s`, is how long after an earlier item this one was posted. The header does not say after which one. It is the time since the item's parent: [tree_builder.py](../coder/instrument/v32/tools/tree_builder.py) writes `dt_parent`, the item's time less its parent's. `[1.1]` came 1.8 minutes after `[1]`.
- **↑** is the item's score when it was collected, weeks after the event, and `[sticky@retrieval]` its sticky flag then. They are not facts about the week. `↑?` means no score is held.
- **After the arrow**, a coded line lists the item's chunks in text order: a code id where the coder coded the chunk, `na` where the coder passed over a stretch of 40 or more characters. The coder's labels follow in the same order. `[na c0022 na]` means the post opens with uncoded text, then a coded passage, then more uncoded text.
- **An uncoded turn** shows `[na]` and the start of its text in quotes. The header counts 59 "bridge" items in this room: in `tree_builder.py`'s words, "no code, but a coded descendant", kept so the distance between two coded turns stays visible, like `[2.1]` and `[2.1.1]` here.
- **A dropped item** "carried no code and had no coded descendant". Dropped items are counted in a line such as `\-- [...] (26 un-coded items)`, which closes this thread below the excerpt.

Two further points come from the sources. The forest shows order; it does not show cause. In the contract's words, a reply is a reply. And the coder's cut can hide the mechanism. In the lion episode, the Dutch replies that moved the lion from east to west were pruned as carrying no code.

### The codes in this excerpt

Joined from the room's [`codes.jsonl`](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/codes.jsonl) and [`themes.jsonl`](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/themes.jsonl) by `code_id` and `theme_id`. The participant's words are the exact coded passage.

| code | coder's first-order label | participant's words | second-order theme |
|---|---|---|---|
| c0022 | ordering westward expansion at all costs | "EXPAND TO THE WEST AS QUICKLY AS POSSIBLE AND AT ALL COSTS" | t02 expanding, defending, and maintaining Armenian pixels |
| c0024 | hoping to find peace with Dutch participants | "I still hope we may be ale to find peace somehow." | t04 negotiating borders and restraining expansion |
| c0023 | advising Armenia to extend left and abandon the east | "Extend your flag to the left, and don't repair the east." | t01 planning where and how to make Armenian flags and hearts |
| c0032 | suggesting Dutch participants help make the Armenian flag | "The best way to get them worked up would be if the Dutch would help *make* the Armenian flag instead of taking over it." | t03 asking neighbours for pixel help and returning it |
| c0025 | rallying support from other subreddits | "I'm trying to rally support from other subreddits." | t03 asking neighbours for pixel help and returning it |
| c0031 | promising to help Greece rebuild after the war | "We will do our best to help you guys rebuild and thrive in your new current location once the war is over." | t03 asking neighbours for pixel help and returning it |
| c0026 | joking that small westward flags make another diaspora | "We have created a diaspora once we can do it again ;)" | t07 joking through the great flag war |
| c0165 | urging Armenia to take over Turkey | "Why don't you guys just take over turkey" | t05 fighting and narrating flag takeovers |
| c0027 | proposing Turkish-flag territory as a new home | "I think we should give that territory up and start taking over the Turkish flag as our new territory." | t01 planning where and how to make Armenian flags and hearts |
| c0028 | refusing to give up westward expansion | "I'm gonna keep expanding west im not giving up boys" | t02 expanding, defending, and maintaining Armenian pixels |
| c0029 | asking Armenia to spare Nehalennia while relaying Cirkeltrek intentions | "Our small subreddit /r/Nehalennia is trying to make a name for ourselves there, as it is related to the Netherlands. From what I've heard on /r/Cirkeltrek, most Dutchmen are no longer interested in expanding west." | t04 negotiating borders and restraining expansion |
| c0030 | making Armenian expansion conditional on Dutch restraint | "We'll stop when they do" | t04 negotiating borders and restraining expansion |

Code ids do not follow the order of the thread: `emit.py` numbers codes in the order they are made (`c0001`, `c0002`, ...). `c0165` stands out: the case account says the counter-reading search found this comment late, and it "became a late code".

The coder's case account names this thread when it sets posts against comments: the post orders expansion "AS QUICKLY AS POSSIBLE AND AT ALL COSTS", while a comment hopes for peace. The replies in the excerpt also plan a move, offer help to Greece and set terms with the Dutch. Its twelve codes fall under six of the room's thirteen second-order themes.

## Where to go next

- Armenia's coded files: [case.md](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/case.md), [codes.jsonl](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/codes.jsonl), [themes.jsonl](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/themes.jsonl), [threads.jsonl](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/threads.jsonl), [pointers.jsonl](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/pointers.jsonl), [brief.md](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/armenia/brief.md).
- Armenia's forest: [trees/armenia.md](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/trees/armenia.md).
- The joined store: [package/store/](../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/).
- Reference pages: [the aggregator's files](files/aggregator/README.md), [the coder's files](files/coder/README.md).
- The whole coded rooms of this example, as the yard verified them, each with its run and its inputs archived: [armenia](../coder/rooms/armenia/ROOM.md), [PlaceNL](../coder/rooms/PlaceNL/ROOM.md), [thenetherlands](../coder/rooms/thenetherlands/ROOM.md), [cirkeltrek](../coder/rooms/cirkeltrek/ROOM.md), [Goodboye](../coder/rooms/Goodboye/ROOM.md), [greece](../coder/rooms/greece/ROOM.md), [sweden](../coder/rooms/sweden/ROOM.md), [norge](../coder/rooms/norge/ROOM.md), [norway](../coder/rooms/norway/ROOM.md), [czech](../coder/rooms/czech/ROOM.md), [blackmirror](../coder/rooms/blackmirror/ROOM.md), [indonesia](../coder/rooms/indonesia/ROOM.md), [mindcrack](../coder/rooms/mindcrack/ROOM.md), [placehearts](../coder/rooms/placehearts/ROOM.md). Twelve of them keep their case lead's saved session in [`coder/lead-sessions/`](../coder/lead-sessions/), so the lead can be reopened and asked about its room ([how](memory/coder-lead.md)); Goodboye and norway have none. The other rooms of the census reach the aggregator as their six coded files, in `aggregator/input/coders/rooms/`.
