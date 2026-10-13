#!/usr/bin/env python3
"""B4a-02: the conflicts pass (stage B4 section 4) over adjudication packet 2's theme notes alone
(out/_adjudication-B4/packet-02/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl, as b4_conflicts_p01.py did for packet 1: two or more coders describing the same practice in
incompatible terms, seen across rooms, with the sibling pairs among the readings it may explain. Item keys are checked
against the store and the residual list is found from the notes' own words. Appends once per packet; dry run unless
--write."""
import importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
PACKET, LEG = 2, "B4a-02"

C = [
    {"id": "CC-009", "practice": "coordination moved to a chat together with scripts, bots, templates or border deals",
     "conflict": "Coders name the venue as the practice and list scripts, bots, templates and border deals inside it, so the note does not say whether the theme moves the talk, runs the placing by script, hands out the template or settles a border.",
     "terms": {"2007scape/t09": "Moving coordination through Discord, scripts, templates, and mirrors",
               "denmark/t06": "coordinating through Discord, bots, and shared tools",
               "uwaterloo/t09": "moving plans through Discord, scripts, and bots",
               "TheFarLeftSide/t08": "moving coordination into Discord and scripts",
               "onepunchman/t07": "placing pixels through timers, teams, Discord, and tools",
               "leagueoflegends/t17": "Moving pixel work into Discord, scripts, and border deals",
               "tf2/t06": "Moving coordination through Discord, templates and scripts",
               "rocketleague/t04": "carrying the canvas plan through Discord and templates"},
     "pairs": ["T3-014|T3-028", "T3-014|T3-070", "T3-010|T3-014"]},
    {"id": "CC-010", "practice": "canvas talk sent to another named subreddit or chat",
     "conflict": "The same move to another named venue is written as containing the flood, as moving the planning, or as reaching another community for help, and one coder files a redirect to shared threads inside the sub under the new-venue heading.",
     "terms": {"osugame/t04": "Moving Place talk out of the main room",
               "buffalo/t07": "keep r/place talk from clogging the room",
               "fivenightsatfreddys/t11": "trying to contain r/place talk in the subreddit",
               "italy/t05": "funnelling repeated and misplaced posts into shared threads",
               "crusaderkings/t05": "moving coordination to r/CKCrusaders and Discord",
               "norway/t06": "sending canvas business to r/norge and Discord",
               "linux/t09": "sending coordination to r/linuxmasterrace and Discord",
               "NewMexico/t06": "reaching outside the thread for help and talk"},
     "pairs": ["T3-015|T3-090", "T3-014|T3-090", "T3-062|T3-090", "T3-075|T3-090"]},
    {"id": "CC-011", "practice": "showing newcomers where the work is and how a pixel is placed",
     "conflict": "Answering newcomers with the coordinates, the timer and how to place is named recruitment in some rooms, instruction in others, and explaining the event in a third.",
     "terms": {"pcmasterrace/t05": "recruiting and teaching people to place pixels",
               "philippines/t03": "bringing people into the pixel work",
               "yugioh/t15": "recruiting and teaching scarce pixel helpers",
               "penguins/t05": "showing newcomers where and how to place pixels",
               "oman/t04": "showing people where and how to draw",
               "bisexual/t02": "showing people where Place and the flags are",
               "clashroyale/t09": "showing newcomers where and how to place pixels"},
     "pairs": ["T3-002|T3-070", "T3-016|T3-070", "T3-002|T3-016"]},
    {"id": "CC-012", "practice": "getting placers onto one plan",
     "conflict": "The same phrase, getting everyone onto one plan, names publishing a template, holding placers to it against rival versions, concentrating hands on one piece, and asking the moderators for an official project.",
     "terms": {"uofm/t03": "getting everyone onto the current template",
               "heyyea/t01": "keeping everyone on the current template",
               "Temple/t04": "getting everyone onto one plan, template, or script",
               "greenbaypackers/t08": "getting everyone onto one G",
               "weezer/t03": "trying to get scattered workers on the same page",
               "msu/t06": "getting everyone onto one building and defence plan",
               "PlaceNL/t01": "publishing and updating the current plan",
               "suomi/t17": "asking moderators to make one project official"},
     "pairs": ["T3-070|T3-091", "T3-049|T3-091", "T3-069|T3-091", "T3-002|T3-091"]},
    {"id": "CC-013", "practice": "fitting the work to the hands available",
     "conflict": "Coders write the same scaling-down of a design to the few hands present as working around the limit in some rooms and as doubting the room's strength in others.",
     "terms": {"sadboys/t03": "scaling plans down to what a handful can make",
               "Peru/t03": "making a few builders count",
               "sabres/t04": "scaling plans to the people and effort available",
               "samuraijack/t15": "cutting canvas plans down to what the room can make",
               "vinesauce/t08": "working out what this small group can manage",
               "toolband/t07": "fitting one plan to the people and space available"},
     "pairs": ["T3-074|T3-136", "T3-042|T3-136", "T3-069|T3-136"]},
    {"id": "CC-014", "practice": "people drawn to the room by its canvas mark",
     "conflict": "First arrivals and returning fans are joined in one note ('coming back or joining'), so the note does not say whether the visitor is new or lapsed, and a third coder files the arrival as ordinary fandom talk.",
     "terms": {"nerf/t07": "coming back or joining because r/place brought them",
               "evedreddit/t06": "turning the r/place ad into a return to Dreddit",
               "fireemblem/t11": "welcoming people through the pixel art",
               "pathofexile/t16": "treating the canvas picture as bringing a player back",
               "parahumans/t11": "folding canvas newcomers into ordinary fandom participation",
               "bakchodi/t17": "using r/place publicity to grow bakchodi"},
     "pairs": ["T3-044|T3-196", "T3-017|T3-044"]},
    {"id": "CC-015", "practice": "bringing the chat's decisions back to the thread",
     "conflict": "Most coders fold the relay of chat decisions into moving the planning ('moving ... and bringing back'); two make the relay the theme's whole practice.",
     "terms": {"chelseafc/t11": "moving crest decisions into private chat and bringing instructions back",
               "DestinyTheGame/t10": "moving live plans to Discord and bringing directions back",
               "madokamagica/t03": "taking planning to Discord and returning decisions",
               "metalgearsolid/t08": "moving plans through Discord and bringing directions back",
               "notredame/t07": "moving coordination into Discord and bringing plans back",
               "cubers/t05": "bringing Discord work back to Reddit",
               "popheads/t01": "bringing joke material back from Discord"},
     "pairs": ["T3-014|T3-152"]},
]
RESIDUAL = re.compile(r"belongs with no other|single-code theme|single code|stands alone|singleton|belongs with nothing else|no other practice|no other code", re.I)


