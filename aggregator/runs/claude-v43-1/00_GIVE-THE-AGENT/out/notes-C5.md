# Notes, stage C5 (the account)

## The criterion (section 5), written before pass 1

Written at C5a-01, 2026-10-14 (UTC), before any pass of the account exists. I will prefer a later account to an earlier one when all of the following hold.

1. **It states fewer untested claims.** Every sentence that says one thing brings about another rests on an arrow whose order count beats its null, on a finding, or on a test that could have failed. Any other causal sentence is marked theorised or thin. The later account has fewer unmarked causal sentences than the earlier one.
2. **It tells at least as much with no more elements.** The story rooms of passes 1 to 5 (`story_rooms-p5.jsonl`: 16 told, 19 told with a residue, none untold) are the first test. The later account tells at least as many of them without a residue, using the same or fewer elements at the top.
3. **It keeps every tested arrow.** An account that drops an arrow whose order count beats its null, in order to read more simply, is rejected.
4. **More names pass the prose test.** In the later account, more fourth-order themes and dimensions do theoretical work in a sentence of the form "because the room had X, Y could happen".
5. **At the check legs, the readers recover more of what I meant.** The readers recover more of my claims in `author_claims.jsonl` and fewer claims I did not write.

I reject a later account that gains reach by loosening an element, by a sentence that no count or quote supports, or by a claim the readers recover that I did not intend. When the criteria conflict, the order above is the order of priority.

## J's rulings of 15 October (01:29 Berlin), as the handler relayed them

1. **Work after hour 73 is curation.** Organizing to make the artwork ends at hour 73. After it, members curate: they clean, copy, record and argue over which version of the canvas and of the event is kept. The account tells this as curation of the record (P12, with P22 tentative), apart from carrying on (P13), and not as a fourth part of making the work.
2. **The declaration prose pass comes first, in this pass.** The rule is written first. Each of the 28 declarations is read against its members' quotes, starting with Stigmergy, Completion ritual, Live and let live and Mobilization. Each amendment is logged as a move. A cut moves only where the members' quotes force it.
3. **The two sources for Stigmergy.** Heylighen (2016) and Grassé (1959) are in `out/sources-from-J/`. I read both whole before amending Stigmergy, and mark each claim I take from them verified, with its page. I recut Stigmergy only if, as cut, it joins things the field keeps apart.
4. **The second reader is stage C5's three readers.** The rule and the amended declarations go into the C5b packets with the quotes each declaration rests on, and the readers' disagreements are recorded.
5. **J's language ruling stands.**

QC4-002: the renamed link `out/_field-link-superseded-C4a` stays as it is, and I read the field only from `out/field`.

## The declaration prose rule, written before the pass

Written at C5a-01, 2026-10-14 (UTC), before I read any declaration in this pass.

**What the rule reads.** In each of the 28 construct blocks in `fourth/fourth.jsonl`, the rule reads every sentence of the `prose`, `changed` and `mistaken_for` fields that says something about these rooms or their members. A sentence about a source construct, saying what Gieryn or Mintzberg holds, is about the literature. It is read only for its mark, verified or recalled.

**Which sentences are in question.** A sentence is in question when it is:
- **universal:** every, all, no one, nothing, never, always, any, only;
- **comparative:** more, most, less, fewer, strongest, than, as much as;
- **causal:** because, so, makes, brings, turns into, leads to, keeps alive, why, explains, or a verb that gives one act as the cause of another;
- **cyclic:** again, each time, returns, renews, a loop.

