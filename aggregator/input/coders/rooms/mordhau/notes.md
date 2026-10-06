## What was hard

The hardest distinction was between apparent vandalism and the community's own relocation. The exchange at `dfqg7tm`, `dfqhc3l`, and `dfqhqby` explicitly separates a sanctioned move from people cutting through the new M, so I preserved the correction instead of treating every changed pixel as attack.

The alliance thread also contains incompatible positions without a shared resolution: expansion and tribute, sparing r/placestart, mockery, and a statement that r/place has nothing to do with Mordhau. I treated these as contrasting speakers rather than a change in collective opinion.

The theme grouping was reviewed after the counter-reading and did not change. “working around neighbouring marks” and “keeping the mark clean and on-pattern” nearly merged; they stayed apart because the first works out relations and routes at the mark's edges, while the second performs or judges upkeep of the mark itself. Relocation also remained separate because its codes organise a specific move and distinguish sanctioned change from interference.

The code I would defend hardest is “calling the small group to keep its messy stamp neat.” The thinnest I kept is “mocking the alliance as a life goal.”

## Data problems

The body of the first r/place proposal (`62rci5`) is deleted, and four deleted comments interrupt the large upkeep thread. The surviving title and replies are coded without reconstructing the missing words. Linked images and schematics were recorded as pointers, but I did not inspect or infer their contents.

The corpus header says only 370 of 385 reply parents are present across the room, although the coded forest has no orphaned node. This limits whole-room absence claims. The briefing describes a different, selectively served week and is orientation only; I did not use it as case evidence.

The initial display of `63axcm` clipped. I recovered the omitted middle through `read.py ... thread 63axcm` piped to a bounded `sed` section before excluding it as a game-mechanics argument.

The first `emit.close()` exposed that the final four served, out-of-scope threads had not yet been appended. I immediately appended their dispositions, closed again, rebuilt the forest, and reran the audit. The complete tally then showed zero undisposed threads. This explains `reopened_after_close: true`; it was a completion repair, not a change to any interpretation or code.

## Anomalies and leads

The participant who says “there's not many of us” is corrected indirectly by a highly scored reply crediting the forums and Chivalry subreddit too. This is a lead about distributed contribution, but the other venues are not in the record.

The only searched statement asking people not to damage others' work, `dftv5mj`, is after the case window. It was read and reported as context, not coded as in-window conduct.

## Counter-reading search

Before searching, I recorded the competing account that a few people mainly displayed images while the wider room rejected r/place and substantive work occurred elsewhere. I searched `(?i)(nothing|nice life goals|not just this sub|what does it .*mord|no need to screw up others)`. The search returned 15 hits. I opened the five relevant items through `read item`: `dfpklps`, `dfrc2yp`, `dfrlazy`, `dfs4g0w`, and `dftv5mj`. The strongest contrary item was `dfs4g0w`. The other ten hits were unrelated uses of “nothing” in game or Kickstarter discussion. No late in-window code was needed because all relevant in-window items were already coded; `dftv5mj` was after the window.

The query found no further in-window contrary practice within those phrases. That null applies only to the supplied corpus and query vocabulary; deletions, missing parents, linked images, and credited outside venues make it weak evidence for broader absence.

## Complaints

The documented shell heredoc setup failed because the environment could not create a temporary heredoc file. A normal foreground `python3 -c` invocation worked and kept all writes inside the run directory.

The contract requires a second-look grouping statement but exposes no separate `emit` call for a no-change grouping review. I recorded the review explicitly here; actual regrouping would have been recorded in `regrouped_from`, but none occurred.

## How the reading held up

I did not work from memory of a thread instead of served text. I went back only to recover the clipped middle of `63axcm`, not because I could not remember it. Earlier event threads remained distinct while later ones were read; the compact seven-thread r/place cluster and the forest made their sequence manageable. The run was not interrupted or resumed. The mistaken early close was detected within this run and repaired from the journal without restarting or rereading disposed threads.

## Method cautions

The forest establishes reply structure and instrument-measured latency, not causation. Relations in the case account use the later speaker's answering words; cross-thread order is described only as sequence.

No bot-like account was identified in the header. No retained event item was treated as machine-generated conduct.