def main():
    store = bpf.pk.Store(ROOT, OUT)
    notes = open(os.path.join(OUT, "_adjudication-B4", "packet-%02d" % PACKET, "notes.md"), encoding="utf-8").read().splitlines()
    resid = []
    for ln in notes:
        m = re.match(r"- ([^/\s]+)/(t\d+) \((.*?)\): (.*)$", ln)
        if m and RESIDUAL.search(m.group(4)):
            resid.append("%s/%s" % (m.group(1), m.group(2)))
    rows = []
    for c in C:
        bad = [k for k in c["terms"] if tuple(k.split("/")) not in store.themes]
        if bad:
            sys.exit("%s: not in the store: %s" % (c["id"], bad))
        miss = [k for k, v in c["terms"].items() if not any(ln.startswith("- %s (" % k) and v in ln for ln in notes)]
        if miss:
            sys.exit("%s: term not found in its note: %s" % (c["id"], miss))
        rows.append({"id": c["id"], "packet": PACKET, "leg": LEG, "pass": "theme_note alone", "practice": c["practice"],
                     "conflict": c["conflict"], "items": sorted(c["terms"]), "subs": sorted({k.split("/")[0] for k in c["terms"]}),
                     "terms": c["terms"], "pairs_it_may_explain": c["pairs"]})
    rows.append({"id": "CC-016", "packet": PACKET, "leg": LEG, "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "As CC-008 for packet 1: the coder groups a code by exclusion ('belongs with no other practice', 'single-code theme'), so the note gives the scheme nothing to place.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {},
                 "pairs_it_may_explain": ["T3-002|T3-017", "T3-017|T3-074", "T3-034|T3-098"]})
    p = os.path.join(OUT, "coder_conflicts.jsonl")
    if os.path.exists(p) and any(json.loads(x).get("packet") == PACKET for x in open(p, encoding="utf-8") if x.strip()):
        sys.exit("coder_conflicts.jsonl already holds packet %d's conflicts" % PACKET)
    for r in rows:
        print("%s %s: %d items over %d rooms" % (r["id"], r["practice"], len(r["items"]), len(r["subs"])))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("coder_conflicts.jsonl now %d lines" % sum(1 for x in open(p, encoding="utf-8") if x.strip()))


if __name__ == "__main__":
    main()
