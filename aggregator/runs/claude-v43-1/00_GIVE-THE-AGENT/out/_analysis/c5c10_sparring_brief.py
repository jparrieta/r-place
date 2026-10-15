#!/usr/bin/env python3
"""C5c-10, problem 4: write the brief for one adversarial reader on Stigmergy (J, QC5-002 and 13:45: 'you may ask an
adversarial reader for reasons on both sides'). The brief serves the declarations of D02, T4-006, T4-007 and T4-008 as
the ledgers hold them, the member themes' definitions (scheme_v2.jsonl), the 72 records of the three codings with each
coder's code (c5c2_stigmergy_three.json) and their words through cite.py, the C3 mapping lines, the line ranges of the
source passages, the four options, and the contract's two questions. No note of the analyst's is served. Writes
out/_analysis/c5c10_sparring_brief.md.

    python3 out/_analysis/c5c10_sparring_brief.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return {r.get("id") or r.get("fourth"): r for r in
            (json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip())}


def cite(sub, code):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", sub, "--code", code, "--json"],
                       capture_output=True, text=True, cwd=ROOT)
    try:
        q = json.loads(p.stdout)["quotes"][0]
        return "h%.2f: \"%s\"" % (q["hour"], q["text"].replace("\n", " ").strip())
    except (ValueError, KeyError, IndexError):
        return "(did not resolve)"


fourth, dims, scheme = jl("fourth/fourth.jsonl"), jl("dimensions.jsonl"), jl("scheme_v2.jsonl")
mapping = jl("mapping-C3.jsonl")
three = json.load(open(os.path.join(OUT, "_analysis", "c5c2_stigmergy_three.json"), encoding="utf-8"))
L = ["# Brief for an adversarial reader: Stigmergy in this study", "",
     "You are asked for the strongest reasons for and against each of four options below. Judge each against the "
     "members' records and the sources named, not against a model of your own. You decide nothing: the analyst weighs "
     "your reasons and decides. Write plain prose, under 1,200 words: for each option, the best case for it and the best "
     "case against it, each tied to records (by citation) or to a source passage (by page). Then say which reasons you "
     "find hardest to answer. Do not write any file.", "",
     "## The study in one paragraph", "",
     "In April 2017 Reddit's r/place let any account place one pixel every few minutes on a shared canvas; placement "
     "stopped at hour 73. The study reads the talk of 705 subreddits ('rooms') about the canvas. Coders cut members' "
     "words into concepts, grouped into third-order themes (T3), fourth-order themes (T4, constructs) and dimensions (D). "
     "The record holds the talk in the threads, not the placing.", "",
     "## The contract's two questions", "",
     "- Theory: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to "
     "them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work "
     "alive?",
     "- Method: can independently reconstructed case histories be composed into a shared dynamic account that supports "
     "explanations at successive levels of specificity, while keeping access to the evidence? Construction runs upward: "
     "concepts to third-order themes to fourth-order themes to dimensions. A fourth-order theme should group its members "
     "and answer a question they do not answer alone.",
     "- The study also maps each fourth-order theme to one of four universal problems of organizing (task division, "
     "task allocation, reward provision, information provision).", "",
     "## The dimension and its themes, as the ledgers hold them", ""]
d = dims["D02"]
L += ["### D02 %s" % d["label"], "", "- question: %s" % d["question"], "- predicate: %s" % d["predicate"],
      "- members: %s" % ", ".join("%s %s" % (m, fourth[m]["name"]) for m in d["members"]),
      "- changed: %s" % d["construct"]["changed"], "- mistaken_for: %s" % d["construct"]["mistaken_for"], ""]
for t in ("T4-006", "T4-007", "T4-008"):
    r = fourth[t]
    L += ["### %s %s" % (t, r["name"]), "", "- source: %s" % r.get("source", ""),
          "- members: %s" % ", ".join("%s (%s)" % (m, scheme[m]["name"]) for m in r["members"]),
          "- prose: %s" % r["prose"], "- changed: %s" % r["changed"], "- mistaken_for: %s" % r["mistaken_for"]]
    if t in mapping:
        L.append("- mapped to the universal problem: %s. %s" % (mapping[t]["problem"], mapping[t]["why"]))
    L.append("")
L += ["## Member themes named in the options", ""]
for m in ("T3-038", "T3-041", "T3-060", "T3-008", "T3-034", "T3-049", "T3-070", "T3-091"):
    s = scheme[m]
    L.append("- %s %s: %s" % (m, s["name"], s.get("definition") or ""))
L += ["", "## The three codings of 72 records (drawn at random, 24 per theme, from T3-038, T3-041 and T3-060)", "",
      "Codes, written before the reading: M, the record reports the state of the work (placed, done, missing, where) or "
      "says the member acted on what the canvas showed; MP, a proposal that names the state of the canvas prompting it "
      "(counted with M); P, a proposal or request of what to add with no state of the canvas named; O, other. Each record "
      "takes the code at least two of three coders gave (the analyst, a fleet reader, the field analyst). Rule written "
      "before the tally: a member theme leaves Stigmergy if P is at least half of its records that are not O. Result: "
      "T3-038 P 4 of 14, stays; T3-041 P 8 to 10 of 15, moved to T4-006; T3-060 P 10 of 20, moved to T4-006.", ""]
for t in ("T3-038", "T3-041", "T3-060"):
    L += ["### %s %s" % (t, scheme[t]["name"]), ""]
    for r in three[t]["rows"]:
        sub, code = r["record"].split("/")
        L.append("- [%s] %s | codes: analyst %s, fleet %s, field %s; majority %s" % (
            r["record"], cite(sub, code), r["mine"], r["fleet"], r["field"], r["majority"]))
    L.append("")
L += ["## Sources (read the passages; all files in out/sources-from-J/)", "",
      "- moffett-et-al-2021-ant-colonies-jod.md (Journal of Organization Design 10:55-74): lines 392-414 (pp. 58-59, "
      "stigmergy defined); lines 834-870 (p. 63, Warglien and Sartoris on Grasse and on human stigmergy); lines 891-968 "
      "(p. 64, temporary organizations, Venice); lines 1555-1563 (p. 71, conclusions).",
      "- okhuysen-bechky-2009.md (Academy of Management Annals 3:463-502; printed page = PDF page + 461): lines 383-393 "
      "(p. 469, the definition of coordination); lines 586-651 (pp. 474-475, objects and representations); lines "
      "898-1007 (pp. 481-483, integrating conditions); lines 1138-1247 (pp. 486-488, predictability and common "
      "understanding).",
      "- heylighen-2016.md and grasse-1959.md: the construct's original sources (search for 'trace', 'marker', "
      "'communicate').", "",
      "## The options", "",
      "- (a) Keep Stigmergy (T4-007) with its one member, T3-038, as now, re-argued from organization design.",
      "- (b) Withdraw Stigmergy and place T3-038 in another fourth-order theme of D02.",
      "- (c) Return T3-041 and T3-060 to Stigmergy, reading proposals that extend the mark as grounded in its state, "
      "against the three-coder rule's outcome.",
      "- (d) Merge Stigmergy and Standardization of output (T4-008) into one fourth-order theme named for Okhuysen and "
      "Bechky's coordination mechanism 'objects and representations'.", ""]
open(os.path.join(OUT, "_analysis", "c5c10_sparring_brief.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("c5c10_sparring_brief.md: %d lines, %d bytes" % (len(L), len("\n".join(L).encode("utf-8"))))
