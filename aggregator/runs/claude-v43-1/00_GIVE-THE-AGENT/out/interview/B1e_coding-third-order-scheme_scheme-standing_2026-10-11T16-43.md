# Interview brief, B1e: the third-order tier standing

Target length: under 800 words. Written 2026-10-11.

## What I did

I turned the working grouping of 197 third-order themes into the shipped scheme. I worked one family at a time. For every theme I wrote a name, a gloss, a gate (must show, must not show, decide when both), discriminators against its near neighbours, what varies, one case it is not, and up to three exemplars. Every exemplar is confirmed word for word through `cite.py`. I put the themes in 21 families of themes a reader would confuse, and renamed 115 of them so that each name says what its gate admits.

I read the floor for every theme, counting rooms that tell one episode as one. 183 themes rest on two rooms unlike each other and are main; 14 are rare. I ranked 17 confusion pairs from the rule 0 record. I opened `findings.jsonl` with the scheme's claim. Then I ran the hand-over checks: the two-or-half argument for every theme, a stranger test, the ten biggest second-order themes, the running-file entries dropped, and token sizes.

## What I found

- The kinds saturated at 197. `prior.md` expected 250 to 450.
- Half the placed second-order themes (51.1%) sit on one kind; the rest need two or three.
- Dealing with neighbours is where one stretch of talk does most things at once. Borders, truces, alliances, help traded and restraint keep turning up in the same theme. Those themes sit on one kind 36% of the time, against 54% for the rest.
- The hardest pair is defending the work (T3-005) against watching and repairing it (T3-021). 131 of 655 second-order themes hold both acts, and the record splits 60 to 66 on which comes first.
- canucks fits the scheme best: 40 second-order themes, each on one kind, across 18 families. turkey fits worst among rooms with eight themes or more: 13 of its 14 themes need two or three kinds.

## What surprised me

The grain of the second-order themes predicts how many kinds they need. Themes with five concepts or fewer sit on one kind 70% of the time. Themes with six to twenty sit on one kind only 35 to 38% of the time. canucks has about five concepts a theme and turkey about nineteen. Part of what looks like rooms doing several things at once is how finely the A1 coder cut them.

I was also surprised by how many of my gates, as first drafted, leaned on things a stranger will never see: leg names, theme and concept ids, counts of rule 0 lines. 42 fields had to be rewritten in words.

## What I doubt

- The family boundary between G14 (space and help between rooms) and G15 (pacts and envoys). A reader holding one of them will file truces and alliances under T3-010.
- The stranger test. `mem.py theme` showed me the working placements while I placed, so my five-for-five agreement on primaries proves little.
- The exemplars' rivals. I did not search every passing quote in each room, so most exemplars name no rivals. The prior's tie-breakers (placement bracket, earlier hour) were not applied one by one.
- The rare tier. T3-007 and T3-077 each have a second room's concept that is not placed on them. T3-128 is rare only because its three rooms tell one episode.
- Whether 197 is right, or whether the deal kinds should be fewer. I kept them apart because a reader can tell a truce from a border deal from bartering. The bags say that the rooms often did not keep them apart.

## Three questions I would most like to be asked

1. Should truces, alliances, bartering and border deals be one kind with its variation written out? The rooms often do all four in one thread, so what does keeping them apart buy?
2. How much of the multi-kind placement is the A1 coder's grain, and how would you test that before stage B3?
3. Which second-order theme would you put in front of a fresh reader to break the T3-005/T3-021 line, and what rate of disagreement would make you merge them?
