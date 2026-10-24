# The rooms the model cannot compose (stage D3, section 4)

Written at D3a-56, 2026-10-21 (UTC). The model under test is the one the readers were served: pass 15 (e15f9647…b3fecd). The verdicts are in `verdicts-D.jsonl`. The readers' lines stay there, and my rulings on the 163 split rooms follow them as lines with `ruled_by: analyst` (G60, G60a and seven readings in `notes-D3.md`).

## Which rooms are here

A room is here when its verdict is `does-not-compose`. Both readers gave that verdict to one room, picturegame. No reader gave it to any other room, and no split involved it (notes-D2). None of my 163 rulings is `does-not-compose`: in each split room the restatement in the model's terms stood, and no named item contradicted a standing element or arrow the room bears on. So one room is read here.

I read the room whole through its forest, in its own words (rule 12). For it I say what it did, what the model would need in order to say it, whether the model should have that, and the condition that separates it from the rooms that compose. The kind is mine, not the readers'.

## picturegame

**The record.** The window holds 129 threads. The coder read 52 in full, triaged 77 and judged 127 out of scope. Two threads are coded: 13 concepts in 4 second-order themes, from hour 4 to hour 42. The room names one off-platform venue, its usual game chat.

**What it did.** picturegame is a guessing-game sub. In a thread of emoji nominations, opened before the canvas, members propose emojis and their meanings. One member asks about people who called themselves kiwis (c0001). Another bases an emoji on a kiwi figure seen on the canvas, to stand for the game's teamwork (c0003, hour 42). On April Fools (hours 22.7 to 23.7) the room plays a round of its game by sound only. The round is marked as an April Fools round (c0004). A player says the sound round clashes with the game (c0006), and the host answers that the room is playing a sound game that day (c0007). A deaf player asks for help (c0009). The host promises and gives a picture hint (c0010, c0011). A guess is made and marked correct (c0012, c0013). The moderator's bot invites players to the game's chat (c0005). No member calls for hands, starts a mark, builds, keeps or defends canvas work, or deals with a neighbour in the record.

**What the model would need.** It would need an account of a sub running its own game on the joke day: a themed round, an accommodation for a player, a hint, a judged guess. None of this is canvas organizing. The one canvas act, a figure on the canvas taken as the game's emoji, is P13's (the mark kept as an emblem), and the April Fools round sits under K01's frame. The labeler kept the room inside those two entries and marked every canvas element unobserved.

**Should the model have it.** No. The model is about how rooms organize work on the canvas. The room's play is the sub's own business beside the canvas. At D3a-55 I ruled 387 propose lines of that kind outside the model's scope, in rooms that also did canvas work. Here that business is the whole record.

**Kind: `out-of-scope`.** The room did not organize canvas work; it played. This bounds the model's scope, not its claims. It is not `too-thin`, since 13 readable concepts show what the room did, and they show no canvas organizing that the record leaves out. It is not `outside-the-model`, since the room did not organize something the model cannot say.

**The condition that separates it from the rooms that compose.** Every room that composes has at least one act of its own on canvas work in its record: a call, a start, building, keeping, or a deal over space. picturegame's record holds none. Its one link to the canvas takes a figure already on the canvas as an emoji.

**Its verdicts, kept.** The pre-adaptation verdict is `does-not-compose` from both readers. The labeler's grade is `composes-with-residue`, and its local status is `unresolved`, as in every room (notes-D2). No re-check line exists. The room's local account is resolved in its own terms: an out-of-scope room, with one P13 act and one K01 frame.

## The out-of-scope rooms, read together

One room is too few to form a kind of its own. What picturegame did instead of canvas work does recur, though. In other rooms, the sub's ordinary business and its April Fools play run beside the canvas work: 251 propose lines under T3-017 and 48 under T4-001's themes, nearly all ruled particulars outside the scope at D3a-55. picturegame is the one room in which that business is all the coded record holds. The kind goes to D4 and D5 as a bound of scope. These are rooms whose evidenced activity on the canvas days is their own business, and they are counted apart from rooms that organized.

## Carried to D4, D5 and E1

- picturegame: `does-not-compose`, kind `out-of-scope`, condition: no act of its own on canvas work.
- No split room was ruled `does-not-compose`. The 163 rulings are 61 `composes` and 102 `composes-with-residue` (counted by script), and the readers' lines stand beside them.

## The re-check (D3c, 2026-10-24)

Line 25's "No re-check line exists" was true at D3a-56. At D3a-57 all 705 rooms went back, picturegame among them, and the labelers and readers returned against 46384686…, the version frozen at D3c. Read by `_analysis/d3c_room_recheck.py` (`_analysis/d3c_picturegame_recheck.txt`):

- **The re-check readers.** Both give `composes-with-residue`. r1 restates the room as a sub keyed as April Fools play, with chat, asking and explaining, and jokes; its residue is the sound round and the emoji proposals. r2 restates the play, the chat invitation and the question and answer under K01, P23 and P24; its residue is the same two acts and the picture hint for the deaf player.
- **The re-check lines, 72, all ruled.** K01 holds three accepted lines and P13 two. Three `propose` lines are particulars outside the scope (the sound round made playable with a picture hint, and ordinary sub talk twice). 64 lines are absent, and 63 of them are evidence limits.
- **What changed.** The room's record did not change. The model gained candidates that name chats (P23) and asking and explaining (P24). So the re-check readers can restate the room's side business, and they leave its play as residue. The play is the same business that made the room `out-of-scope` at the first return.
- **The kind, kept.** The first-return verdict stays `does-not-compose`, kind `out-of-scope`, with its version (e15f9647…). The re-check verdict stays `composes-with-residue`, with its version (46384686…). No room is `does-not-compose` at the re-check. The bound of scope goes to D4, D5 and E1 as written above. A room whose whole record is its own play can be restated by the candidates for chats and for asking and explaining; this does not show that the room organized canvas work.
- **The close-check's reading.** `validate.py D3` prints this room's kind as `outside-the-model`. It takes the first of the three kind names that the room's block contains, in its fixed order, and the block above names `outside-the-model` to say that the room is not of that kind. The kind is `out-of-scope` as ruled. I report this reading and do not change the block to suit it.
