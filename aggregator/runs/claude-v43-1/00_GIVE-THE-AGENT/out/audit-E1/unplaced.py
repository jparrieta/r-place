#!/usr/bin/env python3
"""E1 section 1, the unplaced, counted here and read in the audit section.

    python3 out/audit-E1/unplaced.py > out/audit-E1/unplaced.json

Declared before the run (E1a):
  - second-order themes with no placement: no third-order theme in mem.py's overlay (assignments_final.jsonl), with
    their room, label and size, and whether unplaced-B1.jsonl lists them;
  - concepts unreachable from any theme in rooms above concept_reach_threshold (0, notes-A1.md, so every room): a
    concept with no theme_id, or whose theme is not in themes.jsonl, or whose theme has no placement;
  - third-order themes no fourth-order theme took (the scheme in use, against fourth/fourth.jsonl members), with
    their name, tier and how many themes are placed in them;
  - fourth-order themes no dimension gathered (fourth.jsonl against dimensions.jsonl members).
"""
import collections, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import mem  # noqa: E402


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def main():
    st = mem.Store(ROOT, OUT)
    ov = st.overlay()
    placed = ov["placed"]
    themes = st.rows("themes")
    codes = st.rows("codes")
    tkey = {(t["sub"], t["theme_id"]): t for t in themes}
    b1 = {(r.get("sub"), r.get("theme_id") or r.get("theme")) for r in jl(os.path.join(OUT, "unplaced-B1.jsonl"))}
    unpl = [{"theme": "%s/%s" % k, "label": t.get("second_order"), "n_codes": t.get("n_codes"), "in_unplaced_B1": k in b1}
            for k, t in sorted(tkey.items()) if not (placed.get(k) or [])]
    no_theme = sum(1 for c in codes if not c.get("theme_id"))
    no_theme_row = sum(1 for c in codes if c.get("theme_id") and (c["sub"], c["theme_id"]) not in tkey)
    via_unplaced = sum(1 for c in codes if (c["sub"], c.get("theme_id")) in tkey and not (placed.get((c["sub"], c["theme_id"])) or []))
    fourth = jl(os.path.join(OUT, "fourth", "fourth.jsonl"))
    took = set().union(*[set(r.get("members") or []) for r in fourth]) if fourth else set()
    scheme = ov["scheme"]
    use = collections.Counter(x for v in placed.values() for x in (v or []))
    t3_out = [{"id": k, "name": v.get("name") or v.get("label"), "tier": v.get("tier"), "themes_placed": use.get(k, 0)}
              for k, v in sorted(scheme.items()) if k not in took]
    placed_ids_not_in_scheme = sorted(k for k in use if k not in scheme)
    dims = jl(os.path.join(OUT, "dimensions.jsonl"))
    gathered = set().union(*[set(r.get("members") or []) for r in dims]) if dims else set()
    t4_out = [{"id": r["id"], "name": r.get("name"), "in_model": r.get("in_model")} for r in fourth if r["id"] not in gathered]
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a):")[1].strip(),
                      "scheme_file": ov.get("scheme_file"), "assign_file": ov.get("assign_file"),
                      "second_order_themes": len(themes), "unplaced_second_order": len(unpl),
                      "unplaced_listed_in_unplaced_B1": sum(1 for u in unpl if u["in_unplaced_B1"]),
                      "unplaced_B1_lines": len(b1),
                      "concepts": len(codes), "concepts_without_theme": no_theme, "concepts_theme_missing": no_theme_row,
                      "concepts_under_unplaced_themes": via_unplaced,
                      "third_order_in_scheme": len(scheme), "third_order_no_fourth_took": len(t3_out),
                      "placed_ids_not_in_scheme": placed_ids_not_in_scheme,
                      "fourth_order": len(fourth), "fourth_no_dimension_gathered": len(t4_out),
                      "unplaced_list": unpl, "third_order_list": t3_out, "fourth_list": t4_out}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
