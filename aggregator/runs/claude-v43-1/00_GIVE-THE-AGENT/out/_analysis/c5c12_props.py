#!/usr/bin/env python3
"""C5c-12, the fold-in: set the proposition fields the four serial findings list (serial-C5/finding-1 to finding-4) in
c5_propositions.json. Each change is a whole field; the field's current text must begin with 'starts' (or the field be
absent where 'starts' is null). Pass 9's spec is kept as c5_propositions-p9.json. c5_propositions.py --replace then
rewrites propositions.jsonl, carrying each arrow's current mechanism and count.

    python3 out/_analysis/c5c12_props.py            check
    python3 out/_analysis/c5c12_props.py --write    write the spec
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SP = os.path.join(ROOT, "out", "_analysis", "c5_propositions.json")
spec = json.load(open(SP, encoding="utf-8"))
CH = [
 ("N01", "statement", "When a member starts a mark", "When a member starts a mark (R01), the room calls others to place (P01); after a call, the room builds the mark and members report it (P03); once the mark stands, the room keeps it (P05)."),
 ("N02", "statement", "When members keep a mark", "When a room keeps a mark (P05), it turns to other rooms: it talks borders with neighbours (P08), asks other rooms for help (P16) and joins coalitions under attack (P17). Where border talk comes before upkeep, it mostly offers terms before any damage."),
 ("N02", "decides", "On the late side only 6 of 15", "On the late side only 6 of 15 rooms hold A04's order. In the 166 rooms where border talk comes first, two coders read the first border talk in 40: it offers terms before any damage in 19 of 26 to 36 of 38 of the records that bear on it (Cohen's kappa 0.19; A04's bound)."),
 ("N03", "statement", "A call to place can turn members", "A call to place can turn members against a rival's work (P01 to P09). The same room answers the call to attack: members refuse it, in written replies usually with a reason (F-014), the room reins in the attackers or apologises (P07), or points to a truce (P08). Where the attack goes on, the rooms carry the contest on in talk (P18)."),
 ("N03", "decides", "Sparing comes first, with no call", "Sparing comes first, with no call, in 22 of 104 rooms. In 52 rooms a refusal by another member replies to a specific attack call within minutes (127 transitions). In written, coded replies, refusals give a reason in 23 of 38 read pairs and acceptances in 2 of 14 (F-014), a ratio of kinds set by the draw; on calls to place, refusals gave a reason in 3 of 3 and acceptances in 6 of 31 (F-023). The coding of themes does not produce this. More than half of all calls carry no written reply, so the asymmetry is about what members wrote."),
 ("N04", "statement", "After members report a mark done", "After members report a mark done (P03), the room celebrates it (P11), records what it celebrated (P12) and carries the record on (P13). Placement stops at hour 73 for every room; after it, rooms can celebrate, record, curate the record and carry it on, and no one can place."),
 ("N05", "statement", "When members call for hands", "When a room calls for hands in a standing sub (P01), the host sub's moderators and members draw a line around canvas talk (P20): a megathread, removals by rule, a canvas sub, objections to the flood."),
 ("N06", "statement", "When upkeep needs more placements", "When the room's upkeep needs more placements than its members can make (P05), members turn to scripts and spare accounts (P14)."),
 ("N07", "statement", "Members try to align", "Rooms align their members' placing without deciding how they are organized: members answer a call in a bare line (P15), a design argued in a thread is settled by a posted template (P04), and a decided element of order appears in 46 of 705 rooms (C01). In 233 of the 370 rooms that called for hands, the record reports a work up after the first call (F-021); the others tried."),
 ("N07", "finding", "F-006", "F-021"),
 ("N07", "primary", "words", "pattern"),
 ("N07", "level", "element: two theorised arrows", "element: two theorised arrows and claims on findings (F-021, F-023, F-006)"),
 ("N07", "decides", "Nothing in the record decides it.", "The record counts its parts: a work reported up after the first call in 233 of 370 rooms with calls (F-021); written acceptances bare in 25 of 31 replies to calls to place (F-023); decided order in 46 of 705 rooms (F-006). The rival is not decided: chats reached the thread with a decision in 33 rooms, and the claim that decided order is absent elsewhere is about rooms writing in public, and weak (contract section 5)."),
 ("N07", "boundary", "Rooms that govern a territory", "Rooms that govern a territory for a colour or vet others' requests to build, where decided order is coded more often, the gap lying in the smaller rooms (F-006's bound). Rooms whose record reports no work up after their calls, where the room tried (137 of 370; F-021)."),
 ("N08", "statement", "When members judge that the room", "When a room judges it has too few hands to hold its spot (K02), it stops fighting for it and moves (P10), and members keep calling for the new spot."),
 ("N08", "finding", "F-002", "F-019"),
 ("N08", "decides", "The order holds in 11 of 21 rooms", "The order holds in 11 of 21 rooms. Read whole at C5c-09, the judgment came before a move after a loss in 10 of the 20 rooms that moved (9 if a coalition's move is read so), voiced for the room in 7; in the other 10 the loss itself prompted the move (F-019). A late room wrote its judgment after the move (guatemala, h79.1)."),
 ("N08", "boundary", "Rooms inside a coalition", "Rooms inside a coalition that move by the coalition's plan (A10's bound). Rooms that judge their hands too few after a loss and give the work up instead: of 36 rooms that voiced such doubt and lost their work, 10 moved and 11 gave the work up (F-019)."),
 ("N09", "statement", "A settled border (P08) gives members", "A settled border (P08) opens a channel through which the two rooms trade help (P16). Sparing a neighbour's work (P07) follows border talk in more rooms than chance gives, but the line a settled border would give is theorised: the first sparing names a border or deal in 17 of 124 rooms, and mostly states the room's own norm (F-020)."),
 ("N09", "finding", None, "F-020"),
 ("N09", "level", "inside Order without law", "inside Order without law; two thin arrows, A05's mechanism theorised"),
 ("N09", "decides", "Sparing comes first in 52 of 158", "Read whole at C5c-09: the first help names a deal, border, truce, alliance, an exchange or the neighbour relation in 63 of 127 rooms where border talk comes first, against 23 of 67 where help comes first (F-020). Both arrows beat their nulls' 95th percentile by a little: A05 by 0.013, A14 by 0.009."),
 ("N09", "boundary", "Neighbours who spare each other", "Neighbours who spare each other with no talk at all, on the room's own norm (Live and let live; F-020)."),
]
for pid, f, starts, new in CH:
    cur = spec[pid].get(f)
    if starts is None:
        if cur is not None:
            sys.exit("%s.%s exists: %r" % (pid, f, str(cur)[:60]))
    elif not str(cur or "").startswith(starts):
        sys.exit("%s.%s does not begin with %r: %r" % (pid, f, starts, str(cur)[:60]))
    spec[pid][f] = new
print("%d fields check" % len(CH))
if "--write" in sys.argv:
    json.dump(spec, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("c5_propositions.json written")
