# Audit, section 1, part 1: the quotes and the clocks (E1b-01)

Written at E1b-01, 27 October 2026. This part covers four items of stage E1 section 1: the logs against the claims (every quote and every id), the quotes against the raw record, the store's figures recomputed, and the clocks. Every figure below comes from a script in `audit-E1/`, with its output beside it under the same stem, or from a reading by hand that the diary logs. A stranger reruns a script with `python3 out/audit-E1/<script>.py > out/audit-E1/<output>`. The scripts written at this leg are `unresolved_read.py`, `unresolved_hand.py`, `quote_sources_check.py`, `labels_read.py`, `case_missing_read.py`, `relations_clock.py` and `links_views.py`. Each states its rule in its docstring, written before it ran. Nothing here comes from any account of the run, my own included; where an earlier file differs, this part says which is wrong.

## 1. Logs against claims

### Every quote in every output

`quotes_resolve.py` (E1a) scanned 5,953 files I wrote: every `.md` file under `out/` and the string fields of my ledgers. It left out the harness's, the fleets', the principal investigator's and the generated files, which its docstring names. 5,166 of the files hold a quote. A quote is a span between paired double quotes on one line. The script resolved each span in a fixed order: the participant's words of a concept, then a label or note, then the coder's case account, then the instrument's texts, then the instructions, then nothing.

| quotes | spans | resolve to |
|---|---|---|
| cited to a concept (`sub/cNNNN`) | 3,230 | 3,218 to the concept cited (99.63 per cent); 12 do not |
| cited to an item (`` `itemid` ``) | 405 | 361 to a concept's words, 34 to the case account alone, 2 to a label, 8 to nothing |
| uncited, five words or more, in `.md` files | 76,848 | 69,079 to a concept's words, 3,639 to a label or note, 1,955 to the instrument's texts, 73 to the instructions, 68 to a case account, 2,034 to nothing |

**The 12 cited quotes that do not resolve to their concept**, read by hand in their files against `cite.py`. Two are faults of form. Ten are faults of the script, not of the quote.

| file, line | cited | what it is |
|---|---|---|
| `account-p1.md` 23 | suomi/c0098 | **Fault.** My English translation of the Finnish post is set in quotation marks beside the original, which resolves, with no word saying it is a translation. |
| `notes-A1.md` 700 | predators/c0047 | **Fault by the stage's rule.** The quote is the concept's label, and the sentence says it is a label. Nothing is passed off as a member's words. |
| `forms/F06-account.md` 100, `forms/F10-account.md` 164, `forms/F23-account.md` 125, `notes-C5.md` 564 | rust/c0144, buffalobills/c0127, greyblob/c0037, pokemon/c0506 | The quote is a coder's or reader's return line, or an element's statement, named as such; the citation belongs to the next sentence. |
| `serial-C5/finding-1-unit.md` 71 to 74 | fireemblem/c0412, utahjazz/c0030, lakers/c0155 | The quote is the model's wording, in a table beside a column of evidence ids. |
| `forms/F16-account.md` 161 | pcmasterrace/c0596 | "focus on the plan" is in pcmasterrace/c0593, cited one clause before for the same member's post. |
| `serial-C5/finding-2-reason-test.md` 82 | polyamory/c0002 | The store writes the slash as `/r\/place`; the quote is word for word. |

**The 2,042 spans that resolved to nothing** (2,034 uncited and 8 cited to an item). `unresolved_read.py` sorts them. 983 are field values of JSON records printed inside `.md` files (the structure files hold 927 of them), not quotes. 975 are found whole once the store's escapes, asterisks and backticks are set aside: 131 in a concept's words, 31 in the forest, 2 in a case account, 320 in the readers' and coders' returns, 5 in the operator's texts and 486 in the run's own other files. The 8 cited to an item are the field's quotes, found whole in `out/field/`. That leaves 84, 52 near a source and 32 near none. `unresolved_hand.py` finds where each first appears in the transcripts, and I read each in its line.

