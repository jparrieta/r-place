#!/usr/bin/env python3
"""steps.py: the stages, their steps and the leg ids, from steps.tsv beside this file.

A leg id is the stage, the step letter, and a count where the step repeats:

    B1a            a step taken once
    B1b-03         the third leg of a step that repeats (two digits)
    B2a-r1         a pilot round (build or check round K)
    D1a, D1a-02    a step that may be split into batches
    B1c-p2         any leg continued after a pause: -p2, -p3 ... at the end

    python3 tools/steps.py check <leg> [--stage NN]   one line: stage kind interview label, or exit 1
    python3 tools/steps.py stages                     stage ids in order
    python3 tools/steps.py steps <stage>              the stage's steps, one per line
    python3 tools/steps.py label <leg>                the file label: B1b-03_coding-third-order-scheme_getting-lost
    python3 tools/steps.py name <stage>               the stage name
    python3 tools/steps.py first <stage> <kind>       the first step of that kind (for dispatch's "next")
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEG = re.compile(r"^([A-E][1-6])([a-e])(?:-(\d{2}|r\d+))?(?:-p(\d+))?$")


def table(path=None):
    p = path or os.path.join(HERE, "steps.tsv")
    rows = []
    with open(p, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        for l in f:
            if l.strip():
                rows.append(dict(zip(head, l.rstrip("\n").split("\t"))))
    return rows


def stages(rows=None):
    out = []
    for r in rows or table():
        if r["stage"] not in out:
            out.append(r["stage"])
    return out


def norm_stage(x, rows=None):
    x = (x or "").strip().upper()
    return x if x in stages(rows) else None


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def parse(leg, rows=None):
    """The leg's stage, step and kind, or a ValueError saying what is wrong."""
    rows = rows or table()
    m = LEG.match(leg or "")
    if not m:
        raise ValueError("a leg id is the stage, the step letter and, where the step repeats, a count "
                         "(A1a, B1b-03, B2a-r1; a leg after a pause adds -p2); got %r" % leg)
    st, step, n, cont = m.groups()
    r = next((r for r in rows if r["stage"] == st and r["step"] == step), None)
    if r is None:
        have = ", ".join(x["stage"] + x["step"] for x in rows if x["stage"] == st) or "none"
        raise ValueError("stage %s has no step %s (its steps: %s)" % (st, step, have))
    rep = r["repeat"]
    if rep == "yes" and not (n and n.isdigit()):
        raise ValueError("%s%s repeats: give its count, e.g. %s%s-01" % (st, step, st, step))
    if rep == "round" and not (n and n.startswith("r")):
        raise ValueError("%s%s is a round: give it, e.g. %s%s-r1" % (st, step, st, step))
    if rep == "no" and n:
        raise ValueError("%s%s is taken once: no count (a leg continued after a pause is %s%s-p2)" % (st, step, st, step))
    return {"leg": leg, "stage": st, "step": step, "count": n, "cont": cont, "kind": r["kind"],
            "interview": r["interview"], "stage_name": r["stage_name"], "step_name": r["step_name"],
            "round": n[1:] if n and n.startswith("r") else None}


def label(leg, rows=None):
    p = parse(leg, rows)
    return "%s_%s_%s" % (leg, slug(p["stage_name"]), slug(p["step_name"]))


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    rows = table()
    cmd = argv[0]
    try:
        if cmd == "check":
            p = parse(argv[1], rows)
            if "--stage" in argv:
                want = norm_stage(argv[argv.index("--stage") + 1], rows)
                if want != p["stage"]:
                    raise ValueError("leg %s belongs to stage %s, not %s" % (argv[1], p["stage"], want))
            print("%s\t%s\t%s\t%s\t%s" % (p["stage"], p["kind"], p["interview"], p["round"] or "-", label(argv[1], rows)))
        elif cmd == "stages":
            print("\n".join(stages(rows)))
        elif cmd == "steps":
            st = norm_stage(argv[1], rows)
            if not st:
                raise ValueError("no stage %s" % argv[1])
            for r in rows:
                if r["stage"] == st:
                    print("%s%s\t%s\t%s\t%s\t%s" % (st, r["step"], r["step_name"], r["kind"], r["repeat"], r["interview"]))
        elif cmd == "label":
            print(label(argv[1], rows))
        elif cmd == "name":
            st = norm_stage(argv[1], rows)
            if not st:
                raise ValueError("no stage %s" % argv[1])
            print(next(r["stage_name"] for r in rows if r["stage"] == st))
        elif cmd == "first":
            st = norm_stage(argv[1], rows)
            r = next((r for r in rows if r["stage"] == st and r["kind"] == argv[2]), None)
            if not r:
                raise ValueError("stage %s has no %s step" % (argv[1], argv[2]))
            print(st + r["step"])
        else:
            raise ValueError("no such command: %s" % cmd)
    except (ValueError, IndexError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
