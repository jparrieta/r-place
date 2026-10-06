---
title: "Aggregator contract v38: what to change and why"
date: 2026-09-22
status: proposal, no instrument built; §11 carries J's decisions of 2026-09-24; one coder instrument assumed since 2026-09-23 (§2 is stale on that point until rewritten)
target_length: 3,000 words
sources: the composition interview (ChatGPT, 19 Sept, turns 27 to 63), the memory branch (ChatGPT, 19 Sept, turns 23 to 51), the v37 handler log (CONTROL/handler-log, 21 to 22 Sept), the eighteen handbacks in 00_GIVE-THE-AGENT/out, HANDOVER_2026_09_22.md
---

# Aggregator contract v38: what to change and why

This note proposes changes to `CONTRACT-aggregator.md`, `STANDING-INSTRUCTIONS.md` and the stage
files of v37. It is written before any rewrite, as with v37. Nothing is built. Each change names
its source. Where I disagree with a source I say so.

Four things changed since v37 froze. The interview settled what composition means. The memory
branch settled how the analyst holds its state. The handler log measured what the run lost and to
what. The frame moved from 300 small rooms to 696, coded under two instruments.

## 1. The question and what composition means

**Replace the question in §1 with the one the interview settled.** The current question asks what
forms organizing took, how they differ, and which kept the work alive. It stays as the theory
question. Above it goes the method question, which is what the study tests (J, 2026-09-24: the
contract names them as the method RQ and the theory RQ):

> Can independently reconstructed case histories be composed into a shared dynamic account that
> supports explanations at successive levels of specificity, from population-wide patterns,
> through forms and subforms, to particular organizational histories, while retaining access to
> the evidence from which those explanations were developed?

**Rename the tiers after Gioia, Corley and Hamilton, with the numbering continued** (J,
2026-09-24). Five tiers, one table: first-order concepts and second-order themes from the coders
(the package's `code` and `case_theme`, the yard's `code` and `second_order`, both mapped at the
store build); third-order themes, fourth-order themes and aggregate dimensions from the analyst.
"Case theme", "chunk" and "third-order chunk" go from the contract, the tools, the store fields and
the stage-18 scripts in one sweep, with a rename table in the change log, because the naming trap of
v37 came from exactly this seam. The paper says which tier each agent built. The rule that bans
construct names moves with its tier: it binds the third-order tier.

**Add to §3 the direction of construction against the direction of explanation.** Construction runs
upward: first-order concepts to second-order themes to third-order themes to fourth-order themes to
dimensions to arrows. Once built,
the account is examined in both directions. Descending must reveal more specific process, not more
quotations. The waterfall sentence belongs in the contract in J's words: continuity at the top,
drops at the bottom, a model all the way down, and the lower levels end up describing decline and
continuity.

**Add what a form is.** Organizations of one form handle organizing problems in similar ways, not
with identical actions or trajectories. A form may bind some aspects tightly and leave others free;
the contract asks for both, what members share and where they may differ without ceasing to
exemplify the form. Distinguish variation a form accommodates, recurring differences that warrant
a subform, and particulars that belong to one history. Never cut a category so that every case
gets its own label.

**Add the composition check in both directions.** Toward the leaves, each step adds warranted
specificity without contradicting the level above. Toward the population, the detailed accounts
together support the broad pattern and preserve the distinctions the population's diversity needs.
A collection of case accounts does not establish composition; nor does a taxonomy in which every
case has a place.

**Prediction stays secondary.** A counterfactual at the leaf may borrow from a neighbouring leaf
that met the phenomenon, with the shared mechanism and the uncertainty explicit. It is a use of the
account, not a condition of composition.

## 2. The frame (§4)

§4 is written for 300 small rooms at 2 per cent of the population's text. That is no longer the
run. **Rewrite §4 for 696 rooms and two coder instruments.**

- The population is the atlas-resolved census, `MASTER-census.csv`, 696 rows. The analysed set is
  at most 623, less the three `none` rooms, which are absent from the census. The eleven package
  `trace` rooms stay in; verdict is the wrong filter, case-theme count is the right one.
- Two coder instruments produced the material: the package (v16 to v27, Claude) and the yard (v30,
  GPT-5.6 Sol). They share no room. `coder_version.csv` is the join. The contract must name
  `coder_version` as a covariate that is never a feature, in the same words rule 7 uses for the
  canvas: nothing is clustered, cut, placed or measured for distance on it, and every population
  figure is reported split by it before it is reported whole.
