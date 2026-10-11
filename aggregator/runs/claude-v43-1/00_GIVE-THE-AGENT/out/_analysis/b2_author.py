#!/usr/bin/env python3
"""B2a-r1: the author's placements of the hard set and the gold set, written before any packet exists.

Each entry: item, set (r1|gold), third_order (primary first), why per theme, confidence, support.
The script checks every theme id against scheme.jsonl and every support code against the item's own
concepts in the store, adds `source` from the draw lists, and `working` (the item's kinds in
scheme_current.jsonl) so a difference from the B1 grouping is on the record.
Writes out/author_items.jsonl (r1) and out/gold_items.jsonl (gold) with --write; dry run otherwise.
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
A, C = "arguable", "clear"

P = [
 # ---- round 1 ----
 ("r1", "GreenCorner/t03", [("T3-005", "alarms and calls to defend and retake the corner against Blue's invasion lead (c0014, c0062, c0065, c0068)"),
                            ("T3-021", "fixing miscolours and cleaning are upkeep with concepts of their own (c0006, c0031)")], A, ["c0014", "c0062", "c0065", "c0068", "c0006", "c0031"]),
 ("r1", "anarcho_capitalism/t12", [("T3-149", "a truce offered by a rival faction and the Void's non-aggression promise accepted (c0126, c0136, c0137)"),
                                   ("T3-010", "fitting the sign between the snek and the text is space shared with a neighbour (c0129, c0132)")], A, ["c0126", "c0136", "c0137", "c0129", "c0132"]),
 ("r1", "AyyMD/t08", [("T3-001", "the room's own reversed loyalties, fake petition and fake resignation, then the bamboozle reveal (c0037, c0040, c0041, c0039)")], C, ["c0037", "c0040", "c0041", "c0039"]),
 ("r1", "england/t03", [("T3-028", "a placing script handed out with its run command (c0005, c0007, c0008, c0025)"),
                        ("T3-070", "coordinates and the image asked for and given for helpers (c0003, c0006, c0010)")], A, ["c0005", "c0007", "c0008", "c0025", "c0003", "c0006"]),
 ("r1", "nyu/t01", [("T3-004", "the template made more detailed and the purple surround added (c0007, c0015)"),
                    ("T3-020", "the start coordinates set and then moved (c0001, c0004)")], A, ["c0007", "c0015", "c0001", "c0004"]),
 ("r1", "dofus/t01", [("T3-033", "a member offers the Emerald to the room and points to its space (c0002, c0003)"),
                      ("T3-003", "the member reports doing it alone and adding pixels (c0015, c0017)")], A, ["c0002", "c0003", "c0015", "c0017"]),
 ("r1", "korea/t15", [("T3-015", "a moderator keeps all planning to one thread sorted by new (c0122, c0123)"),
                      ("T3-075", "members complain of twenty threads a day and ask for bans (c0096, c0125)")], A, ["c0122", "c0123", "c0096", "c0125"]),
 ("r1", "furry/t10", [("T3-070", "coordinates and templates shared for helpers and defenders (c0034, c0073, c0209, c0233)"),
                      ("T3-004", "the lettering's size and layout settled (c0092, c0093)")], A, ["c0034", "c0073", "c0209", "c0233", "c0092", "c0093"]),
 ("r1", "flashtv/t13", [("T3-073", "what became of the logo told: fixed before the end, colours changed, where it forms in the timelapse (c0212, c0214, c0215, c0216)"),
                        ("T3-009", "the finished logo celebrated (c0186, c0213)")], A, ["c0212", "c0214", "c0215", "c0216", "c0186", "c0213"]),
 ("r1", "signal/t01", [("T3-038", "interest gathered and the design being drawn at a location (c0001, c0002)"),
                       ("T3-009", "we did it and thanks with the final version (c0003, c0004)")], A, ["c0001", "c0002", "c0003", "c0004"]),
 ("r1", "acecombat/t05", [("T3-084", "other subs enlisted for aid and thanked as indispensable (c0035, c0041)"),
                          ("T3-010", "a mutual border agreed and a crossing cleared with a neighbour (c0054, c0056)")], A, ["c0035", "c0041", "c0054", "c0056"]),
 ("r1", "parabola/t02", [("T3-150", "an offered alliance to protect each other accepted, and protection agreements listed (c0011, c0012, c0016, c0019)")], A, ["c0011", "c0012", "c0016", "c0019"]),
 ("r1", "4chan/t07", [("T3-010", "the sign moved after talks and the border negotiated with neighbours (c0128, c0136, c0138, c0143)"),
                      ("T3-024", "members asked not to mess with the neighbouring art (c0011)")], A, ["c0128", "c0136", "c0138", "c0143", "c0011"]),
 ("r1", "stardustcrusaders/t19", [("T3-009", "the final product shown and an appreciation thread opened (c0304, c0306)"),
                                  ("T3-043", "the people who worked on it thanked by name of their work (c0308, c0310)")], C, ["c0304", "c0306", "c0308", "c0310"]),
 ("r1", "donaldglover/t04", [("T3-001", "the room's own fake news and pranks, and answers to them; the room testing its own fakes stays here (c0012, c0050, c0053, c0035)")], A, ["c0012", "c0050", "c0053", "c0035"]),
 ("r1", "megaman/t11", [("T3-087", "the attacker traced to a Void splinter cell and the beam said not to be the room's (c0032, c0042)"),
                        ("T3-188", "the room says it has virtually no control over the beam fired in its name (c0067)")], A, ["c0032", "c0042", "c0067"]),
 ("r1", "DevonUK/t02", [("T3-044", "an outsider finds the sub through the flag and others ask where it is (c0002, c0004, c0005)")], A, ["c0002", "c0004", "c0005"]),
 ("r1", "floridagators/t09", [("T3-014", "coordination moved to a Discord and builders sent there (c0020, c0062, c0091, c0095)"),
                              ("T3-152", "the Discord's plan brought back to the subreddit (c0067)")], A, ["c0020", "c0062", "c0091", "c0095", "c0067"]),
 ("r1", "darksouls/t13", [("T3-015", "updates gathered in a megathread and posts sent to the sticky (c0150, c0162, c0183)"),
                          ("T3-063", "proposals removed under the sub's Dark Souls 1 rule (c0181, c0185)")], A, ["c0150", "c0162", "c0183", "c0181", "c0185"]),
 ("r1", "placestart/t15", [("T3-006", "calls to kill, remove or replace other rooms' work (c0082, c0208, c0289, c0454)")], A, ["c0082", "c0208", "c0289", "c0454"]),
 ("r1", "redhotchilipeppers/t09", [("T3-009", "we did it and we made it onto the canvas, repeated (c0086, c0087, c0100, c0106, c0129)"),
                                   ("T3-043", "Discord friends, a neighbour and one member credited (c0101, c0102, c0090)")], A, ["c0086", "c0087", "c0100", "c0106", "c0101", "c0102"]),
 ("r1", "n64/t02", [("T3-038", "a member starts the logo from a reference at stated coordinates and reports it done (c0011, c0012, c0014)")], A, ["c0011", "c0012", "c0014"]),
 ("r1", "orderofthebluecorner/t08", [("T3-087", "a person named and blamed for ruining the blue corner, and bans asked (c0038, c0009)")], A, ["c0038", "c0009"]),
 ("r1", "kpop/t04", [("T3-033", "what the room should draw proposed and argued (c0015, c0018, c0019, c0024)"),
                     ("T3-136", "doubt that enough people will take part (c0020, c0022)")], A, ["c0015", "c0018", "c0019", "c0024", "c0020", "c0022"]),
 ("r1", "Goodboye/t03", [("T3-084", "pleas for assistance and cooperation from other rooms (c0026, c0004)"),
                         ("T3-011", "outsiders pledging to fight for and help reclaim the doggo (c0010, c0012, c0035)")], A, ["c0026", "c0004", "c0010", "c0012", "c0035"]),
 ("r1", "simonfraser/t08", [("T3-084", "help asked of other universities' rooms (c0042, c0063)"),
                            ("T3-011", "members help another university's logo (c0029, c0064)")], A, ["c0042", "c0063", "c0029", "c0064"]),
 ("r1", "nVade/t04", [("T3-011", "the room honours its pledge to protect another room's figure and helps its creation (c0037, c0038, c0039)"),
                      ("T3-005", "a coordinated defence called and an attack reported (c0044, c0052)")], A, ["c0037", "c0038", "c0039", "c0044", "c0052"]),
 ("r1", "cubers/t12", [("T3-169", "the sub's name added as a tag below the cube and defended (c0044, c0075, c0084, c0079)")], A, ["c0044", "c0075", "c0084", "c0079"]),
 ("r1", "survivor/t24", [("T3-037", "whether the canvas is worth caring about, said and answered (c0304, c0305)")], C, ["c0304", "c0305"]),
 ("r1", "drumcorps/t07", [("T3-014", "decisions made on Discord and builders sent there to coordinate (c0082, c0089, c0105, c0137)")], A, ["c0082", "c0089", "c0105", "c0137"]),
 ("r1", "catalunya/t01", [("T3-065", "the Senyera, the homeland's flag, proposed, called for and built (c0001, c0003, c0005, c0008)")], C, ["c0001", "c0003", "c0005", "c0008"]),
 ("r1", "criticalrole/t06", [("T3-063", "a sub rule (spoiler tags) applied to a canvas post by AutoModerator (c0043)")], A, ["c0043"]),
 ("r1", "WisconsinBadgers/t04", [("T3-076", "members argue against sabotaging fellow conference logos and for keeping their own (c0029, c0030)"),
                                 ("T3-006", "members taking a rival's spot apart, reported (c0027)")], A, ["c0029", "c0030", "c0027"]),
 ("r1", "duckgame/t02", [("T3-005", "alarms and calls to defend the duck against named attackers (c0009, c0015, c0041, c0042)")], A, ["c0009", "c0015", "c0041", "c0042"]),
 ("r1", "harrypotter/t08", [("T3-017", "the sub's usual Quidditch bot game and house points (c0024, c0025, c0026, c0033)"),
                            ("T3-043", "house points awarded to those who organised, designed and negotiated the canvas work (c0309, c0311, c0328)")], A, ["c0024", "c0033", "c0309", "c0311", "c0328"]),
 ("r1", "oneplus/t02", [("T3-095", "members test whether the company's Dash Energy announcement is real (c0003, c0007, c0021, c0022)")], C, ["c0003", "c0007", "c0021", "c0022"]),
 ("r1", "ice_poseidon/t16", [("T3-031", "damage to the room's figure recast as the room's running jokes (c0182, c0211, c0213, c0224)")], A, ["c0182", "c0211", "c0213", "c0224"]),
 ("r1", "farmcarrots/t15", [("T3-050", "an outsider taunts the room for its loss and the room relishes its replies (c0182, c0185)")], A, ["c0182", "c0185"]),
 ("r1", "guatemala/t02", [("T3-065", "the national flag started and announced (c0005, c0008, c0010)"),
                          ("T3-167", "a start time set so the first placers are not overrun (c0003, c0004)")], A, ["c0005", "c0010", "c0003", "c0004"]),
 ("r1", "Slovakia/t07", [("T3-024", "members told not to destroy neighbouring art and a plan rejected for destroying flags (c0017, c0085)"),
                         ("T3-079", "Slovak hearts made among the hearts of other nations (c0019, c0038, c0053)")], A, ["c0017", "c0085", "c0019", "c0038", "c0053"]),
 # ---- gold ----
 ("gold", "lego/t13", [("T3-021", "calls to preserve and maintain a deteriorating logo, the void only named as a threat (c0188, c0191, c0192)")], A, ["c0188", "c0191", "c0192"]),
 ("gold", "russia/t09", [("T3-010", "borders kept, permission to paint nearby asked, and order agreed with a neighbour (c0030, c0041, c0101, c0102)"),
                         ("T3-024", "refraining from encroaching on the Czechs (c0029)")], A, ["c0030", "c0041", "c0101", "c0102", "c0029"]),
 ("gold", "nuclearthrone/t06", [("T3-001", "fake startup problem and fake changelog posts (c0023, c0031, c0034, c0035)"),
                                ("T3-023", "the sub's flairs restyled for the day (c0021, c0022, c0025)")], A, ["c0023", "c0031", "c0034", "c0021", "c0022", "c0025"]),
 ("gold", "GabrielDropout/t03", [("T3-070", "location, coordinates, size and font rules given for the build (c0002, c0030, c0038, c0066)")], A, ["c0002", "c0030", "c0038", "c0066"]),
 ("gold", "mit/t01", [("T3-004", "letter thickness, whitespace and the red dot settled (c0009, c0010, c0011, c0012)"),
                      ("T3-020", "the upper-left corner set and corrected (c0002, c0003, c0004)")], A, ["c0009", "c0010", "c0011", "c0002", "c0003"]),
 ("gold", "dankmemes/t10", [("T3-033", "one-off proposals of what to draw (c0182, c0373, c0565)")], A, ["c0182", "c0373", "c0565"]),
 ("gold", "overwatch/t23", [("T3-015", "moderators asked to sticky a canvas megathread (c0441)"),
                            ("T3-075", "a filter asked because canvas posts have nothing to do with the game (c1161)")], A, ["c0441", "c1161"]),
 ("gold", "predators/t04", [("T3-070", "a colour-correct picture and a grid image given for all to use (c0012, c0014)"),
                            ("T3-004", "a redesign of the space around the logo (c0040)")], A, ["c0012", "c0014", "c0040"]),
 ("gold", "montenegro/t04", [("T3-009", "we succeeded, and congratulations (c0011, c0012)")], A, ["c0011", "c0012"]),
 ("gold", "roosterteeth/t03", [("T3-038", "the logos placed and reported, from start to nearly finished (c0003, c0030, c0037, c0060, c0075)"),
                               ("T3-004", "the surround colour settled for visibility (c0038, c0039, c0040)")], A, ["c0003", "c0030", "c0037", "c0060", "c0038", "c0040"]),
 ("gold", "DevonUK/t04", [("T3-010", "how much of the neighbour's space the Cornish flag may take, agreed (c0011, c0014)"),
                          ("T3-151", "help offered in return for working around the neighbour's logo (c0009)")], A, ["c0011", "c0014", "c0009"]),
 ("gold", "cubers/t27", [("T3-010", "borders surveyed, opened and merged with neighbours' consent (c0253, c0256, c0257, c0259)"),
                         ("T3-150", "an official border alliance of neighbours proposed (c0260, c0261)")], A, ["c0253", "c0256", "c0257", "c0259", "c0260", "c0261"]),
 ("gold", "kurdistan/t03", [("T3-010", "a deal to share and extend the Hungarian flag's space proposed (c0011, c0013)"),
                            ("T3-024", "holding back from marking the Hungarians' work (c0013)")], A, ["c0011", "c0013"]),
 ("gold", "mcgillrobotics/t02", [("T3-009", "we did it, celebrated twice (c0005, c0006)")], A, ["c0005", "c0006"]),
 ("gold", "uiuc/t04", [("T3-001", "the room's own fake news and false advice (c0028, c0030, c0032)"),
                       ("T3-095", "members test whether outside news and requests are April Fools (c0022, c0027, c0029)")], A, ["c0028", "c0030", "c0032", "c0022", "c0027", "c0029"]),
 ("gold", "polska/t10", [("T3-188", "members say the organised room does not control every Polish placer (c0039, c0061, c0085, c0114)")], A, ["c0039", "c0061", "c0085", "c0114"]),
 ("gold", "natsume/t01", [("T3-044", "newcomers led to the sub by the figure (c0003, c0010)"),
                          ("T3-082", "a member announces the figure found on the canvas with its coordinates (c0001, c0002)")], A, ["c0003", "c0010", "c0001", "c0002"]),
 ("gold", "twice/t09", [("T3-014", "a Discord opened and members sent there for live discussion and the plan (c0058, c0078, c0092, c0119)")], C, ["c0058", "c0078", "c0092", "c0119"]),
 ("gold", "floridagators/t04", [("T3-015", "proposals and helpers gathered into one thread and a stickied hub (c0016, c0041, c0100, c0119)"),
                                ("T3-063", "duplicate threads deleted and new posts removed by rule (c0032, c0120)")], A, ["c0016", "c0041", "c0100", "c0119", "c0032", "c0120"]),
 ("gold", "finland/t06", [("T3-015", "canvas posts collected in one sticky and redirected (c0068, c0080, c0082)"),
                          ("T3-063", "separate threads removed by the moderator (c0058, c0067)")], A, ["c0068", "c0080", "c0082", "c0058", "c0067"]),
 ("gold", "cuboulder/t04", [("T3-039", "backing off for the expanding neighbouring flag and making room (c0014)"),
                            ("T3-004", "a new plan for the logo circulated and proposed (c0015, c0016)")], A, ["c0014", "c0015", "c0016"]),
 ("gold", "Villanova/t01", [("T3-038", "the logo's plan, progress and reference image reported while building (c0003, c0005, c0009, c0011)")], A, ["c0003", "c0005", "c0009", "c0011"]),
 ("gold", "tinytardis/t06", [("T3-010", "how two neighbouring pictures share space, negotiated to a settlement (c0031, c0050, c0053, c0058)"),
                             ("T3-123", "the room refuses to move or change its TARDIS (c0052, c0056)")], A, ["c0031", "c0050", "c0053", "c0058", "c0052", "c0056"]),
 ("gold", "edboxes/t02", [("T3-002", "calls for hands and to spread the word (c0013, c0014, c0022)")], A, ["c0013", "c0014", "c0022"]),
 ("gold", "alberta/t04", [("T3-006", "a call to relocate Quebec's flag, cast as an invasion and as war (c0011, c0015, c0016)"),
                          ("T3-076", "members reject the attack call (c0012, c0019)")], A, ["c0011", "c0015", "c0016", "c0012", "c0019"]),
 ("gold", "ukraine/t07", [("T3-009", "praise for the work and the final result posted (c0036, c0047, c0049)")], A, ["c0036", "c0047", "c0049"]),
 ("gold", "dankmemes/t16", [("T3-073", "what happened to drawings reported: deleted, failed, too late (c0637, c0638, c0660)")], A, ["c0637", "c0638", "c0660"]),
 ("gold", "mariokart/t04", [("T3-084", "another room's member asks this room for reinforcements (c0012, c0013, c0014)")], C, ["c0012", "c0013", "c0014"]),
 ("gold", "mindcrack/t03", [("T3-002", "calls to help on the logo and for help from fellow members (c0027, c0030, c0051)")], A, ["c0027", "c0030", "c0051"]),
 ("gold", "msu/t04", [("T3-016", "the event explained as Reddit's April Fools (c0006)")], C, ["c0006"]),
 ("gold", "portugal/t41", [("T3-137", "a member worked on an outside group's build instead of the room's own (c0305, c0306)")], A, ["c0305", "c0306"]),
 ("gold", "livecounting/t02", [("T3-021", "a damaged letter spotted and fixed, repeatedly (c0007, c0008, c0009, c0029)")], A, ["c0007", "c0008", "c0009", "c0029"]),
 ("gold", "ireland/t12", [("T3-160", "calls to join a memorial for the dead (c0158, c0202)"),
                          ("T3-084", "another room's call for help posted here (c0199)")], A, ["c0158", "c0202", "c0199"]),
 ("gold", "mordhau/t05", [("T3-009", "pride in the small mark and that it is still going strong (c0011, c0026)")], A, ["c0011", "c0026"]),
 ("gold", "uofmn/t01", [("T3-048", "the university's own logo prank, announced and reacted to (c0001, c0003, c0005)")], A, ["c0001", "c0003", "c0005"]),
 ("gold", "rainbowgrid/t09", [("T3-037", "the value of an ever-changing canvas argued (c0004)")], A, ["c0004"]),
 ("gold", "rit/t01", [("T3-048", "an organisation's own April Fools joke awaited and its reveal posted (c0001, c0029)")], A, ["c0001", "c0029"]),
 ("gold", "cloud9/t12", [("T3-002", "a last call that it is the room's turn (c0080)")], A, ["c0080"]),
 ("gold", "pakistan/t04", [("T3-016", "what the canvas is for asked and explained (c0013, c0014)")], C, ["c0013", "c0014"]),
 ("gold", "shitredditsays/t09", [("T3-063", "a call for moderators to act on a reply; the concept alone does not show more (c0055)")], A, ["c0055"]),
]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ids = {r["id"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
    themes = {(t["sub"], t["theme_id"]): t for t in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
    lab2id = {(t["sub"], t["second_order"]): t["theme_id"] for t in themes.values()}
    working = collections.defaultdict(set)
    for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
        for m in r["members"]:
            working[(m["sub"], lab2id.get((m["sub"], m["second_order"]), m["second_order"]))].add(r["theme"])
    src = {}
    for name, s in (("b2_hardset_r1.tsv", "r1"), ("b2_goldset.tsv", "gold")):
        for line in open(os.path.join(OUT, "_analysis", name), encoding="utf-8").read().splitlines()[1:]:
            item, source, _, why = line.split("\t")
            src[item] = (s, source, why)
    rows, errs = {"r1": [], "gold": []}, []
    for s, item, places, conf, support in P:
        sub, tid = item.split("/")
        if src.get(item, (None,))[0] != s:
            errs.append("%s is not in the %s draw" % (item, s))
        codes = set(themes[(sub, tid)].get("code_ids") or [])
        for t, _ in places:
            if t not in ids:
                errs.append("%s: %s not in scheme.jsonl" % (item, t))
        for c in support:
            if c not in codes:
                errs.append("%s: support %s is not a concept of the item" % (item, c))
        to = [t for t, _ in places]
        w = sorted(working.get((sub, tid), []))
        rows[s].append({"sub": sub, "theme_id": tid, "item": item, "third_order": to, "multi": len(to) > 1,
                        "why": {t: y for t, y in places}, "confidence": conf, "support": support,
                        "source": src[item][1], "drawn_as": src[item][2], "working_B1": w,
                        "differs_from_working": sorted(set(to) ^ set(w)), "placed_by": "author", "stage": "B2", "leg": "B2a-r1"})
    for s in ("r1", "gold"):
        n = len(rows[s]); d = sum(1 for r in rows[s] if r["differs_from_working"])
        print("%s: %d items (draw %d); clear %d, arguable %d; multi %d; differ from the B1 working grouping %d" % (
            s, n, sum(1 for v in src.values() if v[0] == s), sum(r["confidence"] == C for r in rows[s]),
            sum(r["confidence"] == A for r in rows[s]), sum(r["multi"] for r in rows[s]), d))
    missing = sorted(k for k, v in src.items() if k not in {r["item"] for s in rows for r in rows[s]})
    if missing:
        errs.append("drawn but not placed: %s" % missing)
    for e in errs:
        print("ERROR", e)
    if errs or "--write" not in sys.argv:
        return
    for s, name in (("r1", "author_items.jsonl"), ("gold", "gold_items.jsonl")):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            for r in rows[s]:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote out/author_items.jsonl and out/gold_items.jsonl")


if __name__ == "__main__":
    main()
