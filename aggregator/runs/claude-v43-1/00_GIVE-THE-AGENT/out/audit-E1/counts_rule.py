#!/usr/bin/env python3
"""E1 section 1, the counts rule (rule 19): counts recomputed from their governing files.

    python3 out/audit-E1/counts_rule.py > out/audit-E1/counts_rule.json

Declared before the run (E1a):
  - the census, stated twice: package/store/rooms.jsonl and the room folders under package/; the analysed set from
    tools/counts.py; out/dropped.jsonl, each drop with its reason;
  - stage D4 section 4's four counts (checks/stage_D4.four_counts, the close-check's own), and whether they sum to the
    analysed set;
  - every ledger's line count now, against the head's "Ledgers (lines)" sentence, read from out/_head.md by pattern;
  - every count phrase in every handback (a number, then within three words a counted noun: rooms, lines, themes,
    concepts, findings, elements, arrows, branches, moves, passes, quotes, items, threads, readers, legs, verdicts,
    adaptations), listed with file and line, for the audit section to check against its governing file by hand.
    The final messages are in the transcripts and are drawn with the diary check.
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
NOUN = r"(rooms?|lines?|themes?|concepts?|findings?|elements?|arrows?|branches|branch|moves?|passes|pass|quotes?|items?|" \
       r"threads?|readers?|legs?|verdicts?|adaptations?|cross-links?|forms?|propositions?|cells?|changes?)"
PHRASE = re.compile(r"(?<![\w.-])(\d[\d,]*(?:\.\d+)?)\s+(?:[\w'-]+\s+){0,3}?%s\b" % NOUN)


def lines(p):
    return sum(1 for l in open(p, encoding="utf-8") if l.strip()) if os.path.exists(p) else None


def main():
    res = {}
    rooms = [json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"), encoding="utf-8") if l.strip()]
    folders = [d for d in os.listdir(os.path.join(ROOT, "package")) if os.path.isfile(os.path.join(ROOT, "package", d, "case.md"))]
    dropped = [json.loads(l) for l in open(os.path.join(OUT, "dropped.jsonl"), encoding="utf-8") if l.strip()]
    cp = subprocess.run([sys.executable, "tools/counts.py", ".", "out/"], cwd=ROOT, capture_output=True, text=True)
    res["census"] = {"rooms_jsonl": len(rooms), "room_folders_with_case": len(folders),
                     "same_set": set(rooms) == set(folders), "dropped": len(dropped),
                     "drop_reasons": [d.get("reason") for d in dropped],
                     "counts_py": [l for l in cp.stdout.splitlines() if l.strip()][:12]}
    try:
        from checks import stage_D4 as s11
        ctx = {"root": ROOT, "package": os.path.join(ROOT, "package")}
        fc = s11.four_counts(OUT, ROOT, ctx, stage="E1")
        if fc is not None:
            analysed, in_branch, unad, rest, unret = fc
            res["D4_four_counts"] = {"in_a_branch": len(in_branch), "unadapted": len(unad), "rest": len(rest),
                                     "unreturned": len(unret), "sum": len(in_branch) + len(unad) + len(rest) + len(unret),
                                     "union": len(in_branch | unad | rest | unret), "analysed": len(analysed)}
    except Exception as e:  # the close-check's function is the authority; a failure is reported, not hidden
        res["D4_four_counts"] = {"error": repr(e)}
    led = {"adjudications": "adjudications.jsonl", "verdicts": "verdicts-D.jsonl", "tier history": "tier_history.jsonl",
           "model history": "model/history.jsonl", "findings": "findings.jsonl", "elements": "model/elements.jsonl",
           "arrows": "model/arrows.jsonl", "branches": "branches.jsonl", "cross-links": "crosslinks.jsonl",
           "departures": "departures.jsonl", "defects": "defects.jsonl", "adaptations": "adaptations.jsonl",
           "propositions": "propositions.jsonl", "proposals (D6)": "proposals-D6.jsonl", "asks": "asks.jsonl"}
    head = open(os.path.join(OUT, "_head.md"), encoding="utf-8").read()
    m = re.search(r"\*\*Ledgers \(lines\):\*\*([^*]+)", head)
    said = {}
    if m:
        for name, num in re.findall(r"([a-z][a-z ]+?) ([\d,]+)", m.group(1)):
            said[name.strip()] = int(num.replace(",", ""))
    res["ledgers"] = {k: {"now": lines(os.path.join(OUT, f)), "head": said.get(k),
                          "agree": None if said.get(k) is None else said.get(k) == lines(os.path.join(OUT, f))}
                      for k, f in led.items()}
    hb = {}
    for p in sorted(glob.glob(os.path.join(OUT, "handback-*.md"))):
        rows = []
        for n, line in enumerate(open(p, encoding="utf-8"), 1):
            for mm in PHRASE.finditer(line):
                rows.append({"line": n, "phrase": mm.group(0)})
        hb[os.path.basename(p)] = {"count_phrases": len(rows), "phrases": rows}
    res["handbacks"] = {k: v["count_phrases"] for k, v in hb.items()}
    res["handback_phrases"] = hb
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main())