- The two codebooks scale differently. `log(codes) ~ log(items)` has slope 0.729 in the package and
  0.293 in the yard; the yard's theme count is flat at about fourteen from 729 items to 2,918. §4's
  ban on raw counts across communities gets that second reason: a count that tracks corpus size in
  one codebook and not the other is not a property of the communities.
- The yard's `themes.jsonl` labels its case theme `second_order`. The store build maps it to
  `case_theme` before the analyst sees it; the analyst never sees the yard's field name.
- The scope sentence no longer says "the smallest rooms". It says: 623 of 696, under two
  instruments, with the venues outside the atlas not in the frame.
- The denominator question goes into the contract: membership is reported over the trimmed and
  the full analysed set side by side, and "N of M communities" says what M holds.

## 3. Stage 10, rewritten as the return to the cases

The interview gave stage 10 a job the v37 file does not ask for. At present stage 10 returns a
verdict per room: composes, composes with residue, does not compose, cannot tell. **Keep the verdict.
Add the adaptation ledger.** For each room the analyst, or the fleet holding the fixed model, asks:

> What must be specified, elaborated or corrected for this model to explain how this organization
> worked?

Each answer is a line in `adaptations.jsonl` with the claim in the shared model it touches, the
case evidence through `cite()` or a forest transition, the change, its kind, and what the change
explains. Three kinds, and the contract keeps them apart:

| kind | what it means |
|---|---|
| specification | how a shared process operates here: who, with what, under what condition |
| elaboration | a finer process or condition the shared account leaves open; a candidate subform |
| correction | a claim the case contradicts, or a scope the case restricts |

The adaptation shelf has two tiers, as the model-building shelf does (J, 2026-09-24: the analyst
keeps its freedom; the read tier stays small). Read, shipped with stage 10: Fisher and Aguinis
(2017), whose seven tactics are the source of the operation vocabulary, and Busse, Kach and
Wagner (2017), whose amend-against-bound distinction is the difference between `contradict` and
`restrict`. Available on request through `mem.py shelf`, one line each, never pushed: Vaughan
(1992), Ketokivi and Choi (2014), Sætre and Van de Ven (2021), Makadok, Burton and Barney (2018),
Welch et al. (2022), Eisenhardt (2021), Ragin (2023), Robinson (1951), Turner (1953), Lakatos
(1970). The stage-07 read tier stays Gioia, Corley and Hamilton; Grodal, Anteby and Holm (from
02); Eisenhardt (1989); Langley (1999). For the hierarchy at 11 and 12, read: Doty and Glick
(1994), for what a type must contain before it is theory, with the caution that prediction from
fit to type stays secondary here; and the emergence section of Kozlowski and Klein (2000), for the
words for the levels. On request: McKelvey (1975), Rich (1992), Grimm et al. (2005), Gray, Bryant
and Greenhill (2010), Hsu and Hannan (2005). J, 2026-09-24:
cross-case analysis is the way back down to the field.

Calling all three corrections would hide the difference between an abstraction that wants detail
and an explanation that is wrong. Rule 12 already says a room that does not compose bounds the
model once a second room names the condition. The ledger is how that rule gets its evidence.

**Two outputs per room** (J, 2026-09-24). A room model, `model-10.md`: the case lead's `case.md`
rewritten in the global model's vocabulary, element ids where the model applies, plain names where
it does not, `cite()` on every claim. And the adaptations as the diff between that room model and
the global model: each line names the element (C3), the operation, the condition, the evidence
codes, one sentence on what it explains, and its kind. The reconstruction test at stage 18:
global plus adaptations, rebuilt and compared with the room model by a reader. The blind
`case.md` and the informed `model-10.md` are kept as a pair for the audit. How it runs (J,
2026-09-24): every room's coder documents are copied into the fork before the run; at stage 10 the
aggregator's build leg writes `out/handoff-10/` (a `RETURN-10.md`, one labeler task per room with
the coder documents, the global model packet and the id vocabulary, and one handler brief); the
adaptation handler runs it in OpenAI Codex; returns land in `DROPS/10/<sub>/` and the check leg
validates and ingests them. Labelers are fresh GPT sessions holding the room's full coder record.
The yard is not touched at run time.

