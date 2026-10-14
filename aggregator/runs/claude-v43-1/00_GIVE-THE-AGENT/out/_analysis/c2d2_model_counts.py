#!/usr/bin/env python3
"""C2d-02: the model's counts for the close (notes-C2.md pass 5, handback-C2.md, the final message): elements by kind
and status, arrows by kind, strength, grounding, in_model, theorised, bound, beaten base rate and negative check, and the
history events by leg. Reads model/*.jsonl only; writes nothing.

    python3 out/_analysis/c2d2_model_counts.py
"""
import collections, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, "model", p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


els, arrows, hist = jl("elements.jsonl"), jl("arrows.jsonl"), jl("history.jsonl")
print("elements: %d" % len(els))
print("  by kind: %s" % dict(collections.Counter(e["kind"] for e in els)))
print("  by status: %s" % dict(collections.Counter(e.get("status") for e in els)))
stand = [e for e in els if e.get("status") not in ("candidate", "withdrawn")]
print("  standing by kind: %s" % dict(collections.Counter(e["kind"] for e in stand)))
print("  not standing: %s" % ", ".join("%s (%s)" % (e["id"], e.get("status")) for e in els if e not in stand))
print("arrows: %d" % len(arrows))
fields = ("kind", "strength", "grounding", "in_model", "status", "base_rate_beaten", "negative_check",
          "mechanism_failure_present")
for k in fields:
    print("  by %s: %s" % (k, dict(collections.Counter(str(a.get(k)) for a in arrows))))
theo = [a["id"] for a in arrows if a.get("theorised") or "theor" in str(a.get("grounding", "")) or "theor" in str(a.get("status", ""))]
print("  theorised (by field): %s" % ", ".join(theo))
print("  bounded: %s" % ", ".join(a["id"] for a in arrows if a.get("bound")))
print("  thin: %s" % ", ".join(a["id"] for a in arrows if a.get("strength") == "thin"))
print("  with support quotes: %d; with support transitions: %d" % (
    sum(1 for a in arrows if a.get("support")), sum(1 for a in arrows if a.get("support_transition"))))
print("history lines: %d" % len(hist))
print("  by leg: %s" % dict(collections.Counter(h.get("leg") for h in hist)))
print("  events: %s" % dict(collections.Counter(h.get("event") for h in hist)))
