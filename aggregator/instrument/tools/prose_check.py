#!/usr/bin/env python3
"""prose_check.py FILE [FILE ...]: the watch words of WRITING.md, with their lines. It decides nothing
and exits 0; what to fix is the writer's judgment. Text inside double quotation marks is skipped, since
a quote is the participants' and is never edited.
    python3 tools/prose_check.py out/account.md out/notes-C5.md
"""
import re, sys

WATCH = {
    "inflated significance": r"\b(stands as|serves as a testament|a testament to|pivotal|crucial|vital|underscor\w*|highlight\w*|reflects broader|enduring|landscape|tapestry|vibrant|robust|intricate|intricacies|foster\w*|showcas\w*|garner\w*|valuable insights?|setting the stage)\b",
    "trailing analysis": r",\s*(highlighting|ensuring|reflecting|contributing to|emphasizing|emphasising|symbolizing|symbolising|cultivating|encompassing|enhancing)\b",
    "vague attribution": r"\b(observers|experts|some critics|many (?:argue|believe|have noted)|several (?:sources|studies|scholars)|various|widely (?:seen|regarded|considered)|it is (?:widely|generally) (?:accepted|believed))\b",
    "editorial aside": r"\b(it is (?:important|worth|crucial|critical) to (?:note|remember|consider)|worth noting|notably|significantly|arguably|interestingly)\b",
    "negative parallelism": r"\b(not (?:only|just|merely|simply) \w+(?: \w+){0,8}[,;]? but(?: also)?|it is not about \w+)\b",
    "copula avoided": r"\b(serve[sd]? as|function(?:s|ed)? as|operat(?:es|ed) as|boast(?:s|ed)?|represent(?:s|ed) a)\b",
    "hollow closer": r"\b(in summary|in conclusion|overall,|challenges and (?:future )?prospects|despite (?:its|these|this) \w+(?: \w+){0,4}, (?:it|they) faces?)\b",
    "chat remnant": r"\b(certainly!?|i hope this helps|would you like|let me know|as an ai|as of my last (?:update|training)|here is a (?:detailed )?breakdown)\b",
    "stacked hedge": r"\b(may possibly|might perhaps|could potentially|possibly suggest|seems? to (?:possibly|perhaps))\b",
    "dash": r"[—–]",
    "curly quote": r"[“”‘’]",
    "emoji": r"[\U0001F300-\U0001FAFF☀-➿]",
    "contraction": r"\b(?:don|doesn|didn|isn|aren|wasn|weren|can|couldn|won|wouldn|shouldn|hasn|haven|hadn|it|that|there|they|we|you|i)'(?:t|s|re|ve|ll|d|m)\b",
}
QUOTED = re.compile(r'"[^"\n]*"')


def main(paths):
    total = 0
    for path in paths:
        try:
            lines = open(path, encoding="utf-8").read().splitlines()
        except OSError as e:
            print("%s: %s" % (path, e)); continue
        hits = []
        for n, line in enumerate(lines, 1):
            bare = QUOTED.sub('""', line)
            for kind, pat in WATCH.items():
                for m in re.finditer(pat, bare, re.I):
                    if kind == "contraction" and m.group(0).lower() == "let's":
                        continue
                    hits.append((n, kind, m.group(0)))
        total += len(hits)
        print("%s: %d" % (path, len(hits)))
        for n, kind, word in hits:
            print("  %5d  %-22s %s" % (n, kind, word.strip()))
    print("%d watch-word hits; this decides nothing (WRITING.md, rule 6)" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) if len(sys.argv) > 1 else print(__doc__))
