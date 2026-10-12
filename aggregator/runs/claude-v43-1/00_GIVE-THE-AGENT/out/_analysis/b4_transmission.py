#!/usr/bin/env python3
"""B4a-01: transmission-B4.md, section 3's four rows over the 90 items with my answer on record, from
out/_analysis/b4_prepare.json (computed before any ruling). Row 4 carries my reading of each item, made at B4a-01
through mem.py theme against the frozen scheme (JUDGE below). Writes out/transmission-B4.md (refuses to overwrite)."""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ROWS = {1: "the scheme decides", 2: "fails to transmit", 3: "the instrument does not decide this item",
        4: "teaches something unintended"}
# row 4, read one by one: "wrong" = I was wrong; "unintended" = the scheme taught something I did not intend
JUDGE = {
    "AyyMD/t08": ("wrong", "My 'clear' T3-001 missed that the moderators staged the switch (a moderator's resignation, the Novideo CSS, the sub's own joke): four concepts carry T3-023, four T3-001; the readers' T3-023 follows the label."),
    "Slovakia/t07": ("wrong", "The Slovak hearts are added into r/placehearts' shared work, T3-060's 'own part to a shared mark'; T3-079 asks for hearts between national flags, which these are not."),
    "cloud9/t12": ("wrong", "One ambiguous call against one report that the canvas had ended; the label is the closing exchange, and the readers' T3-117 reads it."),
    "dofus/t01": ("wrong", "Counting the acts gives a tie between proposal and placing, and the frozen tie rule sends it to T3-038 'when the work was placed'; my answer predates that rule."),
    "harrypotter/t08": ("wrong", "Four concepts award house points for canvas work (T3-159's mock prizes); T3-017's own rule adds usual talk beside a canvas theme, it does not lead. The readers kept the primary I missed; they also dropped T3-017's four concepts."),
    "DevonUK/t04": ("wrong", "The help offered in return is the term of the border bargain (two concepts); T3-010 carries the deal and my T3-151 adds nothing the deal does not hold."),
    "cubers/t27": ("wrong", "The 'Grey Border Alliance' is a coalition about borders, not for defence or a fight; T3-150 asks for the latter."),
    "floridagators/t04": ("wrong", "Both deletions point to the gathering thread, which T3-015's own rule keeps in T3-015; T3-063 has no concept of its own here."),
    "natsume/t01": ("wrong", "The announcement and coordinates are not members finding their own mark; only the newcomers' two concepts carry a theme, T3-044."),
    "overwatch/t23": ("wrong", "One concept asks for a filter; T3-075 rests on it alone and T3-015 carries the item."),
    "uiuc/t04": ("wrong", "The claims tested are the room's members' own fakes, which T3-095's rule keeps in T3-001 'even when readers test it'."),
    "alberta/t04": ("unintended", "Three concepts rein the attack in, and T3-076's decide_when_both says 'rule 0 pairs them both ways'; both readers placed the attack alone. The pairing sentence did not transmit."),
    "finland/t06": ("unintended", "Two moderator removals carry no pointer to the thread, T3-063 by T3-015's own rule, which says 'the other under rule 0'; both readers dropped it."),
    "korea/t15": ("unintended", "Two complaints about the flood against two concepts gathering the talk; T3-075's rule puts 'the other under rule 0', and both readers kept only T3-015."),
    "mit/t01": ("unintended", "Three concepts set and correct the corner coordinates, and T3-004's rule adds the spot 'under rule 0'; both readers kept only the design."),
    "Goodboye/t03": ("unintended", "One concept trades help and one asks outright; the rest are offers. Both readers took T3-151 from the label's 'trading pixels' and the note's 'in return'."),
    "ireland/t12": ("unintended", "Calls to 'join the cause' of a memorial read as T3-002's calls to placers; T3-160 does not say whether a call to join a memorial is the memorial. B2 carried this item to C1."),
    "nVade/t04": ("unintended", "A pledge to protect another room's figure is T3-011 by the T3-005 discriminator ('a pledge to protect it included'); both readers placed defence alone. The clause sits only in a discriminator."),
    "parabola/t02": ("unintended", "A border offered 'to help protect each other' and an alliance agreed read as T3-010; the word 'border' pulls a protection pact to the border theme."),
    "uofmn/t01": ("unintended", "A member posts the university's official logo joke; both readers read the poster as staging it (T3-001). T3-001 does not say that relaying an official joke is T3-048. B2 carried this item to C1."),
}


