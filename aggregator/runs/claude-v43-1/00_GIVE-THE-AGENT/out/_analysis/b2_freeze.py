#!/usr/bin/env python3
"""B2b-r3-p3: freeze the scheme (stage B2 section 5; J, QB2-012). Writes, from out/scheme.jsonl and out/scheme.md as
assembled after edits 1 to 306 and with every gate pair confirmed:
  out/scheme_final.jsonl  one line per theme, every field as in scheme.jsonl; tier "rare" for the rare tier and
                          "common" for the main tier (the B2 check's word; QB2-014 asks J which word stands)
  out/scheme_final.md     scheme.md with a frozen header in place of the working one
families.jsonl stays beside them as assembled. Refuses if either frozen file exists, if any gate pair is unconfirmed
or stale, or if mem.py gates' mechanical check finds a defect. Dry run unless --write."""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib

TIER = {"main": "common", "rare": "rare"}


def main():
    for f in ("scheme_final.jsonl", "scheme_final.md"):
        if os.path.exists(os.path.join(OUT, f)):
            sys.exit("%s exists; the scheme is frozen already" % f)
    rows = [json.loads(x) for x in open(os.path.join(OUT, "scheme.jsonl"), encoding="utf-8") if x.strip()]
    grows, _ = vlib.gate_scheme(OUT)
    rep = vlib.gate_report(grows, vlib.family_ids(OUT))
    conf = vlib.gate_confirmations(OUT, grows)
    open_pairs = [sorted(p) for p in rep["pairs"] if conf.get(p, ("none",))[0] != "confirmed"]
    if rep["unresolved"] or rep["one_way"] or rep["mns_no_disc"] or open_pairs:
        sys.exit("not frozen: unresolved %d, one-way %d, must_not_show with no discriminator %d, pairs not confirmed %d"
                 % (len(rep["unresolved"]), len(rep["one_way"]), len(rep["mns_no_disc"]), len(open_pairs)))
    fin = []
    for r in rows:
        if r.get("tier") not in TIER:
            sys.exit("%s has tier %r" % (r["id"], r.get("tier")))
        fin.append(dict(r, tier=TIER[r["tier"]]))
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in fin)
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    md = open(os.path.join(OUT, "scheme.md"), encoding="utf-8").read()
    cut = md.index("How to read a theme.")
    n_rare = sum(1 for r in fin if r["tier"] == "rare")
    fams = len({r["family"] for r in fin})
    edits = sum(1 for x in open(os.path.join(OUT, "scheme_edits.jsonl"), encoding="utf-8") if x.strip())
    head = ("# The third-order scheme, frozen at stage B2\n\n"
            "Frozen at stage B2, leg B2b-r3-p3, %s (UTC). %d themes in %d families; %d are on the rare tier (seen in "
            "one room, or in rooms that tell one episode). The pilot ran three rounds; round 3's pairwise agreement "
            "on the hard set, 0.728, cleared the declared 0.70, and the rounds stopped (J, QB2-012). The sentences are "
            "those of scheme.jsonl after the %d lines of scheme_edits.jsonl; the edits made at the freeze (the "
            "T3-002, T3-033 and T3-038 cluster, T3-070's question against T3-038, T3-072 and T3-157 against T3-009) "
            "are tested only by the gold round. Every pair of themes whose gates name each other, %d, is confirmed "
            "against these sentences in gate_checks.jsonl.\n\n"
            "In scheme_final.jsonl the rare tier is marked \"tier\": \"rare\" and the main tier \"tier\": \"common\" "
            "(QB2-014). families.jsonl stands beside it. sha256 of scheme_final.jsonl: %s.\n\n"
            % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), len(fin), fams, n_rare, edits,
               len(rep["pairs"]), sha))
    print(head)
    print("themes %d (common %d, rare %d); families %d" % (len(fin), len(fin) - n_rare, n_rare, fams))
    if "--write" not in sys.argv:
        return
    open(os.path.join(OUT, "scheme_final.jsonl"), "w", encoding="utf-8").write(body)
    open(os.path.join(OUT, "scheme_final.md"), "w", encoding="utf-8").write(head + md[cut:])
    print("wrote scheme_final.jsonl and scheme_final.md")


if __name__ == "__main__":
    main()
