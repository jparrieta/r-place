# Lead running notes

## Before fleet dispatch

- Fresh run: `read.py ... state` reported cursor 0.
- Step 1 completed from `brief.md` and the full `openings.md` before the gate. The briefing describes ordinary recurring art, discussion, and weekly formats. The openings place the event among those formats: event threads begin with proposing and completing a Rainbow Dash image, continue through defense, template correction, neighboring-community approaches, additional pony images, and automation, and end with thanks, mementos, and retrospective posts. A separate moderator-led April Fools “best pony” schism also occupies the window and must remain distinct from the canvas event.
- The first attempt to record `step1_brief` used a shell here-document that the sandbox rejected before Python ran. I immediately recorded the stage with a direct foreground Python invocation and repeated the briefing read afterward.
- Gate: branch B; threshold 500; items_in_window 3264; chars_by_people 470654. Seven slices. Batch 01 spans `62ljzv` through `62qehq`, 66 threads and 426 in-window items.
- At collection, check event-named openings disposed out of scope, preserve the separation between the canvas and the room's own April Fools conduct, inspect appended timeline/lexicon lines as facts rather than readings, and record strikes and step-5 carryovers in the ledger.

## Batch 01 collected

- Collection reported 45 codes, timeline +2 lines, and lexicon +6 lines. The batch preflight supplied by the scheduler passed.
- The coder disposed all 66 slice threads, keeping seven. Event-titled threads were retained where served evidence supported them; the two deleted-body event posts were coded from their surviving titles.
- Facts-file review: no lines struck. The two timeline additions describe item-linked edit histories/status reports; the six lexicon additions are unglossed, item-linked local terms.
- Carry forward: Pinkie work redirected toward Rainbow Dash; Discord/Manechat coordination returning to Reddit; ongoing defense at the slice boundary; multiple participant accounts of damage; and the r/BerryTube lead. Preserve the distinction between canvas conduct and the room's separate April Fools jokes.

## Batch 02 collected

- Collection reported 37 codes, timeline +6 lines, and lexicon +4 lines. No facts-file lines were struck: timeline additions are item-linked edit/status facts, and lexicon additions are unglossed local terms.
- The slice inherits completed Rainbow Dash from batch 01 but shows “done” becoming maintenance: guarding shifts, ranked repair priorities, template circulation, neighbor agreements, and recurrent correction.
- Carry forward the `PONIES`-as-griefer-magnet tactic; guard vocabulary; reciprocal watching with r/halo and border talks with r/parahumans; competing templates and participant-reported bot conflict; coordination moving through Manechat/r/SaveDashie; and the unanswered Pinkie-with-OSU proposal.
- Data limitation: the coder reports display truncation inside the very large `62qfpd` full-thread response despite a second served call; it coded only visibly returned passages.

## Batch 03 collected

- Collection reported 26 codes, timeline +5 lines, and lexicon +4 lines.
- Struck the timeline line describing TheeLinker's purge as “mock”: that adjective interprets the episode as a joke rather than recording only a moderator action or edit. Retained the other four item-linked moderator/removal facts and all four unglossed lexicon terms. This strike must be reported in final `notes.md`.
- Carry forward: the GreenLattice arrangement and direct pixel help; moderation consolidating canvas posts while members distinguish repair from celebration; maintenance over expansion; shared auto-repair work moving to GitHub; and the room's distinct April Fools takeover with altered emotes/flairs and faction subreddits.
- Both canvas defense/tool work and the local styling joke remain unresolved at the slice boundary. Off-platform GreenLattice Discord and GitHub activity is visible only through what returns to Reddit.

## Batch 04 collected

- Collection reported 30 codes, six factual timeline entries plus a batch heading, and lexicon +4 lines. No lines struck: the timeline entries report item-linked moderator actions/reasons and participant answers, while the lexicon entries are unglossed local terms.
- Carry forward the tension between repeated alarm posts and moderator consolidation; the answer that a “done” title hides continuing maintenance; removals prompting r/SaveDashie; patrol/template/script/triage practices; the unresolved `PONIES!` dispute; Manechat coordination; and reciprocal watching with r/parahumans.
- Keep the inherited best-pony April Fools performance separate from canvas defense. Evidence from Manechat and r/SaveDashie remains limited to what participants return to Reddit.

## Batch 05 collected

