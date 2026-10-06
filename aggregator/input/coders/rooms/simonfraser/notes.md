## What was hard

The hardest boundary was between canvas practice and the subreddit’s own April Fools conduct. The UBC banner, website change and wifi claim occur at the same time as r/place but are explicitly about SFU’s own sites and teaching; I retained them as community conduct and marked every code as not about the canvas.

The account `HALK_Bot` was flagged only because its name ends in “bot.” Its first-person turn at `dfpf52j` claims “Our thread” and negotiates land while describing Discord and Facebook organising. I treated that turn as a participating community operator rather than generic machine output and stated the judgment in its note. By contrast, explicit boilerplate from `TotesMessenger` and `sneakpeekbot`, and the automatic-only `retroredditrobot` post, was not coded.

Image and link posts often left only titles or commenters’ descriptions. I coded a surviving title only where the body was gone and did not infer what an image showed. The phrase “war” was frequent, but it varied between a land claim, a joke, a description of prior fighting, and the preface to a peace agreement; grouping it by vocabulary alone would have hidden those differences.

## Data problems

The header reports 26 deleted or removed item bodies and two replies whose parent is not present. Two retained posts, `62ri8u` and `6376ba`, support only title-level codes because their bodies are unavailable. Deleted turns also interrupt the logo and crest discussions.

The record points to organising on Discord and Facebook but does not contain it. The Reddit negotiation is visible; the off-platform decision process and participants are not. No attempt was made to retrieve it.

The forest reports 46 threads total in window while the corpus has 47 thread records because the automatic-only Capilano thread contributes no people-written in-window item. This did not prevent a disposition or audit pass.

## Anomalies and leads

The community’s own UBC identity swap and wifi joke overlap the canvas period but remain analytically separate from it. They may be useful later as a within-community contrast between identity play performed through local infrastructure and collaborative drawing performed on the shared canvas.

The Turkish agreement is unusually explicit about exchange terms and later obligation: stop hostilities, protect the flag, and keep holding up the deal. The strongest lead for cross-case comparison is not generic alliance language but this sequence of bargained protection followed by maintenance.

## Complaints

The `find` query uses substring matching, so “war” returned many false hits inside “towards,” “awards,” and similar words. I read every returned item and treated those as false matches, but word-boundary behavior would make the counter-reading cleaner.

The pointer rule is broad enough to cover both organising venues and ordinary image/template links, while its off-platform fields assume talk moved there. I recorded the explicit organising venues and named subreddits, but did not force every image host into a record about moved organising.

## Grouping review

The two themes that nearly merged were “claiming space and refusing to move” and “trading protection for peace with Turkey.” They stayed apart because the first holds or contests a location, while the second exchanges ongoing protection and explicitly maintains an agreement. I reviewed the grouping before and after the counter-reading; no further regrouping was needed, and every theme’s instrument record states the reviewed boundary or merge.

## Codes I would defend

Hardest-defended: `trading protection for peace with Turkey` (code `c0045`, “announcing the agreement to defend Turkey's flag for peace”).

Thinnest kept: `pitying BCIT` (code `c0070`).

## How the reading held up

I did not work from memory of an unserved thread. I did not go back because I had forgotten a thread; the only returns were contract-required full-thread reads after triage, item reads for every counter-search hit, and the forest/timing review. Earlier threads did not become indistinct relative to later ones; the openings file and chronological reading kept the room’s ordinary business, its local April Fools jokes, and its canvas work distinct. The run was not interrupted or resumed: the initial cursor was 0.

The first attempt to announce `step1_brief` used a shell heredoc and failed because the environment would not create its temporary file. The briefing still printed in that command; I immediately reissued the stage with a normal foreground Python invocation before reading the openings. No emit record was lost or duplicated.

## Gate and method

The gate selected branch A at threshold 500, with 215 in-window items and 38,327 characters by people. I followed branch A without departing from the threshold. The briefing’s orientation was not used as evidence. Openings were read before triage, as required, and all evidence in the account comes from served passages and instrument measurements.
