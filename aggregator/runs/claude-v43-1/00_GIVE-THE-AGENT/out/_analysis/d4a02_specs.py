#!/usr/bin/env python3
"""D4a-02, the second pass: write the specs of the cuts F07 to F35 for d4_cut.py, from my reading of each key's lines
(out/_analysis/d4a02_keys/<key>.txt, by d4_key_lines_bynode.py), under cut rules R1 to R3 and the dated amendment
R1a to R1c. Each spec carries the reading that grounds it; the quoted phrases are the labelers' how sentences, not
members' words. Writes out/_analysis/d4a02_cut_<id>.json; never overwrites.

    python3 out/_analysis/d4a02_specs.py
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
TOP = ("Cut rules R1 and R2 (tree-D4.md), with R1a (the level): the key's lines, read whole in "
       "_analysis/d4a02_keys/%s.txt, state one shared change to %s. ")
SUB = ("Cut rule R3: a level-3 child of %s's key, held by 5 or more of its members, whose lines (read in "
       "_analysis/d4a02_keys/%s.txt) state a narrower change than %s's. ")
S = []


def top(fid, key, level, name, wic, why):
    el = key.split(":")[1]
    f4 = key.split(":")[0] + "_" + el + "_" + key.split(":")[2]
    S.append({"id": fid, "parent": None, "level": level, "keys": [key], "name": name, "what_it_changes": wic,
              "move": "merging", "why": TOP % (f4, el) + why + " These are the labelers' how sentences.",
              "ground": "keys"})


def sub(fid, parent, pkey, key, name, wic, why):
    f4 = "%s_%s_%s" % tuple(pkey.split(":"))
    S.append({"id": fid, "parent": parent, "level": "third", "keys": [key], "name": name, "what_it_changes": wic,
              "move": "splitting", "why": SUB % (parent, f4, parent) + why + " These are the labelers' how sentences.",
              "ground": "keys"})


top("F07", "restrict:P05:T4-006", "fourth",
    "the telling clause not shown at the design: informed members reject the planned change",
    "P05's added clause says that a planned change is repaired away until its keepers are told. In these rooms the "
    "lines limit the clause where the design is settled. About half say that members who know of the change reject "
    "it, so repair or recolouring enforces a competing design, and telling does not settle it. The others say the "
    "record does not show the untold keepers, the agreed change or the loss that the clause needs. The frozen clause "
    "holds here only in part.",
    "R1a: T3-004 (settling the mark's design) holds 47 of the 59 rooms, under 80 per cent, so the branch is declared "
    "at the fourth order. 'Informing keepers of an agreed colour does not secure acceptance when a participant "
    "explicitly rejects the vote after being told its result' (AyyMD); 'When keepers explicitly reject a proposed "
    "design, restoration can enforce competing commitments rather than result from not being told' (flashtv); "
    "'The information-failure explanation requires evidence of an agreed change, reversal, and failed communication' "
    "(coldplay). Two lines are the re-check corrections of polska and satania (F-024).")
top("F08", "add-step:P14:T3-028", "third",
    "machine hands kept on one target: installing, teaching and updating every runner",
    "P14 says the room adjusts its machine hands. In these rooms the adjusting is a step of its own: members install "
    "the script and teach it, and they keep every runner's target current, because a stale target undoes the room's "
    "own new design. A revision must reach the operator and the target file, not only the people.",
    "R1a: T3-028 (running scripts for the work) holds 50 of the 58 rooms. 'Synchronizing script versions and "
    "coordinates prevents outdated targets ... from wasting placements by repairing one another' "
    "(AmericanFlaginPlace); 'Friendly alterations require disabling or retargeting active repair scripts rather than "
    "only telling humans about a new plan' (teslamotors); 'A proposed revision must reach the operator and be encoded "
    "in the target before automated upkeep stops undoing it' (zootopia).")
top("F09", "link:P03:T4-014", "fourth",
    "the move returns to building: relocation followed by renewed construction",
    "The model runs from building to keeping and, after a loss, to the move (P10), but no arrow runs from the move "
    "back to building. In these rooms it does: after a relocation the room recruits, designs and builds again at the "
    "new spot, and members report the new work.",
    "R1a: T3-022 (relocating after losing the spot) holds 41 of the 54 rooms and T3-020 (choosing a canvas spot) 11, "
    "so the branch is declared at the fourth order; the two state the same change, so neither is a subform. "
    "'Relocation after loss returns participants to placing and progress reports rather than ending the building "
    "process' (animalcrossing); 'The loss-triggered move immediately restarts construction with a different design, "
    "supplying a local return omitted by the standing arrows' (msu).")
top("F10", "add-step:P08:T3-010", "third",
    "a deal carried out as work: prepared in the room, then implemented and relayed",
    "P08 says rooms propose, settle and contest deals and hold each other to them. In these rooms a deal also takes "
    "work around it: members prepare it inside the room (local consensus, a contact, checks on the counterpart's "
    "credibility), and they carry it out by moving placed work, changing templates and bot targets, and relaying the "
    "terms to placers who do not know them.",
    "R1a: T3-010 (settling borders with neighbours) holds 38 of the 47 rooms. 'Making accommodation effective "
    "requires contacting responsible bot operators and changing the target after permission is reported' "
    "(drumcorps); 'Distributing an agreement to ordinary placers remains a separate task after organizers approve "
    "it' (skyrim); 'Members seek local consensus before communicating a territorial proposal' (ohio).")
top("F11", "add-step:P13:T4-028", "fourth",
    "carrying on as renewed work, begun before the close",
    "P13 says that near the close and after it the room decides what of its effort to keep. In these rooms carrying "
    "on is work in its own right, and it starts while placement is live: on another canvas the room recruits, builds "
    "and defends again, members remake the work in other media, and the mark is adopted into the room before the "
    "close.",
    "R1a: T3-054 (carrying work to new canvases) holds 22 of the 43 rooms, T3-057 9 and T3-156 7, so the branch is "
    "declared at the fourth order. 'Continuation after the original closure includes renewed recruitment, building, "
    "coordinates, and design adjustment on replacement canvases' (gravityfalls); 'Remaking in another medium begins "
    "while the original canvas remains live' (prequelmemes).")
sub("F12", "F11", "add-step:P13:T4-028", "add-step:P13:T3-054",
    "the spine restarted on another canvas",
    "Within F11, the room carries its work to a successor canvas, and there the spine runs again: recruiting, "
    "choosing a site, building, defending and losing work.",
    "'Continuation on another canvas restarts recruitment, representation and defense' (bindingofisaac); "
    "'Successor-canvas continuation renews building and vulnerability to loss instead of merely preserving an image' "
    "(gamindustri).")
sub("F13", "F11", "add-step:P13:T4-028", "add-step:P13:T3-057",
    "the work remade in other media, often before the close",
    "Within F11, members remake the canvas work elsewhere (fan art, games, physical copies, a quoted text), and this "
    "often begins while the original is still live.",
    "'Design reuse begins during live construction and continues in later fan making' (lovelive); 'Participants "
    "recruit creative work and turn canvas features into proposed game characters, locations, plots and fanart' "
    "(touhou).")
sub("F14", "F11", "add-step:P13:T4-028", "add-step:P13:T3-156",
    "the mark adopted as the room's emblem while it is still placed, damage included",
    "Within F11, the room takes the mark into its own sub (banner, flair, a room feature) during placement, and it "
    "may adopt the damaged form as fitting.",
    "'Adoption can occur during live placement and include correction of the image already installed on the "
    "subreddit' (pitt); 'Members revalue an unwanted final blemish as an emblem' (cgpgrey).")
top("F15", "add-step:P04:T4-008", "fourth",
    "the plan kept current: correcting, updating and re-circulating the template",
    "P04 says members circulate a template or coordinates and ask strays to keep to them. In these rooms the template "
    "needs upkeep of its own: members correct the reference against the canvas, replace stale plans, make updates "
    "noticeable, route helpers to the current version and message friendly placers who still follow a superseded one.",
    "R1a: T3-070 (sharing coordinates, templates and how-to) holds 33 of the 42 rooms, just under 80 per cent, so "
    "the branch is declared at the fourth order. 'Members correct references against current placements and replace "
    "stale plans' (FloydVsVoid); 'Helpers request warnings on obsolete templates and links to current designs so "
    "intended repair does not undo the plan' (monalisaclan); 'Revised targets need repeated visibility work among "
    "keepers who otherwise restore the old form' (linux).")
top("F16", "add-step:P23:T3-014", "third",
    "the chat kept open: invitations renewed, entrants screened, decisions relayed",
    "P23 (a candidate) says members move planning into a chat and invite helpers. In these rooms the chat's access "
    "is upkeep: members replace expired invitations and broken links, screen who comes in, and relay decisions back "
    "to the thread for those outside.",
    "R1a: T3-014 (moving planning into a chat) holds 35 of the 39 rooms. 'Access to the planning venue requires "
    "replacing expired invitations and responding when the replacement expires again' (pcmasterrace); 'Organizers "
    "screened applicants and shared invitations privately' (stevenuniverse); 'Returning decisions to accessible "
    "threads lets people without chat access follow design and alliance changes' (theexpanse).")
top("F17", "add-step:P11:T4-026", "fourth",
    "the marking provisional and contested: success judged and credit disputed while the work goes on",
    "P11 says that when a work is up the room marks it: announces, celebrates and credits. In these rooms marking "
    "comes while the work is still live and is open to dispute: success is judged by what survives, completion is "
    "provisional, upkeep goes on, and credit is challenged and corrected.",
    "R1a: T3-009 (celebrating the finished work) holds 15 of the 36 rooms and T3-043 (crediting who made the work) "
    "14, so the branch is declared at the fourth order. 'Completion can be provisional and answered by an instruction "
    "to keep working' (fxKorea); 'Participants contest authorship during active work' (afip).")
sub("F18", "F17", "add-step:P11:T4-026", "add-step:P11:T3-009",
    "success judged while upkeep continues",
    "Within F17, the room judges success by recognizable survival rather than a perfect mark, treats completion as a "
    "milestone, and keeps the obligation to maintain.",
    "'Participants assess success through recognizable survival rather than perfect lettering, while maintenance "
    "continues after celebration' (bostonceltics); 'Celebration can mark a temporary accomplishment while members "
    "explicitly retain the obligation to maintain it' (ripcity).")
sub("F19", "F17", "add-step:P11:T4-026", "add-step:P11:T3-043",
    "credit contested during the work",
    "Within F17, members dispute and correct who made the work while it is still being placed: accusations, denials, "
    "competing labour claims and corrected omissions.",
    "'Credit is actively checked and corrected during ongoing work rather than appearing only at the close' (anime); "
    "'Attribution includes disputes about authentic makers, first arrival and proof during ongoing work' (Okami).")
top("F20", "add-step:P12:T3-117", "third",
    "the close as news: late arrivals told that placement has ended",
    "P12 says the room records what happened and marks the end. In these rooms the end itself must travel: members "
    "who did not know offer to rebuild or ask for help, and others tell them that placement has ended and correct the "
    "stale call.",
    "add-step on P12 at T4-027 (33 rooms) was set aside, since its lines state several different steps; its child "
    "T3-117 (marking the canvas's end, 10 rooms) states one, so it is cut on its own at the third order. 'Members "
    "correct a stale rebuilding promise before its proposer acknowledges that the event has ended' (hatsune); 'An "
    "ending announcement informs a participant whose workday delayed awareness' (eder).")
top("F21", "restrict:K01:T4-001", "fourth",
    "the canvas call not a joke: the April Fools frame kept apart from the canvas work",
    "K01 says that a claim in the host sub, a call to the canvas included, may be a joke. In these rooms the play "
    "stays with the sub's own business: its fakes and takeovers do not make the canvas calls jokes, and the frame "
    "does not decide what the canvas work was.",
    "R1a: T3-001 holds 10 of the 32 rooms, T3-048 8 and T3-023 7, so the branch is declared at the fourth order. "
    "'Responses to an external platform prank establish a local joke dispute without establishing host parody or a "
    "joking frame for canvas recruitment' (twitch); 'The host's play frame cannot decide the truth of a particular "
    "canvas plan' (utaustin).")
top("F22", "add-condition:P16:T4-017", "fourth",
    "help conditional on the helper's own work and spare hands",
    "P16 says rooms help one another, trade help and turn requests away. In these rooms help waits on conditions "
    "the statement does not hold: the helper's own work must be safe or finished, the helper must have pixels and "
    "time to spare, and the terms (space, non-interference, recognizable help) must hold.",
    "R1a: T3-011 holds 12 of the 30 rooms and T3-151 10, so the branch is declared at the fourth order. 'Offered aid "
    "depends on keeping one's own work secure and having placements to spare' (OnePiece); 'Outgoing help receives "
    "turns only when the home plot needs no correction' (hentai); 'Help is offered explicitly on condition that the "
    "neighbour does not interfere with the host's work' (shishamo).")
top("F23", "add-condition:P13:T4-028", "fourth",
    "the close scoped to the original canvas: continuation renewed, uncertain and contested",
    "P13 places the decision near the close and after it. In these rooms the stop at hour 73 binds only the original "
    "canvas: on successor canvases placement goes on, and continuation is often one member's attempt, contested or "
    "unfinished, and conditioned on tolerable upkeep and access.",
    "R1a: T3-054 holds 23 of the 30 rooms, under 80 per cent, so the branch is declared at the fourth order. "
    "'Cessation at hour 73 applies to the original platform, while successor canvases allow renewed placement after "
    "that closure' (rotmg); 'A successor project can remain an individual's contested attempt rather than become a "
    "room-wide decision to continue' (bardmains).")
top("F24", "restrict:P14:T4-009", "fourth",
    "machine hands debated, not shown placing",
    "P14 says members add placements with scripts, bots and spare accounts, and argue over them. In these rooms only "
    "the arguing part shows: scripts are offered, debated, refused or attributed to outsiders, and the room's own "
    "machine placement is not shown.",
    "R1a: T3-027 holds 14 of the 27 rooms and T3-028 11, so the branch is declared at the fourth order. 'Script "
    "debate and explicit refusal must be distinguishable from local adoption' (mindcrack); 'The record establishes "
    "script provision and reception but does not establish execution or additional placements' (rutgers).")
top("F25", "restrict:P13:T4-028", "fourth",
    "carrying on in talk: proposals and single attempts, not shown taken up",
    "P13 says the room decides what to keep. In these rooms carrying on shows as invitations, proposals and one "
    "member's attempt; collective uptake and durability are not shown, and some reuse begins during live placement.",
    "R1a: T3-054 holds 17 of the 27 rooms, so the branch is declared at the fourth order. It shares fewer than 5 "
    "rooms with F23 (R1b). 'Replacement proposals and one proposer's completed flag establish individual "
    "continuation but not collective adoption or lasting organization' (czech); 'Reuse can begin during live "
    "placement rather than only near or after the close' (pcmasterrace).")
top("F26", "restrict:P05:T3-010", "third",
    "the telling clause not shown at the border: informed members contest the terms",
    "As in F07, P05's added clause holds only in part, here where the planned change is a border or compromise "
    "agreed with a neighbour: members who know the terms contest them or refuse the concession, or the record does "
    "not show untold keepers or the loss.",
    "R1a: T3-010 holds 23 of the 27 rooms. 'Continued opposition cannot be explained solely by missing instructions "
    "when informed members dispute the agreement or reject the concession' (harrypotter); 'Informed holdouts can "
    "reject an approved change after knowing of it' (placeportalpattern). One line is maryland's re-check correction "
    "(F-024).")
top("F27", "restrict:P05:T4-013", "fourth",
    "the telling clause not shown in keeping: interference seen, its cause and loss not",
    "As in F07, P05's added clause holds only in part, here in watching, repairing and defending: interference with a "
    "planned change is seen, but who was told, whether keepers knew, and whether the change was lost for want of "
    "telling are not, and informed disagreement also occurs.",
    "R1a: T3-005 holds 14 of the 27 rooms and T3-021 11, so the branch is declared at the fourth order. 'Wrong repairs "
    "establish distorted upkeep but not obsolete keeper knowledge or failed communication reversing an agreed change' "
    "(lakers); 'Telling keepers about a change does not itself establish acceptance' (radiohead). One line is armok's "
    "re-check correction (F-024).")
top("F28", "add-condition:P16:T3-010", "third",
    "help at the border conditional: on the home work, the terms and harm to a third room",
    "As in F22, help waits on conditions the statement does not hold, here where neighbours settle borders: the "
    "helper's home work comes first, help depends on stopping attacks or on sparing a work, it can entail destroying a "
    "third room's mark, and offers often stay offers.",
    "R1a: T3-010 holds 22 of the 27 rooms. 'Outgoing help competes with defending or finishing the home mark and can "
    "wait until that work is secure' (quebec); 'Helping one recipient can entail destroying a third party's work' "
    "(hungary); 'Rebuilding aid is conditional on cooperation and stopping attacks' (catalunya).")
top("F29", "add-condition:P23:T3-014", "third",
    "the chat's reach conditional: access, and the return of decisions to the thread",
    "P23 (a candidate) says members move planning into a chat and bring its decisions back. In these rooms the "
    "chat's reach depends on working access, and those outside it learn only what returns to the thread; its "
    "decisions do not bind those who cannot see them.",
    "R1a: T3-014 holds 25 of the 26 rooms. 'Participation through chat depends on usable invitations and access that "
    "several participants report lacking' (placestart); 'Chat coordination must reach placers outside the chat' "
    "(masseffect); 'Reported chat decisions cannot be treated as room-wide consensus when nonparticipants and "
    "competing factions contest the chat's authority' (fivenightsatfreddys).")
top("F30", "restrict:P23:T3-014", "third",
    "the chat seen only from outside: invitations and returned reports, not its decisions",
    "P23 (a candidate) says the room's design, borders and diplomacy can be settled in the chat. In these rooms the "
    "record shows only the outside of the chat: invitations, venue proposals and reports that come back. Its "
    "deliberation, membership and authority are not shown.",
    "R1a: T3-014 holds all 24 rooms. 'Public reports establish chat coordination but not the hidden decisions, "
    "membership or diplomatic proceedings inside it' (chile); 'The record shows referrals into planning but not how "
    "the unseen chat decided or whether it could command placers' (porterrobinson).")
top("F31", "restrict:P19:T3-010", "third",
    "hosting as one-off permission: requests and leave, no standing host rule",
    "P19 says one room's work lives on another's mark under the host's rule, with hosts ruling on requests. In these "
    "rooms hosting shows only as a guest's request and a one-off permission, often provisional or contested; a "
    "standing host rule, an approval procedure or durable guest status is not shown.",
    "R1a: T3-010 holds 22 of the 23 rooms. 'Request-level permission does not establish a durable host-rule system "
    "or compliance by all placers' (chicago); 'Claimed hosting rules remain contestable and a replacement permission "
    "is explicitly provisional' (malaysia).")
top("F32", "link:P05:T3-009", "third",
    "the marking returns to keeping: celebration followed by renewed defence",
    "The model runs from building to marking (A07) and from building to keeping (A03), but not from marking back to "
    "keeping. In these rooms it does: a celebration or completion post draws renewed defence calls, repair and night "
    "cover in its own thread.",
    "R1a: T3-009 (celebrating the finished work) holds 21 of the 23 rooms; 19 of the 23 lines were ruled "
    "elaborations. 'A completion celebration receives a direct protection appeal, making celebration a point for "
    "renewing upkeep rather than simply ending work' (httyd); 'Celebration threads reopen into vigilance and night "
    "coverage rather than terminating maintenance' (newzealand).")
top("F33", "add-step:P04:T4-006", "fourth",
    "the plan kept current while the design settles",
    "As in F15, the template needs upkeep of its own, here while the design is still being settled: members check "
    "details against one another's instructions, correct and replace the reference, retire outdated posts and "
    "message overwriters, so that one updated plan replaces competing ones.",
    "R1a: T3-004 holds 13 of the 23 rooms, so the branch is declared at the fourth order. It shares fewer than 5 rooms "
    "with F15. 'Maintainers synchronize revised pixels and message overwriters so an updated reference can replace "
    "competing understandings' (gatech); 'Standardization includes retiring outdated posts, announcing changed "
    "locations and stopping work on obsolete outlines' (tf2).")
top("F34", "add-condition:P02:T4-006", "fourth",
    "the design sized to the hands: scale and detail conditioned on crew, upkeep, space and colours",
    "P02 says the room settles what its mark will show. In these rooms the design is conditioned by what the room "
    "can build and keep: its scale and detail depend on the crew it can assemble, the upkeep it can sustain, the "
    "space it can protect and the colours available.",
    "R1a: T3-004 holds 10 of the 22 rooms and T3-033 6, so the branch is declared at the fourth order. 'The "
    "preferred design is conditional on assembling a sufficiently large crew' (anaheimducks); 'Further detail "
    "depended on the ability to maintain it' (strangerthings); 'A small pool of builders makes compactness a "
    "condition of finishing' (evex).")
top("F35", "add-step:P01:T3-002", "third",
    "the call made workable: answers ask for a task, and callers supply it",
    "P01 says the room calls members and kindred subs to place. In these rooms answering a call is an exchange: a "
    "willing member asks what to do, where to start or for backup, and the caller supplies instructions, location "
    "cues and visibility (a sticky, other venues), reaching people beyond the room.",
    "R1a: T3-002 (calling members in to place) holds 18 of the 20 rooms; 19 of the 20 lines were ruled elaborations. "
    "'An interested answer can return the next action to the caller by asking what to do' (polyamory); 'Accepting "
    "participation can simultaneously request the coordinates or backup needed to make the commitment workable' "
    "(stargate); 'Moderators increased a recruitment call's visibility by stickying it' (littlewitchacademia).")
for s in S:
    p = os.path.join(AN, "d4a02_cut_%s.json" % s["id"])
    if os.path.exists(p):
        raise SystemExit("refusing to overwrite %s" % p)
for s in S:
    json.dump(s, open(os.path.join(AN, "d4a02_cut_%s.json" % s["id"]), "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
print("wrote %d specs: %s" % (len(S), ", ".join(s["id"] for s in S)))
