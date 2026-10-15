# The declaration prose rule

Target length: about 700 words. The analyst wrote this rule before amending the 28 fourth-order declarations, and extended it to the eight dimensions before amending them. It is given here as written. You do not hold the files it names. Judge from what each sentence carries and from the quotes and findings in these packages.

## The rule, for the fourth-order themes

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

## The extension, for the dimensions

**The scope.** The declaration prose rule above now also reads the eight dimension declarations in `dimensions.jsonl`. It reads every sentence of the `construct` block's `changed` and `mistaken_for` fields that says something about these rooms or their members. The `question` and `predicate` fields define what the dimension gathers. They are read only for a claim about the rooms stated as fact.

**What stays the same.** The word classes, the four supports, the rewrite and the record are as in the rule above. A dimension amendment is a `tier_history.jsonl` line with `tier: dimension`, the old line as `was`, a logged move and a snap. Names and members do not change unless the members' declarations show that the dimension joins what its source keeps apart.

## The four setting facts

- Each account could place one pixel per interval.
- Anyone may change any pixel.
- Placement stopped at hour 73.
- No one holds authority over another's placing.
