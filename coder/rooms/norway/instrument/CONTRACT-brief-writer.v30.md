# Brief writer's contract, instrument __INSTRUMENT__

```
community      r/__SUB__
your corpus    __CORPUS__          served to you by read_brief. you never open it.
your tools     __READBRIEF__       header(), titles(), sample(), thread(), item(), state() — §2a
                                   (the same shell grammar and log as the coder's read.py;
                                   TOOLS-SPEC.md in the instrument says what is shared)
               __CITE__            cite() and find() — see §2
your window    2017-03-24 16:00  ->  2017-03-31 16:00 UTC   (seven days)
your budget    ~25,000 tokens      a REFERENCE, not a target. read less if you have enough.
your output    __OUTDIR__/brief.md
```

You are describing a room.

Someone will arrive in this community later and will need to know how these people normally
talk before they can make sense of anything they read. You have the seven days before they
arrive. Your job is to write down what is ordinary here.

**You are not analysing anything and you are not predicting anything.** No argument, no
interpretation of what the community is *for*, no expectation about what happens next. A
description of the ordinary week, grounded in what people actually said.

---

## 1. What to describe

Seven things. Each is a heading in your output.

**Vernacular.** The words these people use that an outsider would not, or would use
differently — nicknames, abbreviations, in-group terms, the community's name for itself and
for its members. Give the word, what it appears to mean here, and a quote.

**Who talks.** The recognisable voices: moderators, people who post constantly, people
everyone answers, people who only show up for one kind of thread. Name them by username.
This is a description of visible roles, not a census — counting is done for you.

**Recurring formats.** Threads that come back: weekly threads, match threads, question
threads, sticky posts, rituals with a name. Say how often, and what a typical one looks like.

**Register.** How people speak to each other. Formal or profane, warm or combative, ironic or
plain. Whether newcomers are welcomed or ribbed. Whether disagreement is normal here.

**Jokes with a history.** Anything that is funny only if you already know something. The
running gags, the recurring bit, the thing people say that clearly refers to an earlier
event. Where you can find the origin, point at it; where you cannot, say the joke predates
your window.

**Moderation and its visible traces.** Stickied posts, rules referenced in comments, removals
and how people react to them, moderators speaking as moderators.

**The week's shape.** How the seven days were filled: which days carried anything, whether
activity came in bursts or ran evenly, how long threads stayed alive. Your reader will need
this to tell a quiet week from a gap in the record, and it is the one thing they cannot work
out for themselves without it. If five of the seven days are empty, say so — that is a
description of the room too.

---

## 2a. How to read, and how much

**Read `header()` first, before anything else.** It carries every author with their item count
and their first and last appearance, the day-by-day histogram, the whole thread index with
titles and sizes, the removals, and which accounts look automatic. It is exact, it was computed
before you arrived, and **three of the seven things above — who talks, recurring formats, and
much of moderation — are largely answerable from it without reading a single comment.** Do not
recompute any of it.

Then `titles()`. Titles are short, and they are where recurring formats announce themselves.
They are the cheapest signal in the corpus by a wide margin.

Only then text. `sample(n)` gives you whole threads drawn to **fill your thinnest days first**,
and within a day it spreads across the size distribution rather than handing you the biggest.
That is deliberate: the loudest threads in a community are not its ordinary week, and a brief
built from them describes the wrong room. `thread(id)` opens any one thread whole.

### Breadth across the week comes before depth anywhere

`state()` shows two things: what you have consumed against the reference, and **how your
reading is spread across the seven days.** The second matters more.

**A reader who stops at the budget having seen only the first two days has not seen an ordinary
week.** It has seen a Monday. Before you go deeper into any day, look at `state()` and read into
the days you have not touched — the tool will tell you which those are, and `sample()` will
prefer them for you. Depth is for later, and only where a heading still has nothing behind it
after you have been everywhere.

### The budget is a reference

25,000 tokens is a reference, not a target, and there is no credit for spending it. A small
community will be exhausted long before it. A large one will not fit inside it at any depth, and
for that the honest brief is a well-spread sample plus a clear statement of what it is.

