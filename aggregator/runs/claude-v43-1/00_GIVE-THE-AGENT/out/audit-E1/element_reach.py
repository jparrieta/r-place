#!/usr/bin/env python3
"""E1 section 3, prior.md section 3's local measure, its element-reach half (J's ruling of 27 October 09:30, carried by
the PI to E1): each second-order theme that holds a coordinating turn, reached by an element of the model.

    python3 out/audit-E1/element_reach.py > out/audit-E1/element_reach.json

Declared before the run (E1a), from prior.md section 3 ("A room's organizing is accounted for when every one of its
second-order themes that holds a coordinating turn (under section 5) is reached by an element of the model or by a
validated adaptation, or is listed as unresolved with its reason") and section 5 (the rule):
  - A coordinating turn: a concept that out/_analysis/a1_ends.py's coordinating() accepts, the A1 rule as coded
    (the store's first_order and hour). Its per-room totals are checked against organizing_end-A1.jsonl.
  - A theme holds a coordinating turn when one of its concepts is one.
  - The theme's placement: the third-order themes mem.py's overlay gives it (assignments_final.jsonl, the last write).
  - Reached by an element: one of its third-order themes is a member of a fourth-order theme (fourth/fourth.jsonl)
    that a standing element of the frozen model names in its `tier` (model/elements.jsonl, the D3 freeze 46384686).
    Candidates (the fifteen) are counted apart, as a second figure, never in the first.
  - Denominators as section 3 names them: the 705 rooms; the rooms with at least one coordinating turn; the themes
    holding a coordinating turn. A room is reached in full when every such theme of it is reached.
This is the element-reach half only; the other half (a validated adaptation, or unresolved with a reason) is not
computed here. The figure is a structural reach through the tiers, not a reading of the room.
"""
import collections, importlib.util, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import mem  # noqa: E402

spec = importlib.util.spec_from_file_location("a1_ends", os.path.join(OUT, "_analysis", "a1_ends.py"))
a1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a1)


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    st = mem.Store(ROOT, OUT)
    codes = st.rows("codes")
    placed = st.overlay()["placed"]
    fourth = {r["id"]: set(r.get("members") or []) for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
    els = jl(os.path.join(OUT, "model", "elements.jsonl"))
    def t3_of(status):
        s = set()
        for e in els:
            if (e.get("status") or "standing") in status:
                for t4 in e.get("tier") or []:
                    s |= fourth.get(t4, set())
        return s
    standing = t3_of({"standing", "bounded"})
    with_cand = t3_of({"standing", "bounded", "candidate"})
    status_seen = collections.Counter(e.get("status") for e in els)
    coord = collections.defaultdict(set)
    per_room_turns = collections.Counter()
    for c in codes:
        if a1.coordinating(c):
            coord[c["sub"]].add(c["theme_id"])
            per_room_turns[c["sub"]] += 1
    a1_end = {r["sub"]: r.get("coordinating_turns") for r in jl(os.path.join(OUT, "organizing_end-A1.jsonl"))}
    agree = sum(1 for s, n in a1_end.items() if per_room_turns.get(s, 0) == n)
    rooms = sorted({c["sub"] for c in codes})
    out_rooms, unreached_t3, unplaced = {}, collections.Counter(), []
    th_n = th_r = th_rc = full = full_c = 0
    for s in rooms:
        ts = sorted(coord.get(s, set()))
        if not ts:
            continue
        reached = [t for t in ts if set(placed.get((s, t)) or []) & standing]
        reached_c = [t for t in ts if set(placed.get((s, t)) or []) & with_cand]
        miss = [t for t in ts if t not in reached]
        for t in miss:
            p = placed.get((s, t)) or []
            if not p:
                unplaced.append("%s/%s" % (s, t))
            for x in p:
                unreached_t3[x] += 1
        th_n += len(ts)
        th_r += len(reached)
        th_rc += len(reached_c)
        full += not miss
        full_c += len(reached_c) == len(ts)
        out_rooms[s] = {"themes_with_turn": len(ts), "reached": len(reached), "unreached": miss}
    print(json.dumps({
        "rule": __doc__.split("Declared before the run (E1a), ")[1].strip(),
        "element_status": dict(status_seen),
        "check_against_A1": {"rooms_in_organizing_end": len(a1_end), "rooms_whose_turn_count_agrees": agree,
                             "turns_now": sum(per_room_turns.values()), "turns_A1": sum(v or 0 for v in a1_end.values())},
        "rooms": len(rooms), "rooms_with_a_coordinating_turn": len(out_rooms),
        "rooms_without": sorted(set(rooms) - set(out_rooms)),
        "themes_with_a_coordinating_turn": th_n,
        "reached_by_a_standing_element": th_r, "share": round(th_r / th_n, 4) if th_n else None,
        "reached_with_candidates": th_rc, "share_with_candidates": round(th_rc / th_n, 4) if th_n else None,
        "rooms_reached_in_full": full, "rooms_reached_in_full_with_candidates": full_c,
        "unreached_themes_unplaced": len(unplaced), "unreached_themes_unplaced_list": unplaced,
        "unreached_by_third_order_theme": unreached_t3.most_common(),
        "third_order_reached_by_standing_elements": len(standing), "third_order_in_scheme": len(fourth and set().union(*fourth.values())),
        "by_room": out_rooms}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
