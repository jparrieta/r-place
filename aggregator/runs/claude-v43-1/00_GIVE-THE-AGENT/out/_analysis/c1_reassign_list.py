#!/usr/bin/env python3
"""C1: apply a reviewed list of re-placements, one `mem.py reassign` each, from a JSON object
{"<sub>:<tNN>": {"theme": "T3-a,T3-b", "codes": "T3-a=c1,c2;T3-b=c3", "reason": "..."}}. Checks first that every
code named belongs to the item and that no code is given to two themes; dry run without --write (mem.py --dry-run).
Stops at the first refusal.

    python3 out/_analysis/c1_reassign_list.py --file out/_analysis/c1_rechecks/review-pass4-moves.json [--write]
"""
import argparse, importlib.util, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--file", required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    plan = json.load(open(os.path.join(ROOT, a.file), encoding="utf-8"))
    store = bpf.pk.Store(ROOT, OUT)
    for it, d in plan.items():
        s, t = it.split(":")
        own = set(store.themes[(s, t)].get("code_ids") or [])
        seen = []
        for part in d["codes"].split(";"):
            th, cs = part.split("=")
            if th not in d["theme"].split(","):
                sys.exit("%s: codes name %s, not in --theme" % (it, th))
            for c in cs.split(","):
                if c not in own:
                    sys.exit("%s: %s is not a concept of this item" % (it, c))
                if c in seen:
                    sys.exit("%s: %s given to two themes" % (it, c))
                seen.append(c)
    for it, d in plan.items():
        cmd = [sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "reassign", it, "--theme", d["theme"],
               "--codes", d["codes"], "--reason", d["reason"]] + ([] if a.write else ["--dry-run"])
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = " ".join((r.stdout or "").split())
        if r.returncode != 0 or not (out.startswith("moved") or out.startswith("dry run")):
            sys.exit("stopped at %s: %s %s" % (it, out[:300], (r.stderr or "").strip()[-300:]))
        print(("wrote " if a.write else "checked ") + it)


if __name__ == "__main__":
    main()