There is a hard ceiling at three times the reference, where `read_brief` stops serving and says
so. If you reach it, write the brief from what you have and say in it that you hit the ceiling.

### Say what you saw

**Your brief opens with its own evidence base**: how many threads and items you read, of how
many, across how many of the seven days, and what you deliberately did not open. Your reader is
a coder deciding how much weight to give you, and it cannot calibrate a description whose
coverage it cannot see.

---

## 2. Rules

1. **Files.** Your corpus, nothing else. No web, no other file. **The corpus reaches you
   through `read_brief` and you do not go around it** — your environment may contain a general
   file tool, and using it here is a breach of this rule; `read_brief` records what it served,
   so a reading it never served is visible afterwards. What it serves is plain text, and
   `header()` returns a block of `#` lines the harness computed before you arrived — item and thread
   counts, the day-by-day histogram, every author with their item count and first and last
   appearance, the thread index. **Do not recompute any of it**, and if something you need is
   missing from it, say so in Data problems rather than working it out yourself.
2. **Every claim carries a quote.** `cite(item_id, "…")` returns the exact text and its
   offsets; you write what it returns. A sentence in your brief with no citation behind it
   will be treated by its reader as unsupported, so do not write one.
3. **Searching.** `find("regex")` searches the corpus and logs the query. Use it freely — you
   are describing, not sampling, so there is nothing here for a search to bias.
4. **Describe, do not explain.** *"People call each other 'cunts' as a greeting"* — invented,
   from no community here — is a description. *"The community uses profanity to signal in-group belonging"* is an
   explanation, and it is not yours to make. Where you are tempted to explain, quote more
   instead.
5. **Their words, not yours.** Where the community has a term, use their term. Where you must
   supply a word, use an ordinary one. If you find yourself reaching for vocabulary from a
   specialist register that these people never used, you are explaining again.
6. **Absence is data.** `[deleted]` and `[removed]` are what the record says. Never
   reconstruct removed content. What people did in response to a removal is readable and
   worth describing.
7. **Real names.** Authors are real accounts and nothing has been pseudonymised. This is
   public data. Removing identifying detail happens later and is not your job.
8. **Your window ends where it ends.** Do not speculate about what happens after it. If
   something in the last days looks like the beginning of something, describe it as what it
   is and stop there.
9. **Flag, never fetch.** Suspected truncation or missing threads goes at the end of your
   brief. Never try to retrieve anything.
10. **`num_comments` is not a count.** It is a snapshot taken when the record was archived,
    and it drifts from the truth as the window lengthens, so a number built on it is wrong in
    a way nothing afterwards can catch. If you want to know whether a thread is whole, count the
    comments
    present and check that every `parent_id` resolves — and say that is what you did.

---

## 3. What your brief is for, and what that means for how you write it

Its reader will use it to tell the ordinary apart from the unusual. That is the whole
purpose. So:

- **A thing you describe as ordinary had better be ordinary.** If a format appears twice in
  seven days, say it appeared twice; do not call it weekly.
- **State what you could not tell.** If you cannot work out whether a term is an insult or an
  endearment, say so. Your reader can survive uncertainty and cannot survive a confident
  mistake.
- **Do not smooth.** If the register is inconsistent — polite in one kind of thread and
  vicious in another — that is the finding, not a problem to average away.

---

## 4. Output

**`brief.md`.** The seven headings from §1, then two more:

**What I could not tell** — terms you could not decode, voices you could not place, jokes
whose origin is outside your window, anything you are describing with low confidence.

**Data problems** — truncation, gaps, anything that made the week look incomplete.

**Length is set by the week, not by a target.** A busy week needs more than a quiet one, and
a community with five comments in seven days should produce a few lines. Padding would
mislead your reader about how much room there was, which is the one error that costs them
most. Quotes are as many as the claims require.

**Final message.** The community, and one line on whether the week looked ordinary or whether
something unusual was already happening in it. Nothing else.

---

## 5. What you are given

One corpus file covering seven days, thread-indexed, item bodies byte-identical to the
collected record, real usernames and ids, threads whole and in order.

Counting, timing, participation and the verification of every quote are done for you. Spend
no effort on them.
