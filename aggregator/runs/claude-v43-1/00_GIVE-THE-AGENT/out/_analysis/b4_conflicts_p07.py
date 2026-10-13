#!/usr/bin/env python3
"""B4a-07: the conflicts pass (stage B4 section 4) over adjudication packet 7's theme notes alone
(out/_adjudication-B4/packet-07/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl, as b4_conflicts_p06.py did for packet 6: two or more coders describing the same practice in
incompatible terms, seen across rooms, with the sibling pairs among the readings it may explain. Item keys are checked
against the store, each quoted term against its note, and the residual list is found from the notes' own words.
Appends once per packet; dry run unless --write."""
import importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
PACKET, LEG = 7, "B4a-07"

C = [
    {"id": "CC-063", "practice": "the room's account of its finished work",
     "conflict": "Coders write the room's account of its finished work as one practice: celebrating it, thanking and crediting makers and allies, saving images, mourning losses and telling what survived: 'Celebrating, thanking and saving what they made', 'celebrating and recounting what they made', 'Accounting for what survived when r/place ended'. The scheme splits the acts: the finished work celebrated (T3-009), its makers credited (T3-043), allies thanked (T3-072), screenshots and timelapses kept (T3-105), a lost work mourned (T3-029), what happened to the work told (T3-073), what working together meant (T3-157), one's own placing told (T3-003). T3-009 is both readings' primary in 126 of packet 7's themes and T3-073 in 42; the readings split T3-009|T3-073 in 22 and T3-009|T3-043 in 10, stage B2's predicted pairs 9 and 14.",
     "terms": {"AprilKnights/t12": "Celebrating, thanking and saving what they made",
               "australia/t13": "Celebrating and documenting the build",
               "denmark/t09": "celebrating, thanking, and remembering the work",
               "india/t09": "celebrating and recounting what they made",
               "masseffect/t09": "celebrating, mourning, and remembering the shared work",
               "2007scape/t12": "Accounting for what survived when r/place ended",
               "thebluecorner/t09": "recounting, mourning, and celebrating the finished fight",
               "toolband/t10": "celebrating, thanking and recording what they made",
               "FaroeIslands/t05": "showing what survived and thanking everyone who helped"},
     "pairs": ["T3-009|T3-073", "T3-009|T3-043", "T3-009|T3-072", "T3-009|T3-105", "T3-029|T3-073", "T3-043|T3-073", "T3-073|T3-105"]},
    {"id": "CC-064", "practice": "the canvas's end and the work's end as one practice",
     "conflict": "Coders write the end of the canvas and the end of the room's work as one practice of closing: 'marking Place's ending and keeping its result in view', 'ending, mourning, and preserving the final image', 'ending r/place by stopping, mourning, debating, and retelling'. The scheme splits them: the canvas's end registered (T3-117), the room's work mourned (T3-029), the work celebrated (T3-009), what happened told (T3-073), images kept (T3-105), a later canvas taken up (T3-054), the sub's ordinary talk resumed (T3-017).",
     "terms": {"cirkeltrek/t10": "marking Place's ending and keeping its result in view",
               "unturned/t13": "ending, mourning, and preserving the final image",
               "terraria/t09": "ending r/place by stopping, mourning, debating, and retelling",
               "PlaceNL/t15": "thanking one another and singing the event closed",
               "Rainbow6/t16": "Marking the canvas finished and looking back",
               "bakchodi/t14": "marking the end and thanking the people who did the work",
               "empiredidnothingwrong/t20": "marking the canvas over and mourning what remains",
               "muse/t11": "wrapping up the canvas and going back to normal"},
     "pairs": ["T3-009|T3-117", "T3-029|T3-117", "T3-073|T3-117", "T3-043|T3-117", "T3-105|T3-117", "T3-017|T3-117"]},
    {"id": "CC-065", "practice": "credit for the work and its dispute",
     "conflict": "Coders write giving credit, claiming a share and disputing who made or saved the work as one practice: 'celebrating the Vivec and sorting out who did it', 'arguing over who built or spoiled the result', 'arguing that the people who built the sign decide what it says'. The scheme splits it: makers credited and disputes over who made it (T3-043), allies thanked (T3-072), an alliance's conduct disputed (T3-030), blame laid after the close (T3-058), who speaks for a room (T3-126), members finding a mark they did not know of (T3-082), one's own placing told (T3-003).",
     "terms": {"ElderScrolls/t04": "celebrating the Vivec and sorting out who did it",
               "france/t19": "arguing over who built or spoiled the result",
               "FloydVsVoid/t13": "arguing over what made the prism survive",
               "DCFU/t03": "arguing that the people who built the sign decide what it says",
               "azores/t01": "working out who made it and claiming a part in it",
               "wallstreetbets/t13": "turning the finished figure into collective credit and recruitment",
               "prequelmemes/t10": "carrying the finished work into memories and credit",
               "Russiaclan/t11": "thanking coordinators and settling the story after place ends"},
     "pairs": ["T3-043|T3-072", "T3-030|T3-043", "T3-043|T3-058", "T3-043|T3-126", "T3-043|T3-082", "T3-003|T3-043"]},
    {"id": "CC-066", "practice": "keeping the work after the close",
     "conflict": "Coders write every way of keeping the finished work as one practice of preserving it: 'Turning Storn into a keepsake', 'carrying the finished picture into banners, murals, cloaks, and links', 'making keepsakes and histories'. The scheme splits the carrier: screenshots, timelapses and final images kept as records (T3-105), the work remade in another medium (T3-057), the mark adopted as the sub's banner, flair or emblem (T3-156), the work entered in an atlas or wiki (T3-112), the work carried to a later canvas (T3-054).",
     "terms": {"heroesofthestorm/t08": "Turning Storn into a keepsake",
               "pathofexile/t20": "carrying the finished picture into banners, murals, cloaks, and links",
               "ireland/t14": "cleaning up and carrying the picture home",
               "greenlattice/t21": "making keepsakes and histories",
               "mexico/t16": "keeping the picture and preparing for next time",
               "tf2/t14": "Reusing canvas art as sprays, flairs and icons",
               "AvoArmy/t10": "ending the canvas and keeping the AvoArmy connected",
               "fireemblem/t10": "preserving the mural after placement"},
     "pairs": ["T3-057|T3-105", "T3-105|T3-156", "T3-057|T3-156", "T3-105|T3-112", "T3-054|T3-105"]},
    {"id": "CC-067", "practice": "carrying the canvas or the room on after it closed",
     "conflict": "Coders write carrying the work to another canvas and deciding the canvas room's next life as one practice of continuing: 'ending the war and looking for somewhere to continue', 'carrying pixel play and the community on elsewhere', 'deciding what Goodboye becomes after place'. The scheme splits it: a later canvas answered either way (T3-054), the canvas sub's or chat's future (T3-111), the end marked with a bare hope it returns (T3-117), a new spot on the same canvas after a loss (T3-022), the work remade elsewhere (T3-057).",
     "terms": {"AmericanFlaginPlace/t16": "ending the war and looking for somewhere to continue",
               "argentina/t17": "trying to keep pixel work going after closure and being told basta",
               "greenlattice/t20": "carrying the lattice beyond Place",
               "thebluecorner/t10": "trying to carry the Blue Corner onto new canvases",
               "Goodboye/t11": "deciding what Goodboye becomes after place",
               "PlaceNL/t18": "carrying pixel play and the community on elsewhere",
               "Temple/t08": "keeping the place room and T going after the canvas closed",
               "SquareSpiral/t14": "carrying the spiral on after Place"},
     "pairs": ["T3-054|T3-111", "T3-054|T3-117", "T3-054|T3-057", "T3-111|T3-156", "T3-022|T3-054"]},
    {"id": "CC-068", "practice": "judging an imperfect or lost finish",
     "conflict": "Coders write judging a flawed or failed finish as one practice, whether the judgement is pride, grief, a joke, a victory or blame: 'deciding whether the finish counted as a win', 'reckoning with the imperfect ending', 'making the damaged ending feel properly NIN'. The scheme splits it: a lost work mourned (T3-029), the finished work celebrated (T3-009), what happened told (T3-073), victory over rivals claimed (T3-154), the room's joke played (T3-031), blame after the close (T3-058).",
     "terms": {"kcroyals/t07": "deciding whether the finish counted as a win",
               "uoft/t18": "reckoning with UofT’s final mark",
               "cubers/t31": "reckoning with the imperfect ending",
               "Temple/t09": "mourning and joking about the one wrong final pixel",
               "miamidolphins/t12": "remembering what was imperfect or might have been",
               "kamenrider/t05": "calling Game Over while keeping what remained",
               "nin/t08": "making the damaged ending feel properly NIN",
               "smite/t10": "looking back on an imperfect finish"},
     "pairs": ["T3-009|T3-029", "T3-029|T3-073", "T3-009|T3-031", "T3-009|T3-154", "T3-029|T3-058"]},
    {"id": "CC-069", "practice": "what the canvas meant, argued after it",
     "conflict": "Coders write arguing what the canvas or the room's part in it meant as one practice, whether the argument is about worth, cooperation, identity or ideology: 'arguing why making a mark together matters', 'arguing whether the logo effort was fanboy culture', 'arguing whether the canvas is spectacle, empire, or harmless fun'. The scheme splits it: the canvas's worth argued (T3-037), what working together meant (T3-157), ideology argued from the canvas (T3-179), support felt through the canvas (T3-164), complaints that canvas posts crowd the sub (T3-075).",
     "terms": {"chess/t13": "arguing why making a mark together matters",
               "AMD/t22": "arguing whether the logo effort was fanboy culture",
               "vegan/t11": "arguing about what the pixel work meant",
               "completeanarchy/t10": "arguing whether the canvas is spectacle, empire, or harmless fun",
               "philippines/t09": "arguing what the pixel work means and where it belongs",
               "ockytop/t10": "arguing over taking the pixels too personally",
               "rotmg/t12": "working out what the canvas work meant",
               "babymetal/t14": "remembering the exhausting shared moment and weighing another round"},
     "pairs": ["T3-037|T3-157", "T3-037|T3-179", "T3-157|T3-164", "T3-037|T3-075", "T3-037|T3-085"]},
    {"id": "CC-070", "practice": "completion claimed while the work goes on",
     "conflict": "Coders write calling the work done and showing it as one practice whether placement is still going or has ended: 'calling the picture complete while its status keeps changing', 'celebrating and claiming the work while it is still underway', 'celebrating and keeping the finished wheel alive'. The scheme splits it by time and act: the finished work celebrated (T3-009), the mark announced as up during placement (T3-026), progress reported (T3-038), builders cheered on during the work (T3-104), upkeep (T3-021), a further piece (T3-041).",
     "terms": {"pathofexile/t14": "calling the picture complete while its status keeps changing",
               "teslamotors/t13": "calling the image finished and marking the canvas ending",
               "sonicthehedgehog/t02": "celebrating Sonic and moving on to Tails",
               "NieR/t07": "building and declaring Emil finished",
               "starryknights/t01": "making and showing the masterpiece",
               "witcher/t03": "celebrating and claiming the work while it is still underway",
               "prequelmemes/t04": "showing progress and celebrating what they made",
               "detroitredwings/t10": "celebrating and keeping the finished wheel alive"},
     "pairs": ["T3-009|T3-038", "T3-009|T3-026", "T3-009|T3-104", "T3-009|T3-021", "T3-009|T3-041"]},
    {"id": "CC-071", "practice": "calls and questions that arrive after the close",
     "conflict": "Coders write the answers to late calls, late questions and late fixes as one practice of telling people the canvas is over: 'making sense of a call that came too late', 'correcting late arrivals after placement ended', 'mistaking closure for fixing the Block O'. The scheme splits it: the canvas's end registered (T3-117), the event explained (T3-016), calls to place (T3-002), repair (T3-021), the work celebrated (T3-009).",
     "terms": {"ducks/t04": "making sense of a call that came too late",
               "philippines/t12": "correcting late arrivals after placement ended",
               "stardustcrusaders/t17": "stopping proposals when placement ends",
               "monalisaclan/t15": "explaining that r/place ended and releasing late helpers",
               "oman/t06": "telling a late helper the sub had already finished",
               "osu/t09": "mistaking closure for fixing the Block O",
               "croatia/t15": "Working out whether placement has ended"},
     "pairs": ["T3-016|T3-117", "T3-002|T3-117", "T3-021|T3-117", "T3-009|T3-038"]},
]

