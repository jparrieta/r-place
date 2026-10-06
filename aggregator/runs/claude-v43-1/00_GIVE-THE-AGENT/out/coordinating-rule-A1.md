# The coordinating-turn rule, stage A1

Written 2026-10-07, leg A1b-19, after all 705 room notes. Stage B1 copies it into `prior.md` §5. It may change only by a logged departure, and every figure computed under it is then reported under the rule before and after the change.

The rule is applied by `out/_analysis/a1_ends.py` to every first-order concept of the analysed set (115,388 concepts, read through `mem.py codes` by `out/_analysis/a1_codes_dump.py`). Its output is `out/organizing_end-A1.jsonl`.

## What counts as a coordinating turn

A coordinating turn is a coded turn that moves the shared work on the canvas. The coder's first-order label opens with the act the turn performs. The rule reads that act.

A turn counts when it does one of these:

1. It calls people to the work. The rooms say "call backup" (ProfessorLayton), "DEFEND THE FORT" (NieR), "NEW SPOT, MOVE UP" (torontoraptors). The label opens with calling for, calling on, calling everyone, urging, rallying, recruiting or inviting.
2. It assigns or plans the work: coordinates, a template ("Current Template", heyyea), a grid image, a script, a Discord, a site, a design, a choice to drop expansion and hold what the room has ("maintain what they have", earthbound).
3. It reports placement before hour 73: work done, started, under attack, overrun.
4. It defends the work, or asks others to.
5. It makes, keeps or breaks an alliance, a truce, a border or a deal. The rooms say "truce" (liverpoolfc), "non-aggression" (calgaryflames), "pacto de paz" (epublica), "Kolache alliance" (texas).
6. It corrects another's placement: asks a neighbour to move, stop or respect a boundary, or repairs what was overrun.

In the labels this means one of three things. The label opens with a directive or building verb (proposing, starting, placing, fixing, moving, negotiating, accepting, refusing, dropping and others). Or it opens with "calling" followed by for, to, on or a group sent to act. Or it names a directive object: help, coordinates, permission, a truce, an alliance, a deal, a border, a move, a defence, a repair, a template, a script, a Discord, an attack.

## What does not count

A turn does not count when it looks back or looks away from the work:

- recounting, remembering or explaining what happened;
- joking, mocking, teasing, or anything about April Fools, a prank, a meme, the sidebar or the stylesheet;
- mourning, lamenting, or "RIP Eightfold and RIP r/place" (paranatural);
- thanking, praising, crediting, celebrating, "We did it hreddit!" (croatia);
- apologizing, blaming, accusing, wondering, hoping;
- a moderator removing, locking or stickying a post, or sending discussion to a megathread;
- an argument about a choice ("defending the script as fun"), which defends a position and not the work;
- a plan for next year or next time.

## After hour 73

The canvas closed at hour 73. A turn after it counts only when it calls people to canvas work or plans it: a call, a proposal, an invitation or an organizing turn that names the canvas, a logo, a flag, a design or a rebuild. Most such turns are calls to rebuild on a successor canvas. Recounting the week does not count, even when the label names an alliance.

## Examples

Ten coordinating turns, each with the rule's reason:

- predators c0014: asking everyone to use one grid image (an assignment).
- predators c0024: asking red-dot placers for a truce by private message (a truce).
- predators c0039: persuading a turquoise-pixel placer to move elsewhere (a correction of another's placement).
- predators c0047: accepting the 529 boundary to settle things (a border).
- Russiaclan c0009: marking the flag done and asking people to maintain it (a report of placement, then a call).
- Russiaclan c0018: announcing an alliance with the Toronto Maple Leafs (an alliance).
- Russiaclan c0040: dropping expansion to secure the gain (a plan).
- Russiaclan c0080: giving coordinates for the Serbian heart (an assignment).
- winnipegjets c0020: negotiating space for the pink S (a deal).
- winnipegjets c0042: calling for backup as the lettering and logo come under attack (a defence).

Ten turns that do not coordinate:

- Russiaclan c0028: joking about recruiting a troll brigade (joking).
- Russiaclan c0055: removing political replies from the cooperation thread (a moderator's removal).
- Russiaclan c0085: mourning that the canvas closed before the heart was finished (mourning).
- Russiaclan c0090: crediting success to negotiating with neighbours (crediting; it names a deal but looks back).
- Russiaclan c0116: recounting rebuilding beside Serbia after a Dutch attack, at h74.05 (recounting after hour 73).
- predators c0058: mourning the ending (mourning).
- predators c0063: recounting others taking the spot during the move (recounting).
- predators c0086: joking about herding the room (joking).
- winnipegjets c0022: recounting a turf war with the ladybug (recounting).
- winnipegjets c0068: apologizing for starting LAME and asking to work together (apologizing). The room's note took this turn, at h72.89, as its last coordinating turn. The rule does not. The rule's last coordinating turn for the room is c0046 at h60.68, abandoning a phrase that crossed r/placecanada's borders.

## work_remained

`work_remained` is the room's own last word on what became of its work. The rule takes the latest concept whose label reports an outcome, opened by a verb of telling: saying, reporting, declaring, mourning, celebrating, thanking, showing and others. It skips labels that are hypothetical, conditional, unsure, or about griefing or a joke. Survived, intact, made it, held, immortalized, finished, restored and came back mean kept. Destroyed, gone, lost, erased, wiped, overrun, failed and dead mean lost. A recovery word wins over a loss word in the same label. When no label says either, the room is silent and carries no ids.

The verdict comes from the forest and never from the canvas. Russiaclan is lost by c0085, though the canvas keeps a Serbia-Russia work. Silence is an unknown outcome in this public record. It does not show that organizing stopped.

## Results and limits

Under the rule: 44,116 of 115,388 concepts coordinate (0.382). Nine rooms have no coordinating turn: watchmen, Redox, yerbamate, Lugarix, azores, ReBoot, PokemonSage, UNLincoln, tetris. 146 rooms have their last coordinating turn after hour 73. work_remained: kept 347, lost 218, silent 140.

Each note's `ended` line was reconciled with the file in `out/_analysis/organizing_end-reconcile-A1.tsv`. The rule picks the same concept as the note in 268 rooms. It picks a different concept within one hour in 156 rooms. It differs by more than an hour, or the note names no concept, in 281 rooms. The notes judged turns by reading. The rule judges them by the label's first verb. Most of the 281 differences are of two kinds. The rule counts a post-73 call to rebuild that the note set aside. Or the note took a turn the rule's verbs refuse, as in winnipegjets above.

The rule reads labels, not passages, so it misreads some. In a hand check of 40 rooms' work_remained outcomes, about six were doubtful. Most of them were a label about another room's work: a neighbour's flag ruined, an ally's work destroyed. In a hand check of reddevils' labels, a few questions about Discord counted as coordinating. These are known limits. Stage B1 should read the turn itself where a room's end hour carries weight.
