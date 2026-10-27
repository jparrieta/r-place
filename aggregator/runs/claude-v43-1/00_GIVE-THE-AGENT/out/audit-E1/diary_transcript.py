#!/usr/bin/env python3
"""E1 section 1, the diary against the transcript, for legs drawn by seed, one per stage at least.

    python3 out/audit-E1/diary_transcript.py > out/audit-E1/diary_transcript.json

Declared before the run (E1a). The legs are the rows of out/_transcripts/INDEX.md (one per leg close). Drawn with
random.Random(int(out/seed.txt, 16)): one leg per stage, in stage order, and one more among the D6 extra legs
D6a-09 to D6a-18 (J's ruling that they are part of the run audited). For each drawn leg, every diary line of that
leg (out/diary/, read whole by script) is looked for in the leg's transcript: the line's first twelve words, lower-cased
with everything but letters and digits made a space, against the transcript's text normalised the same way. A line found
is borne out as written by a mem.py log call in that session; a line not found is listed, to be read by hand in the
audit section (it may have been written in a continuation of the leg, or the log call was refused). What each entry
claims against what the transcript shows the tools returned is read by hand there.
"""
import collections, glob, json, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
TD = os.path.join(OUT, "_transcripts")
ORDER = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "E1"]


def words(s, n=None):
    w = re.sub(r"[^a-z0-9]+", " ", s.lower()).split()
    return " ".join(w[:n] if n else w)


def main():
    rows = []
    for line in open(os.path.join(TD, "INDEX.md"), encoding="utf-8"):
        m = re.match(r"^\| ([A-E]\d)\.(\S+) \| (\S+) \| (\S+) \| (\d+) \| (\S+) \|", line)
        if m:
            rows.append({"stage": m.group(1), "leg": m.group(2), "session": m.group(3), "file": m.group(4),
                         "lines": int(m.group(5)), "closed": m.group(6)})
    seed = open(os.path.join(OUT, "seed.txt")).read().split()[0]
    rnd = random.Random(int(seed, 16))
    drawn = []
    for st in ORDER:
        legs = [r for r in rows if r["stage"] == st]
        if legs:
            drawn.append(rnd.choice(legs))
    extra = [r for r in rows if r["stage"] == "D6" and re.match(r"D6a-(09|1\d)$", r["leg"]) and r not in drawn]
    if extra:
        drawn.append(rnd.choice(extra))
    diary = collections.defaultdict(list)
    for p in glob.glob(os.path.join(OUT, "diary", "*.jsonl")):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                diary[r.get("leg")].append(r)
    out = []
    for d in drawn:
        p = os.path.join(TD, d["file"])
        text = words(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else ""
        lines_ = sorted(diary.get(d["leg"], []), key=lambda r: r.get("t") or "")
        found, missing = 0, []
        for r in lines_:
            key = words(r.get("text") or "", 12)
            if key and key in text:
                found += 1
            else:
                missing.append({"t": r.get("t"), "kind": r.get("kind"), "text": (r.get("text") or "")[:200]})
        out.append(dict(d, transcript_present=bool(text), diary_lines=len(lines_), borne_out=found, not_found=missing))
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a).")[1].strip(), "seed": seed,
                      "legs_in_index": len(rows), "stages_in_index": sorted({r["stage"] for r in rows}, key=ORDER.index),
                      "drawn": out,
                      "totals": {"legs": len(out), "diary_lines": sum(x["diary_lines"] for x in out),
                                 "borne_out": sum(x["borne_out"] for x in out)}}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