**When a sentence in question stands.** It stands only if one of these supports it:
- an order count in `model/arrows.jsonl` that beats its null;
- a line in `findings.jsonl`;
- a count in `structure-C4.md` (rule 5's three numbers, or the rooms carrying a theme);
- a fact of the setting as the contract states it. The setting facts are: one pixel per interval for each account; anyone may change any pixel; placement stopped at hour 73; no one holds authority over another's placing.

**Otherwise the sentence is rewritten.** The new sentence says what members did, in how many rooms, in the members' own terms. Each act it names must be shown by at least one member's quote. The quotes are the exemplars and material in `structure-C4.md`, and for the first four declarations a further seeded draw through `cite.py`.

**What does not change.** Names, members and the cut do not change, unless the members' quotes show that the theme joins acts the declared construct keeps apart. A recut needs that showing, written down before it is made.

**How each amendment is recorded.** Each amended declaration gets one `tier_history.jsonl` line with the old line as `was`. It is logged with `mem.py log --kind move`, naming the move:
- **developing or dropping working hypotheses,** when an untested claim is dropped or rewritten as a description;
- **relating or contrasting,** when the amendment compares the theme with a source.

Each amendment is snapped as `C5 move-<move>-<n>`.

## Stigmergy against its sources: the rules for an abductive read, written first

**The question.** J's question is whether Stigmergy, as cut, joins things its sources keep apart. Both sources separate coordination through the work itself from communication between members:
- Grassé (1959, pp. 65, 74 to 75);
- Heylighen (2016, pp. 9 to 10).

Heylighen admits a shared record of the work's state, kept with markers, as a stigmergic medium (p. 9). The record of my rooms holds only talk. So the test reads what the talk under each member of Stigmergy does.

**The sample.** For T3-038 (building and reporting the mark) and T3-041 (extending the room's work), 24 records each, drawn from the store with seed 20261015, at most two per room. For T3-060 (adding a personal piece), every record, up to 24. Each record is read whole.

**The codes.**
- **M, the trace or a marker.** The member reports the state of the work to the thread (what is placed, done, missing, or where). Or the member says they acted on what the canvas showed. Or the member points others to the canvas's state.
- **MP, a proposal grounded in the trace.** The record proposes an addition and names, in the same record, the state of the canvas that prompts it. It counts with M, since the trace is "an opportunity for advancement" (Heylighen 2016, p. 8).
- **P, a proposal or request.** The member proposes, asks, invites or instructs other members or another room about what to add, where or how. The record names no state of the canvas that prompts it.
- **O, other.** A celebration, a call for hands, upkeep, a joke, or talk off the work.

**The decision rules.**
- A member joins what the sources keep apart if P is at least half of its records that are not O.
- **If T3-041 meets the rule,** it moves to Collective representation, where proposals of what the mark shows already sit (T3-033, T3-004). Its C1 note named that as the alternative.
- **If T3-038 meets the rule,** I report it. The theme would need a third-order split, which reassigns second-order themes, and I do not make it in this pass.
- **If no member meets the rule,** Stigmergy keeps its cut. Its declaration then says that the record holds talk that registers the state of the work, and members' words about reading the canvas, not the placing itself.

**The result.** No member met the rule.
- T3-038: P in 5 of the 15 records that are not O.
- T3-041: P in 8 of 17.
- T3-060: P in 8 of 20.

Stigmergy keeps its cut. T3-041 is close: one doubtful code would move it to 9 of 17 (`c5_stigmergy_codes.json`, "doubtful"). Across the three members, 31 of 52 records report the work's state or act on the canvas, and 21 propose or ask what to add. The amended declaration says both. Coded by me alone. The C5b readers check the prose against these quotes.

## Pass 1 (C5a-01)

**What the pass did.**
- **The declaration prose pass.** All 28 fourth-order declarations were read against their members' quotes and amended under the rule: `prose`, and `changed` and `mistaken_for` where they made claims. Each amendment is a `tier_history.jsonl` line, a logged move and a snap (C5-move-relating-53, C5-move-developing-54 to 80). No name, member or cut changed.
  - **What the pass dropped.** These sentences made causal claims with no count behind them ("explains", "turns ... into", "pays"), universal claims ("every", "no one", "only"), uncounted comparisons ("most", "constantly"), and figures of speech.
  - **What replaced them.** Each declaration now gives its acts with their rooms, the counted orders that touch it, and its sources marked recalled or verified.
  - **What the run's own tests contradicted.** Attribution called itself the hinge between restraint and attack. Collective efficacy said doubt shapes whether hands come. Both claims were tested and not found.
- **Stigmergy.** I read its two sources whole, and the abductive read above kept its cut.
- **Rule 14.**
  - mapping-C3.jsonl was corrected in place for Attribution, Visibility returns and Completion ritual.
  - F-016 was superseded, because Completion ritual is now mapped to reward by reading, not by construction. No count changed.
  - A21 got the `negative_check` the arrow checks require.
- **The account, the prose test and the sketches.** `account.md` was drafted from the pass 5 story, with curation after hour 73 apart from carrying on (J's ruling 1). `prose-test-C5.md` passes all 36 names and flags four. `sketches.md` holds three arrangements.

**What the criterion says.** Prefer, against the pass 5 story as the first draft.
- **Unmarked causal sentences: fewer.** The story said, unmarked, that one-line answers are "how a room with no membership list sees its numbers", which F-015 failed. The account marks each thin or theorised arrow, and the declarations it rests on no longer carry untested causal sentences.
- **Rooms told: unchanged.** The account names the same 19 rooms the story told with a residue, and I did not read the story rooms again in this pass.
- **Tested arrows: all kept.** All 18 counted arrows are in the account.
- **The prose test:** all 36 names pass. There is no earlier test to compare against.
- **Readers:** not applicable before the check leg.

**Section 4, simplification: nothing cut in pass 1, three candidates.** P06 (attribution), K01 (the April Fools frame) and R02 (the envoy) are standing elements with no arrow.
- **Cutting P06** loses the model's statement that members work out who changed their work (155 rooms). The account could still say the step was tested and not found.
- **Cutting K01** loses the condition the odd room runs inside. F-009 would carry the finding that the frame did not delay the work.
- **Cutting R02** loses the named role. P08 already holds envoys.

Each cut would lower the count of elements and might add residue at the return, since the rooms still carry these acts. I decide in pass 2, after the account is cut toward two pages and the story rooms are read against it.

**Section 5, recuts: none in pass 1, three candidates from the sketches.**
- **P08 (border talk)** holds both terms offered before any damage (day9 at h33.9; the field's buffer at h5) and talk after erosion (A04). The test for pass 2 is to read P08's first concepts in the 166 rooms where A04's order fails, and count those that offer terms before any damage.
- **P05 (upkeep)** sits in two places in two drawings. I read this as the spine passing through it, and I check it again in pass 2.
- **P10 (the move)** ends a fight and starts new work, and no counted arrow returns from it to building. This is not a recut. It is the loop the model cannot ground.

**Limits of the pass.**
- **Fields outside the rule's scope.** The rule read `prose`, `changed` and `mistaken_for`. It did not read the `adaptation` field, the `disconfirm` field, or the question each theme answers. Some of these still hold sentences the rule would flag, such as Completion ritual's question "How a room pays members no one could pay". `structure-C4.md` still prints them, and its prose lines are now stale beside `fourth/fourth.jsonl`. For the C5b packets I generate the declarations from the ledger, not from `structure-C4.md`.
- **The dimensions.** The eight dimension declarations were not read under the rule. D03 Maintenance says attribution decides between repair, forgiveness and retaliation, which the run's test contradicts. Pass 2 reads the eight under the same rule.
- **The record cannot show who placed a pixel.** I first wrote that no one could see who placed a pixel. That was a claim about the setting the contract does not state, and it is withdrawn wherever it appeared (Attribution, mapping-C3.jsonl).

**Slips, C5a-01.**
- **Two parallel writes to the same files.** Two amendment scripts that write `fourth/fourth.jsonl` and `tier_history.jsonl` (T4-015, T4-005) ran as parallel calls. Both writes landed, and the harness appears to have run them one after the other. Snap C5-move-developing-55 may or may not include T4-005's change.
- **Writes and their checks in one turn,** twice: the mapping Edit and the C3 validator, and the prose test's Write and its word count.
- **A malformed field.** The superseding F-016 line first carried `supersedes: 'F-016 (C3c)'`. The check refused it. It was fixed in place, and the writing script was fixed too.
- **A read twice.** The account's 44 quotes were served twice, once to measure the output and once to read it.
- **A wrong format for tier events.** The pass 1 line first listed tier events as 'ledger:id:event' strings. The check resolves ids, so the line was rewritten with the ids, and the writing script was fixed.
- **A no-op command.** One shell call only printed a word, which breaks the rule against no-op commands.
- **A hedge in the account.** The account said "in some rooms" for C02. It now gives F-013's count.
- **Parallel edits to one file, at the close.** The head's last four Edits ran as parallel calls. Each changed a different passage, and each reported success. The head was checked afterwards in a turn of its own.

## The close-check, C5a-01

`python3 tools/validate.py C5`, run after the notes body and before the head was rewritten:

```
stage C5:
  leg: build; passes 1, propositions 0, elements 30, arrows 21, history lines 89


0 errors (0 distinct shapes), 0 warnings
```

`done.sh C5` runs the same check at the close. Its report is in the leg's closing diary line.