- **63 in my files.**
  - 16 are the operator's or the harness's words. Each first appears in a message to me: J's rulings in the head, the principal investigator's leg messages, a ruling that came as an attachment, and the brief's phrase "N threads out of scope".
  - 8 are texts I first saw in a tool's output: shelf pages, and counts quoted from an earlier file.
  - 8 are literature quotes that `quote_sources_check.py` puts beside the shelf. The shelf files are two-column extractions, so the words come interleaved with the other column and broken at line ends. Read through, each quote is the paper's words. One example: Felin and Zenger's "a set of contrarian beliefs" is "a set of con-trarian beliefs" across a line break.
  - 24 are my own earlier wordings, quoted as such: statements under test, an earlier version of a proposition, a sentence later corrected.
  - 1 is a translation I declared as mine (`literature-C3.md` line 235, "My translation").
  - 2 are small misquotes of the instrument. `notes-C1.md` line 144 has "apply" where the stage has "applying". Line 453 has "a rivalry" where the scheme has "A dispute or rivalry".
  - 3 are examples of my own in quotation marks, which a reader could take for members' words: "help us at 200, 300" (`_adjudication-B4/boundaries.md` 59), "those were not our people" (`confusions.md` 47) and "defending the script as fun" (`coordinating-rule-A1.md` 32). No concept holds them.
  - 1 cannot be checked. J's instruction on reading is quoted in `notes-B2.md` line 5, but no transcript holds its words before my own Write at B2a-r1. The message that carried it is outside my reach, so the wording rests on my record alone.
- **21 in the readers' room models** (`rooms/<sub>/model-D*.md`, written by the D2 and D3 readers, not by me). 11 quote a concept with small changes: a word dropped, a spelling corrected, a contraction opened. 3 paraphrase inside quotation marks: r/armenia's line on the Dutch, r/zootopia's "patch of artwork" for "patch of space", and r/straya's "breaking the truce is Un-Australian". 7 are in no concept of the room. They may come from uncoded items, which the forest drops, or they may not; I cannot tell.

**The 3,641 spans that resolve to a label or note** (3,639 uncited and 2 cited to an item). The stage counts a quote that resolves to a label as a defect. `labels_read.py` sorts them. 3,560 are the `second_order` field of the JSON exemplar records in the structure files, not quotes. Of the 81 in prose, I read a seeded 25.
- In my files, 16 name a label as a label: a theme by its name, or a room note's "struck by" line. 1 is a packet's line format, and 1 is a defect.
- In the readers' room models, 4 are faithful quotes whose concept text holds link or emphasis markup. 2 paraphrase inside quotation marks (r/asexuality, r/smite), and 1 cannot be told (r/norge).

The 2 cited to an item are both defects of mine, made at D6a-17 and D6a-18. In `dutch-telling-D6/greece.md` line 36, "the heart was placed cooperatively later" is the coder's English for a Greek post (greece/c0126, item `dfrvs5t`), and I gave it as a member's words with no original. In `form-telling-D6-r2/room-E-paladins.md` line 26, "April Fools' shenanigans" is the coder's wording; the post says "April Fools' Day, so expect shenanigans" (paladins/c0001). I carried both from the case account. My D6 quote check tested quotes against the case account, so it passed them.

**Five quotes drawn by seed** (`cd472a6087a223d4`, from the cited quotes that resolve), checked by hand with `cite.py --room --code`. All five hold word for word, with the room, the concept and the hour the accounts give:
- Moondye7/c0066 (`forms/F19-account.md` 17);
- lebanon/c0105 (`forms/F35-account.md` 60);
- fivenightsatfreddys/c0074 (`forms/F07-account.md` 160, "at h+7"; the store has 7.15);
- OnePiece/c0228 (`forms/F27-account.md` 9, "hour 51.18"; the store has 51.18);
- Rainbow6/c0589 (`forms/F20-account.md` 162, "at the close"; the store has 73.29).

### Every id in the head, the questions and the views

