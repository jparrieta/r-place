#!/usr/bin/env python3
"""B4a-01: the conflicts pass (stage B4 section 4) over adjudication packet 1's theme notes alone
(out/_adjudication-B4/packet-01/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl: two or more coders describing the same practice in incompatible terms, seen across
rooms, with the sibling pairs among the readings it may explain. Item keys are checked against the store and the
residual list is found from the notes' own words. Appends once per packet; dry run unless --write."""
import importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)

C = [
    {"id": "CC-001", "practice": "a one-day flood of posts in one joke format",
     "conflict": "Coders name the same practice as the sub's own takeover, as members' April Fools posting, as an ordinary posting burst that is 'not r/place work', or as a repost series of someone else's parody.",
     "terms": {"bindingofisaac/t11": "the room's own April Fools takeover", "porterrobinson/t08": "the concentrated April Fools flood",
               "nlsscirclejerk/t08": "the room's own April Fools conduct", "harrypotter/t06": "the rooms own April Fools performance",
               "OneTrueEmilia/t01": "the room's own April Fools posting practice", "rit/t02": "the room's own April Fools posting wave",
               "twentyonepilots/t09": "the burst itself, not r/place work", "gameofthrones/t08": "repeatedly submit the same ... parody"},
     "pairs": ["T3-001|T3-023", "T3-017|T3-031", "T3-001|T3-031", "T3-001|T3-048"]},
    {"id": "CC-002", "practice": "an April Fools joke made by someone other than the room's members (a company, university, another sub)",
     "conflict": "Coders write 'the room's own April Fools' to mean 'not canvas conduct', for jokes the room's members made and for jokes a maker or another sub made, so the note's 'own' does not say who staged the joke.",
     "terms": {"uofmn/t01": "the subreddit's own logo prank", "pathofexile/t04": "the room's own April Fools jokes",
               "austria/t12": "the subreddit's own April conduct", "iastate/t01": "the room's own April Fools conduct",
               "Braveryjerk/t01": "the room's own April Fools conduct", "paydaytheheist/t01": "the room's own April Fools activity",
               "dota2/t01": "Valve's question-mark deny", "rit/t01": "the separate 1RIT joke"},
     "pairs": ["T3-001|T3-048", "T3-023|T3-048", "T3-048|T3-095"]},
    {"id": "CC-003", "practice": "members checking whether a claim is an April Fools joke",
     "conflict": "Some coders fold the testing into the room's own joke-making ('make, test, explain'), others make the testing the theme's whole practice whatever the claim's source.",
     "terms": {"kpop/t02": "put the claim on trial", "kurdistan/t06": "tests whether it is the room's prank",
               "de/t08": "testing and evaluating dated deception", "loltyler1/t01": "make, question, explain, or puncture",
               "hearthstone/t01": "testing April Fools claims before believing them", "romania/t12": "expose or test bait",
               "paladins/t05": "working out whether apparently serious posts ... are April Fools jokes"},
     "pairs": ["T3-001|T3-095", "T3-048|T3-095"]},
    {"id": "CC-004", "practice": "moderators applying the sub's rules to posts on the joke day",
     "conflict": "The same removals and rule calls are written as part of the April Fools performance, as ordinary moderation kept in force, or as rule-making about humour.",
     "terms": {"leagueoflegends/t10": "Enforcing the joke and the room's posting rules", "nintendo/t03": "maintaining ordinary content arrangements during the joke day",
               "metalcore/t07": "applies the room's ordinary genre boundary to an April Fools submission", "twice/t04": "the moderator's ordinary act of removing a purported update",
               "flashtv/t10": "policing and correcting the boundary for local humour", "ss13/t11": "moderator actions inside the room's April Fools conduct",
               "anime_irl/t05": "permits the single event post"},
     "pairs": ["T3-023|T3-063", "T3-063|T3-185", "T3-017|T3-063", "T3-032|T3-063"]},
    {"id": "CC-005", "practice": "containing canvas talk inside the sub",
     "conflict": "Complaint, routing to one thread and removal are bundled in one theme per room, and coders lead with different terms ('funnelling', 'containing', 'policing', 'arguing over'), so the note does not say which act leads.",
     "terms": {"france/t08": "funnelling r/place talk into the megathread", "denmark/t07": "moving r/place posts into megathreads",
               "mexico/t12": "containing r/place talk and keeping the subreddit readable", "canada/t09": "Concentrating and contesting r/place talk",
               "unitedkingdom/t07": "Policing where r/place talk belongs", "stlouisblues/t13": "arguing over how much r/place should stay",
               "trees/t13": "apply ordinary posting rules", "nin/t05": "arguing whether place belongs in r/nin or one sticky"},
     "pairs": ["T3-015|T3-063", "T3-015|T3-075", "T3-063|T3-075"]},
    {"id": "CC-006", "practice": "help given between neighbouring works with something given back",
     "conflict": "Coders call reciprocal help 'helping neighbours' or 'reciprocal pixel work' in one room and 'asking allies for help and offering help back' in another; the note does not say whether the help was traded.",
     "terms": {"skyrim/t06": "helping neighbors and trading protection", "teslamotors/t11": "reciprocal pixel work",
               "russia/t08": "asking allies for help and offering help back"},
     "pairs": ["T3-011|T3-151", "T3-084|T3-151"]},
    {"id": "CC-007", "practice": "a joke promised if a post reaches an upvote threshold",
     "conflict": "The same upvote-indexed promise is written as a deal, an accountability exchange, a proposal or voting as enforcement.",
     "terms": {"partyparrot/t16": "the bounded deal that authorises the local turn", "titanfall/t05": "proposes changing the subreddit theme if it reaches a vote target",
               "warframe/t06": "voting is the means of enforcement", "warriors/t04": "setting an upvote condition",
               "clashroyale/t04": "an upvote-indexed burning promise", "4chan/t12": "trade each upvote for a day without shitposting"},
     "pairs": ["T3-023|T3-051", "T3-001|T3-051"]},
]
RESIDUAL = re.compile(r"belongs with no other|single-code theme|single code|stands alone|singleton|belongs with nothing else|no other practice", re.I)


def main():
    store = bpf.pk.Store(ROOT, OUT)
    notes = open(os.path.join(OUT, "_adjudication-B4", "packet-01", "notes.md"), encoding="utf-8").read().splitlines()
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
        rows.append({"id": c["id"], "packet": 1, "leg": "B4a-01", "pass": "theme_note alone", "practice": c["practice"],
                     "conflict": c["conflict"], "items": sorted(c["terms"]), "subs": sorted({k.split("/")[0] for k in c["terms"]}),
                     "terms": c["terms"], "pairs_it_may_explain": c["pairs"]})
    rows.append({"id": "CC-008", "packet": 1, "leg": "B4a-01", "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "The coder groups a code by exclusion ('belongs with no other practice', 'single-code theme'), so the note gives the scheme nothing to place; the readings of these items split most often between T3-017 and a neighbour.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {}, "pairs_it_may_explain": ["T3-017|T3-031", "T3-016|T3-017"]})
    p = os.path.join(OUT, "coder_conflicts.jsonl")
    if os.path.exists(p) and any(json.loads(x).get("packet") == 1 for x in open(p, encoding="utf-8") if x.strip()):
        sys.exit("coder_conflicts.jsonl already holds packet 1's conflicts")
    for r in rows:
        print("%s %s: %d items over %d rooms" % (r["id"], r["practice"], len(r["items"]), len(r["subs"])))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
