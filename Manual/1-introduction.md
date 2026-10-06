# Introduction

*Kind of page: explanation: what the study is for and how this Manual is laid out.*

This repository holds the instruments of a study of r/place, the shared pixel canvas Reddit ran for April Fools' Day in 2017. For 73 hours any logged-in user could place one pixel at a time, and anyone could paint over it. Hundreds of communities organized to put something on the canvas and keep it there: flags, logos, mascots, in-jokes. Most of them talked about it in their own subreddits while they did it, and that talk is public.

The study asks a method question first. Does knowledge from many case studies compose into knowledge about a population? A single qualitative study follows a handful of cases, or a few dozen at most. Here there is a census: every community the canvas atlas ties to an artwork, about seven hundred of them, all facing the same task in the same week under the same rules. The aim is to read each one as a case, on its own terms, and then build one grounded model across all of them that still explains each case when you go back down to it.

The theory question sits under the method question. What forms did organizing take, how do they differ, and which of them kept the work alive once the first rush was over?

**Where it stands.** Coding is nearly done: the aggregator's frame holds 705 of the 706 communities (r/the_donald is not coded), and [the numbers](numbers.md) give the current count. The aggregator's run on instrument v43 has not started, so this repository offers a method, the coders' readings and the trail that lets you check them, not yet a model or findings. The stage table on the [front page](README.md) shows how far the run has got.

## Two instruments

The work is split between two instruments, and most of the files in this repository belong to one of them.

**The coder** reads one community's week and codes it. It works in the manner of Gioia, Corley and Hamilton for the codes and of Eisenhardt for the account: codes in the participants' own words, themes that group them by what these people were doing, and a within-case account written as if no other case existed. In Gioia's terms both the codes and the themes are first-order concepts; the files call the themes `second_order`, and [the reviewers' page](10-for-reviewers.md) maps every tier to Gioia's. Each coder is sealed. It sees its own community's record and nothing else, so no reading of one room leaks into another. A room small enough for one reader is read whole by one agent. A large room is read by a serial fleet, one coder per slice, and a case lead writes the account at the end.

**The aggregator** builds the model across all coded communities. It holds every coder's sealed work at once, reads every room, builds the higher tiers of the data structure (third-order themes, fourth-order themes, aggregate dimensions), draws a model with arrows, and then returns the model to every room to learn what it would have to change to explain that room. The forms of organizing are read off those changes.

The coder works in context: a room's material mostly fits in one agent's window, and the agent reads it. The aggregator cannot work that way, because no window holds seven hundred rooms. Its knowledge lives in files it writes, and it makes decisions in context. That difference explains a great deal of what follows.

## The handlers

Neither instrument runs itself. Each runs under a handler: an agent that launches the working agents, checks what they wrote, saves and restores them, gives them feedback when a check fails, and takes to J (Jose Arrieta, the principal investigator) only the questions that are his to answer. On the coder side the handler is the yard's scheduler. On the aggregator side it is the run's handler, working through a harness of scripts. The handlers grew more complex as the instruments did, and a good share of the files exist to support them.

## How to read this Manual

The Manual runs from the general to the particular. Read the first five pages in order if you are new to the project; after that, go where your question takes you.

1. **This page.** What the study is for and how the parts fit.
2. [r/place and the study](2-rplace.md). The event, the census of communities, and the data behind it.
3. [How it was built](3-how-it-was-built.md). The history of both instruments, told as an explanation of why each kind of file exists. If a file puzzles you, its reason is probably here.
4. [The coder](4-the-coder.md). The coder instrument as a hierarchy, from the contracts down to one room and the yard that runs them all.
5. [The aggregator](5-the-aggregator.md). The same for the aggregator: what governs it, what it holds, its verbs, its memory and its harness.
6. [The handlers](6-the-handlers.md). How the agents that run the instruments work, and what they may and may not do.
7. [Tool usage](7-tool-usage.md). Which tools the agents used, counted from their transcripts, and which almost never.
8. [The v37 run](8-the-v37-run.md). The previous run of the aggregator, and what it taught. It is described here, not shipped.
9. [Talking with a leg, and continuing a run](9-resuming.md). What the command on each stage page does, piece by piece, and how a run is continued.
10. [For reviewers](10-for-reviewers.md). The tiers against Gioia's, which model did each step, the departures the method names, and how to check one room yourself.

Reference material sits beside those pages:

- [The glossary](glossary.md) defines the project's own words: room, leg, cut, forest, drop, and the rest.
- [The file pages](files/README.md) give one page per file or kind of file, grouped by instrument: [the coder's files](files/coder/README.md) and [the aggregator's files](files/aggregator/README.md). Each page says what the file holds, who writes it and when, why the design has it, and where the real file is.
- The memory pages say how each side remembers across sessions: [the aggregator](memory/aggregator.md) and [the coder lead](memory/coder-lead.md).

## A word on the record

Superseded versions are moved, never deleted, and every instrument version has a fingerprint, so a room coded under one version can be told from a room coded under another. Counts that move daily, such as how many rooms the yard has coded, are given with their date or not at all.
