# Case-lead notes

branch B; threshold 500; items_in_window 19914; chars_by_people 2785634

## What was hard

The hardest distinction was between a post that recruited for a canvas mark and evidence that participants actually maintained it. Logo, King and Wizard vocabulary recurred, but repetition alone did not make them one practice or establish completion. I retained proposals as calls, kept Wizard labour separate, and treated the Princess as sustained only where instructions, progress, repair or defence were explicit.

The Tool-logo exchange required special care: “abandon that space” refers to the failed logo location, whereas “shouldn't abandon the princess” explicitly protects the Princess. I did not turn those contrasting speakers into a claim that the community changed its mind. The final Princess image posts are participant presentations; because their images are unavailable, I did not treat “beautiful” or “almost finished” as independent visual findings.

## Data problems

The header says threads are not whole and reports 1,838 deleted or removed items across the wider corpus. The forest contains five orphaned items and 103 substantial uncoded stretches in coded items. Images, templates and screenshots were not fetched, so designs and final appearance cannot be verified. Discord was used for coordination, but only Reddit invitations and reports return to this record; the decisions inside Discord are unseen.

Branch B divides the week into arbitrary whole-thread slices. No single coder read the whole week, there is no inter-reader agreement measure, and a reply in an old thread can occur long after the slice's opening boundary. I therefore used adjacency only for sequence and put relations in the account only where the later passage answers, names or recalls the earlier practice.

## Fact-file review

All 43 batches' additions to `out/timeline.md` and `out/lexicon.md` were reviewed at collection. Fifty-two timeline lines were struck because they interpreted what edited items were doing instead of recording a bare edit fact: `dfnqdmf`, `dfoqg1n`, `dfoqkez`, `dfot67r`, `dfp48mf`, `dfozjcd`, `dfp0gwm`, `62thtd`, `62tnl1`, `dfprdkn`, `62twvp`, `62u4r0`, `62v3x7`, `dfpd30w`, `62vc9q`, `62vhcq`, `62vnya`, `dfpge0j`, `dfq473e`, `dfrp23q`, `62w8t2`, `62wlla`, `62x0po`, `62x6pi`, `62x8mo`, `62xbs5`, `dfpsye6`, `62xu9g`, `62xzfa`, `62y1p5`, `62y37d`, `62ymlk`, `dfq1633`, `dfq4sal`, `62zygk`, `dfqmmtz`, `dfqmcdl`, `dfqmlhi`, `631mtv`, `631t9z`, `dft3obe`, `632cu9`, `6355su`, `635fl9`, `dfrl4ud`, `dfth66b`, `dfthcpa`, `dfthfhk`, `dfthmw9`, `dfthy8o`, `dftimdj`, and `dftip4f`. Retained timeline entries are direct moderator, automation or participant-action facts; retained lexicon entries are unglossed participant terms with first-use IDs. Batch-by-batch decisions remain in `out/ledger.md` and `out/_lead_notes.md`.

## Grouping review

I regrouped after reviewing the pooled codes. An initial broad April Fools grouping was split into making fake news, swapping subreddit presentations, and renaming people on Discord because these are different practices despite shared timing and vocabulary. An initial canvas grouping was split into calling for marks, teaching newcomers, constructing the Princess, constructing the Wizard, and negotiating with neighbours. Post-event Princess accounting was separated from jokes under images. All regroupings are recorded in the themes' `regrouped_from` fields, and every live code is assigned once.

The two themes that nearly merged were “calling people to put Clash Royale marks on the canvas” and “building and defending our Princess”; what kept them apart was the difference between proposing/recruiting for possible emblems and reporting hands-on construction, repair or defence of one continuing image.

Code I would defend hardest: “asking everybody to make at least three grey blocks to complete our princess” (`c0412`). Thinnest code kept: “posting fake r/Place humour” (`c0439`).

## Counter-reading audit

Before searching I stated the alternative that the logo, King or Wizard became the sustained project while the Princess was abandoned or peripheral, and that contrary evidence should contain later repair, defence, completion or credit for those alternatives plus rejection of the Princess. The logged broad search was noisy, so I narrowed it to project terms paired with canvas terms and then to explicit completion, defence and abandonment language. I inspected relevant hits through `read.py item`.

The strongest contrary item was `dfrrtwj`, “Help make CR logo!”, at H+70.46. It showed that logo recruitment persisted late and was coded at step 5 as `c0452`, then added to the existing call-for-marks theme. The same thread, `630lvc`, had already been read whole by its fleet coder, so no late `read thread` was required and no thread disposition changed. The searches returned explicit abandonment of the Tool-logo location (`dfr4p61`, `dfr4qj3`) and explicit resistance to abandoning the Princess (`dfr94zc`), but no textual claim of completed, sustained or post-event-owned logo, King or Wizard work. That null result is limited to the logged queries and partial textual corpus; it does not establish absence from the canvas or Discord.

## Anomalies and leads

The logo petition `6373yj` followed the late logo link in `dfrrtwj` by 58 seconds, but neither names the other, so I reported a sequence rather than a causal relation. The two takeover calls `62zdu3` and `62ze1s` are likewise 91 seconds apart without a textual link. The post-event Princess titles claim ownership and near completion while their comment layers mostly consolidate or joke; this is useful evidence of retrospective identity, not image verification.

The first shell attempt at the lead's initial close used a here-document that the environment refused before Python ran. The chained forest command nevertheless executed. I confirmed that no close was journalled, recovered with a direct Python invocation, rebuilt the authoritative forest, and then ran the gate. The gate passed. This operational difficulty did not alter evidence or append-only records.

## Complaints

The branch-B design makes whole-case relations laborious because related comments stay with an old thread while slice ordering follows first in-window thread appearance. The rule is workable only with the forest and explicit cross-slice restraint. Image-bearing posts are especially frustrating: strong participant claims survive, but the visual object needed to assess them does not. The search tool reports lexical matches rather than analytical relevance, so broad queries produce many game-mechanics false positives; narrowing was necessary and is visible in the query log.

## How the reading held up

- I did not code or write relations from memory of a raw thread. I used the pooled code file, slice cases, forest, pointers, and `read.py item` for counter-reading hits.
- I went back to batches 11, 13, 15, 19, 23, 25, 26, 29, 31, 33, 35–38 because I needed their exact posts-against-comments contrasts, not because I was substituting memory.
- Earlier slices became less distinct while the late canvas slices remained sharper; the ordered pooled-code pass and forest reread restored the early April Fools and first-canvas sequence.
- The run was interrupted at the scheduler's required checkpoint after batch 43. On resume I read `out/_lead_notes.md`, `out/ledger.md`, the contracts, the pooled slice cases and codes, and followed the prescribed consolidate/close/forest/gate order before theming.
- The first 43-slice collection itself was scheduler-paced across turns. The ledger and lead notes, rather than conversational memory, carried each slice's fact-file review and open edge forward.

## Complete-record check

The account contains all eight required headings in order and cites each item or thread ID individually in backticks. Episode endpoints are individually cited, quotations are readable, and all reported times and intervals come from `package/tree_index.json` through `_lead_times.py` or from a slice coder's recorded figure. Descriptive contrasts, participant explanations and supported response relations are labelled separately; adjacency-only pairs are sequences.

Every disposed `coded` thread retains at least one live code. Every read `out_of_scope` thread with ten or more in-window items retains the exact exclusion citation required by the instrument. The late counter-reading code is attached to exactly one existing theme. The branch line above was copied from the final reread of `out/_gate.json`. Final machine preflight is run after the verdict close; any reported failure is repaired and the complete preflight rerun.