`links.py` and `validate.py --links` both exit 0, and all ids resolve (`links_check.txt`). But `links.py` reads three files only: `_head.md` and the two question files. It does not read the views. `links_views.py` applies its own resolver, imported, to the 35 text files of `out/_views/`. They hold 537,153 tokens of an id's shape, and 487 do not resolve. I read all 487:
- 413 are in `data-structure.tsv`, and all are members' words in its material column: 363 subreddit names as typed (210 distinct, typos among them), and 50 tokens such as "the D2 logo", "N64" and "P90".
- 40 are the proposition ids N01 to N09 in `figure-model.md`. `propositions.jsonl` holds them, but `links.py` does not load it.
- 32 are stage names written bare in the generated views (D2, D3, D4 and D6).
- 1 is a logo name in a reader's line (C53).
- 1 comes from one store pointer that names two rooms in one string.

No id of the model, the scheme or the store fails to resolve.

## 2. The quotes against the raw record

`quote-check-E1.json` was computed by the handler outside my session, over 80 rooms drawn with seed 13. It is the one place where the run touches the raw record. The store and `cite.py` serve only the coded record, and the methods paragraph says so. The file gives two shares:

- **code_quote_found_share: 1.0** (100 per cent). Of 14,587 coded quotes, 13,374 are at their offsets in the item and 1,213 are elsewhere in it; 0 are absent and 0 items are missing.
- **case_quote_found_share: 0.6573** (65.73 per cent). Of 1,599 quoted strings of 25 characters or more in the case accounts, 1,051 are found in the room's corpus.

**The 548 against the 389.** The file lists 389 missing strings, against 548 by its own count (1,599 less 1,051). It lists at most ten a room. In the 13 rooms where it lists fewer than it counts, 289 are missing and 130 are listed; 289 less 130 is 159, and 548 less 159 is 389.

**What the 389 are** (`case_missing_read.py`, then a reading by hand):

| kind | strings | what it is |
|---|---|---|
| in the room's coded passages | 242 | Participant words. The raw check missed them because the coder put punctuation inside the closing quote, or because the item holds link markup or other quote marks. |
| the coder's own labels | 85 | Theme or concept labels, quoted in the case account as labels. |
| near quotes | 10 | Participant words with link markup removed or inner quote marks changed. |
| thread titles | 7 | Titles of the room's threads. |
| another room's concept | 1 | A quote from outside the room's corpus: the r/PokemonSage account quotes a post that r/TheFarLeftSide's record holds. |
| the coder's translations | 5 | English in quotation marks beside the Albanian originals, which are quoted and cited (r/albania). |
| the coder's own phrases | 6 | A counter-reading's wording in quotation marks ("negotiated rather than destructive", "failure caused the strategy change"). |
| participant words from uncoded items, cited by item id | 33 | Outside my reach. The forest drops uncoded items, so I cannot check these against the raw record. Five are titles of threads the store does not hold. |

So, of the strings I could check, none is an invention. The missing share is mostly a matter of punctuation and markup, of the coder's own labels and phrases, and of translations. The five translations among the 389 are set beside their originals. The r/greece translation found in part 1, outside this sample, has none. 33 strings remain unchecked.

## 3. The store's figures recomputed

`store_figures.py` (E1a) sets `README-store.md`, stage A1's recomputation and the store as it stands in three columns. All 16 figures agree, so there is no defect. A dash in the table means the source gives no figure.

| figure | README-store.md | A1 | now |
|---|---|---|---|
| rooms | 705 | 705 | 705 |
| concepts | 115,388 | 115,388 | 115,388 |
| retracted, dropped | 175 | 175 | 175 |
| second-order themes | 7,844 | 7,844 | 7,844 |
| unjoined concepts | 38 | 38 | 38 |
| items in the store | 158,227 | 158,227 | 158,227 |
| threads in the store | 42,906 | 42,906 | 42,906 |
| pointers | 20,110 | 20,110 | 20,110 |
| briefs | 705 | 705 | 705 |
| transitions | 62,838 | - | 62,838 |
| forest: threads given | - | 42,906 | 42,906 |
| forest: items | - | 531,851 | 531,851 |
| forest: coded | - | 109,807 | 109,807 |
| forest: bridge | - | 28,350 | 28,350 |
| forest: removed | - | 617 | 617 |
| forest: dropped | - | 393,077 | 393,077 |

