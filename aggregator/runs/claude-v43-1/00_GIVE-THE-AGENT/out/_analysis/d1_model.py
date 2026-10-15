#!/usr/bin/env python3
"""D1a: write out/MODEL-D1.md, the global model as prose with ids for the labelers (stage D1 §1), from account.md's
structure and the frozen ledgers (model/elements.jsonl, model/arrows.jsonl at e15f9647...b3fecd). Statements, ranges and
mechanisms are read from the ledgers, never typed; every arrow reads "when X, Y follows, because Z". No room is named,
no quote is served, no count of rooms is given (the model describes the universe, not the mode), and nothing refers to
a room note, a branch, the analyst's notes or the canvas. Checks the declared ceiling (WORD_CEILING) and refuses to
write over it.

    python3 out/_analysis/d1_model.py            count only
    python3 out/_analysis/d1_model.py --write    write out/MODEL-D1.md
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
WORD_CEILING = 6000


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


E = {e["id"]: e for e in jl("model/elements.jsonl")}
A = {a["id"]: a for a in jl("model/arrows.jsonl")}
census = {json.loads(l)["sub"].lower() for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}

# X: a clause for the element when it opens an arrow; Y: a noun phrase for it when it follows
X = {"R01": "a member starts a mark", "P01": "the room calls for hands",
     "P02": "the room argues what its mark will show", "P03": "the room builds its mark and members post its state",
     "P05": "the room keeps its placed work", "P08": "the room talks borders, truces and deals with a neighbour",
     "P09": "a call turns hands against a rival's work", "P11": "the room marks a work that is up",
     "P12": "the room records what happened to its work", "K02": "the room judges it has too few hands to hold its spot"}
Y = {"P01": "a call for hands", "P03": "building the mark and posting its state",
     "P04": "a posted template that settles the design", "P05": "upkeep of the placed work",
     "P07": "restraint toward the other room's work (sparing, refusal or apology)",
     "P08": "border talk with the neighbours",
     "P09": "a call to attack a rival's work", "P10": "a move to a new spot, a smaller version or a fresh start",
     "P11": "marking the work: announcing, celebrating and crediting it", "P12": "recording what happened to the work",
     "P13": "deciding what of the temporary effort to keep", "P14": "the use of scripts, bots and spare accounts",
     "P15": "a bare answer from a member", "P16": "help traded between rooms", "P17": "joining a coalition",
     "P18": "the contest carried on in talk", "P20": "the host sub's line around canvas talk",
     "P21": "dispute over who may commit the room to an agreement"}
THEORISED = {"A11", "A12"}


def lower1(s):
    return s if (not s or re.match(r"[A-Z]{2,}|[A-Z]\d", s)) else s[0].lower() + s[1:]


def elem(i):
    e = E[i]
    tag = " *(tentative)*" if e.get("status") == "tentative" else ""
    rng = (e.get("range") or "").strip()
    end = "" if rng.endswith((".'", '."', ".")) else "."
    return "- **%s**%s. %s Range: %s%s" % (i, tag, e["statement"].strip(), rng, end)


def arrow(i):
    a = A[i]
    marks = [a.get("strength") or ""]
    if i in THEORISED:
        marks.append("theorised: no order count beats its null")
    if "mechanism is marked theorised" in (a.get("grounding_note") or ""):
        marks.append("its order beats the null; its mechanism is theorised")
    if a.get("status") == "tentative":
        marks = ["tentative"]
    mech = " ".join(a["mechanism"].split()).rstrip(".")
    return "- **%s** (%s to %s; %s). When %s [%s], %s [%s] follows, because %s." % (
        i, a["from"], a["to"], "; ".join(m for m in marks if m), X[a["from"]], a["from"], Y[a["to"]], a["to"],
        lower1(mech))


S = []
S += ["# The global model, as prose with ids", "",
      "Model version: e15f96470271763d9913e79ed8e332c164a1f176106eefacfe8ffac8e1b3fecd (the `VERSION` file). This is the "
      "model your room is read against. It was built from many rooms' talk about a shared canvas on which any account "
      "could place one pixel per interval, anyone could change any pixel, no one held authority over another's placing, "
      "and placement stopped for everyone at hour 73 (hours run from the canvas's opening).", "",
      "## How to read it", "",
      "- **Ids.** P is a process, K a condition, C a claim, R a role, A an arrow between two elements. Every id here is in "
      "`VOCABULARY.json`.",
      "- **The unit is the room, or a group of rooms.** The room is the actor where its members spoke or acted for it: "
      "in its threads, in the first person plural, in its calls or in plans it adopted. Members are the actor where they "
      "act apart from the room, or where the act is a person's (placing a pixel, running a script, answering a call).",
      "- **Each element has a range.** The range runs from the smallest form the element takes to the largest. A room "
      "that does something odd may be running the same structure in its own way; read it against the range before "
      "you call it something the model lacks.",
      "- **Each arrow reads: when X, Y follows, because Z.** Its strength is strong, fair or thin. A thin arrow beats its "
      "null by a small margin or rests on few rooms. A theorised arrow, or a theorised mechanism, is a reading the "
      "record has not shown: a room may show it, show its absence, or not bear on it.",
      "- **The record holds talk, not the placing.** An answer to a call can be given by placing and leave no line. "
      "Silence about an element is not its absence: mark what your room's record cannot show as unobserved or "
      "not-testable, not as absent.", ""]
SECTIONS = [
    ("The start, the calls and building",
     "Rooms run one order: a start, the room's calls for hands, building, and keeping the work. A call proposes what the "
     "room will act on. Members accept it mostly by doing, or in a bare line; a member who refuses usually says why. The "
     "room settles what its mark will show by talk, and coordinates many hands by two routes that run largely apart: "
     "members post the state of the work in the thread, or they share a template that divides the picture into tasks.",
     ["R01", "P01", "P15", "P20", "P02", "P03", "P04", "P14"], ["A02", "A01", "A12", "A20", "A11"]),
    ("Keeping the work",
     "Once a mark stands on a surface anyone can change, keeping it becomes the work. Under strain, members add "
     "placements by machine.",
     ["P05"], ["A03", "A06"]),
    ("Other rooms",
     "Keeping the work brings the room up against its neighbours. Rooms talk borders, truces and deals, trade help and "
     "join coalitions, and no room can make every placer keep an agreement. A room spares a neighbour's work mostly on "
     "its own norm; help between rooms often runs through a deal.",
     ["P08", "P07", "P16", "P17"], ["A04", "A05", "A13", "A14", "A19"]),
    ("The contest",
     "A call to place can turn hands against a rival's work. The same room answers the attack call: some members refuse "
     "it, the room reins in its attackers or apologises, or it points to a truce. Where the attack goes on, the contest "
     "is carried on in talk.",
     ["P09", "P18"], ["A15", "A16", "A17", "A18"]),
    ("A loss, and a move",
     "After its work is erased or overrun, a room weighs fighting for the spot against moving. A room that judges its "
     "hands too few stops fighting for it; it moves, or it gives the work up. A move sends the room's organizing back "
     "to a start; giving up ends the organizing, not the room. No loop is drawn: no counted arrow runs from the move "
     "back to building.",
     ["K02", "P10"], ["A10"]),
    ("The close, and after hour 73",
     "Placement stopped at hour 73 for every room. Before and after it, the room marks the work, records it, and decides "
     "what of the effort to keep. After hour 73 a room can record and curate, and no one can place.",
     ["P11", "P12", "P13"], ["A07", "A08", "A09"]),
    ("Beside the work",
     "The condition below runs beside the work and carries no arrow: the model claims no effect of it. The two claims "
     "stand on findings and carry no arrow.",
     ["K01", "C01", "C02"], []),
    ("Tentative entries",
     "These entries are tentative. Answer them from your room's record like any other element, silence included.",
     ["P21", "P22"], ["A21"]),
]
for title, intro, els, ars in SECTIONS:
    S += ["## %s" % title, "", intro, ""]
    S += [elem(i) for i in els]
    if ars:
        S += [""] + [arrow(i) for i in ars]
    S.append("")
cands = [i for i, e in sorted(E.items()) if e.get("status") == "candidate"]
S += ["## Candidate elements: in the vocabulary, not in the standing model", "",
      "These ids are in `VOCABULARY.json` but stand outside the model: each was cut from it, or never admitted. A room "
      "may instantiate one, or show it absent, like any element; a line on a candidate says what the room shows and "
      "does not change the standing model.", ""]
S += ["- **%s** (candidate). %s" % (i, E[i]["statement"].strip()) for i in cands]
S += ["", "## Where the model stops", "",
      "The model does not tell, and a room may need something the model lacks, where:",
      "- a faith in a colour, and not the work, names a room's rivals and rules on its guests;",
      "- a host rules on the guests who build on its mark;",
      "- a late room enters the canvas through another room: it joins that room's coalition, takes up its offer of space, "
      "or asks it for space before it has a mark of its own;",
      "- a mark brings something back into its room, such as newcomers who find the room through it;",
      "- the coders coded few of a room's replies, so the record holds too little to tell.", "",
      "Where your room's record shows organizing that no element covers, say so with `propose` or a `[new: …]` marker; "
      "unshared does not mean false.", ""]
text = "\n".join(S)
words = len(text.split())
bad = sorted(w for w in set(re.findall(r"\b[a-z0-9_]{4,}\b", text.lower())) if w in census)
print("MODEL-D1.md: %d words (ceiling %d); elements %d, arrows %d, candidates %s; census names found: %s" % (
    words, WORD_CEILING, sum(len(s[2]) for s in SECTIONS), sum(len(s[3]) for s in SECTIONS), cands, bad))
if "--write" in sys.argv:
    if words > WORD_CEILING:
        sys.exit("over the ceiling; not written")
    open(os.path.join(OUT, "MODEL-D1.md"), "w", encoding="utf-8").write(text)
    print("wrote out/MODEL-D1.md")
