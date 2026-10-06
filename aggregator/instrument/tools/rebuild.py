#!/usr/bin/env python3
"""rebuild.py — a room's model rebuilt from the global model plus its accepted adaptations.

    python3 tools/rebuild.py <sub> [--out out] [--model out/model] [--json]

Prints the skeleton: every element of the global model at the frozen version, in dimension
order, with this room's accepted, modified or supported particular lines applied: instantiated (with the source theme
and how), absent, conditioned, extended by a step, linked, restricted, contradicted; proposed
elements the room contributed; then every arrow in the model with its ends, its mechanism and
the room's lines on it. The latest accepted return manifest selects the effective ledger,
including an empty recheck. Pending lines remain unresolved until explicitly adjudicated.
Both text and JSON retain evidence states and model-version uncertainty. This is what the stage-E1 reader receives beside the coder's blind case.md
(SCHEMA §8). Nothing here reads model-D.md.
"""
import argparse, collections, json, os, sys
from adaptation_ledger import effective_lines, effective_rooms
import vlib

def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sub")
    ap.add_argument("--out", default="out")
    ap.add_argument("--model", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    md = a.model or os.path.join(a.out, "model")
    elements = {e["id"]: e for e in jl(os.path.join(md, "elements.jsonl"))}
    arrows = jl(os.path.join(md, "arrows.jsonl"))
    dims = jl(os.path.join(a.out, "dimensions.jsonl"))
    lines = [l for l in effective_lines(a.out, include_particular=True) if l.get("sub") == a.sub]
    all_lines = [l for l in effective_lines(a.out, include_particular=True, include_pending=True)
                 if l.get("sub") == a.sub]
    return_record = effective_rooms(a.out).get(a.sub, {})
    re_lines = return_record.get("phase") == "recheck"
    by_el = collections.defaultdict(list)
    for l in lines:
        by_el[l.get("element")].append(l)
    def text(l):
        return l.get("condition") or l.get("statement") or ""
    order = []
    for d in dims:
        for e in elements.values():
            if e.get("dimension") == d["id"] and e["id"] not in order:
                order.append(e["id"])
    for e in elements:
        if e not in order:
            order.append(e)
    skel = {"sub": a.sub, "ledger": "recheck" if re_lines else "D2",
            "model_version": vlib.model_hash(a.out), "return_model_version": return_record.get("model_version"),
            "local_account": vlib.local_return_states(a.out).get(a.sub, {}),
            "unresolved_adaptations": [l for l in all_lines if l.get("decision") not in ("accept", "modify", "particular") and l.get("op") != "none"],
            "elements": []}
    for eid in order:
        e = elements[eid]
        if e.get("status") == "withdrawn":
            continue
        entry = {"id": eid, "kind": e.get("kind"), "statement": e.get("statement"),
                 "dimension": e.get("dimension"), "applies": "unstated", "ops": []}
        for l in by_el.get(eid, []):
            op = l["op"]
            entry["ops"].append({"op": op, "source": l.get("source"), "lift": l.get("lift"),
                                 "text": text(l), "how": l.get("how"), "codes": (l.get("evidence") or {}).get("codes", []),
                                 "decision": l.get("decision"), "observation": l.get("observation"),
                                 "adaptation": l.get("id"), "model_version": l.get("model_version")})
            if op == "instantiate":
                entry["applies"] = "yes"
            elif op == "absent":
                entry["applies"] = {"observed-absent": "no", "not-needed": "not-needed",
                                    "not-testable": "not-testable"}.get(l.get("observation"), "unobserved")
            elif op in ("restrict", "contradict"):
                entry["applies"] = "contested"
            elif entry["applies"] == "unstated":
                entry["applies"] = "adapted"
        if skel["local_account"].get("version_status") not in ("current", "unaffected-carry-forward") and entry["ops"]:
            entry["applies_at_return"] = entry["applies"]
            entry["applies"] = "unverified-current"
        skel["elements"].append(entry)
    skel["proposed"] = [{"statement": l.get("statement"), "source": l.get("source"), "how": l.get("how"),
                         "codes": (l.get("evidence") or {}).get("codes", [])} for l in by_el.get(None, []) if l["op"] == "propose"]
    skel["arrows"] = [{"id": x.get("id"), "from": x.get("from"), "to": x.get("to"), "kind": x.get("kind"),
                       "mechanism": x.get("mechanism"),
                       "ops": [{"op": l["op"], "source": l.get("source"), "text": text(l), "how": l.get("how"),
                                "codes": (l.get("evidence") or {}).get("codes", [])} for l in by_el.get(x.get("id"), [])]}
                      for x in arrows if x.get("in_model") and x.get("status") != "withdrawn"]
    if a.json:
        print(json.dumps(skel, ensure_ascii=False, indent=1)); return 0
    print("# r/%s rebuilt from the global model (%s) plus %d %s" % (a.sub, skel["model_version"], len(lines),
          "adjudicated re-check lines" if re_lines else "supported local adaptations"))
    local = skel["local_account"]
    print("\nAdapted-local status: %s; grade: %s; version status: %s." %
          (local.get("local_status", "unresolved"), local.get("local_grade", "unknown"),
           local.get("version_status", "stale-or-unknown")))
    print("Return model version: %s; current model version: %s." %
          (skel["return_model_version"] or "unknown", skel["model_version"] or "unknown"))
    if local.get("version_status") not in ("current", "unaffected-carry-forward"):
        print("The local return is stale or its version is unknown; its evidence below is not validation of the current model.")
    print("Unresolved adaptations: %d (not asserted support)." % len(skel["unresolved_adaptations"]))
    for pending in skel["unresolved_adaptations"]:
        print("   [%s] %s: %s %s" % (pending.get("id"), pending.get("element") or "new",
              text(pending), pending.get("how") or ""))
    for en in skel["elements"]:
        print("\n[%s] %s  (%s; applies here: %s)" % (en["id"], en["statement"], en["dimension"], en["applies"]))
        for o in en["ops"]:
            print("   %-13s %-14s %s  %s  [%s]" % (o["op"], o["source"] or "", o["text"], o["how"] or "", ",".join(o["codes"])))
    if skel["proposed"]:
        print("\nproposed by this room:")
        for p in skel["proposed"]:
            print("   %s  %s  [%s]" % (p["statement"], p["how"], ",".join(p["codes"])))
    print("\narrows in the model: %d" % len(skel["arrows"]))
    for ar in skel["arrows"]:
        print("\n[%s] %s -> %s (%s): %s" % (ar["id"], ar["from"], ar["to"], ar["kind"], ar["mechanism"] or ""))
        for o in ar["ops"]:
            print("   %-13s %-14s %s  %s  [%s]" % (o["op"], o["source"] or "", o["text"], o["how"] or "", ",".join(o["codes"])))
    return 0

if __name__ == "__main__":
    sys.exit(main())
