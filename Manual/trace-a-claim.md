# Trace one claim down to the Reddit text

*Kind of page: tutorial: about ten minutes, with a terminal and `zstd` (`brew install zstd` on macOS, `apt install zstd` on Linux). Run the commands from the repository root.*

A qualitative reader asks of any claim: which words, said by whom, and read how? This page follows one claim of the r/armenia case from the coder's account down to the Reddit comment it rests on. Every coded claim in the study can be traced the same way, and the aggregator's store carries the same code, so a claim of the model can be followed down through it too.

## 1. The claim, in the case account

`case.md` is the case lead's account of the room's week; it sits at `out/case.md` inside the room's run, which step 2 opens. For r/armenia it says, in its chronology:

> `dfp16pe` announces an alliance with r/greece in which "They will help us and we will help them."

The backticked id is a Reddit item: a post (six characters) or a comment (seven). An account may only cite items its coders read; the gate checks this before the room is verified.

## 2. Open the room's run

```bash
mkdir -p /tmp/armenia && zstd -dc coder/rooms/armenia/run.tar.zst | tar -x -C /tmp/armenia
cd /tmp/armenia/run
```

On Linux, GNU tar prints lines about an unknown keyword `LIBARCHIVE.xattr.com.apple.provenance`: the archives were made on a Mac, and the lines are harmless. `out/` holds what the coders wrote; `coder_corpus.jsonl` is the record they read, one Reddit item per line.

## 3. The code behind the claim

```bash
grep '"item_id": "dfp16pe"' out/codes.jsonl
```

returns code `c0006`: first-order label "getting an alliance with r/greece", theme `t03`, thread `62qqvs`, characters 0 to 25 of the item, and the quoted passage `I got us in an [alliance]`.

## 4. The theme the code belongs to

```bash
grep '"theme_id": "t03"' out/themes.jsonl
```

`t03`, "asking neighbours for pixel help and returning it", groups 23 codes. This is the coder's second-order theme, bound to this one case; the themes across cases are the aggregator's work ([for reviewers](10-for-reviewers.md)).

## 5. The words in the record

```bash
grep '"id": "dfp16pe"' coder_corpus.jsonl
```

returns the comment as the archive holds it: a reply in thread `62qqvs` (`parent_id` `t3_62qqvs`), written 2017-04-01 15:41 UTC, whose body begins `I got us in an [alliance](...) with /r/greece. They will help us and we will help them fight against invaders.` (the link, to an r/greece thread, shortened here) Characters 0 to 25 of the body are exactly the code's quote. The gate's check C3 made this comparison for every code in the room.

## 6. That the coder read it

`out/_read.jsonl` logs every call to the reading tool, in order. Its entries 10 and 11 serve the post `62qqvs` and then the comment `dfp16pe`; the gate's C9 checks that every code sits on an item the tool served.

## 7. On Reddit

`permalink` in the record is `/r/armenia/comments/t3_62qqvs/dfp16pe`, in the archive's form; on Reddit the same comment is at `https://www.reddit.com/r/armenia/comments/62qqvs/_/dfp16pe/`. It may have been deleted since; the archive keeps it as it was taken in 2017.

## From the aggregator's side

The aggregator's store holds the same code: `aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/package/store/codes.jsonl`, `sub` armenia, `code_id` c0006, with its text. A third-order theme the analyst builds lists the second-order themes it groups, and each of those its codes, so any claim of the model leads to codes like this one and down the steps above.