**Three legs.** 10a, the build: packets and the handoff folder. 10b, the Codex handoff. 10c, the
adjudication: the aggregator receives every room's adaptations, validated and ingested, and reads
them by element, never as a list. `mem.py adaptations --element <id>` returns the lines touching
one element across rooms; a rooms by elements view is built first. One leg per element group with
bounded packets; each line accepted, modified or rejected with reasons into `adjudications.jsonl`;
a correction met in two rooms revises the model in the same leg, logs the move to `tier_history`
and forces a cut. Unattached lines (touching no element) become candidate subforms or particulars.
Stage 11 clusters the adjudicated ledger; the reconstruction sample at 18 uses it too.

**The guard against exception-stacking.** This is the one thing the interview left open, and the
contract must settle it rather than leave it to the analyst. Three conditions make an adaptation
count:

1. It names a code or a transition, through the logged tools.
2. It is stated as a condition another room could meet. An adaptation that can only be stated with
   the room's name in it is a particular, and is filed as one.
3. A correction met in two rooms goes back into the shared model in the same pass, and the model's
   affected findings are re-examined under rule 14.

And one report: per pass, the count of particulars against the count of shared-model revisions.
A model whose adaptations are all particulars has not composed. It has a heap of exceptions, and
the stage says so in those words.

**The coder review.** J's proposal from the parent chat: return each room's working model to a
branch of the coder that read the room, from its checkpoint before it met the shared model, with
its threads restored, and ask for an evidence-supported critique, not a score. The instruction is
not "defend your coding"; the record outranks both readings. The aggregator accepts, modifies or
rejects each proposed change with reasons; recurring elaborations feed the subforms. Two limits go
in the contract. The reviews are development record, not validation, so the human audit samples
approved claims as well as disputes. And the review needs a coder checkpoint: the yard keeps one
per room (331 compressed case-lead stores today), the package does not. The contract names which
rooms it covers.

## 4. The taxonomies (stages 11, 12, 16, 17)

The interview moved the taxonomy. J: "I would rather do a taxonomy of model similarities, with
corrections and elaborations. That is the taxonomy." And: the problem dendrogram "is not great",
the third-order chunks "less solid". The handler log agrees on the numbers: the v37 problem
partition carries volume (Spearman 0.774 between active problems and cells in scope), half the
communities sit on one profile, and the declared null put the verdict at percentile 100.0 where a
volume-holding null puts it at 1.7.

**Stage 11 becomes the taxonomy from adaptations.** Rooms belong together when their working models
share processes and required the same elaborations. Subforms are recurring elaborations. The unit
is the adaptation ledger, not a chunk share. This is the aggregator's own act, in J's earlier
ruling: the clusters are yours, no blind cluster maker. The dendrogram is a readable view of it, not
its structure: two forms may share one finer process, and the contract should allow cross-links.

**The chunk-share dendrogram and the problem dendrogram become supplementary views.** They stay at
their stages, with three changes from the handler log:

- The volume-holding null is declared first, in every stage that asks for a percentile. It moved
  the stage 17 ARI from the 0.1st percentile to the 34.4th. Nothing in v37 required it.
- A stage that clusters a 0/1 table reports the occupancy of its feature space before it cuts:
  profiles occupied, share on the largest, share of pairs at distance zero.
- Stage 11's two rulings go into the stage file as method: first-order code shares per chunk with a
  Dirichlet-multinomial shrinkage and no zero replacement; 200 resamples and 100 permuted copies
  per k, mean and median margins, two seeds.

Neither supplementary view determines the taxonomy or the composition verdict. The contract says
so in one sentence, because the interview's last correction was exactly that the problem clustering
had been conflated with composition.

## 5. Memory and the shape of the run

The memory branch's diagnosis holds against the v37 files: the standing instructions load four
files at every stage start, and two of them grow without bound. `rooms_index.md` was 200 KB by
stage 17 and the analyst read part of it. **Replace the startup rule.**

- At stage start the analyst reads `_head.md`, the stage file, and runs `validate.py --open`.
  Nothing else by default.
- `rooms_index.md` and `findings.jsonl` are queried, not read: `mem.py note <sub>` exists; add
  `mem.py finding <id>` and `mem.py findings --touching <element>`.
- `_head.md` gets a ceiling, about 1,500 words, and a section the v37 spec lacks: the unresolved
  distinctions, each with the file that holds the argument. The head is a narrative of the
  argument, not a checklist. The rest of the v37 spec stays.
