"""Stage A1 section 5: the coordinating-turn rule applied to every first-order concept, and organizing_end-A1.jsonl.

python3 out/_analysis/a1_ends.py <allcodes.jsonl> <note_ends.tsv> [--write]
Input: the dump written by out/_analysis/a1_codes_dump.py (every concept of the analysed set, read through mem.py),
and a table of each note's `ended:` line (sub, hour, concept id) for the reconciliation.
Prints the counts and the agreement with the notes. With --write, writes out/organizing_end-A1.jsonl and
out/_analysis/organizing_end-reconcile-A1.tsv.

The rule (coordinating-rule-A1.md states it in prose). The coder's first-order label opens with the act the turn
performs. A concept is a coordinating turn when that act moves the shared work:
  - a directive or building verb (STRONG: proposing, rallying, directing, warning, starting, placing, fixing,
    defending, moving, negotiating, promising ...), or "calling" followed by for/to/on or a group to act; or
  - any other verb whose label names a directive object (DIRECTIVE: help, coordinates, permission, a truce,
    an alliance, a deal, a border, a move, defence, repair, a template, a script, a Discord, an attack); or
  - before hour 73, a report of placement (reporting, announcing, warning, posting, showing that work is done,
    started, under attack or overrun).
Never: a label opening with a verb of recounting, joking, mourning, praising, explaining, blaming or wondering
(NONCOORD); a moderator removing or stickying a post; a label about April Fools, a joke, the sidebar or a
next-year rematch with no directive object.
Concepts after hour 73 are judged by the same rule.
work_remained: the room's last label (latest hour) that says its work survived (KEPT) or did not (LOST);
silent when no label says either.
"""
import collections, json, re, sys

STRONG = set("""proposing urging rallying recruiting inviting requesting petitioning ordering organizing organising
coordinating directing redirecting warning starting placing building fixing repairing rebuilding restoring protecting
maintaining guarding moving relocating expanding extending shifting negotiating promising pledging volunteering
joining helping relaying cleaning stopping abandoning dropping scrapping switching seeking demanding attacking
retaliating raiding overwriting covering securing consolidating drawing outlining filling supplying reclaiming
retaking whitening whitewashing recoloring recolouring redrawing redesigning resizing shrinking enlarging aligning
bordering surrounding crossing ceding yielding permitting authorising authorizing banning forbidding enlisting
mobilizing mobilising summoning gathering regrouping finishing completing contributing trading dividing assigning
scheduling choosing deciding planning prioritising prioritizing designating staking allying merging
accepting rejecting refusing agreeing declining conceding offering""".split())
NONCOORD = set("""joking recounting mourning celebrating thanking praising laughing mocking remembering admiring marvelling
marveling lamenting congratulating crediting cheering complaining wondering wishing hoping loving liking feeling
enjoying regretting reacting teasing taunting cursing condemning questioning explaining describing comparing
contrasting noticing spotting finding recognising recognizing identifying admitting greeting saluting hailing
chanting rating judging imagining pretending baiting revealing playing reminiscing doubting worrying fearing
expecting predicting mistaking confusing guessing suspecting realizing realising discovering wanting preferring
voicing ridiculing insulting swearing apologizing apologising forgiving consoling reassuring appreciating quoting
reposting crossposting summarizing summarising retelling reflecting musing blaming accusing summing reframing
recasting welcoming attributing""".split())
CALL = re.compile(r"^calling (for|to|on|in|out to|everyone|everybody|people|all|the room to|the sub to|members|helpers|fans|"
                  r"users|redditors|brothers|comrades|others|friends|the boys|lads|attention|\w+ (fans|members|users) to|"
                  r"\w+ to (help|build|defend|join|fix|make|stop|move|attack|protect|repair|rebuild|draw|write|finish|hold))\b",
                  re.I)
MOD_ROUTE = re.compile(r"^(re)?directing\b.*\b(post|posts|discussion|thread|material|update|talk|questions?)\b.*\b(to|into)\b"
                       r".*\b(megathread|thread|subreddit|r/\w+|sticky)", re.I)
CANVAS = re.compile(r"\b(place|canvas|pixels?|pxls|placetwo|logo|flag|build\w*|rebuild\w*|draw\w*|template|design|sign|"
                    r"banner|crest|heart|road|art|tiles?|image|spot|space|corner|border)\b", re.I)
