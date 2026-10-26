#!/usr/bin/env python3
"""D4a-08c: deliverables for the D4a-08b weighting cut at 6 (recommended), 4 and 8, the core placed by its codes;
from d4a08c_forms.json; stdout only.

    --what forms | tsv | tier --form X --move-no N | fill TEMPLATE
"""
import argparse, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
T = json.load(open(os.path.join(AN, "d4a08c_forms.json"), encoding="utf-8"))
T5 = json.load(open(os.path.join(AN, "d4a05_tree3.json"), encoding="utf-8"))
PB = T5["primary_branch"]
N8 = {"A": "the design and its marking", "B": "keeping, with traded help and carrying on", "C": "the work behind the thread: the chat and the scripts",
      "D": "the sub's April Fools play", "E": "the terms between neighbours", "F": "the plan made and announced",
      "G": "the spot: lost, chosen or yielded, and building again", "H": "raiding as the work"}
N6 = {
    "A": ("the terms between neighbours, with the plan announced", "E and F", "In part. Negotiated order in 87 per cent of the defining members: the changes limit A04 and A05 (talk with neighbours can come before keeping; sparing holds where an agreement is known and accepted). The plan made and announced is folded in and loses its own account."),
    "B": ("the work behind the thread: the chat, the scripts and raiding", "C and H", "No single account: its three signatures are each held by under half its members (workarounds 43, backstage decision-making 42, attack calls 35 per cent). Scripts (A06 limited) and raiding could each carry one; together they do not. It holds 12 of the 21 raiding-heavy rooms."),
    "C": ("the design and its marking", "A", "In part. Collective representation in 98 per cent: the design is argued and sized, and a template does not settle it (A11, the held proposal)."),
    "D": ("keeping, with traded help and carrying on", "B", "In part. Repair work in 74 per cent: keeping gains conditions the model lacks (coverage, handoffs, sleep)."),
    "E": ("the sub's April Fools play", "D", "Yes, for the frame, which sits beside the canvas work: the sub's play gains steps the model holds only as a key. 26 of the 33 takeover rooms are here."),
    "F": ("the spot: lost, chosen or yielded, and building again", "G", "Yes. Territoriality in 94 per cent: the move follows a loss or a neighbour's advance more than a judgement of too few hands (A10 limited), and the room builds again at the new spot, a return the model lacks."),
}
N4 = {
    "A": ("making the mark: the design, with the work behind the thread and raiding", "A, C and H", "In part, for the design only (collective representation in 73 per cent). The chat, the scripts and raiding are folded in and lose their accounts."),
    "B": ("the terms between neighbours, with the plan announced", "E and F", "In part, as at six forms."),
    "C": ("holding ground: keeping, or moving and building again", "B and G", "In part, and only as a pair. Its signatures are weak (territoriality 44, traded help 34, carrying on 34 per cent). Keeping and moving are the model's two answers to losing ground, and the return from the move to building is the part the model lacks. But the spot no longer has an account of its own."),
    "D": ("the sub's April Fools play", "D", "Yes, for the frame, as at six forms."),
}
ap = argparse.ArgumentParser()
ap.add_argument("--what", required=True)
ap.add_argument("--form")
ap.add_argument("--move-no", type=int)
ap.add_argument("template", nargs="?")
a = ap.parse_args()
C6, C4, C8 = T["cuts"]["6"], T["cuts"]["4"], T["cuts"]["8"]


def members(c, f):
    return sorted((s for s, x in c["rooms"].items() if x == f), key=str.lower)


if a.what == "forms":
    for f in sorted(C6["forms"]):
        v = C6["forms"][f]
        print(json.dumps({"id": f, "level": "form", "k": 6, "weights": {"changes": T["w_changes"], "codes": round(1 - T["w_changes"], 4)},
                          "name": N6[f][0], "of_the_eight_D4a08b": v["of_the_eight"], "a_differing_account": N6[f][2],
                          "n": v["n"], "defining": v["ward_n"], "thin": v["thin"], "core_placed_by_codes": v["core"],
                          "change_signature_T4": v["sig"], "codes_over": v["codes_over"], "median_codes": v["median_codes"],
                          "mixture": v["mixture"], "members": members(C6, f), "since": "D4a-08",
                          "status": "the cut recommended for a short technical appendix; put to J; the leg is open"}, ensure_ascii=False))