- Collection reported 43 codes, five timeline facts plus a batch heading, and lexicon +3 lines.
- Struck the timeline line calling `630fm8` the end of a “separate April Fools moderator split”: that classification is a case reading, not a bare moderator/edit fact. Retained the other item-linked edits, redirects, and participant-reported decisions, plus all three unglossed lexicon terms. Report this strike in final `notes.md`.
- Carry forward: BerryTube recruiting Dashie defenders and reaching maintain mode; Manechat voting returning as a template; r/SaveDashie redirection; participant-reported neighbor settlements and reciprocal watching; r/parahumans adjacency becoming a fandom exchange; and the unresolved fixRD/bot dispute.
- The local April Fools reunion closes the staged split in its post while comments prolong the performance. Manechat and r/SaveDashie deliberation remain unseen except for returned templates and summaries.

## Batch 06 collected

- Collection reported 26 codes, two timeline facts plus a batch heading, and lexicon +3 lines. No lines struck: timeline additions are item-linked edit histories with attributed statements, and lexicon additions are unglossed participant terms.
- Carry forward the closed r/Halo request: conditional help, checking the neighbor's internal dispute, refusal, then withdrawal. Also carry inherited Mane Chat/template coordination, late addition proposals, and the distinction between scripts for defense and scripts for creating new art.
- The slice begins a participant retrospective about repair, scripts, distraction, and survival. Any claim that `PONIES!` protected Dashie must remain a participant explanation rather than a supported causal relation. Batch 07 must settle the final outcome.

## Batch 07 collected — fleet checkpoint

- Collection reported 35 codes, two timeline facts plus a batch heading, and lexicon +5 lines. No batch-07 lines were struck: the timeline additions are item-linked moderator actions and the lexicon additions are unglossed participant terms.
- Carry forward the immediate ending conversation: assessing stray pixels, thanking builders/defenders and neighbors, recounting exhaustion and disputed scripting, and calling the recognizable survival a success. Also carry the moderator removal/reversal between near-simultaneous final posts.
- The earlier Worm/MLP bargain produces an actual first-viewing report and a promise to continue. Defense memory becomes prints, orders, and timelapses. The main ending conversation closes, but memento fulfillment and crossover follow-through continue beyond the study boundary.
- Fleet complete: seven batches collected. Facts-file strikes across collection were the batch-03 line classifying `62t5hq` as a “mock” purge and the batch-05 line classifying `630fm8` as the end of a “separate April Fools moderator split.” Both were removed because they were readings rather than bare facts. No consolidation, pooling, themes, forest, audit gate, or steps 4–5 have begun; stop for scheduler checkpoint.

## After consolidation; before first close, forest, and audit

- Resumed after scheduler checkpoint. `tools/fleet.py consolidate` pooled 242 codes, 375 thread dispositions, and 70 pointers from all seven batches and wrote `package/codes_by_thread.md`; the lead journal now holds the fleet records.
- Next prescribed order: first `emit.close()`, forest from `package/codes.jsonl`, then `tools/audit_fleet.py`. If the audit fails, stop without theming.

## Before step 4 themes

- First close completed; forest built. Fleet audit PASSED: 242/242 live codes at offsets and on forest nodes, 70/70 pointers verified, 28/28 exclusion quotes verified, 375 dispositions across seven slices, and 85 coded threads represented.
- Consolidate incrementally in batches 01–07 using `package/codes_by_thread.md` with each slice case. Open themes from actual shared practices, extend them when later slices repeat them, and retain single-code themes where nothing else belongs. Record the grouping review explicitly.

## After step 4; before step 5 and counter-reading

- Read `package/codes_by_thread.md` slice by slice with all seven slice cases. Assigned all 242 codes once across 15 themes. Batches 01–02 founded mobilizing, target switching, off-platform coordination, template instruction, guarding, pixel priorities, neighbor reciprocity, local April Fools performance, completion/thanks, and bot dispute. Batch 03 added moderator consolidation; batch 05 added the Worm/MLP bargain and one single-code r/place comparison; batch 06 added participants' retrospective explanation; batch 07 added mementos/timelapse replay.
- Grouping review: codes were compared by shared practice, not shared words or adjacency. `PONIES!` codes split across prioritizing scarce pixels, live repair, and later retrospective explanation according to what speakers were doing. April Fools codes remain separate from canvas practice. The ordinary Art Battle comparison remains a single-code theme. No regrouping was needed after reviewing the full slice sequence; record this in final notes.
- One-sentence whole-case reading to test: the room turned an initially partly hidden pony build into a public, long-running maintenance effort organized through Reddit, Manechat/r/SaveDashie, templates, human guard shifts, neighbor agreements and disputed scripts, then made the defense into shared memory.
- Most consequential competing account, stated before search: the visible survival was chiefly automatic/scripted and off-platform, while the subreddit supplied alarms and celebration rather than consequential human coordination. If the reading is wrong, the record should contain participants saying bots did essentially all the preserving, human defense was unnecessary or abandoned, or the defense was pointless/not worth continuing; post-event talk should reject rather than claim collective work.
