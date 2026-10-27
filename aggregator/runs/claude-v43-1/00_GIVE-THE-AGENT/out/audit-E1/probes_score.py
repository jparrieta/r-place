#!/usr/bin/env python3
"""E1 section 1, probes-E1.md's figures: the recall probe over every out/_probe/ answer file.

    python3 out/audit-E1/probes_score.py > out/audit-E1/probes_score.json

Declared before the run (E1a). probe.py NN --leg L --score ran at every close (the harness's; each answer file has its
NN-L.json beside it). This script does not rerun it: --score writes into _probe/, which is the harness's, and scores
the open distinctions against the question files as they stand now, not as they stood at the close. Instead:
  - as filed: each NN-L.json's status per question (right, wrong, missing, n/a), counted per stage and per question;
  - re-read: probe.py's own matching rule reads a line 'goal: ...'. Where the answer file writes '- **goal:** ...'
    (markdown bold), that rule finds nothing and the question is 'missing'. The script re-reads each answer file with
    the bold and list marks stripped and judges it by probe.py's own rules against the `expected` values the harness
    stored in NN-L.json at the close (for goal, the four key words of the method question). Both are reported; the
    filed score is the record, the re-read says how much of it is the parse.
  - n/a (nothing on record to check) is counted apart, never as recall.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PD = os.path.join(ROOT, "out", "_probe")
Q = ("goal", "open", "rooms", "changed", "next")


def reread(path):
    ans = {}
    for line in open(path, encoding="utf-8"):
        # every leading list or bold mark goes (a first run stripped one character only; probes_score.superseded-1.json)
        s = re.sub(r"^[\s\-*]+", "", line).replace("**", "")
        m = re.match(r"^\s*(goal|open|rooms|changed|next)\s*:\s*(.*)$", s, re.I)
        if m:
            ans[m.group(1).lower()] = m.group(2).strip()
    return ans


def judge(ans, exp, filed):
    st = {}
    def j(k, applicable, ok):
        if not applicable:
            st[k] = "n/a"
        elif not ans.get(k, "").strip():
            st[k] = "missing"
        else:
            st[k] = "right" if ok else "wrong"
    j("goal", True, sum(1 for w in ("compos", "case", "level", "evidence") if w in ans.get("goal", "").lower()) >= 3)
    op = set(exp.get("open") or [])
    said = {s.strip().strip("`,.;") for s in re.split(r"[\s,;]+", ans.get("open", "")) if s.strip()}
    j("open", bool(op), len(op & said) >= max(1, len(op) // 2))
    last = exp.get("rooms") or []
    j("rooms", bool(last), sum(1 for s in last if s.lower() in ans.get("rooms", "").lower()) >= min(2, len(last)))
    ids = exp.get("changed") or []
    j("changed", bool(ids), any(i in ans.get("changed", "") for i in ids))
    words = re.findall(r"[A-Za-z0-9_/-]{4,}", (exp.get("next") or "").lower())
    j("next", bool(words), sum(1 for w in words if w in ans.get("next", "").lower()) >= max(1, len(words) // 3))
    return st


def main():
    filed = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    redo = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    legs, empty, bold = 0, [], 0
    per_leg = []
    for a in sorted(glob.glob(os.path.join(PD, "*.answers.md"))):
        base = a[:-len(".answers.md")]
        name = os.path.basename(base)
        stage = name.split("-")[0]
        js = base + ".json"
        if not os.path.exists(js):
            per_leg.append({"leg": name, "json": False})
            continue
        legs += 1
        r = json.load(open(js, encoding="utf-8"))
        txt = open(a, encoding="utf-8").read()
        if not txt.strip():
            empty.append(name)
        if "**goal:**" in txt or "**goal**" in txt:
            bold += 1
        st2 = judge(reread(a), r.get("expected") or {}, r.get("status") or {})
        for q in Q:
            filed[stage][q][(r.get("status") or {}).get(q, "absent")] += 1
            redo[stage][q][st2[q]] += 1
        per_leg.append({"leg": name, "filed": r.get("status"), "reread": st2, "filed_score": r.get("score")})
    def flat(d):
        return {s: {q: dict(c) for q, c in qs.items()} for s, qs in d.items()}
    def tot(d):
        t = collections.defaultdict(collections.Counter)
        for qs in d.values():
            for q, c in qs.items():
                t[q].update(c)
        return {q: dict(c) for q, c in t.items()}
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a).")[1].strip(),
                      "answer_files": len(glob.glob(os.path.join(PD, "*.answers.md"))), "scored_legs": legs,
                      "empty_answer_files": empty, "answer_files_in_bold_markdown": bold,
                      "filed_by_question": tot(filed), "reread_by_question": tot(redo),
                      "filed_by_stage": flat(filed), "reread_by_stage": flat(redo),
                      "notes_jsonl_lines": sum(1 for l in open(os.path.join(PD, "notes.jsonl")) if l.strip()),
                      "per_leg": per_leg}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
