#!/usr/bin/env python3
"""E1e: the facts experience-E1.md is written from, computed so that none is typed from memory.

    python3 out/audit-E1/experience_facts.py > out/audit-E1/experience_facts.json

- Tokens by stage, from RUN.json's legs: legs closed, input, cache creation, cache read and output tokens summed.
- The diary by stage, from out/diary/*.jsonl: lines, lines by kind, and the notes that record a compaction (a note
  whose text begins "compacted").
- The operator's answers, out/_answers/*.md: each question id with the answer's first 300 characters.
- The heads on file (out/_head*.md) and the handbacks (out/handback-*.md), with their word counts.
"""
import collections, glob, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
ORDER = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "E1"]


def main():
    run = json.load(open(os.path.join(ROOT, "RUN.json"), encoding="utf-8"))
    tok = collections.defaultdict(lambda: collections.Counter())
    for l in run["legs"]:
        s = l.get("stage")
        tok[s]["legs"] += 1
        for k, v in (l.get("tokens") or {}).items():
            tok[s][k] += v
    diary = collections.defaultdict(lambda: collections.Counter())
    for p in glob.glob(os.path.join(OUT, "diary", "*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            s = str(r.get("stage"))
            diary[s]["lines"] += 1
            diary[s]["kind:" + str(r.get("kind"))] += 1
            if str(r.get("text", "")).strip().lower().startswith("compacted"):
                diary[s]["compactions"] += 1
    answers = []
    for p in sorted(glob.glob(os.path.join(OUT, "_answers", "*.md"))):
        t = re.sub(r"\s+", " ", open(p, encoding="utf-8").read()).strip()
        answers.append({"id": os.path.basename(p)[:-3], "answer": t[:300]})
    stages = [s for s in ORDER if s in tok or s in diary] + sorted((set(tok) | set(diary)) - set(ORDER))
    print(json.dumps({
        "by_stage": {s: {"tokens": dict(tok.get(s, {})), "diary": dict(diary.get(s, {}))} for s in stages},
        "totals": {"legs": sum(t["legs"] for t in tok.values()),
                   "output_tokens": sum(t["output_tokens"] for t in tok.values()),
                   "input_tokens": sum(t["input_tokens"] for t in tok.values()),
                   "cache_read_input_tokens": sum(t["cache_read_input_tokens"] for t in tok.values()),
                   "cache_creation_input_tokens": sum(t["cache_creation_input_tokens"] for t in tok.values()),
                   "diary_lines": sum(d["lines"] for d in diary.values()),
                   "compactions": sum(d["compactions"] for d in diary.values())},
        "answers": answers,
        "heads": {os.path.basename(p): len(open(p, encoding="utf-8").read().split()) for p in sorted(glob.glob(os.path.join(OUT, "_head*.md")))},
        "handbacks": {os.path.basename(p): len(open(p, encoding="utf-8").read().split()) for p in sorted(glob.glob(os.path.join(OUT, "handback-*.md")))},
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
