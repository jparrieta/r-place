#!/usr/bin/env python3
"""E2a: what the harness's first messages added to the standard leg message, leg by leg.

    python3 out/_analysis/e2_first_messages.py > out/_analysis/e2_first_messages.txt

Each file in handling/harness-log/first-messages/ is split into sentences. A sentence counts as standard when it is
one of the leg message's fixed sentences (the stage and leg named, continuing the conversation, orienting, the
reads, doing the work, closing, stopping), matched after the stage and leg names are replaced. Every other
sentence is printed with its leg, so that the additions (the dispatch's notes, the handler's lines) can be read.
The script also prints how many first messages carry no addition.
"""
import collections, glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
D = os.path.join(ROOT, "handling", "harness-log", "first-messages")
STANDARD = (r"^Stage \S+, leg \S+\.$", r"^This leg continues the last close's conversation",
            r"^Orient before you write", r"^Do this leg's work as the stage file says", r"^Then stop\.$",
            r"^This is the run's first leg", r"^Read AGENT\.md")


def sentences(t):
    t = re.sub(r"\s+", " ", t).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`(])", t) if s.strip()]


def key(name):
    stage, leg = os.path.basename(name)[:-4].split(".", 1)
    return name


def main():
    plain, extra = 0, collections.OrderedDict()
    for p in sorted(glob.glob(os.path.join(D, "*.txt")), key=os.path.getmtime):
        leg = os.path.basename(p)[:-4]
        add = [s for s in sentences(open(p, encoding="utf-8").read())
               if not any(re.search(rx, s) for rx in STANDARD)]
        if add:
            extra[leg] = add
        else:
            plain += 1
    print("first messages with no addition: %d; with additions: %d\n" % (plain, len(extra)))
    seen = collections.Counter(s for v in extra.values() for s in v)
    for leg, add in extra.items():
        print("%s: %s" % (leg, " | ".join(s if seen[s] == 1 else s + " [x%d]" % seen[s] for s in add)))


if __name__ == "__main__":
    main()
