#!/usr/bin/env python3
"""E2a: the dialogue of each interview transcript in handling/interviews/, in order, without tool calls or results.

    python3 out/_analysis/e2_interviews.py > out/_analysis/e2_interviews.txt
    python3 out/_analysis/e2_interviews.py --stats

For each transcript named in interviews.tsv (in the file's order): its stage and leg; then each dialogue turn with a
running number, the role (PI for a user turn with text, ANALYST for an assistant text block), its timestamp and its
text whole. User turns that hold only tool results, attachments and harness records are skipped. A turn is cited in
handling-E2.md as <leg> turn <n>.
"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
H = os.path.join(ROOT, "handling", "interviews")


def texts(content):
    if isinstance(content, str):
        return [content]
    out = []
    for b in content or []:
        if isinstance(b, dict) and b.get("type") == "text" and b.get("text", "").strip():
            out.append(b["text"])
    return out


def main():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(H, "interviews.tsv"), encoding="utf-8") if l.strip()]
    stats = "--stats" in sys.argv
    for utc, leg, _sess, fid in rows:
        turns = []
        for line in open(os.path.join(H, fid + ".jsonl"), encoding="utf-8"):
            d = json.loads(line)
            if d.get("type") not in ("user", "assistant") or d.get("isSidechain"):
                continue
            msg = d.get("message") or {}
            role = "PI" if d["type"] == "user" else "ANALYST"
            for t in texts(msg.get("content")):
                turns.append((role, d.get("timestamp", ""), t))
        # The transcript holds the forked leg's conversation first; the interview begins at the last PI turn that
        # opens "This is an interview" (turn numbers still count from the transcript's first dialogue turn).
        starts = [i for i, t in enumerate(turns) if t[0] == "PI" and t[2].lstrip().startswith("This is an interview")]
        first = starts[-1] if starts else 0
        if stats:
            body = turns[first:]
            print(leg, fid, "interview from turn", first + 1, "of", len(turns), "chars", sum(len(t[2]) for t in body),
                  "PI chars", sum(len(t[2]) for t in body if t[0] == "PI"))
            continue
        print("\n" + "=" * 20 + " %s (%s, %s); interview from turn %d" % (leg, utc, fid, first + 1))
        for i, (role, ts, t) in enumerate(turns, 1):
            if i - 1 >= first:
                print("\n--- %s turn %d %s %s\n%s" % (leg, i, role, ts, t))


if __name__ == "__main__":
    main()