The 158,227 item lines hold 137,732 distinct room and item ids. 21,011 lines are in the state `collapsed`, which `README-store.md` does not name; stage A1 recorded this as a defect.

## 4. The clocks

**The coder's time against the item's** (`clocks.py`, E1a). In all 115,350 concepts whose item the store holds, the concept's `created_utc` equals the item's. Every concept's `hour` matches its own `created_utc`. The denominator is 115,350 of 115,388 concepts; the 38 others are the unjoined concepts. One limit: the store's builder, `tools/build_store.py`, is not in the folder. So I cannot tell whether the coder wrote the concept's time or the build copied it from the item. If the build copied it, the agreement holds by construction and says nothing about the coder.

**The second check, against `relations.jsonl`** (`relations_clock.py`; `tools/relations.py` builds the graph and checks no clock). A pair counts where both rooms are studied, each room's coder recorded the other, and the two sides record one act from both ends (attacked and attacked-by, gave and asked help, negotiated, allied). There are 476 such pairs. For each, the script takes the smallest gap between a concept of one side and a concept of the other:
- 187 lie within 1 hour;
- 142 more lie within 6 hours;
- 105 more lie within 24 hours;
- 42 lie further apart.

Ten pairs drawn by seed, read by hand with `cite.py`:
- **Four date one encounter close together, as the words say.**
  - r/anime and r/satania, 0.91 hours: the sign's maker thanks r/satania, and r/satania gathers its threads.
  - r/europe and r/formula1, 2.6 hours: "let them have their white border", then "EU flag overlaps with our logo".
  - r/chibears and r/finland, 0.04 hours: one member's comment, whose edit links the plea that member then posted in r/finland.
  - r/suomi and r/unitedkingdom, 0.83 hours.
- **Four hold different moments of a longer tie:** r/uiuc and r/uofm, r/stevenuniverse and r/yogscast, r/OnePiece and r/pathofexile, r/lakers and r/nbaspurs.
- **Two hold concepts that do not speak of each other:** r/placestart and r/thebluecorner; r/argentina and r/uruguay, where the nearest r/argentina concept is about the room's own work, not about r/uruguay's call for help.

No pair dates one encounter at two times. One order is unsettled. In r/suomi a member writes "I have opened negotiations" 0.83 hours before the same member's opening post in r/unitedkingdom. The concept's label ties the negotiation to r/argentina's offer, so the words do not settle with whom it was opened.

**Datings in written order** (`clocks.py`). In 237 of the 598 case accounts with two or more datings in their Chronology, the datings step back at least once. Each model arrow names 2 to 4 rooms (A21 names none), and 14 of the 21 arrows name at least one such room. This does not touch a loop: stage C2 admits a loop only where one room's datings run the whole way round, and the model grounds no loop. The arrows' order rests on the items' own times, which the transitions carry, not on the order in which a case account tells its threads. A Chronology that steps back tells one thread and then returns to an earlier one.

## 5. Defects named at this leg

Eight lines were appended to `defects.jsonl` (lines 102 to 109, stage E1, leg E1b-01), by `_analysis/e1b01_defects_lines.py`. No earlier file is changed.
- **The instrument's (5):**
  - my translation in quotation marks (`account-p1.md` 23);
  - the two D6 quotes carried from case accounts (r/greece, r/paladins);
  - two small misquotes of the instrument (`notes-C1.md` 144 and 453);
  - three examples of my own in quotation marks;
  - five paraphrases in quotation marks in the readers' room models.
- **Provenance (1, not sure):** J's reading instruction in `notes-B2.md` has no record before my own Write.
- **The material's (2):**
  - the case accounts' translations, labels and phrases in quotation marks;
  - one store pointer whose name holds two rooms.

## What this part cannot say

- Whether 33 case-account strings and 7 reader quotes are the participants' words. They come from uncoded items, which neither the store nor the forest holds.
- Whether the coder or the build wrote each concept's time.
- Whether J's reading instruction was worded as `notes-B2.md` quotes it.
- How the 80 rooms of the raw check would compare with the other 625. The 0.6573 is that sample's share, and my sorting of its 389 listed strings is a reading of the listed strings only.
