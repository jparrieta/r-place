#!/usr/bin/env python3
"""D3a-32: build A05's add-condition and add-step rulings (G4a and G37) from one table, so each id carries its own
evidence and the statement that holds its condition. Every id must be in the add packets, and every packet id here.
Evidence paraphrases the packet's code labels, without quotation marks.

  python3 out/_analysis/d3_a05_adds.py
"""
import json
import subprocess
import sys

P21 = ("the condition, that an agreement restrains only the placers it reaches and who accept it, is held by P21's "
       "statement (members state the limits of who may commit the room) and by A05's mechanism (members remind others "
       "of the line)")
P14 = ("the condition, that agreed restraint reaches scripted placement only when the scripts' targets are changed, is "
       "held by P14's statement (the room argues over its machine hands and adjusts them) and P21's")
BOUND = ("the condition, that sparing can rest on a norm, a memorial, the work's first maker, a complaint or an apology "
         "with no settled border, is held by A05's own bound ('Sparing often comes first and tacit, before any talk')")
TALK = ("the condition, that restraint can be promised while terms are still being talked, is held by A05's own "
        "connection, which counts border talk, truce or deal before the first sparing, not a finished settlement")
ROWS = [
    ("2007scape-032", "(2)", "c0723 a truce proposed, c0724 a truce rejected because this is open wildy, c0765 a doubt that the call-off will reach everyone", P21),
    ("AmericanFlaginPlace-033", "(2)", "c0173 the flag held to its border under a truce, c0216 the expansion admitted too aggressive, c0275 unsanctioned expansion called out", P21),
    ("DestinyTheGame-030", "(2)", "c0216 a call to war, c0218 a member saying there is no war, c0219 the deal invoked to stop removing Scotland's banner", P21),
    ("GrowTheTree-029", "(2)", "c0059 some neighbours helping while the rest expand, c0060 a Discord deal unable to steer an inattentive hivemind", P21),
    ("ManningPlace-026", "(2)", "c0055 some people not having the memo after most agreed to go under", P21),
    ("ScottPilgrim-029", "(2)", "c0015 a no-overlap agreement with r/Telegram, c0039 most sprite workers said to be beyond control", P21),
    ("TheFarLeftSide-035", "(2)", "c0377 a protectorate undone, c0460 an official pact sought so members stop undoing it", P14),
    ("TheHulk-037", "(1)", "c0013 discussion opened, c0015 an apology and a promise to leave the overlap alone, c0017 the border agreed", TALK),
    ("ainbowroad-052", "(2)", "c0277 unsanctioned expansion disavowed, c0365 agreement not to support it, c2039 hivemind action blamed", P21),
    ("berkeley-042", "(2)", "c0098 a builder refusing entreaties for Oski and accepting it may be deleted", P21),
    ("bindingofisaac-048", "(2)", "c0143 HotS telling its people not to ruin Isaac, c0184 rogue people blamed", P21),
    ("buffalobills-026", "(2)", "c0025 the Harry Potter deal announced, c0026 the border repaired, c0133 a warning that pushing the red breaks the deal", P21),
    ("calgaryflames-050", "(2)", "c0149 Waldo's hair fixed to keep the promise, c0150 a member joining after learning of it", P21),
    ("clg-031", "(2)", "c0067 Broncos fans messaged one by one about the truce, c0068 an announcement asked for", P21),
    ("columbia-031", "(1)", "c0031 a proposal that Tails stays while both leave the banner alone, c0032 neutrality agreed after talk in the other sub", TALK),
    ("de-050", "(2)", "c0518 a counterattack dropped after learning of the merger plan, c0755 an agreement denied", P21),
    ("denverbroncos-027", "(1)", "c0094 a deal offered to prevent destruction, c0095 overlap promised without destroying the neighbour's work", TALK),
    ("epublica-023", "(2)", "c0040 a pixel undone before learning of the Hoodr agreement, c0049 an apology after learning it", P21),
    ("fivenightsatfreddys-033", "(1)", "c0521 an apology for painting through the Philippines flag, c0567 an ally's last squid spared as rude to take", BOUND),
    ("france-037", "(2)", "c0185 a boundary at parallèle 771, c0280 an apology for another French community's erasure, c0467 lines renegotiated after allies vandalised the treaty", P21),
    ("futurama-039", "(1)", "c0101 r/toolband welcomed on condition they do not touch Bender, c0102 Pokemon said not to touch Bender", TALK),
    ("greenbaypackers-024", "(2)", "c0211 attackers told to keep the truce because the Vikings have more people", "the condition, that a member asks for the truce to be kept because a fight would be lost, is held by A16's mechanism (a refusal states the attack's cost)"),
    ("habs-027", "(1)", "c0177 a refusal to ruin what MIT and McGill worked on, c0185 the repaired drawing left alone", BOUND),
    ("india-035", "(2)", "c0315 a promise to keep Squidward's nose short, c0321 scripts that ignore the nose while the flag stops at the border", P14),
    ("italy-054", "(2)", "c0140 protected pixels added to the script, c0146 no way to know who overwrites, c0183 protected coordinates offered", P14),
    ("leafs-032", "(2)", "c0267 a visitor apologising after learning of a deal, c0231 border damage called a communication issue", P21),
    ("lebanon-035", "(2)", "c0188 an unaware placer messaged about the treaty, c0192 a breach shrugged off for another conquest", P21),
    ("metroid-048", "(1)", "c0174 the Puffle explained as a memorial, c0177 the memorial honoured, c0178 the proposal withdrawn", BOUND),
    ("minnesotavikings-046", "(2)", "c0199 an apology after learning of the truce, c0247 an attack made without knowing of it, c0254 neither side able to control everyone", P21),
    ("monero-021", "(2)", "c0073 unattended bots gone rogue, c0075 the treaty said to be upheld, c0081 differing scripts making helpers fight", P14),
    ("monsterhunter-028", "(2)", "c0138 potion repairs stopped for the placestart pact, c0162 repairs still running after the treaty", P14),
    ("mylittlepony-036", "(1)", "c0054 a refusal to mess with anyone else's art, c0153 bronies asked to stop cutting into Sans's head", BOUND),
    ("nVade-028", "(2)", "c0034 agreement not to expand into Rainbow Road, c0035 the deal not holding, c0049 a member standing down after missing the directive", P21),
    ("neu-054", "(2)", "c0015 an apology for missing the truce, c0033 red pixels blamed on people who missed the leaders' peace", P21),
    ("ockytop-036", "(1)", "c0024 peace offered if Tennessee stops at TN, c0025 the compromise rejected with a call to war", "the condition, that an offered border must be accepted before it can guide restraint, is held by A05's own connection, which needs border talk, a truce or a deal, and P08's contesting of terms"),
    ("osugame-032", "(2)", "c0339 the original agreement explained, c0340 the truce kept while negotiation waits for rebuilding", P21),
    ("overwatch-039", "(2)", "c1111 an apology for colouring over the rainbow and a repair, c1112 territorial agreements said to break through lack of information", P21),
    ("pepe-027", "(2)", "c0031 Pepe asked to pull back from a tree under truce, c0032 control over Pepe's placers denied", P21),
    ("placecanada-031", "(2)", "c0109 people told not to take 1G territory, c0110 building there anyway", P21),
    ("placesnek-032", "(2)", "c0012 a Discord agreement to fix snek, c0098 Poland still stepping on it", P21),
    ("pokemon-053", "(1)", "c0473 an attack on the Ukraina flag challenged, c0474 an apology and a promise not to touch it, c0492 a giant image over smaller art refused", BOUND),
    ("poland-054", "(2)", "c0039 peace negotiated and waiting for news to spread, c0046 and c0080 calls to repel or remove AMD", P21),
    ("quebec-026", "(1)", "c0169 a memorial asked to be left alone, c0170 agreement to leave it", BOUND),
    ("radiohead-025", "(2)", "c0247 a defender sent to the agreement, c0248 the instruction accepted, c0240 the concern dismissed", P21),
    ("reddevils-049", "(2)", "c0144 a truce post asked for so ignorant attacks stop, c0204 a breach admitted, c0212 reminders said to do only so much", P21),
    ("rhythmheaven-047", "(2)", "c0057 everyone told while the logo runs on autopilot, c0059 builders shouted at to stop ruining Play-Yan", P21),
    ("stevenuniverse-027", "(2)", "c0314 people asked not to restore Pink Diamond over r/polandball's text, c0362 many not knowing Discord plans or peace accords", P21),
    ("stlouisblues-044", "(2)", "c0116 an apology after missing the alliance sticky, c0118 well-meaning allies harder to defend against than vandals", P21),
    ("straya-041", "(2)", "c0050 PMs to people going against official plans and the non-aggression pact, c0134 an offer that does not promise the whole room", P21),
    ("texastech-026", "(2)", "c0027 the script edited to share a border with NEU, c0040 the green blob proposed for more space, c0042 help promised if it fights back", "the condition, that restraint toward the neighbour agreed with can sit beside encroaching on a third, is held by P09's statement (encroaching counts as an attack) and P17's (allies backing each other)"),
    ("thesilphroad-042", "(2)", "c0644 an assurance not to touch the Pokémon, c0645 removal stopped for now with a warning", P21),
    ("titanfall-028", "(1)", "c0114 a call to fight withdrawn after learning UB was there first, c0115 an apology and a retreat", BOUND),
    ("torontoraptors-028", "(2)", "c0132 a proposal to cover VT, c0133 the effort it would need, c0134 the treaty with r/vermont recalled, after placement closed", "the condition, that a treaty recalled after placement has closed can show restraint only in talk, is held by P12's statement (the room records the work after hour 73) and A05's mechanism"),
    ("uofm-023", "(1)", "c0075 and c0111 reciprocal restraint offered on condition that red attacks end", "the condition, that restraint is offered on condition of the neighbour's own, is P08's terms, which A05's connection counts as border talk before the sparing they set"),
    ("uoft-031", "(2)", "c0125 part of Thailand's flag kept in return for room, c0133 authority to speak for all of r/Thailand disclaimed, c0151 a broken border promise", P21),
    ("weezer-047", "(2)", "c0065 a breach explained as missed communication and repaired, c0067 taking the space endorsed despite the treaty", P21),
    ("wholesomememes-029", "(1)", "c0026 PEACE tiles placed around a chequered pattern rather than over it", BOUND),
    ("xcom-046", "(2)", "c0041 XCOM asked to stop removing the neighbours' beam, c0042 the beam repaired, c0043 builders asked to keep it", P21),
    ("xenoblade_chronicles-024", "(1)", "c0048 green left in place because it does not vandalize the Monado", BOUND),
    ("yugioh-034", "(2)", "c0110 terms agreed, c0112 the agreement unable to reach sudden greenlattice helpers, c0114 their help regretted", P21),
    ("GreenCorner-036", "(1)", "c0025 a request to build around the RIP TOM memorial, c0091 agreement to build around it", "the step, sparing a memorial on request with no settled border, is held by A05's own bound ('Sparing often comes first and tacit, before any talk')"),
    ("landry-005", "(1)", "c0002 a complaint that Landry builds over r/Predators, c0004 a promise of no more trouble and help to rebuild, c0006 building stopped there", "the step, withdrawal answering a complaint before any border is settled, is held by A05's own bound"),
]


def packet_ids():
    ids = []
    for op, n in (("add-condition", 60), ("add-step", 2)):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A05", "--op", op,
                              "--offset", "0", "--limit", str(n)], capture_output=True, text=True).stdout
        ids += [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]
    return ids


ids = packet_ids()
mine = [r[0] for r in ROWS]
assert sorted(ids) == sorted(mine) and len(set(mine)) == len(mine), (set(ids) ^ set(mine))
with open("out/_analysis/d3_rulings/A05-adds.jsonl", "w") as f:
    for aid, clause, ev, held in ROWS:
        reason = f"G4a {clause} and G37: {ev}; {held}; a specification"
        f.write(json.dumps({"adaptation": aid, "decision": "accept", "kind": "specification", "reason": reason},
                           ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A05-adds.jsonl")
