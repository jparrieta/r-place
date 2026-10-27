#!/usr/bin/env python3
"""E1 section 2 (E1b-06): the ledgers, the stories, what a reader was given, the departures and the defects, by
script. Prints JSON.

    python3 out/audit-E1/ledgers_stories.py > out/audit-E1/ledgers_stories.json

The rule, declared before the run (E1b-06):
- findings.jsonl: lines by status; for each finding id, its statuses in line order with the stage of each line (a
  change of status is a line whose status differs from the id's line before); the warrant of each id's last line;
  the ids whose last line has an empty or missing `refuted_by`.
- Every other ledger in out/ (*.jsonl at the top, model/, fourth/): its non-empty lines now; its size in every snap
  that lists it, in snap order, and whether the size ever falls (a fall shows an edit or a cut; a rise does not
  prove that no line was edited, which a hash cannot show).
- New kinds per hundred themes: theme_discovery.jsonl's kinds over the second-order themes of the census.
- The stories: saturation.jsonl's passes, with rooms and the three counts each; story_rooms-pN.jsonl's rooms; rooms
  read against a story in all and distinct; the last pass's rooms not told, and how each fared in verdicts-D.jsonl's
  first return; the rooms no story was read against, and how many of them do not compose in the first return.
- account_passes.jsonl: its passes.
- account.md: its words; its cited quotes, and how many carry an hour; the rooms it names against branches.jsonl.
- departures.jsonl: each line's stage, leg and provision; whether it states a cost (a field or a sentence naming
  cost or would have); whether its own words say it was in use or acted on before it was written.
- defects.jsonl: lines by stage, and by whose: a line whose text says "The material's" or names the store, the
  package, a case account or the coders' records is the material's; "The instrument's", the analyst's files, the
  fleets' returns or the tools are the instrument's; else unsorted, read by hand.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    R = {}
    F = jl(os.path.join(OUT, "findings.jsonl"))
    by_id = collections.defaultdict(list)
    for f in F:
        by_id[f["id"]].append(f)
    changes = []
    for i, ls in by_id.items():
        prev = None
        for f in ls:
            if f.get("status") != prev:
                changes.append((i, f.get("stage"), f.get("leg"), prev, f.get("status")))
            prev = f.get("status")
    R["findings"] = {"lines": len(F), "ids": len(by_id),
                     "lines_by_status": dict(collections.Counter(f.get("status") for f in F)),
                     "last_status": dict(collections.Counter(ls[-1].get("status") for ls in by_id.values())),
                     "status_changes": changes,
                     "warrant_last": dict(collections.Counter(ls[-1].get("warrant") for ls in by_id.values())),
                     "no_refuted_by": sorted(i for i, ls in by_id.items() if not ls[-1].get("refuted_by"))}
    snaps = []
    for p in glob.glob(os.path.join(OUT, "_snap", "*.sha256")):
        with open(p, encoding="utf-8") as fh:
            m = re.search(r"at (\S+)", fh.readline())
            sizes = {}
            for line in fh:
                parts = line.rstrip("\n").split("  ", 3)
                if len(parts) == 4:
                    sizes[parts[3]] = int(parts[1]) if parts[1].isdigit() else None
        snaps.append((m.group(1) if m else "", sizes))
    snaps.sort()
    ledgers = {}
    for p in sorted(glob.glob(os.path.join(OUT, "*.jsonl")) + glob.glob(os.path.join(OUT, "model", "*.jsonl")) +
                    glob.glob(os.path.join(OUT, "fourth", "*.jsonl"))):
        rel = os.path.relpath(p, OUT)
        if rel.startswith(("_mem_", "_cite_")):
            continue
        seq = [s[rel] for _t, s in snaps if s.get(rel) is not None]
        falls = sum(1 for a, b in zip(seq, seq[1:]) if b < a)
        ledgers[rel] = {"lines": sum(1 for l in open(p, encoding="utf-8") if l.strip()), "snaps": len(seq), "size_falls": falls}
    R["ledgers"] = ledgers
    R["ledgers_with_a_size_fall"] = {k: v for k, v in ledgers.items() if v["size_falls"]}
    td = jl(os.path.join(OUT, "theme_discovery.jsonl"))
    R["kinds_per_hundred_themes"] = {"kinds": len(td), "themes_census": 7844, "per_hundred": round(100 * len(td) / 7844, 2)}
    sat = jl(os.path.join(OUT, "saturation.jsonl"))
    R["passes"] = [{k: s.get(k) for k in ("pass", "rooms", "told", "told-with-residue", "not-told", "cannot-tell")} for s in sat]
    rooms_all, rooms_by_pass = [], {}
    for p in sorted(glob.glob(os.path.join(OUT, "story_rooms-p*.jsonl"))):
        rs = jl(p)
        names = [r.get("sub") for r in rs if r.get("sub")]
        rooms_by_pass[os.path.basename(p)] = len(names)
        rooms_all += names
    R["story_rooms"] = {"files": rooms_by_pass, "in_all": len(rooms_all), "distinct": len(set(rooms_all))}
    last = sat[-1] if sat else {}
    V = {v["sub"]: v for v in jl(os.path.join(OUT, "verdicts-D.jsonl")) if not v.get("stage")}
    def verdict(s):
        v = V.get(s) or {}
        rs = [r.get("verdict") for r in (v.get("readers") or [])]
        return v.get("verdict") or "/".join(sorted(set(rs)))
    not_told = [r for r in (last.get("room_verdicts") or {}) if (last["room_verdicts"][r] in ("not-told", "cannot-tell"))] if isinstance(last.get("room_verdicts"), dict) else []
    R["last_pass"] = {"pass": last.get("pass"), "keys": sorted(last.keys()), "not_told_rooms": not_told,
                      "their_first_return": {s: verdict(s) for s in not_told}}
    story_set = set(rooms_all) | {s for x in sat for s in (x.get("room_list") or [])}
    never = [s for s in V if s not in story_set]
    R["never_read_against_a_story"] = {"rooms": len(never),
                                       "first_return": dict(collections.Counter(verdict(s) for s in never))}
    R["read_against_a_story_first_return"] = dict(collections.Counter(verdict(s) for s in V if s in story_set))
    R["account_passes"] = len(jl(os.path.join(OUT, "account_passes.jsonl")))
    acc = open(os.path.join(OUT, "account.md"), encoding="utf-8").read()
    cites = re.findall(r"\[([A-Za-z0-9_]+)/(c\d{4,5})(?:,\s*h?\s*([\d.]+))?\]", acc)
    named = set(re.findall(r"(?<![\w/])r/([A-Za-z0-9_]+)", acc)) | {c[0] for c in cites}
    inb = set()
    for b in jl(os.path.join(OUT, "branches.jsonl")):
        inb |= set(b.get("members") or [])
    R["account"] = {"words": len(acc.split()), "cited_quotes": len(cites), "with_hour": sum(1 for c in cites if c[2]),
                    "rooms_named": len(named), "named_in_a_branch": len(named & inb), "named_in_no_branch": sorted(named - inb)}
    D = jl(os.path.join(OUT, "departures.jsonl"))
    rows = []
    for i, d in enumerate(D, 1):
        s = json.dumps(d, ensure_ascii=False)
        rows.append({"line": i, "stage": d.get("stage"), "leg": d.get("leg"), "provision": (d.get("provision") or "")[:110],
                     "states_cost": bool(re.search(r"cost|would have|instead of|at the price", s, re.I)),
                     "acted_before_written": bool(re.search(r"logged late|in use before|already in use|before (it|they) (was|were) (stated|written)|acted on before", s, re.I))})
    R["departures"] = rows
    X = jl(os.path.join(OUT, "defects.jsonl"))
    whose = collections.Counter()
    unsorted = []
    for i, d in enumerate(X, 1):
        s = json.dumps(d, ensure_ascii=False)
        if re.search(r"The material's|package/|the store|case account|case\.md|coder", s):
            k = "material"
        elif re.search(r"The instrument's|reader|record slip|fleet|out/|_analysis|\.md|tools/|prediction line", s):
            k = "instrument"
        else:
            k = "unsorted"
            unsorted.append((i, d.get("stage"), s[:160]))
        whose[(d.get("stage"), k)] += 1
    R["defects"] = {"lines": len(X), "by_stage": dict(collections.Counter(d.get("stage") for d in X)),
                    "by_stage_and_whose": {"%s %s" % k: v for k, v in sorted(whose.items())}, "unsorted": unsorted}
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-06):")[1].strip(), **R},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
