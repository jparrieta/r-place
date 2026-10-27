#!/usr/bin/env python3
"""D6a-04: proposals PR-D6-07 to PR-D6-09, from the form lines of D04, Order without law. The rooms are the defining
members whose deciding lines, read whole (d6a04_D04_proposal_read.txt, d6a04_D04_branch_dry.txt and the hows dump), say
what each proposal states (my reading). Prints three JSON lines; append with >>.

    python3 out/_analysis/d6a04_proposals_07_09.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "F": "d5a41"}
BASE = "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525"
LINES = {f: json.load(open(os.path.join(AN, "%s_lines.json" % t), encoding="utf-8"))["lines"] for f, t in TAG.items()}


def codes_for(read, element, ops):
    codes, rooms = [], []
    for f, subs in read.items():
        for s in subs:
            ls = [l for l in LINES[f] if l["sub"] == s and l["element"] == element and l["op"] in ops
                  and l.get("role") == "defining"]
            assert ls, (f, s, element)
            codes.append("%s:%s" % (s, ls[0]["codes"][0]))
            rooms.append(s)
    return codes, rooms


# PR-D6-07: the terms bind the placers they reach (A05)
R07 = {"A": ["placetardis", "rocketbeans", "greenlattice", "placeportalpattern", "bostonbruins", "fireemblem",
             "giantbomb", "RelientK"],
       "B": ["reddevils", "AmericanFlaginPlace", "india", "theitalyplace", "placecanada", "monero", "stlouisblues",
             "minnesotavikings", "placesnek", "straya", "lebanon", "neu"],
       "D": ["bindingofisaac", "radiohead", "calgaryflames", "italy"]}
c07a, r07a = codes_for({"A": R07["A"]}, "A05", ("restrict",))
c07b, r07b = codes_for({"B": R07["B"], "D": R07["D"]}, "A05", ("add-condition",))
SCRIPT07 = ["rocketbeans", "giantbomb", "RelientK", "AmericanFlaginPlace", "india", "theitalyplace", "monero", "italy"]

# PR-D6-08: help from the hands a helper can spare (P16, A13)
R08_A13 = {"C": ["cubers", "eve", "splatoon", "gatech", "calvinandhobbes"],
           "D": ["OnePiece", "mylittlepony", "portugal", "lost", "europe", "homestuck", "southpark"]}
R08_P16 = {"D": ["OneTrueEmilia", "babymetal", "flyers", "furry_irl", "yogscast", "giivasunner"],
           "A": ["ripcity", "utaustin", "mindcrack"]}
c08a, r08a = codes_for(R08_A13, "A13", ("restrict",))
c08b, r08b = codes_for(R08_P16, "P16", ("add-condition",))
ASK08 = {"C": ["PUBATTLEGROUNDS", "bisexual", "NewMexico", "weezer", "thepointing"],
         "D": ["denverbroncos", "frankocean", "denmark", "catholicism", "traaaaaaannnnnnnnnns", "canada", "math"]}

# PR-D6-09: border talk before keeping (A04 in F)
R09 = {"spot": ["dallasstars", "sips", "corridor", "UPenn", "stargate", "wildhockey"],
       "building": ["nbaspurs", "Northwestern", "cmu", "httyd", "KState", "sbu"]}
c09, r09 = codes_for({"F": R09["spot"] + R09["building"]}, "A04", ("restrict",))

out = [
    {
        "id": "PR-D6-07",
        "what": "The terms bind the placers they reach: a settled border is kept by the placers who learn its terms and "
                "accept them, and by the scripts whose targets are changed; placers the terms do not reach keep placing.",
        "change": "A bound on A05 (a settled border is a line members keep): 'This holds for the placers the terms reach, "
                  "told in the thread or the chat, and for the scripts whose targets are changed.' A05's statement, P21, "
                  "A21 and F-020 are not changed by this proposal. It states for A05 the border half of F-026, the "
                  "telling clause at the border.",
        "why": "Three forms change A05. Form A restricts it in 39 of 135 defining rooms (28.9 per cent, against 21.5 per "
               "cent of the 558); form B adds conditions in 16 of 113 (14.2 against 10.2); form D adds conditions in 13 "
               "of 96 (13.5 against 10.2). In 24 of these rooms (A 8, B 12, D 4) the line says restraint followed where "
               "placers learned and accepted the terms; in 8 of the 24 the terms had to reach a script's target. Branch "
               "F26 explains A's cell and branch F08 B's (fractal-D6.jsonl). The other lines say restraint came before "
               "any settlement, by the room's own norm, as F-020 states.",
        "evidence": {"codes": c07a + c07b, "rooms_by_form": R07, "script_target_rooms": SCRIPT07,
                     "fractal_lines": ["A05|A", "A05|B", "A05|D", "A05 by F26 in A", "A05 by F08 in B"],
                     "finding": "F-026"},
        "affected_rooms": sorted(r07a + r07b, key=str.lower),
        "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-04",
    },
    {
        "id": "PR-D6-08",
        "what": "Help comes from the hands a helper can spare: a room gives help when its own work is finished or safe "
                "and it has placements to spare, and holds help back while its own defence is short.",
        "change": "A condition added to P16 (help between rooms): help is given from spare hands, once the helper's own "
                  "work is safe or finished. A bound on A13 (short of hands, a room turns to other rooms): the shortage "
                  "brings the request; whether help comes depends on the other room's spare hands. P16's and A13's "
                  "statements are not changed by this proposal.",
        "why": "Forms C and D restrict A13: 30 of 96 defining rooms in C (31.2 per cent, against 26.0 of the 558) and 33 "
               "of 96 in D (34.4). In 12 of them the line says the help came from the donor's surplus or waited on it "
               "(C 5, D 7). Branch F22 explains D's P16 and A13 cells: in 6 more of its rooms in D help waits on the "
               "helper's secure work and spare pixels; branch F28 states the same at the border in form A (3 more "
               "rooms). In 12 other restrict lines a request under strain is recorded and arriving help is not shown "
               "(my reading); the record cannot show whether it came.",
        "evidence": {"codes": c08a + c08b, "rooms_by_form_A13": R08_A13, "rooms_by_form_P16": R08_P16,
                     "request_without_help_shown": ASK08,
                     "fractal_lines": ["A13|C", "A13|D", "P16|D", "P16 by F22 in D", "A13 by F22 in D",
                                       "P16 by F28 in A"]},
        "affected_rooms": sorted(r08a + r08b, key=str.lower),
        "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-04",
    },
    {
        "id": "PR-D6-09",
        "what": "Border talk before keeping: a room talks with its neighbours when it seeks a spot, and when its building "
                "runs into a neighbour's work, before it has a mark to keep.",
        "change": "Two arrows into P08 (border terms), beside A04 (keeping the mark brings the room to its neighbours): "
                  "from P27 (choosing the spot before any loss), where a room asks a neighbour for permission or access "
                  "before it builds; and from P03 (building), where a neighbour objects to the room's construction or "
                  "expansion over its work. A04's statement is not changed by this proposal; P27 stays a candidate.",
        "why": "Form F, Moving for the spot, restricts A04 in 13 of 34 defining rooms (38.2 per cent, against 22.9 of "
               "the 558). In 6 of the 13 the border talk came while the room sought a spot or permission to build; in "
               "6 it came when building or a script crossed a neighbour's work (my reading of the lines). No branch "
               "explains the cell: F09's rooms hold 4 of the 13 lines, but F09's change is building again after a move; "
               "the reading rests on the form's lines alone.",
        "evidence": {"codes": c09, "rooms_by_route": R09, "fractal_lines": ["A04|F", "P27|F"]},
        "affected_rooms": sorted(r09, key=str.lower),
        "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-04",
    },
]
for o in out:
    print(json.dumps(o, ensure_ascii=False))
