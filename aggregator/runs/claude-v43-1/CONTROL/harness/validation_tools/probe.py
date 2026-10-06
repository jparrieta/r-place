#!/usr/bin/env python3
"""probe.py — the recall probe (STANDING-INSTRUCTIONS §2). Two calls:

    python3 tools/probe.py NN --leg L --ask       # writes _probe/NN-L.questions.md for the fresh turn
    python3 tools/probe.py NN --leg L --score     # scores _probe/NN-L.answers.md against the record

The harness runs the ask at done.sh, opens a fresh turn with the questions, saves the analyst's
answers verbatim to _probe/NN-L.answers.md, and runs the score. A miss is written to
_probe/notes.jsonl with stage, leg and the question missed (a note, not a defect).
"""
import argparse, datetime, json, os, re, sys

QUESTIONS = [
    ("goal", "State the method question in one sentence."),
    ("open", "List the open distinctions by slug, from your question files."),
    ("rooms", "Name the last three rooms you opened in this leg."),
    ("changed", "Name the element or theme you changed in this leg, and why, in one sentence."),
    ("next", "What is the next comparison you intend to make?"),
]

def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("stage"); ap.add_argument("--leg", required=True)
    ap.add_argument("--root", default="."); ap.add_argument("--out", default=None)
    ap.add_argument("--ask", action="store_true"); ap.add_argument("--score", action="store_true")
    a = ap.parse_args(); out = a.out or os.path.join(a.root, "out"); pd = os.path.join(out, "_probe"); os.makedirs(pd, exist_ok=True)
    base = os.path.join(pd, "%s-%s" % (a.stage, a.leg))
    if a.ask:
        with open(base + ".questions.md", "w", encoding="utf-8") as f:
            f.write("# Recall probe, stage %s leg %s\n\nAnswer from memory, without opening any file. One line each.\n\n" % (a.stage, a.leg))
            for k, q in QUESTIONS:
                f.write("%s: %s\n" % (k, q))
        print("probe questions written: %s.questions.md" % base); return 0
    if a.score:
        ap_ = base + ".answers.md"
        if not os.path.exists(ap_):
            print("no answers file"); return 1
        ans = {}
        for line in open(ap_, encoding="utf-8"):
            m = re.match(r"^\s*(goal|open|rooms|changed|next)\s*:\s*(.*)$", line, re.I)
            if m: ans[m.group(1).lower()] = m.group(2).strip()
        # each question is right, wrong, missing (no answer) or n/a (nothing on record to check it against);
        # the score is right over the questions that could be checked, and n/a never counts as recall
        # (review 2026-09-29). What is checked is named: `changed` checks the id, not the reason.
        status, expected = {}, {}
        def judge(k, applicable, ok):
            if not applicable:
                status[k] = "n/a"
            elif not ans.get(k, "").strip():
                status[k] = "missing"
            else:
                status[k] = "right" if ok else "wrong"
        # goal: key words of the method question
        keys = ["compos", "case", "level", "evidence"]
        judge("goal", True, sum(1 for k in keys if k in ans.get("goal", "").lower()) >= 3)
        # open: slugs of question files without a verdict line
        qd = os.path.join(out, "_questions"); open_slugs = set()
        if os.path.isdir(qd):
            for f in os.listdir(qd):
                if f.endswith(".md") and "verdict:" not in open(os.path.join(qd, f), encoding="utf-8").read().lower():
                    open_slugs.add(f[:-3])
        said = {s.strip().strip("`,.;") for s in re.split(r"[\s,;]+", ans.get("open", "")) if s.strip()}
        judge("open", bool(open_slugs), len(open_slugs & said) >= max(1, len(open_slugs) // 2))
        expected["open"] = sorted(open_slugs)
        # rooms: the last three room opens in the read log for this leg
        reads = [r for r in jl(os.path.join(out, "_mem_reads-%s.jsonl" % a.stage))
                 if r.get("verb") == "room" and r.get("args") and r.get("leg", a.leg) == a.leg]
        last = []
        for r in reversed(reads):
            s_ = r["args"][0]
            if s_ not in last: last.append(s_)
            if len(last) == 3: break
        judge("rooms", bool(last), sum(1 for s_ in last if s_.lower() in ans.get("rooms", "").lower()) >= min(2, len(last)))
        expected["rooms"] = last
        # changed: an id from this leg's history lines (the id only; the reason is read by a person)
        hist = [r for r in jl(os.path.join(out, "model", "history.jsonl")) + jl(os.path.join(out, "tier_history.jsonl")) if r.get("leg") == a.leg]
        ids = sorted({r.get("id") for r in hist if r.get("id")})
        judge("changed", bool(ids), any(i in ans.get("changed", "") for i in ids))
        expected["changed"] = ids
        # next: the last `next:` this leg wrote in the diary, when there is one
        nxt = ""
        import glob as _g
        for fp in sorted(_g.glob(os.path.join(out, "diary", "%s-*.jsonl" % a.stage))):
            for r in jl(fp):
                m = re.search(r"\bnext:\s*(.+)$", str(r.get("text") or ""))
                if m and r.get("leg") == a.leg:
                    nxt = m.group(1).strip()
        words = [w for w in re.findall(r"[A-Za-z0-9_/-]{4,}", nxt.lower())]
        judge("next", bool(words), sum(1 for w in words if w in ans.get("next", "").lower()) >= max(1, len(words) // 3))
        expected["next"] = nxt
        scored = [k for k in status if status[k] != "n/a"]
        misses = [k for k in scored if status[k] != "right"]
        result = {"t": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "stage": a.stage, "leg": a.leg,
                  "answers": ans, "expected": expected, "status": status,
                  "scored": len(scored), "unscored": [k for k in status if status[k] == "n/a"],
                  "misses": misses,
                  "score": round(sum(1 for k in scored if status[k] == "right") / len(scored), 3) if scored else None,
                  "checks": "goal: key words; open: slugs; rooms: names; changed: an id, not the reason; next: the diary's last next:"}
        json.dump(result, open(base + ".json", "w"), indent=1)
        if misses:
            # a miss is a note: the head and the diary may hold the answer the turn did not recall
            with open(os.path.join(out, "_probe", "notes.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({"stage": a.stage, "leg": a.leg, "where": "recall probe", "what": "missed: " + ", ".join(misses), "sure": True, "t": result["t"]}) + "\n")
        print(json.dumps({"status": status, "misses": misses, "score": result["score"]})); return 0
    print("probe needs --ask or --score"); return 2

if __name__ == "__main__":
    sys.exit(main())
