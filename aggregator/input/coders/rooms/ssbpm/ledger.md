# ledger — r/ssbpm

The case lead's memory of the fleet, kept by the harness at every `collect` and extended by the lead by hand under each entry. A fork's lead reads it first. Nothing here is a code or a citation; it is what each slice left open, what its coder flagged, and what the lead decided at the time.

## batch 01  hours +0.11 to +53.53  threads 85  (collected 2026-09-07T23:00:57Z)

- disposed 85: coded 17, out of scope 68; codes 90; pointers 7
- coded threads: 61rig3, 62qtid, 62qtuk, 62qwmm, 62qwpi, 62qyzc, 62riv6, 62s9qq, 62sgbw, 62sj3j, 62twx2, 62u1g8, 62uk3z, 62xcgw, 62yzmk, 6316ed, 631xzk
- timeline.md +16: ## added from batch 01 | - d0 03-31 21:08 [edited] comment by Drinkingfood in an Ice Climbers technique thread (dfo1a5l) | - d0 03-31 21:52 [edited] post by Oracle_TX: Player Overview and Watch Guide for Shuffle (62of68) | - d0 04-01 03:20 [edited] comment by InfinityCollision in the Smashbox FAQ (dfohcox) | - d0 04-01 04:24 [edited] comment by InfinityCollision in the Smashbox FAQ (dfojlh7) | - d0 04-01 05:17 [edited; body removed] post by Baz135: Draw the PM logo on /r/place? (62qtuk) | - d1 04-01 21:54 [edited] post by Midnight_B1u3: Battle of BC will host Project M at 600 entrants (6 | - d1 04-02 00:44 [edited] comment by josephgee asking for a mock-up and location (dfpn2zc) | - d1 04-02 01:12 [edited] comment by josephgee about a 20x20 M (dfpo71p) | - d1 04-02 01:59 [edited] comment by josephgee comparing the Melee area and blue corner (dfpq0ed) | - d1 04-02 02:45 [edited] post by NachoBait: Help with adding my own music to stages/menus (62xcgw) | - d1 04-02 07:35 [edited] post by sabreknight: March PM Content Recap (62ygsc) | - d1 04-02 09:00 [edited] post by DarkLeviathan8: My personnal character appreciation Tier List (62y | - d2 04-02 16:15 [edited] comment by chirouDown offering a Project M pixel map (dfqcne3) | - d2 04-02 17:32 [edited] comment by chirouDown reporting placed blocks and opening Discord coordina | - d2 04-02 17:47 [edited] comment by chirouDown supplying the Discord invite (dfqgu16)
- lexicon.md +5: - SPOTW (dfolq4a) | - Wumbo (dfoujlp) | - Project Melee (62riv6) | - blue corner (dfpq0ed) | - green lattice (62yzmk)

**Coder's final message.** r/ssbpm, batch 01. Start edge: first slice, no inherited opening. End edge: logo/Discord coordination and sidebar restoration remain unresolved. Blockers: one full-thread display was truncated; one pointer’s cited target is correct but its code association is wrong and append-only controls prevented correction.

