#!/usr/bin/env python3
"""E1 section 1, probes-E1.md (E1b-05): every wrong re-read answer of the recall probe, sorted into a note (the head,
the diary or the question files held the answer at the close, so the miss is the probe session's recall) or a defect
(nothing on record held it). Reads probes_score.json (E1a) and out/_probe/NN-L.json; prints JSON.

    python3 out/audit-E1/probes_notes.py > out/audit-E1/probes_notes.json

The rule, declared before the run (E1b-05):
- A leg's window: from the previous probe of the same stage (its NN-L.json `t`) to this one's; the diary lines of the
  stage written in that window are the leg's.
- goal: the head states the method question in one sentence at every close (the head's own section), so a wrong goal
  is a note.
- open: a note where every expected slug is a file in out/_questions/ (files are never deleted).
- rooms: a note where every expected room is named in the leg's diary lines.
- changed: a note where at least one expected id is named in the leg's diary lines.
- next: a note where the expected text's first six words are in the leg's diary lines.
- Otherwise a defect. n/a stays apart and is never recall; 'missing' as filed is the parse, reported beside.
"""
import collections, datetime, glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
Q = ("goal", "open", "rooms", "changed", "next")


def ts(s):
    s = (s or "").replace("Z", "").split("+")[0]
    try:
        return datetime.datetime.fromisoformat(s[:19])
    except ValueError:
        return None


def main():
    ps = json.load(open(os.path.join(OUT, "audit-E1", "probes_score.json"), encoding="utf-8"))
    diary = collections.defaultdict(list)
    for p in glob.glob(os.path.join(OUT, "diary", "*.jsonl")):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                diary[r.get("stage")].append((ts(r.get("t")), r.get("text") or ""))
    qfiles = {f[:-3] for f in os.listdir(os.path.join(OUT, "_questions")) if f.endswith(".md")}
    probes = []
    for row in ps["per_leg"]:
        j = json.load(open(os.path.join(OUT, "_probe", row["leg"] + ".json"), encoding="utf-8"))
        probes.append((row, j))
    last_t = {}
    by_stage = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    defects = []
    for row, j in sorted(probes, key=lambda x: x[1].get("t") or ""):
        st, t = j.get("stage"), ts(j.get("t"))
        lo = last_t.get(st)
        last_t[st] = t
        text = "\n".join(x for tt, x in diary.get(st, []) if tt and t and tt <= t and (lo is None or tt > lo))
        exp = j.get("expected") or {}
        for q in Q:
            r = row["reread"].get(q)
            c = by_stage[st][q]
            c["filed " + row["filed"].get(q, "?")] += 1
            if r != "wrong":
                c["reread " + str(r)] += 1
                continue
            e = exp.get(q)
            if q == "goal":
                ok = True
            elif q == "open":
                ok = all(s in qfiles for s in (e or []))
            elif q == "rooms":
                ok = all(x in text for x in (e or []))
            elif q == "changed":
                ok = any(x in text for x in (e or []))
            else:
                ok = bool(e) and " ".join(str(e).split()[:6]) in text
            c["reread wrong: note" if ok else "reread wrong: defect"] += 1
            # Added after the first run (E1b-05): the harness's expected rooms and ids repeat across legs that opened
            # nothing, so they are the last ones on record, not the leg's own. The same test over the stage's diary
            # up to the close is reported beside the declared one; the declared counts stay as they are.
            upto = "\n".join(x for tt, x in diary.get(st, []) if tt and t and tt <= t)
            if q == "rooms":
                ok2 = all(x in upto for x in (e or []))
            elif q == "changed":
                ok2 = any(x in upto for x in (e or []))
            else:
                ok2 = ok
            c["up to the close: note" if ok2 else "up to the close: defect"] += 1
            if not ok:
                defects.append({"leg": row["leg"], "question": q, "expected": e, "on_record_up_to_the_close": ok2})
    tot = collections.defaultdict(collections.Counter)
    for st, qs in by_stage.items():
        for q, c in qs.items():
            tot[q].update(c)
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-05):")[1].strip(),
                      "legs": len(probes), "by_question": {q: dict(tot[q]) for q in Q},
                      "by_stage": {st: {q: dict(c) for q, c in qs.items()} for st, qs in by_stage.items()},
                      "defects": defects}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
