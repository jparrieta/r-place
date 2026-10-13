#!/usr/bin/env python3
"""C1, read-only: every second-order theme placed on the given third-order themes in assignments_final.jsonl, one
line each: sub/tNN, the themes it carries, and its label (second_order), whole. With --notes the theme note follows on
its own line. Prints only.

    python3 out/_analysis/c1_theme_items.py --themes T3-084,T3-011 [--notes]
"""
import argparse, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--themes", required=True); ap.add_argument("--notes", action="store_true")
    a = ap.parse_args()
    want = [t.strip() for t in a.themes.split(",") if t.strip()]
    store = bpf.pk.Store(ROOT, OUT)
    rows = [json.loads(x) for x in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if x.strip()]
    for w in want:
        hit = [r for r in rows if w in (r.get("third_order") or [])]
        print("%s: %d placements" % (w, len(hit)))
        for r in sorted(hit, key=lambda r: (r["sub"].lower(), r["theme_id"])):
            th = store.themes.get((r["sub"], r["theme_id"])) or {}
            print("  %s/%s [%s] %s" % (r["sub"], r["theme_id"], ",".join(r.get("third_order") or []), th.get("second_order")))
            if a.notes:
                print("      note: %s" % th.get("theme_note"))


if __name__ == "__main__":
    main()
