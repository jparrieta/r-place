#!/usr/bin/env python3
"""B2b-r3-p3, the freeze leg: confirm the gate pairs on edited themes (out/_analysis/b2_pairs_list_rest.json, 450), each
read whole in out/_analysis/b2_pairs_read_first.txt (449) and again, for the pairs the second freeze edits touched,
by b2_pairs_new.py (12). Each reason says what decides the pair:
  SAME  the one question, the same in both gates, quoted;
  DIFF  the two wordings, quoted, which send the same material the same way;
  NONE  the decide_when_both or is_not clause that settles the pair, quoted, the other gate naming nothing against it.
OWN below gives the pairs the freeze edits changed their own reason. Skips pairs already confirmed against the
current sentences. Dry run unless --write; --max N slices the calls (mem.py gates --confirm, one per pair)."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib

OWN = {
 ("T3-002", "T3-033"): ("the freeze's one measure for the cluster: both gates count the concepts of an offer against a "
                        "call, the opening post not leading because it comes first, with the same tie rule in all three "
                        "decide_when_both; T3-033's must_not_show and is_not keep calls to a chosen mark at T3-002; they agree"),
 ("T3-002", "T3-038"): ("the freeze's one measure for the cluster: both gates count the concepts of the build and its "
                        "reports against the calls, an opening call not leading; T3-038's must_not_show of calls is read "
                        "under that count (the smaller side under rule 0); they agree"),
 ("T3-033", "T3-038"): ("the freeze's one measure for the cluster: both gates count the concepts of an offer against the "
                        "build and its reports, a proposal not leading because it comes first; ties to T3-038 when the work "
                        "was placed; they agree"),
 ("T3-038", "T3-070"): ("the question reworded at the freeze in both gates: work in progress and where it stands is T3-038, "
                        "directions for placers T3-070, a link only showing the finished work T3-026; T3-070's decide_when_both "
                        "on calls with coordinates does not touch it; they agree"),
 ("T3-026", "T3-038"): ("read at the freeze with the reworded T3-038/T3-070 question: T3-026 keeps the mark announced as up "
                        "and others pointed to where it is, T3-038 the progress; the same question in both gates decides; they agree"),
 ("T3-009", "T3-072"): ("fixed at the freeze: T3-072's decide_when_both now counts the allies against the celebrating, as "
                        "T3-009's does (the side with more concepts primary); the same question in both gates decides the "
                        "kind; they agree"),
 ("T3-009", "T3-157"): ("fixed at the freeze: T3-157's decide_when_both now counts the reflection against the celebrating, "
                        "as T3-009's does; T3-157's is_not keeps a bare 'we did it' with the final image at T3-009; they agree"),
}


def clip(s, n=260):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 3].rsplit(" ", 1)[0] + "..."


def reason(rows, a, b, kind):
    if (a, b) in OWN:
        return "B2b-r3-p3, at the freeze: " + OWN[(a, b)]
    qa = [q for v, q in vlib.discriminators(rows[a]) if v == b]
    qb = [q for v, q in vlib.discriminators(rows[b]) if v == a]
    if kind == "SAME":
        return ("B2b-r3-p3, read at the freeze: the one question in both gates decides it ('%s'); the clauses naming "
                "the other agree with it" % clip(qa[0]))
    if kind == "DIFF":
        return ("B2b-r3-p3, read at the freeze: %s asks '%s' and %s asks '%s'; both send the same material the same way, "
                "and the clauses naming the other agree" % (a, clip(qa[0], 180), b, clip(qb[0], 180)))
    for x, y in ((a, b), (b, a)):
        for f in ("decide_when_both", "is_not"):
            cs = vlib._clauses(rows[x].get(f), y)
            if cs:
                return ("B2b-r3-p3, read at the freeze: no question either way; %s's %s settles it ('%s') and %s names "
                        "nothing against it" % (x, f, clip(cs[0]), y))
    return None


def main():
    rows, _ = vlib.gate_scheme(OUT)
    conf = vlib.gate_confirmations(OUT, rows)
    todo, bad = [], []
    for _, a, b, kind, _ in json.load(open(os.path.join(OUT, "_analysis", "b2_pairs_list_rest.json"), encoding="utf-8")):
        if conf.get(frozenset((a, b)), ("none",))[0] == "confirmed":
            continue
        r = reason(rows, a, b, kind)
        (todo if r else bad).append((a, b, r))
    print("to confirm %d; without a reason %d %s" % (len(todo), len(bad), [x[:2] for x in bad]))
    if todo:
        print("%s|%s: %s" % todo[0])
    if bad or "--write" not in sys.argv:
        return
    if "--max" in sys.argv:
        todo = todo[:int(sys.argv[sys.argv.index("--max") + 1])]
    fail = 0
    for a, b, r in todo:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "gates", a, b, "--confirm",
                            "--reason", r, "--stage", "B2"], capture_output=True, text=True)
        if p.returncode != 0:
            fail += 1
            print("FAILED %s|%s: %s" % (a, b, (p.stdout + p.stderr).strip()[-300:]))
    print("confirmed %d, failed %d" % (len(todo) - fail, fail))


if __name__ == "__main__":
    main()