RESIDUAL = re.compile(r"belongs with no other|single-code|single code|stands alone|singleton|belongs with nothing|no other practice|no other code|shares no|cannot safely join|lone trace|belongs with neither|belongs with no broader|remains its own|This single|isolated code|isolated title|single surviving title|sole surviving title|single thin code|single ambiguous passage|single visitor report|single visitor request|single passage|is its own practice|Nothing else in the pool|lone later turn|lone question", re.I)


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
    rows.append({"id": "CC-072", "packet": PACKET, "leg": LEG, "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "As CC-008, CC-016, CC-025, CC-036, CC-048 and CC-062: the coder groups a code by exclusion ('belongs with no other practice', 'single-code theme', 'singleton'), often a surviving title whose body was deleted or one reply, so the note gives the scheme nothing to place.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {},
                 "pairs_it_may_explain": ["T3-009|T3-117", "T3-029|T3-073", "T3-052|T3-082"]})
    p = os.path.join(OUT, "coder_conflicts.jsonl")
    if os.path.exists(p) and any(json.loads(x).get("packet") == PACKET for x in open(p, encoding="utf-8") if x.strip()):
        sys.exit("coder_conflicts.jsonl already holds packet %d's conflicts" % PACKET)
    for r in rows:
        print("%s %s: %d items over %d rooms" % (r["id"], r["practice"], len(r["items"]), len(r["subs"])))
    print("residual items: " + ", ".join(sorted(set(resid))))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("coder_conflicts.jsonl now %d lines" % sum(1 for x in open(p, encoding="utf-8") if x.strip()))


if __name__ == "__main__":
    main()
