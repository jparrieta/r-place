#!/usr/bin/env python3
"""E1 section 1, the counts rule (E1b-02): the 361 count phrases counts_rule.py listed in the handbacks, sorted, and a
seeded sample of them set out for checking by hand against their governing files; and the head's ledger figures
against the ledgers as the head stands now. Prints JSON.

    python3 out/audit-E1/counts_phrases.py > out/audit-E1/counts_phrases.json

The rule, declared before the run (E1b-02):
- A phrase is not a count where its number is followed by a comma (an id, a move number, a date or an item in a list,
  such as "48, moves"), where the number has a decimal point (a share or a mean), or where it is 10,000,000 or more
  (a seed or a date).
- Of the rest, two per handback are drawn with random.Random(int(out/seed.txt, 16)), handbacks in name order, each
  with its whole line, to be checked by hand against the file that governs the count, as it stood at that stage where
  the file's lines carry a stage. 18 handbacks give 36. Checking all 361 by hand is beyond one leg; the sample and the
  phrases left unchecked are both reported.
- The head's "Ledgers (lines)" sentence, read from out/_head.md as it stands, against each ledger's non-empty lines.
"""
import json, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
LEDGERS = {"adjudications": "adjudications.jsonl", "verdicts": "verdicts-D.jsonl", "tier history": "tier_history.jsonl",
           "model history": "model/history.jsonl", "findings": "findings.jsonl", "elements": "model/elements.jsonl",
           "arrows": "model/arrows.jsonl"}


def kind(phrase):
    m = re.match(r"^(\d+(?:,\d{3})*(?:\.\d+)?)(,?)", phrase)  # thousands commas only; the first run took any comma
    num, comma = m.group(1), m.group(2)
    if comma:
        return "not a count: number then comma"
    if "." in num:
        return "not a count: decimal"
    if int(num.replace(",", "")) >= 10_000_000:
        return "not a count: seed or date"
    return "count"


def main():
    cr = json.load(open(os.path.join(OUT, "audit-E1", "counts_rule.json"), encoding="utf-8"))
    rows = []
    for f in sorted(cr["handback_phrases"]):
        text = open(os.path.join(OUT, f), encoding="utf-8").read().split("\n")
        for p in cr["handback_phrases"][f]["phrases"]:
            rows.append({"handback": f, "line": p["line"], "phrase": p["phrase"], "kind": kind(p["phrase"]),
                         "_text": text[p["line"] - 1] if p["line"] - 1 < len(text) else ""})
    seed = open(os.path.join(OUT, "seed.txt")).read().split()[0]
    rnd = random.Random(int(seed, 16))
    sample = []
    for f in sorted(cr["handback_phrases"]):
        pool = [r for r in rows if r["handback"] == f and r["kind"] == "count"]
        sample += rnd.sample(pool, min(2, len(pool)))
    for r in sample:
        t = r["_text"]
        i = t.find(r["phrase"])
        r["context"] = t[max(0, i - 260):i + len(r["phrase"]) + 200]
    head = open(os.path.join(OUT, "_head.md"), encoding="utf-8").read()
    led = {}
    for name, path in LEDGERS.items():
        m = re.search(re.escape(name) + r" ([\d,]+)", head)
        now = sum(1 for l in open(os.path.join(OUT, path), encoding="utf-8") if l.strip())
        led[name] = {"head": int(m.group(1).replace(",", "")) if m else None, "now": now,
                     "agree": bool(m) and int(m.group(1).replace(",", "")) == now}
    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    for r in rows:
        r.pop("_text", None)
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-02):")[1].strip(),
                      "phrases": len(rows), "by_kind": kinds, "seed": seed, "sample": sample,
                      "head_ledgers_now": led, "all": rows}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
