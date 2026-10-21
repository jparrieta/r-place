#!/usr/bin/env python3
"""D3a-57: write out/MODEL-D3.md, the revised model as prose with ids (stage section 5), for the re-check's labelers
and verdict readers. The section prose is written here at D3a-57; every element's statement and range and every
arrow's gloss and mechanism come from model/elements.jsonl and model/arrows.jsonl as they stand now, so the
revised wording (R01, P05, P21, P22, A21) and the candidates' statements are served as the ledgers hold them.
Refuses to write if an element or arrow is placed in no section or in two, if the file exists, or if the text
is over the 6,000-word ceiling declared for the served model at D1.

    python3 out/_analysis/d3_model_prose.py [--write]
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl")) if e.get("status") != "withdrawn"}
ars = {x["id"]: x for x in jl(os.path.join(OUT, "model", "arrows.jsonl")) if x.get("status") != "withdrawn"}
version = vlib.model_hash(OUT)

SECTIONS = [
    ("The start, the calls and building",
     "A room's organizing runs in one order: a member starts a mark, the room calls for hands, members build, "
     "and then they keep the work. Members who join answer the room's call; joining is not part of the "
     "starter's role. Most answers come by placing, or in a bare line, and a member who refuses usually says "
     "why. The room settles what its mark will show by talk. It coordinates many hands by two routes that run "
     "largely apart: members post the state of the work in the thread, or they share a template.",
     ["R01", "P01", "P15", "P20", "P02", "P03", "P04", "P14"], ["A02", "A01", "A12", "A20", "A11"]),
    ("Keeping the work",
     "Once a mark stands on a surface anyone can change, keeping it becomes the work. Keepers repair the work to "
     "the form they know. So a change the room planned is repaired away as damage until the keepers are told of "
     "it. Under strain, members add placements by machine.",
     ["P05"], ["A03", "A06"]),
    ("Other rooms",
     "Keeping the work brings the room up against its neighbours. Rooms talk borders, truces and deals, trade "
     "help, join coalitions, and live as guests or hosts on one another's marks. A member may act for the room "
     "toward another room. No room can make every placer keep an agreement, and members say so. A room spares a "
     "neighbour's work mostly on its own norm.",
     ["P08", "P07", "P16", "P17", "P19", "R02", "P21"], ["A04", "A05", "A13", "A14", "A19", "A21"]),
    ("The contest",
     "A call to place can turn hands against a rival's work. The same room answers the attack call. Some members "
     "refuse it, the room reins in its attackers or apologises, or it points to a truce. Where the attack goes "
     "on, the contest is carried on in talk. Members work out who changed their work and why. A quarrel the "
     "community had before the canvas can come into it.",
     ["P09", "P18", "P06", "K03", "C02"], ["A15", "A16", "A17", "A18"]),
    ("A loss, and a move",
     "After its work is erased or overrun, a room weighs fighting for the spot against moving. A room that "
     "judges its hands too few stops fighting for the spot; it moves, or it gives the work up. No loop is drawn: "
     "no counted arrow runs from the move back to building.",
     ["K02", "P10"], ["A10"]),
    ("The close, and after hour 73",
     "Placement stopped at hour 73 for every room. The room marks the work, records it, and decides what of the "
     "effort to keep. After hour 73 members record and curate, and they contest which version of the canvas and "
     "of the event is kept. No one can place.",
     ["P11", "P12", "P13", "P22"], ["A07", "A08", "A09"]),
    ("Beside the work",
     "These entries run beside the work and carry no arrow: the model claims no effect of them. The claim "
     "stands on a finding.",
     ["K01", "K04", "C01"], []),
]
CAND = [
    ("How rooms coordinate", ["P23", "P33"]),
    ("Whom the work reaches", ["P24", "P25", "P30"]),
    ("Where the room builds", ["P27"]),
    ("What the room makes of itself and its work", ["P26", "P28", "P29", "P31", "P34"]),
    ("The members and the site", ["P32", "K05", "K06", "K07"]),
]
placed = [i for s in SECTIONS for i in s[2] + s[3]] + [i for c in CAND for i in c[1]]
miss = sorted(set(els) | set(ars) - set(placed)) if False else sorted((set(els) | set(ars)) - set(placed))
twice = sorted({i for i in placed if placed.count(i) > 1})
if miss or twice:
    sys.exit("refused: not placed %s; placed twice %s" % (miss, twice))


def el_line(i):
    e = els[i]
    r = (e.get("range") or "").strip()
    ends = r.rstrip("'\"").endswith((".", "!", "?"))
    rng = (" Range: %s%s" % (r if ends else r.rstrip("."), "" if ends else ".")) if r else ""
    st = "" if e.get("status") == "standing" else " *(%s)*" % e.get("status")
    return "- **%s**%s. %s%s" % (i, st, e["statement"].strip(), rng)


def ar_line(i):
    x = ars[i]
    st = x.get("strength") or "bounded"
    head = "- **%s** (%s to %s; %s, %s)." % (i, x["from"], x["to"], x.get("kind"), st)
    gloss = (" Its gloss: %s." % x["gloss"].rstrip(".")) if x.get("gloss") else ""
    mech = " %s" % x["mechanism"].strip() if x.get("mechanism") else ""
    bound = (" Bound: %s" % x["bound"].strip()) if i == "A21" and x.get("bound") else ""
    return head + gloss + mech + bound


L = ["# The global model, as prose with ids (revised at stage D3)", "",
     "Model version: %s (the `VERSION` file). This is the model your room is read against. It was built from "
     "many rooms' talk about a shared canvas on which any account could place one pixel per interval, anyone "
     "could change any pixel, no one held authority over another's placing, and placement stopped for everyone "
     "at hour 73 (hours run from the canvas's opening). Stage D3 revised it from the rooms' own returns. R01, "
     "P05, P21 and P22 were reworded. P21, P22 and A21, tentative before, now stand, A21 with a stated bound. "
     "P06, R02, K03, K04 and P19, candidates before, now stand. Fifteen new candidates entered from acts that "
     "several rooms' records showed." % version,
     "", "## How to read it", "",
     "- **Ids.** P is a process, K a condition, C a claim, R a role, A an arrow between two elements. Every id "
     "here is in `VOCABULARY.json`.",
     "- **Standing and candidate.** An entry with no mark stands in the model. An entry marked *(candidate)* "
     "entered at stage D3 because several rooms' records showed an act that no standing entry states. A "
     "candidate carries no arrow and no order. Answer it from your room's record like any other entry, silence "
     "included: instantiate it, restrict it, or mark it absent with its evidence state.",
     "- **The unit is the room, or a group of rooms.** The room is the actor where its members spoke or acted "
     "for it: in its threads, in the first person plural, in its calls or in plans it adopted. Members are the "
     "actor where they act apart from the room, or where the act is a person's (placing a pixel, running a "
     "script, answering a call).",
     "- **Each element has a range.** The range runs from the smallest form the element takes to the largest. "
     "Read an odd act against the range before you call it something the model lacks.",
     "- **Each arrow reads: when the first element, the second follows, because of its mechanism.** Its strength "
     "is strong, fair or thin. A thin arrow beats its null by a small margin or rests on few rooms.",
     "- **The record holds talk, not the placing.** An answer to a call can be given by placing and leave no "
     "line. Silence about an element is not its absence: mark what your room's record cannot show as unobserved "
     "or not-testable, not as absent.", ""]
for title, intro, ei, ai in SECTIONS:
    L += ["## %s" % title, "", intro, ""]
    L += [el_line(i) for i in ei]
    if ai:
        L += [""] + [ar_line(i) for i in ai]
    L += [""]
L += ["## Candidates entered at stage D3", "",
      "Each candidate below entered because the records of several rooms showed the act and no standing entry "
      "stated it. None carries an arrow. A room may show a candidate, show it absent, or not bear on it.", ""]
for title, ids in CAND:
    L += ["**%s.**" % title, ""] + [el_line(i) for i in ids] + [""]
L += ["## Where the model stops", "",
      "The model does not tell, and a room may need something the model lacks, where:",
      "- a faith in a colour, and not the work, names a room's rivals and rules on its guests: K04 and P19 state "
      "the faith and the host's rule, and the model claims no order from them;",
      "- an act is reached only by a candidate: the candidates carry no arrow, so the model says nothing of what "
      "comes before or after them;",
      "- the room's decisions were taken in a chat the record does not hold: the record shows what came back "
      "(P23), not how the chat decided;",
      "- the coders coded few of a room's replies, so the record holds too little to tell.", "",
      "Where your room's record shows organizing that no entry covers, say so with `propose` or a `[new: …]` "
      "marker; unshared does not mean false.", ""]
text = "\n".join(L)
words = len(text.split())
print("MODEL-D3.md: %d words, %d bytes; %d elements, %d arrows placed; version %s" % (
    words, len(text.encode("utf-8")), len(els), len(ars), version))
if words > 6000:
    sys.exit("refused: over the 6,000-word ceiling")
p0 = os.path.join(OUT, "MODEL-D3.md")
if os.path.exists(p0):
    same = open(p0, encoding="utf-8").read() == text
    print("out/MODEL-D3.md %s the text this script builds" % ("equals" if same else "DIFFERS FROM"))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
p = os.path.join(OUT, "MODEL-D3.md")
if os.path.exists(p):
    sys.exit("refused: %s exists; never overwrite" % p)
open(p, "w", encoding="utf-8").write(text)
print("wrote", p)