if a.what == "tsv":
    print("\t".join(["room", "form_k6", "form_k6_name", "form_k4", "form_k8", "core_room_placed_by_codes", "primary_branch"]))
    core = set(T["core_codes"])
    for s in sorted(C6["rooms"], key=str.lower):
        print("\t".join([s, C6["rooms"][s], N6[C6["rooms"][s]][0], C4["rooms"][s], C8["rooms"][s], "yes" if s in core else "", PB.get(s, "")]))

if a.what == "tier":
    f = a.form
    print(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "D4", "leg": "D4a-08",
                      "tier": "room-form", "id": "D4a08c-" + f, "move": "merging", "event": "room form named", "move_no": a.move_no,
                      "name": N6[f][0], "why": ("one of the 6 forms of the D4a-08b tree (changes two thirds, codes one third) cut at six, "
                                                 "joining the eight forms %s; recommended for a short technical appendix (J, 22:00 Berlin)" % N6[f][1]),
                      "ground": "the rooms' selected changes and coded concepts; no canvas field, verdict or branch",
                      "parent": None, "members_n": C6["forms"][f]["n"]}, ensure_ascii=False))


def table(c, names, k):
    out = ["| form | the pattern | joins the eight | rooms (thin, core) | change signature (times the population; members holding it) | codes most above the average room | median coded concepts | raiding-heavy rooms | takeover rooms | a differing account? |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for f in sorted(c["forms"]):
        v = c["forms"][f]
        sig = "; ".join("%s (%.1f; %.0f%%)" % (d["name"], d["ratio"], 100 * d["presence"]) for d in v["sig"][:3])
        cod = "; ".join("%s (%.3f against %.3f)" % (d["name"], d["share"], d["mean"]) for d in v["codes_over"])
        joins = ", ".join("%s (%s)" % (x, N8[x]) for x in v["of_the_eight"])
        out.append("| %s | %s | %s | %d (%d, %d) | %s | %s | %g | %d | %d | %s |" % (f, names[f][0], joins, v["n"], v["thin"], v["core"], sig, cod,
                                                                          v["median_codes"], v["raiding"], v["takeover"], names[f][2]))
    return "\n".join(out)


def md(name):
    if name == "six":
        return table(C6, N6, 6)
    if name == "four":
        return table(C4, N4, 4)
    if name == "eight":
        out = ["| form | the pattern | rooms (thin, core) |", "|---|---|---|"]
        for f in sorted(C8["forms"]):
            v = C8["forms"][f]
            out.append("| %s | %s | %d (%d, %d) |" % (f, N8[f], v["n"], v["thin"], v["core"]))
        return "\n".join(out)
    if name == "gap":
        out = ["| k | gap (lifetime of the cut) | size ratio, largest to smallest |", "|---|---|---|"]
        for k in ("4", "5", "6", "7", "8"):
            out.append("| %s | %.4f | %.2f |" % (k, T["gap"][k], T["cuts"][k]["ratio"]))
        return "\n".join(out)
    if name == "core":
        out = ["| core room | coded concepts | at eight forms | at six | at four | at six, full distance with a zero change part |", "|---|---|---|---|---|---|"]
        for s, n in sorted(T["core_codes"].items(), key=lambda kv: (-kv[1], kv[0].lower())):
            out.append("| r/%s | %d | %s | %s | %s | %s |" % (s, n, C8["core_by_codes"][s], C6["core_by_codes"][s], C4["core_by_codes"][s], C6["core_by_full_distance"][s]))
        return "\n".join(out)
    if name == "rooms":
        out = ["| room | six forms | four forms | eight forms | primary branch |", "|---|---|---|---|---|"]
        core = set(T["core_codes"])
        for s in sorted(C6["rooms"], key=str.lower):
            out.append("| %s | %s | %s | %s | %s |" % (s + (" (core)" if s in core else ""), C6["rooms"][s], C4["rooms"][s], C8["rooms"][s], PB.get(s, "")))
        return "\n".join(out)
    return ""


if a.what == "fill":
    for line in open(a.template, encoding="utf-8").read().split("\n"):
        m = re.fullmatch(r"\{\{TABLE:([a-z]+)\}\}", line.strip())
        print(md(m.group(1)) if m else line)