DIRECTIVE = re.compile(r"\b(help|helping|helpers?|coordinat\w*|coords?|coordinates?|permission|truce|allian\w*|ally|allies|"
                       r"pact|treaty|ceasefire|deal|agreement|compromise|border\w*|boundar\w*|move|moving|relocat\w*|defen[cs]\w*|"
                       r"defend\w*|protect\w*|repair\w*|rebuild\w*|fix\w*|maintain\w*|build\w*|place (a|the|pixels?|tiles?)|"
                       r"placing|template|blueprint|scripts?|bots?|discord|grid|attack\w*|raid\w*|invad\w*|invasion|expan\w*|"
                       r"overwrit\w*|stop|leave|join\w*|reinforc\w*|backup|back up|take over|taking over|territor\w*|plan)\b", re.I)
REPORT = re.compile(r"\b(done|finished|underway|complet\w*|started|progress|under attack|being (destroyed|attacked|vandali\w*|"
                    r"overrun|griefed)|taken over|overrun)\b", re.I)
OFF_CANVAS = re.compile(r"\b(april fools?|joke|prank|meme|bait|shitpost|sidebar|flair|css|stylesheet|subreddit style|"
                        r"theme song|game thread|fake|match|season|trailer|episode|recipe|next year|next time|rematch)\b", re.I)
MOD_POST = re.compile(r"^(removing|deleting|locking|stickying|unstickying)\b.*\b(post|thread|submission|comment)", re.I)
KEPT = re.compile(r"\b(surviv\w*|intact|made it|still there|still up|stayed(?! (funny|up|awake))|"
                  r"remain(s|ed)? (intact|up|there|on|standing|whole)|immortali[sz]\w*|final (canvas|image|picture|"
                  r"print|version|cut)|preserved|we did it|did it|held|holding strong|kept|completed|finished|too (good|strong|big) to|"
                  r"near-\w+|withst\w*)\b", re.I)
EVENT_END = re.compile(r"\b(r/)?place (is|was) (finished|over)|place ended|after placement ended\b", re.I)
RECOVER = re.compile(r"\b(coming back|came back|restored|rebuilt|back up|returned|regained|recovered|reclaimed|repaired)\b",
                     re.I)
UNSURE = re.compile(r"\b(unsure|whether|if|wondering|hoping|hopes?)\b", re.I)
LOST = re.compile(r"\b(destroy\w*|gone|lost|los(e|ing) (it|the)|erased|wiped|consumed|overrun|overtaken|ruin\w*|fail\w*|"
                  r"disappear\w*|vanish\w*|taken over|too late|dead|died|killed|obliterat\w*|didn'?t make it|"
                  r"never (made|finished|completed))\b", re.I)


def verb(label):
    w = (label or "").strip().split()
    return w[0].lower().strip(",.:;") if w else ""


CALLERS = set("""proposing urging rallying recruiting inviting requesting petitioning organizing organising
coordinating directing redirecting starting planning""".split())
ARGUE = re.compile(r"^defending (the |their |his |her |its )?[\w'-]+( [\w'-]+)? (as|by|because)\b|"
                   r"^defending (bot|script|use|choice|decision|respect|price|claim|idea|joke)", re.I)


def coordinating(c):
    lab = c.get("first_order") or ""
    v = verb(lab)
    h = c.get("hour") if isinstance(c.get("hour"), (int, float)) else 0
    if MOD_POST.search(lab) or MOD_ROUTE.search(lab) or v in NONCOORD or ARGUE.search(lab):
        return False
    off = bool(OFF_CANVAS.search(lab))
    if h > 73:
        # after the canvas closed a turn coordinates only as a call, an invitation or a plan for canvas work
        if not CANVAS.search(lab) or off:
            return False
        if v == "calling":
            return bool(CALL.search(lab))
        return v in CALLERS
    if v == "calling":
        return bool(CALL.search(lab)) and not off
    if v in STRONG:
        return not off
    if DIRECTIVE.search(lab):
        return not off
    if v in ("reporting", "announcing", "warning", "posting", "showing") and h <= 73 and REPORT.search(lab):
        return not off
    return False


TELLERS = set("""reporting declaring saying mourning lamenting celebrating noting announcing confirming presenting
marvelling marveling thanking claiming posting showing conceding admitting sharing loving qualifying apologizing
apologising accepting recounting observing stating lamenting grieving cheering rejoicing boasting bragging
congratulating regretting acknowledging finding noticing pointing remarking""".split())
HYPOTHETICAL = re.compile(r"\b(could|would|will|might|may|should|not to|threat\w*|if|able to|want\w*|denying|obliterating|"
                          r"destroying|erasing|wiping)\b", re.I)