def main():
    P = json.load(open(os.path.join(OUT, "_analysis", "b4_prepare.json"), encoding="utf-8"))
    rows = P["transmission"]
    miss = [r["item"] for r in rows if r["row"] == 4 and r["item"] not in JUDGE]
    if miss:
        sys.exit("row-4 items not read: %s" % miss)
    p = os.path.join(OUT, "transmission-B4.md")
    if os.path.exists(p) and "--write" in sys.argv:
        sys.exit("transmission-B4.md exists")
    L = ["# Transmission, decomposed (stage B4, section 3)", "",
         "Computed at B4a-01, before any ruling touched `assign_final.jsonl` (`out/_analysis/b4_prepare.py`, `b4_transmission.py`).", "",
         "**Over which items.** The rows exist only where my own answer is on record: the 40 gold items (`gold_items.jsonl`) "
         "and the 50 items stage B2 piloted (`author_items.jsonl`). My answer is the latest recheck in `rechecks-B2.jsonl`, "
         "which all 90 carry; my confidence is the file's. The readers are stage B3's two corpus replicates of each item; "
         "they agree when their sets are equal. For the gold items, the seeded copies' commonest set and its share are "
         "given beside, as a second view; the seeded placements enter no rate. Outside the gold and pilot items my answer "
         "does not exist, so the split rate there cannot be decomposed, and nothing here is extrapolated from the gold "
         "set, which was drawn to be hard.", "",
         "The next table counts the items in each row, gold and pilot apart."]
    L += ["", "| row | readers | me | what it is | gold | pilot |", "|---|---|---|---|---|---|"]
    cnt = {s: collections.Counter(r["row"] for r in rows if r["src"] == s) for s in ("gold_items.jsonl", "author_items.jsonl")}
    spec = {1: ("agree with each other and with me", ""), 2: ("split", "was confident"), 3: ("split", "was also unsure"),
            4: ("agree with each other, diverge from me", "")}
    for k in (1, 2, 3, 4):
        L.append("| %d | %s | %s | %s | %d | %d |" % (k, spec[k][0], spec[k][1], ROWS[k], cnt["gold_items.jsonl"][k], cnt["author_items.jsonl"][k]))
    L += ["", "My answer was 'clear' on 9 of the 90 items (4 gold, 5 pilot) and 'arguable' on 81, so a split mostly lands "
          "in row 3, kept as a finding, and row 2 holds one item.", ""]
    for k in (2, 3, 4, 1):
        its = [r for r in rows if r["row"] == k]
        L += ["## Row %d: %s (%d items)" % (k, ROWS[k], len(its)), ""]
        if k == 2:
            L.append("The readers split where I was confident: a wording defect, the sentence stage C1 must repair.")
        elif k == 3:
            L.append("The readers split and I was unsure too: the instrument does not decide these items. Kept as a finding, never revised away.")
        elif k == 4:
            L.append("Both readers agreed with each other and not with me. Each is read and split both ways: I was wrong, or the scheme taught something I did not intend.")
        else:
            L.append("The scheme decides: both readers placed the set I placed.")
        L += ["", "| family | item | mine | reader 1 | reader 2 | seeded copies' commonest set |" + (" which way, and why |" if k == 4 else ""),
              "|---|---|---|---|---|---|" + ("---|" if k == 4 else "")]
        for r in sorted(its, key=lambda r: (r["family"] or "", r["item"].lower())):
            sm = ("%s (%.0f%% of %d)" % (",".join(r["seeded_mode"]), 100 * r["seeded_mode_share"], r["seeded_n"])) if r["seeded_mode"] else "-"
            line = "| %s | %s | %s | %s | %s | %s |" % (r["family"], r["item"], ",".join(r["mine"]), ",".join(r["r1"]), ",".join(r["r2"]), sm)
            if k == 4:
                w, why = JUDGE[r["item"]]
                line += " %s: %s |" % ("I was wrong" if w == "wrong" else "the scheme taught something unintended", why)
            L.append(line)
        L.append("")
    fam4 = collections.Counter(r["family"] for r in rows if r["row"] in (2, 3, 4))
    L += ["## By family", "", "The next table gives each family's items in rows 2, 3 and 4 (the family of my primary).", "",
          "| family | row 2 | row 3 | row 4, I was wrong | row 4, unintended |", "|---|---|---|---|---|"]
    for f in sorted({r["family"] for r in rows if r["row"] in (2, 3, 4)}):
        fr = [r for r in rows if r["family"] == f]
        L.append("| %s | %d | %d | %d | %d |" % (f, sum(r["row"] == 2 for r in fr), sum(r["row"] == 3 for r in fr),
                 sum(r["row"] == 4 and JUDGE[r["item"]][0] == "wrong" for r in fr),
                 sum(r["row"] == 4 and JUDGE[r["item"]][0] == "unintended" for r in fr)))
    wrong = [i for i, v in JUDGE.items() if v[0] == "wrong"]
    unint = [i for i, v in JUDGE.items() if v[0] == "unintended"]
    c2 = [r["item"] for r in rows if r["row"] == 4 and r["class"] == 2]
    c2w = [i for i in c2 if JUDGE[i][0] == "wrong"]
    L += ["", "## What row 4 says", "",
          "**Which way each went.** %d of the 20 went against me: I was wrong (%s). %d went against the scheme: it taught "
          "something I did not intend (%s)." % (len(wrong), ", ".join(sorted(wrong, key=str.lower)), len(unint), ", ".join(sorted(unint, key=str.lower))), "",
          "**Rule 0's added theme did not transmit.** On alberta t04, finland t06, korea t15 and mit t01 the primary's own "
          "`decide_when_both` tells the reader to add the second theme 'under rule 0', and both readers placed one theme. "
          "Readers apply rule 0's single placement more strictly than the scheme's pairing sentences ask. This is the same "
          "lean stage B2 found, and stage C1 should read these four sentences first.", "",
          "**Rule 2 keeps themes both readers left out.** %d of the 20 row-4 items are class 2, so `assign_final.jsonl` keeps "
          "my B1 grouping on them, the readers' list first, then B1's other themes (J, 12 October). On %d of those (%s) I "
          "judge the kept theme wrong on reading. The class-2 lines stand as J ruled; this is reported, not overruled, and "
          "no agreed item outside these 90 was re-read in search of more." % (len(c2), len(c2w), ", ".join(sorted(c2w, key=str.lower))), "",
          "**What this licenses.** The readers share an architecture with me and with each other, so these rows bound "
          "whether the instrument decides, not whether it is right. A row 1 item says the written scheme reached two "
          "readers the way I meant it; it does not say the placement is true of the room.", ""]
    txt = "\n".join(L)
    print(txt[:1500])
    print("... %d lines" % txt.count("\n"))
    if "--write" in sys.argv:
        open(p, "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    main()
