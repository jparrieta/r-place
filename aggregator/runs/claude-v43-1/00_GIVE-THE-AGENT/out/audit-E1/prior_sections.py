#!/usr/bin/env python3
"""E1 section 1, orderings proved by snaps (E1b-02): prior.md sections 1 to 6 sealed before B1's first
theme_discovery.jsonl line, and sections 7 and 8 added at D1. A snap holds the whole file's hash, so the snaps show
when prior.md moved but not which sections moved. This script rebuilds prior.md's text, write by write, from the
analyst's tool calls in out/_transcripts/, hashes each version, matches the versions to the snaps' hashes, and then
compares the version the B1 snap holds with the file as it stands, section by section. Prints JSON.

    python3 out/audit-E1/prior_sections.py > out/audit-E1/prior_sections.json

The rule, declared before the run (E1b-02):
- The writes: every Write, Edit or MultiEdit tool call whose file_path ends in out/prior.md, in the order of the legs'
  closes (INDEX.md) and, within a leg, of the records; an Edit counts only if its tool_result is not an error. A Bash
  command that names prior.md with a redirect or a move is listed, since it could write the file unseen.
- Each version's sha256 is set against the hashes in the snaps (out/_snap/*.sha256 lines for prior.md).
- Sections are the file's "## " headings. For the version that matches the first snap's hash and for the file as it
  stands: each section's heading, its sha256, and whether the two versions' sections are equal.
"""
import glob, hashlib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
TR = os.path.join(OUT, "_transcripts")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sections(text):
    out, head, buf = [], "(before the first heading)", []
    for line in text.split("\n"):
        if line.startswith("## "):
            out.append((head, "\n".join(buf)))
            head, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out.append((head, "\n".join(buf)))
    return out


def main():
    snap_hashes = {}
    for p in sorted(glob.glob(os.path.join(OUT, "_snap", "*.sha256"))):
        with open(p, encoding="utf-8") as f:
            head = f.readline()
            m = re.search(r"at (\S+)", head)
            for line in f:
                parts = line.rstrip("\n").split("  ", 3)
                if len(parts) == 4 and parts[3] == "prior.md":
                    snap_hashes.setdefault(parts[0], []).append((m.group(1) if m else "", os.path.basename(p)[:-7]))
    legs = []
    for l in open(os.path.join(TR, "INDEX.md"), encoding="utf-8"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[2].endswith(".jsonl"):
            legs.append((cells[4], cells[0], cells[2]))
    legs.sort()
    text, versions, bash_writes = None, [], []
    for _closed, leg, f in legs:
        p = os.path.join(TR, f)
        if not os.path.exists(p):
            continue
        raw = open(p, encoding="utf-8", errors="replace").read()
        if "prior.md" not in raw:
            continue
        recs = []
        for line in raw.split("\n"):
            if "prior.md" in line or '"tool_result"' in line:
                try:
                    recs.append(json.loads(line))
                except ValueError:
                    pass
        errors = {}
        for r in recs:
            c = (r.get("message") or {}).get("content")
            if r.get("type") == "user" and isinstance(c, list):
                for part in c:
                    if isinstance(part, dict) and part.get("type") == "tool_result":
                        errors[part.get("tool_use_id")] = bool(part.get("is_error"))
        for r in recs:
            c = (r.get("message") or {}).get("content")
            if r.get("type") != "assistant" or not isinstance(c, list):
                continue
            for part in c:
                if not isinstance(part, dict) or part.get("type") != "tool_use":
                    continue
                name, inp, tid = part.get("name"), part.get("input") or {}, part.get("id")
                fp = str(inp.get("file_path") or "")
                if name == "Bash":
                    cmd = str(inp.get("command") or "")
                    if "prior.md" in cmd and re.search(r">\s*\S*prior\.md|\bmv\b[^\n]*prior\.md|\bcp\b[^\n]*prior\.md", cmd):
                        bash_writes.append({"leg": leg, "t": r.get("timestamp"), "command": cmd[:300]})
                    continue
                if not fp.endswith("out/prior.md") or errors.get(tid):
                    continue
                if name == "Write":
                    text = inp.get("content") or ""
                elif name == "Edit" and text is not None:
                    old, new = inp.get("old_string") or "", inp.get("new_string") or ""
                    text = text.replace(old, new) if inp.get("replace_all") else text.replace(old, new, 1)
                elif name == "MultiEdit" and text is not None:
                    for e in inp.get("edits") or []:
                        text = text.replace(e.get("old_string") or "", e.get("new_string") or "", 1)
                else:
                    continue
                h = sha(text)
                versions.append({"leg": leg, "t": r.get("timestamp"), "tool": name, "sha": h[:12],
                                 "in_snaps": [x[1] for x in snap_hashes.get(h, [])][:2],
                                 "snap_count": len(snap_hashes.get(h, [])), "_text": text})
    now = open(os.path.join(OUT, "prior.md"), encoding="utf-8").read()
    first_snapped = next((v for v in versions if v["snap_count"]), None)
    cmp = None
    if first_snapped:
        a, b = sections(first_snapped["_text"]), sections(now)
        bd = dict(b)
        cmp = [{"section": h, "sha_then": sha(t)[:12], "sha_now": sha(bd[h])[:12] if h in bd else None,
                "equal": bd.get(h) == t} for h, t in a]
        cmp += [{"section": h, "sha_then": None, "sha_now": sha(t)[:12], "equal": None, "new": True}
                for h, t in b if h not in dict(a)]
    for v in versions:
        v.pop("_text", None)
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-02):")[1].strip(),
                      "snap_hashes": {h[:12]: {"snaps": len(v), "first": v[0], "last": v[-1]}
                                      for h, v in sorted(snap_hashes.items(), key=lambda kv: kv[1][0][0])},
                      "writes": versions, "bash_writes": bash_writes,
                      "now_sha": sha(now)[:12], "now_matches_a_rebuilt_version": any(v["sha"] == sha(now)[:12] for v in versions),
                      "first_snapped_version": {k: first_snapped[k] for k in ("leg", "t", "sha")} if first_snapped else None,
                      "sections_then_against_now": cmp}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
