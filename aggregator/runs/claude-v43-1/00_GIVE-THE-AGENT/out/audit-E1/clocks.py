#!/usr/bin/env python3
"""E1 section 1, the clocks.

    python3 out/audit-E1/clocks.py > out/audit-E1/clocks.json

Declared before the run (E1a):
  1. The coder's time against the item's own: every concept quotes one item id (codes.jsonl `item_id`). Its
     `created_utc`, as the coder wrote it, against the forest's `created_utc` for that item (items.jsonl, the same room
     and item id). Agreement exact and within 60 seconds; the denominator is the concepts whose item the store holds.
     Also the concept's `hour` against its own created_utc (hour = (created_utc - 1490976000) / 3600, README-store.md).
  2. relations.jsonl: no tool; the second check is done by hand in the audit section and logged.
  3. Datings in written order: in each room's case account (package/<sub>/case.md), the Chronology section's datings
     ("dN MM-DD HH:MM") in the order written. A room whose datings ever step back is one whose datings do not run in
     written order. Then, for each arrow of the model (model/arrows.jsonl), how many of the rooms it names (`subs`,
     else the rooms in its `support` or `counts`) are such rooms.
"""
import collections, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
ST = os.path.join(ROOT, "package", "store")
DATING = re.compile(r"\bd(-?\d+) (\d\d)-(\d\d) (\d\d):(\d\d)\b")


def jl(p):
    for l in open(p, encoding="utf-8"):
        if l.strip():
            yield json.loads(l)


def rooms_in(o, frame):
    out = set()
    if isinstance(o, str):
        if o in frame:
            out.add(o)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in frame:
                out.add(k)
            out |= rooms_in(v, frame)
    elif isinstance(o, list):
        for v in o:
            out |= rooms_in(v, frame)
    return out


def main():
    item_t = {}
    for r in jl(os.path.join(ST, "items.jsonl")):
        item_t.setdefault((r["sub"], r["item_id"]), set()).add(r.get("created_utc"))
    n = exact = within = held = hour_ok = 0
    worst = []
    for c in jl(os.path.join(ST, "codes.jsonl")):
        n += 1
        if isinstance(c.get("hour"), (int, float)) and isinstance(c.get("created_utc"), (int, float)):
            hour_ok += abs(c["hour"] - (c["created_utc"] - 1490976000) / 3600) < 0.01
        ts = item_t.get((c["sub"], c["item_id"]))
        if not ts:
            continue
        held += 1
        d = min(abs((c.get("created_utc") or 0) - (t or 0)) for t in ts)
        exact += d == 0
        within += d <= 60
        if d > 60:
            worst.append((d, c["sub"], c["code_id"], c["item_id"]))
    worst.sort(reverse=True)
    frame = {r["sub"] for r in jl(os.path.join(ST, "rooms.jsonl"))}
    back, counted = {}, 0
    for s in sorted(frame):
        p = os.path.join(ROOT, "package", s, "case.md")
        t = open(p, encoding="utf-8").read()
        m = re.search(r"^## Chronology\s*$(.*?)(?=^## |\Z)", t, re.M | re.S)
        body = m.group(1) if m else ""
        ds = [(int(a), int(b), int(c_), int(d), int(e)) for a, b, c_, d, e in DATING.findall(body)]
        if len(ds) >= 2:
            counted += 1
            steps = sum(1 for x, y in zip(ds, ds[1:]) if y < x)
            if steps:
                back[s] = {"datings": len(ds), "steps_back": steps}
    arrows = []
    for a in jl(os.path.join(OUT, "model", "arrows.jsonl")):
        rs = set(a.get("subs") or []) & frame if isinstance(a.get("subs"), list) else set()
        if not rs:
            rs = rooms_in({k: a.get(k) for k in ("support", "counts", "support_transition", "sampled_against")}, frame)
        arrows.append({"id": a["id"], "from": a.get("from"), "to": a.get("to"), "rooms_named": len(rs),
                       "rooms_out_of_order": len(rs & set(back)), "status": a.get("status"), "in_model": a.get("in_model")})
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a):")[1].strip(),
                      "concepts": n, "concepts_whose_item_the_store_holds": held,
                      "coder_time_equals_item_time": exact, "within_60_s": within,
                      "share_exact": round(exact / held, 4) if held else None, "share_within_60_s": round(within / held, 4) if held else None,
                      "hour_matches_own_created_utc": hour_ok, "largest_differences": worst[:12],
                      "rooms_with_two_or_more_chronology_datings": counted,
                      "rooms_whose_datings_step_back": len(back), "rooms_back": back,
                      "arrows": arrows,
                      "arrows_resting_on_any_such_room": sum(1 for a in arrows if a["rooms_out_of_order"])}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
