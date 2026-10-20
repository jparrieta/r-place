#!/usr/bin/env python3
"""D3a-38: G43 reading 4's check, version 4. Version 3 found the answer by any ' answer' in the reason, so a quote
('Short answer', cardinals-013) could stand in for it; and it passed a line on a link through the submission or one
author even where that concept is the earlier layout, not the talk (drugs-010, raocow-041). This version finds the
answer by 'answered by cNNNN', else by the last code before ') answer' (an hour's closing bracket), else the cited
concept latest in hour; and it names the kind of every link: reply (the answer's item under a talk item, or the
same item), member (one author), submission (a talk item is the submission). Lines with no reply link are listed
with the links they have, for a reading in the forest; a submission or member link passes only if the linked
concept is talk. Writes nothing.

  python3 out/_analysis/d3_a11_reply_check4.py
"""
import re

src = open("out/_analysis/d3_a11_reply_check3.py", encoding="utf-8").read().split("flag, how = ")[0]
ns = {}
exec(compile(src, "d3_a11_reply_check3.py", "exec"), ns)
text, pos, tree, CODE = ns["text"], ns["pos"], ns["tree"], ns["CODE"]


def answer_of(ev, cited, room):
    m = re.search(r"answered by (c\d{4})", ev)
    if m:
        return m.group(1), "words"
    m = re.search(r"\) answers?\b", ev)
    if m:
        before = CODE.findall(ev[:m.start()])
        if before:
            return before[-1], "words"
    hs = [(pos[(room, c)][1], c) for c in cited if (room, c) in pos]
    return (max(hs)[1], "latest") if hs else (None, "none")


rows, how = [], {"words": 0, "latest": 0, "none": 0}
for aid in sorted(text):
    room = aid.rsplit("-", 1)[0]
    cited = sorted(set(CODE.findall(text[aid])))
    ans, src_ = answer_of(text[aid], cited, room)
    how[src_] += 1
    if ans is None or (room, ans) not in pos:
        rows.append((aid, "answer not placed", ""))
        continue
    ta, ha = pos[(room, ans)]
    t = tree(room, ta)
    if ans not in t:
        rows.append((aid, "answer not in its forest", ""))
        continue
    da, ua = t[ans]
    links = []
    for c in cited:
        if c == ans or (room, c) not in pos or pos[(room, c)][0] != ta or pos[(room, c)][1] > ha or c not in t:
            continue
        dc, uc = t[c]
        if da == dc or da.startswith(dc + "."):
            links.append(("reply", c, dc))
        elif dc == "0":
            links.append(("submission", c, dc))
        elif ua == uc:
            links.append(("member", c, dc))
    kinds = {k for k, _, _ in links}
    if "reply" not in kinds:
        rows.append((aid, "no reply link; answer %s@%s" % (ans, da),
                     " ".join("%s:%s@%s" % lk for lk in links) or "no link"))
print("transition lines: %d; answer found by words %d, by latest hour %d, none %d; without a reply link: %d" % (
    len(text), how["words"], how["latest"], how["none"], len(rows)))
for aid, why, links in rows:
    print("  %s %s; %s" % (aid, why, links))