- Unresolved distinctions get their own files, `out/_questions/<slug>.md`: the competing readings,
  the supporting and contrary rooms, what would settle it. The head links them. This is the unit
  of thinking on disk for anything open across a stage boundary, and the file a reviewer opens to
  see the argument in progress.
- Stages 13 to 15 get a crossing head, `_head-crossing.md`, written by the analyst at the close of
  stage 12, holding the crossing's state and nothing of the model. The main head is not read at
  13 to 15. The v37 rule that withholds `rooms_index.md` and `findings.jsonl` but requires the head
  and diary reintroduces what it withholds; the branch made that point and the files confirm it.
- **The data structure as one file.** `_views/data-structure.md` and `.tsv`, regenerated by
  `mem.py` at every leg close from the store: representative quote(s), first-order concept,
  second-order theme, third-order theme, fourth-order theme, aggregate dimension, one row per
  first-order concept, at least one quote per concept through `cite()`, more where the store holds
  them. Never hand-edited. The paper's data-structure figure is a sample of its rows; the full file
  is the supplement. If the coders' `codes.jsonl` carries the excerpt, the quotes are a join; if
  not, one fleet leg fills them before stage 02.
- One line in the standing instructions: a single `Read` may return a truncated file without saying
  so; page it or read it with Bash. That line was absent and cost 21 reader attempts.

**On compaction against legs I side with the handler log, not the branch.** The branch settled on
compaction as the default to keep the red thread. The run's ledger says a long session costs ten
to fifteen times more per output token than a short leg, and J introduced the leg split at stage
14 after watching the analyst compact repeatedly inside one leg. The head and the diary make a leg
survivable, and they exist. So: every fleet stage is three launches, build, dispatch, check, and
the dispatch launch reads nothing for meaning. Stages 01 and 02 are legged at declared room
boundaries. The model stages 07 to 09 may share a session: the loop needs continuity and their
cache ratio was tolerable. Compaction guidance goes into `CLAUDE.md` for the sessions that do
compact: preserve the question, the current account, the reasons for revisions, the contrary rooms
and the next comparison; reconcile the head after.

## 6. The fan-out (§7)

Every item here is from the handler log and has a ruling behind it.

- **One return specification per stage**, `RETURN-NN.md`, frozen with the stage file. The packet
  builder emits it verbatim, the brief cites it, and the validator's per-stage schema is generated
  from it. Two documents asking for different fields produced 95 per cent of stage 14's errors.
- **A packet ceiling in bytes**, about 50 KB against the reading tool, asserted in `packets.py`,
  with an end-of-packet marker and one line telling the reader to confirm it reached the marker.
- **Answer keys outside the readers' directory**, served to the scorer. If that cannot be arranged,
  the stage 03 instruction goes in every fleet stage and the harness greps reader transcripts at
  dispatch close.
- **When reissues are exhausted**: stop, diagnose, rebuild the packets. The stage file says so, so
  the answer does not come from a launch line.
- **Keys.** A return line is keyed on packet heading and cell number; the typed theme id is a label.
  Support resolves on `(community, code_id)`: the store holds 27,933 codes under 580 distinct ids,
  so the v37 check passed more than it looked.
- **Stage 15 specifies the panel and the overlap sample from the start**: sixteen adjudicators is
  what 937 cells took, and an adjudication without an agreement measure is not one. The overlap is
  built in the same launch as the packets, before any adjudicator has seen `crossing.jsonl`.
- **The modifier rule.** `goal` and `exception` do not require a gate; `hard_to_place` with no
  problem on is a real state. The brief and the checker disagreed on this at 13 and 15.
- **Serving arm declared** on both sides of any cross-stage reliability comparison. Fleets go to the
  cheap arm by default: 87 per cent of the metered tokens for 12 per cent of the cost.
- **Cells used for a brief's worked examples leave fidelity and transmission.** Fourteen of the 25
  cells behind v37's brief edits sat in the transmission rows.

## 7. Rules

- **Rule 1.** The sanctioned exception at stages 11 and 12 routes through `mem.py room <sub>
  --no-canvas --stage NN`, so the read log exists even for one room.
- **Rule 14.** `findings.jsonl` is append-only; a revision is a new line carrying the id it
  supersedes. Twenty-five of 136 snaps held a findings file that was not a prefix of the current
  one. `defects.jsonl` carries a stage field, enforced at write.