**Episodes the coder tagged [unresolved] or [inherited]** (from its case.md):
- The canvas first enters this slice at d0 04-01 02:40 inside the standing Weekly Discussion Thread. Baz135 proposes, “Hey guys we should build a PM logo on /r/place” (`dfoftln`). The first exchange establishes both willingness and an organizing problem: Nib105N05 asks where the effort will be organiz
- At d0 04-01 08:22, a moderator-operated post explicitly invites discussion of the “Project Melee Subreddit Style” (`62riv6`). Commenters recognize the CSS as an April Fools joke, praise it, compare it with the Melee sub’s style, pretend it is serious, and thank Gimr (`dfopyw1`, `dfoqj69`, `dforypf`,
- At d1 04-02 10:32, `62yzmk` renews the canvas effort by asking the room to “leave our mark on place” and reporting black-square placement under “green lattice.” Participants say they need coordination, prioritize completing the M, call for a pixel map and possibly a new location, propose map sizes, 
- One bodyless image post at d2 04-02 20:13 says only “I found Spooderman!!!” (`631xzk`). Its timing and wording could fit a canvas discovery, but the citable record does not say so. An accessible caption or body establishing where Spooderman was found would settle it. [unresolved]
- The moderator’s CSS discussion post invites likes and dislikes; replies identify the source style, praise the work, request durable elements, and later request the original sidebar (`62riv6`, `dforypf`, `dfp4row`, `62twx2`, `dfr8r0o`). The invitation is explicit, but the corpus does not show whether

**Anomalies and leads** (from its notes.md):
Final QA found that the first strawpoll code label relied on `62s9qq`'s title while its cited span was only the URL. I appended a retraction for `c0044` and emitted a replacement limited to `linking a strawpoll`. The first `r/smashbros` pointer also carries `c0044` because of an adjacent zero-index association error in the call batch; a corrected duplicate pointer was refused by the one-pointer-per-target guard, and the pointer API exposes no retraction. Its cited `r/smashbros` passage, raw target, normalization, thread, and relation remain correct; only that `code_ids` association is wrong. The relevant CSS/sidebar code is `c0043`.

The logo effort appears twice before the dedicated planning thread: first in the WDT (`dfoftln`) and then as a removed-body dedicated post (`62qtuk`). Later threads develop mock-ups, colors, locations, placed starting pixels, relocation, and Discord movement. A later slice should look for the outcome without assuming success.

The CSS joke generated practical requests that outlasted the gag: keeping the sidebar/top bar, retaining visible flair text, and later restoring the original sidebar links. Those requests may be useful leads for whether temporary joke infrastructure became permanent.

The brief was useful for recognizing WDT/DDT and ordinary Project M vernacular, but its claims about stable roles and recurring formats came from a deliberately partial earlier-week reading. I did not extend those claims beyond the passages served here.

**Data problems** (from its notes.md):
The full `61rig3` response was transport-truncated in the shell display even though `read` logged the whole thread as served. The visible beginning, ending, triage window, and all passages later cited were available, but a middle segment was not displayed. I did not retrieve the corpus by another route. This limits confidence that every in-window non-event turn in that selected mixed thread was seen on screen.

The corpus header reports that not every reply parent is present and that deleted or removed text exists. In the selected material, `62qtuk` has a surviving r/place title but a removed body; `62yzmk` contains deleted replies; and `631xzk` is a bodyless image post. None was reconstructed.

Each Python invocation emitted a macOS cache warning saying it could not create an `xcrun` cache file in `/tmp`. The calls still completed, and I wrote no working state outside this run directory.

**Lead's strikes and remarks at collect:** (the lead writes here: which facts lines it struck and why, what it will carry to step 5; nothing else)

- Struck six timeline lines (`dfpn2zc`, `dfpo71p`, `dfpq0ed`, `dfqcne3`, `dfqg4gl`, `dfqgu16`): their descriptions interpret what edited comments were doing rather than recording only the edit metadata. No lexicon lines were struck; all five are unglossed participant terms with first-use item ids.
- Carry to step 5: the unresolved outcome of the logo effort and Discord move; the distinction between the subreddit CSS joke and canvas conduct; the bodyless `631xzk` ambiguity; the possible survival of temporary CSS/sidebar changes; the truncated display of `61rig3`; and the incorrect code association on the otherwise grounded `r/smashbros` pointer.
## batch 02  hours +56.09 to +95.07  threads 23  (collected 2026-09-07T23:17:38Z)

- disposed 23: coded 3, out of scope 20; codes 56; pointers 17
- coded threads: 6339jx, 634grb, 6395tc
- timeline.md +3: ## added from batch 02 | - d2 04-03 00:07 [edited] post by Baz135: Building the PM logo on /r/place is starting to come along | - d3 04-03 19:52 [edited] post by Baz135: Final /r/Place image (6395tc)
- lexicon.md +6: - maintenance duty (6339jx) | - black void (dfr8gst) | - OL (dfr9v64) | - Manning face (dfrhfy7) | - pixeling (dfsfwcg) | - Shroomy (dfsg4lh)

**Coder's final message.** r/ssbpm, batch 02 complete.  Opening edge: inherited.   Closing edge: event action closed; post-event discussion unresolved beyond the window.   Blocked: nothing.

**Episodes the coder tagged [unresolved] or [inherited]** (from its case.md):
- The slice first reaches r/place at d2 04-03 00:07, when an already-running effort is “starting to come along.” The main thread recruits more people to build “just the M,” supplies a location, layout, Discord, timestamped progress, and agreements protecting rainbow letters and a checkered pattern. Re
- A short companion post at d2 04-03 04:01 tells participants not to white out the part of their spot promised to r/rainbowroad; the author then corrects a mistyped community name after an automatic account exposes it (634grb–dfr9zfv). It is one enforcement turn inside the inherited build. [inherited]
- At d3 04-03 19:52, after placement has closed, a final-image post celebrates that the M survived and credits the people who organized, built, and defended it. The comments reconstruct a forced link relocation after r/manningplace expanded beneath them, record that a proposed second move failed for l
- The build’s small scope answers perceived limits: Pseudogenesis recalls thinking the plans were a lost cause “given the size of the sub,” then praises “being realistic and sticking with just the M” (dfrh6gv). That passage explicitly connects the smaller plan to the community’s size. [inherited]
- The insistence on rainbow letters answers a negotiated threat. The opening says rainbow agreed only because the letters would be filled in rainbow and might otherwise “eat through it” (6339jx); when white letters are later proposed for readability (dfrh6gv), Baz135 answers that Rainbow Road might “p
- The slice does not show the passage that first chose the location, the M, Discord, or the rainbow deal. Their appearance before this slice is visible only as already-established instructions and the earlier-slice facts supplied in the timeline, so no causal link is claimed for those beginnings. [unr

**Anomalies and leads** (from its notes.md):
The opening building post calls ChirouDown an organizer and later comments call ChirouDown and Baz135 “mods,” but neither item is moderator-distinguished in the supplied metadata. I retained the participants’ own crediting language without inferring formal subreddit authority.

The rainbowroad correction is itself mistyped as `/r/ainbowroad`; the raw pointer preserves that form and its normalization relies on the correctly spelled name in the opening post of the same short thread.

**Data problems** (from its notes.md):
Two selected-thread comments are deleted. The record also cannot show decisions made inside the Discord, and the final-image thread continues after the analysis window. One unrelated necrobumped thread has an unseen opening/parent, but its surviving exchange clearly concerns the bump and a bot response rather than r/place.

**Lead's strikes and remarks at collect:** (the lead writes here: which facts lines it struck and why, what it will carry to step 5; nothing else)

- No batch 02 fact lines were struck. Its two timeline entries reproduce edited-post metadata and titles, and its six lexicon entries are unglossed participant terms with first-use item ids.
- Carry to step 5: batch 02 supplies the inherited build's defended rainbow/checker agreements, the forced relocation attributed in the final-image discussion, the observed completion and celebration after placement closed, and the explicit explanation that the small M answered the subreddit's size. Mark relations crossing `01|02`; preserve Discord as an evidence boundary, distinguish participant-applied “mods” from moderator metadata, preserve the raw `/r/ainbowroad` typo, and limit the ending because discussion continues beyond the window.
