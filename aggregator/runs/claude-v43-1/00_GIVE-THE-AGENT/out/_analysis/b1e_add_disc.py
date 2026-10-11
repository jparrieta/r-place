#!/usr/bin/env python3
"""B1e: add owed discriminators that `b1e_disc_pairs.py` found missing from one or both gates.

Each entry appends one {vs, question} to a draft line, unless that line already has a
discriminator against the same theme. Dry run by default; --write rewrites the drafts in place.
"""
import glob, json, os, sys

AN = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out", "_analysis")

ADD = [
    ("T3-149", "T3-151", "Is a fight ended or forestalled by a pact (T3-149), or help given in return for help (T3-151)?"),
    ("T3-151", "T3-149", "Is help given in return for help (T3-151), or a fight ended or forestalled by a pact (T3-149)?"),
    ("T3-038", "T3-073", "Is the first build's progress reported (T3-038), or what happened to the work once it stood (T3-073)?"),
    ("T3-188", "T3-195", "Does an organised room say it does not control placers acting in its name (T3-188), or hold another room to an agreement (T3-195)?"),
    ("T3-195", "T3-188", "Is another room held to an agreement (T3-195), or does an organised room say it does not control placers acting in its name (T3-188)?"),
    ("T3-076", "T3-195", "Does the room stop its own attackers (T3-076), or hold another room to an agreement (T3-195)?"),
    ("T3-195", "T3-076", "Is another room held to an agreement (T3-195), or does the room stop its own attackers (T3-076)?"),
    ("T3-050", "T3-017", "Is a rival community taunted (T3-050), or the sub's ordinary talk carried on with no rival in it (T3-017)?"),
    ("T3-017", "T3-050", "Does the sub's ordinary talk go on with no rival in it (T3-017), or is a rival community taunted (T3-050)?"),
    ("T3-024", "T3-168", "Is the restraint kept by hand (T3-024), or written into a script (T3-168)?"),
]


def main():
    write = "--write" in sys.argv
    done = []
    for p in sorted(glob.glob(os.path.join(AN, "b1e_draft_G*.jsonl"))):
        with open(p, encoding="utf-8") as f:
            rows = [json.loads(x) for x in f if x.strip()]
        changed = 0
        for r in rows:
            for a, b, q in ADD:
                if r["id"] == a and b not in {d["vs"] for d in r["discriminators"]}:
                    r["discriminators"].append({"vs": b, "question": q})
                    changed += 1
                    done.append((a, b))
        if changed:
            print("%s: %d added" % (os.path.basename(p), changed))
            if write:
                with open(p, "w", encoding="utf-8") as f:
                    for r in rows:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("added %d of %d; %s" % (len(done), len(ADD), "written" if write else "dry run"))


if __name__ == "__main__":
    main()