FOILED = re.compile(r"\bfail\w* to (remove|destroy|erase|take|wipe|kill|overwrite|cover)\b", re.I)


def remained(c):
    lab = c.get("first_order") or ""
    v = verb(lab)
    if v not in TELLERS or UNSURE.search(lab) or HYPOTHETICAL.search(lab) or re.search(r"\b(grief\w*|joke)\b", lab, re.I):
        return None
    if FOILED.search(lab):
        return "kept"
    k, l = bool(KEPT.search(EVENT_END.sub("", lab))), bool(LOST.search(lab))
    if RECOVER.search(lab) and (k or l):
        return "kept"
    if v in ("mourning", "lamenting") and (k or l):
        return "lost"
    if l and not k:
        return "lost"
    if k and not l:
        return "kept"
    if k and l:
        return "kept" if re.search(r"\b(surviv\w*|intact|made it|remain\w*|still there|too (good|strong|big) to|near-\w+|withst\w*)\b", lab, re.I) else "lost"
    return None


def main():
    src, notes_path, write = sys.argv[1], sys.argv[2], "--write" in sys.argv
    rooms = collections.defaultdict(list)
    for line in open(src, encoding="utf-8"):
        c = json.loads(line)
        rooms[c["sub"]].append(c)
    order = [l.rstrip("\n").split("\t")[1] for l in open("out/order-A1.txt", encoding="utf-8") if "\t" in l]
    notes = {}
    for l in open(notes_path, encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        notes[p[0]] = (p[1] if len(p) > 1 else "", p[2] if len(p) > 2 else "")
    lines, rec, ncoord, nall, agree, near = [], [], 0, 0, 0, 0
    for s in order:
        cs = sorted(rooms.get(s, []), key=lambda c: (c["hour"] if isinstance(c.get("hour"), (int, float)) else -1e9,
                                                      c["code_id"]))
        co = [c for c in cs if coordinating(c)]
        nall += len(cs)
        ncoord += len(co)
        last = co[-1] if co else None
        after_items = {c.get("item_id") or c["code_id"] for c in cs
                       if isinstance(c.get("hour"), (int, float)) and c["hour"] > 73}
        ac = [c for c in co if isinstance(c.get("hour"), (int, float)) and c["hour"] > 73]
        ac_items = {c.get("item_id") or c["code_id"] for c in ac}
        share = round(len(ac_items) / len(after_items), 3) if after_items else None
        wr, wc = "silent", []
        for c in reversed(cs):
            r = remained(c)
            if r:
                wr, wc = r, [c["code_id"]]
                break
        lines.append({"sub": s, "organizing_end_hour": last["hour"] if last else None, "aftermath_share": share,
                      "coordinating_turns": len(co), "turns_after_73": len(after_items), "work_remained": wr,
                      "work_remained_codes": wc, "last_coordinating_code": last["code_id"] if last else None,
                      "aftermath_coordinating_codes": [c["code_id"] for c in ac]})
        nh, nc = notes.get(s, ("", ""))
        sh = last["hour"] if last else None
        same = (nc == (last["code_id"] if last else "")) or (not nc and not last)
        close = False
        if nh and sh is not None:
            try:
                close = abs(float(nh) - sh) <= 1.0
            except ValueError:
                pass
        agree += same
        near += (close and not same)
        rec.append("\t".join([s, nh or "none", nc or "none", "%s" % (sh if sh is not None else "none"),
                              last["code_id"] if last else "none",
                              "same" if same else ("within 1h" if close else "differs")]))
    print("concepts %d, coordinating %d (%.3f)" % (nall, ncoord, ncoord / nall))
    print("rooms %d; note's last coordinating code the same %d; different code within one hour %d; differs %d"
          % (len(order), agree, near, len(order) - agree - near))
    print("work_remained", dict(collections.Counter(l["work_remained"] for l in lines)))
    print("organizing_end_hour > 73:", sum(1 for l in lines if (l["organizing_end_hour"] or 0) > 73))
    print("no coordinating turn:", [l["sub"] for l in lines if l["last_coordinating_code"] is None])
    if write:
        with open("out/organizing_end-A1.jsonl", "w", encoding="utf-8") as f:
            for l in lines:
                f.write(json.dumps(l) + "\n")
        with open("out/_analysis/organizing_end-reconcile-A1.tsv", "w", encoding="utf-8") as f:
            f.write("sub\tnote_hour\tnote_code\trule_hour\trule_code\tverdict\n")
            f.write("\n".join(rec) + "\n")
        print("written")


if __name__ == "__main__":
    main()