- **New rule, counts.** A count asserted in any file was computed in the same act, from the file
  that governs. Where a manifest exists the manifest is the number. This binds the analyst, the
  handler and the operator alike; six handler numbers were wrong and all six were second-hand.
- **New rule, amendments.** A launch line or addendum that permits what a stage file forbids names
  the provision it overrides. If it names none it is advice. Stop writing addenda: one document per
  stage, versioned, hashed in the checkpoint, amendable before launch.
- **New rule, snaps.** Snaps are harness-owned and write-once, the harness writes the snap line into
  the snapped file, and no stage requires a snapped file to grow afterwards; projections go in
  their own file. Two of v37's four ordering claims cannot be proved because the analyst deleted a
  snap and took another.
- **New check.** Where a stage requires a file to change, the close-check hashes it against the
  previous stage's copy and fails on equality. Stage 09 renamed the data structure and nothing
  noticed.
- **The budget paragraph goes.** Replace it with a reporting requirement: `done.sh` writes the
  stage's tokens, main and subagents, into `RUN.json` at every close.

## 8. Stage 18

The audit worked. Three changes. Its floor is declared in the stage file, not decided by what fits:
the transcripts are computed over with named scripts, and the transition ledger and the stage
files are in or out of scope in writing. The unplaced case themes are read: 290 of 2,703 held no
placement in v37, 6.8 per cent of the codes, and nobody read them. The audit samples the
adaptation ledger source-first, disputed and approved lines alike: the human audit the proposal
promises.

## 9. What does not change

The fence, including what it did with a forged system-reminder. The second-order tier's ban on
construct names. No number at any tier. Rule 13 on what a challenge decides. R = 2. Rule 7 as
rewritten for v37. The head and the diary as standing instructions. `done.sh --force` hard to reach.
The stage-01 reading of every room whole: selective retrieval serves reconsideration and never
replaces coverage.

## 10. Where I disagree with the sources

With the branch, on compaction as the default; see §5. With the branch's 200, 2,000, 20,000 word
tiers: a filing convention, and the contract should carry only the two ceilings the run measured
against, the head and the packet. With GPT's proposal paragraph on the coder review, which promises
it for "each proposed case model": yard rooms only. With the handler log I have no disagreement; I
left out what belongs to the harness alone.

## 11. Decisions that are J's

Answered 2026-09-24.

1. **Case-theme dendrogram: kept**, as the supplementary view at 11 and 17. The one to keep is
   the stage-11 second run from the handler's rulings: first-order code shares per chunk,
   Dirichlet-multinomial shrinkage, no zero replacement, two seeds. The crossing's dendrogram was
   cut on 0/1 truth tables over four problems, which allows at most sixteen profiles and put half
   the communities on one; that, and the volume it carried, is why it read poorly. If a problem
   view is ever rebuilt it is on normalised counts, never on truth tables.
2. **Coder review and adaptation are one fleet stage.** The labeler, a fresh GPT session holding the
   room's coder documents, is given a deep, layered packet of the global model (head, model, the wiki pages it
   touches, the id vocabulary), and asked what must be specified, elaborated or corrected for the
   model to explain its community, as typed operations on model elements. The aggregator does
   not write 696 ledgers; it adjudicates them, accepts, modifies or rejects with reasons, and
   revises the shared model on corrections met twice. This stage takes the budget the crossing
   took. Cross-model by construction: GPT-5.6 Sol case leads, Claude analyst.
3. **N is set when coding closes.** Until then the frame is a dated copy of everything coded in
   the yard and in Layer Fork / the Jail, hashed. "N of M" is reported over that copy.
4. **Layer B venues: not in this frame.**
5. **The crossing is an add-on after the last stage**, run only if wanted, as a stage the run can
   reopen for. What stays inside the run is the multi-level description: stage 11 clusters the
   adaptations, and for each branch the analyst writes what the branch does, what it does
   differently from the global model, the codes it employs, and how representative members do the
   work. Room = branch model plus residual particulars.
6. **No holdout** (2026-09-24). Held-out rooms would need placement into the scheme before they
   could be routed up the table, and holding them out touches every stage. The return at stage 10
   is in-sample at the second-order tier and out-of-sample below it; the methods say so, and the
   triage's item 1 stands as a stated limitation, not a design change.
