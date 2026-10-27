#!/usr/bin/env python3
"""E1 section 1, the diary against the transcript, second pass (E1b-05): the 513 diary lines of the 17 drawn legs that
diary_transcript.py (E1a) did not find word for word, read against the tool calls of their leg. Prints JSON.

    python3 out/audit-E1/diary_tool_lines.py > out/audit-E1/diary_tool_lines.json

The rule, declared before the run (E1b-05):
- Each line's tokens: room-and-theme ids (sub:tNN or sub/tNN), third- and fourth-order ids (T3-NNN, T4-NNN), question
  ids (QXX-NNN), element and arrow ids (P01, A13, K02, R01, C02), file names ending .jsonl, .json, .md or .py; for an
  'opened' line, the room's name.
- The leg's transcript records within ten minutes before or after the line's time (UTC), of two types: the analyst's
  tool input (a command or a file written) and a tool's output.
- A line is borne out when one such record holds its first two tokens (its one token, if it has one). A line with no
  token is borne out when a record in the window holds its first five words. Every line not borne out is listed for
  reading by hand; it is a defect only if the reading finds no tool call that wrote it.
"""
import datetime, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
TR = os.path.join(OUT, "_transcripts")
TOK = re.compile(r"[A-Za-z0-9_]+[:/]t\d{2,3}\b|\bT[34]-\d{3}\b|\bQ[A-Z0-9]+-\d{3}\b|\b[PAKRC]\d{2}\b|[\w./-]+\.(?:jsonl|json|md|py)\b")


def ts(s):
    s = (s or "").replace("Z", "").split("+")[0]
    try:
        return datetime.datetime.fromisoformat(s[:19])
    except ValueError:
        return None


def records(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            j = json.loads(line)
        except ValueError:
            continue
        c = (j.get("message") or {}).get("content")
        if not isinstance(c, list):
            continue
        parts = []
        for p in c:
            if not isinstance(p, dict):
                continue
            if p.get("type") == "tool_use":
                parts.append(json.dumps(p.get("input"), ensure_ascii=False))
            elif p.get("type") == "tool_result":
                parts.append(json.dumps(p.get("content"), ensure_ascii=False))
        if parts:
            out.append((ts(j.get("timestamp")), "\n".join(parts)))
    return out


def main():
    dt = json.load(open(os.path.join(OUT, "audit-E1", "diary_transcript.json"), encoding="utf-8"))
    res, unborne = {}, []
    tot = {"lines": 0, "borne_out": 0}
    for g in dt["drawn"]:
        recs = records(os.path.join(TR, g["file"]))
        n = b = 0
        for x in g["not_found"]:
            n += 1
            t = ts(x.get("t"))
            text = x.get("text") or ""
            toks = TOK.findall(text)
            if x.get("kind") == "opened":
                toks = [text.split(" ", 1)[1].split(" ")[0]] if " " in text else toks
            near = [r for tt, r in recs if t and tt and abs((tt - t).total_seconds()) <= 600]
            if toks:
                need = toks[:2]
                ok = any(all(k in r for k in need) for r in near)
            else:
                five = " ".join(text.split()[:5])
                ok = any(five in r for r in near)
            if ok:
                b += 1
            else:
                unborne.append({"leg": g["leg"], "kind": x.get("kind"), "t": x.get("t"), "tokens": toks[:3], "text": text[:200]})
        res[g["leg"]] = {"stage": g["stage"], "not_found_at_E1a": n, "borne_out_by_tool_call": b}
        tot["lines"] += n
        tot["borne_out"] += b
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-05):")[1].strip(),
                      "totals": tot, "by_leg": res, "not_borne_out": unborne}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
