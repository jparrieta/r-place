# The fleet as a population, stage B3

**Basis: a trial assembly, not the record.** These figures come from `tools/assemble.py B3` run on option (c) of QB3-003 in a scratch folder (`out/_analysis/b3_scratch_c.py`): the four half packets (B0192a/b, B0927a/b, 30 positions served in room ids) left out, so 19 items lack a replicate. The assembly of record waits for J's ruling on QB3-003; this report is rebuilt from it with `b3_check.py` and `b3_reports.py`, and this one is kept under a superseded name.

Pass 1, corpus copies. Agreement is as `notes-B2.md` defines it: Jaccard on placement sets, so `["T3-004"]` against `["T3-004","T3-011"]` scores 0.5; alpha uses distance 1 − Jaccard. No exemplar arm was served, so there are no exemplar figures; B2 also served none.

## Agreement

The next table gives corpus-wide agreement between the two replicates over 7825 items.

| Jaccard | exact set | exact list, order kept | primary | alpha |
|---|---|---|---|---|
| 0.786 | 0.703 | 0.693 | 0.838 | 0.782 |

Against stage B2: the stability floor is 0.807 (Jaccard, the arm against itself under two briefs). Corpus-wide Jaccard of 0.786 sits at it, so most of the remaining disagreement is the arm's own.

The next table gives agreement per family (an item counts for each family holding either replicate's primary).

| family | items | Jaccard | exact set | primary |
|---|---|---|---|---|
| G01 | 919 | 0.797 | 0.748 | 0.836 |
| G02 | 606 | 0.773 | 0.746 | 0.777 |
| G03 | 314 | 0.806 | 0.688 | 0.898 |
| G04 | 486 | 0.740 | 0.648 | 0.753 |
| G05 | 223 | 0.653 | 0.529 | 0.691 |
| G06 | 115 | 0.625 | 0.583 | 0.617 |
| G07 | 579 | 0.666 | 0.561 | 0.701 |
| G08 | 585 | 0.627 | 0.520 | 0.653 |
| G09 | 694 | 0.743 | 0.611 | 0.803 |
| G10 | 210 | 0.629 | 0.576 | 0.643 |
| G11 | 210 | 0.832 | 0.719 | 0.895 |
| G12 | 223 | 0.682 | 0.565 | 0.713 |
| G13 | 176 | 0.627 | 0.545 | 0.648 |
| G14 | 608 | 0.697 | 0.581 | 0.750 |
| G15 | 278 | 0.581 | 0.464 | 0.597 |
| G16 | 78 | 0.620 | 0.538 | 0.603 |
| G17 | 159 | 0.644 | 0.579 | 0.679 |
| G18 | 99 | 0.552 | 0.525 | 0.535 |
| G19 | 127 | 0.610 | 0.567 | 0.622 |
| G20 | 790 | 0.743 | 0.713 | 0.752 |
| G21 | 1210 | 0.777 | 0.689 | 0.829 |

The family that agreed least is G18 (Jaccard 0.552 over 99 items).

**Per-theme presence agreement.** The next table lists every theme named on 20 or more items: positive agreement (both name it ÷ either names it), kappa on presence, and Jaccard over its items.

| theme | items either | both | positive | kappa | Jaccard |
|---|---|---|---|---|---|
| T3-152 | 42 | 14 | 0.333 | 0.498 | 0.631 |
| T3-042 | 35 | 13 | 0.371 | 0.540 | 0.400 |
| T3-084 | 54 | 21 | 0.389 | 0.558 | 0.446 |
| T3-039 | 20 | 8 | 0.400 | 0.571 | 0.450 |
| T3-192 | 22 | 9 | 0.409 | 0.580 | 0.424 |
| T3-082 | 43 | 18 | 0.419 | 0.589 | 0.430 |
| T3-058 | 31 | 13 | 0.419 | 0.590 | 0.419 |
| T3-154 | 23 | 10 | 0.435 | 0.605 | 0.464 |
| T3-157 | 32 | 14 | 0.438 | 0.608 | 0.500 |
| T3-153 | 31 | 14 | 0.452 | 0.621 | 0.608 |
| T3-169 | 33 | 15 | 0.455 | 0.624 | 0.530 |
| T3-188 | 22 | 10 | 0.455 | 0.624 | 0.545 |
| T3-149 | 112 | 53 | 0.473 | 0.639 | 0.525 |
| T3-098 | 21 | 10 | 0.476 | 0.644 | 0.452 |
| T3-018 | 71 | 34 | 0.479 | 0.645 | 0.556 |
| T3-061 | 60 | 29 | 0.483 | 0.650 | 0.528 |
| T3-150 | 95 | 49 | 0.516 | 0.678 | 0.557 |
| T3-024 | 83 | 43 | 0.518 | 0.680 | 0.562 |
| T3-185 | 23 | 12 | 0.522 | 0.685 | 0.551 |
| T3-032 | 108 | 57 | 0.528 | 0.688 | 0.606 |
| T3-136 | 32 | 17 | 0.531 | 0.693 | 0.591 |
| T3-091 | 41 | 22 | 0.537 | 0.697 | 0.545 |
| T3-050 | 95 | 51 | 0.537 | 0.696 | 0.546 |
| T3-068 | 57 | 31 | 0.544 | 0.703 | 0.626 |
| T3-141 | 20 | 11 | 0.550 | 0.709 | 0.700 |
| T3-181 | 20 | 11 | 0.550 | 0.709 | 0.625 |
| T3-074 | 43 | 24 | 0.558 | 0.715 | 0.636 |
| T3-151 | 121 | 68 | 0.562 | 0.716 | 0.587 |
| T3-011 | 128 | 72 | 0.562 | 0.716 | 0.617 |
| T3-089 | 23 | 13 | 0.565 | 0.722 | 0.732 |
| T3-097 | 53 | 30 | 0.566 | 0.721 | 0.638 |
| T3-040 | 30 | 17 | 0.567 | 0.723 | 0.611 |
| T3-052 | 72 | 41 | 0.569 | 0.724 | 0.588 |
| T3-046 | 43 | 25 | 0.581 | 0.734 | 0.539 |
| T3-003 | 48 | 28 | 0.583 | 0.736 | 0.626 |
| T3-113 | 29 | 17 | 0.586 | 0.738 | 0.523 |
| T3-043 | 182 | 107 | 0.588 | 0.736 | 0.677 |
| T3-088 | 39 | 23 | 0.590 | 0.741 | 0.752 |
| T3-170 | 39 | 23 | 0.590 | 0.741 | 0.667 |
| T3-051 | 22 | 13 | 0.591 | 0.742 | 0.636 |
| T3-041 | 181 | 107 | 0.591 | 0.738 | 0.590 |
| T3-104 | 27 | 16 | 0.593 | 0.743 | 0.642 |
| T3-033 | 209 | 125 | 0.598 | 0.743 | 0.599 |
| T3-095 | 127 | 76 | 0.598 | 0.745 | 0.627 |
| T3-087 | 132 | 79 | 0.598 | 0.745 | 0.629 |
| T3-020 | 137 | 83 | 0.606 | 0.751 | 0.595 |
| T3-073 | 239 | 145 | 0.607 | 0.749 | 0.596 |
| T3-070 | 230 | 143 | 0.622 | 0.761 | 0.634 |
| T3-062 | 53 | 33 | 0.623 | 0.766 | 0.626 |
| T3-026 | 61 | 38 | 0.623 | 0.766 | 0.628 |
| T3-072 | 54 | 34 | 0.630 | 0.771 | 0.676 |
| T3-048 | 119 | 75 | 0.630 | 0.770 | 0.658 |
| T3-029 | 110 | 70 | 0.636 | 0.775 | 0.685 |
| T3-004 | 341 | 219 | 0.642 | 0.774 | 0.641 |
| T3-021 | 333 | 214 | 0.643 | 0.775 | 0.666 |
| T3-090 | 51 | 33 | 0.647 | 0.785 | 0.693 |
| T3-031 | 344 | 224 | 0.651 | 0.781 | 0.661 |
| T3-081 | 23 | 15 | 0.652 | 0.789 | 0.652 |
| T3-035 | 48 | 32 | 0.667 | 0.799 | 0.733 |
| T3-055 | 21 | 14 | 0.667 | 0.800 | 0.675 |
| T3-117 | 124 | 86 | 0.694 | 0.817 | 0.730 |
| T3-057 | 46 | 32 | 0.696 | 0.820 | 0.772 |
| T3-122 | 23 | 16 | 0.696 | 0.820 | 0.739 |
| T3-006 | 185 | 129 | 0.697 | 0.818 | 0.668 |
| T3-105 | 105 | 74 | 0.705 | 0.825 | 0.689 |
| T3-038 | 290 | 207 | 0.714 | 0.828 | 0.637 |
| T3-017 | 326 | 233 | 0.715 | 0.827 | 0.712 |
| T3-037 | 88 | 63 | 0.716 | 0.833 | 0.725 |
| T3-022 | 120 | 86 | 0.717 | 0.833 | 0.693 |
| T3-076 | 47 | 34 | 0.723 | 0.839 | 0.727 |
| T3-002 | 387 | 280 | 0.724 | 0.832 | 0.704 |
| T3-065 | 102 | 74 | 0.725 | 0.839 | 0.663 |
| T3-005 | 463 | 341 | 0.737 | 0.840 | 0.704 |
| T3-064 | 23 | 17 | 0.739 | 0.850 | 0.761 |
| T3-111 | 23 | 17 | 0.739 | 0.850 | 0.775 |
| T3-027 | 83 | 63 | 0.759 | 0.862 | 0.795 |
| T3-044 | 84 | 64 | 0.762 | 0.864 | 0.786 |
| T3-063 | 99 | 76 | 0.768 | 0.867 | 0.791 |
| T3-100 | 39 | 30 | 0.769 | 0.869 | 0.756 |
| T3-015 | 139 | 107 | 0.770 | 0.868 | 0.801 |
| T3-010 | 444 | 345 | 0.777 | 0.868 | 0.678 |
| T3-023 | 278 | 217 | 0.781 | 0.873 | 0.721 |
| T3-156 | 40 | 32 | 0.800 | 0.888 | 0.787 |
| T3-001 | 409 | 328 | 0.802 | 0.885 | 0.789 |
| T3-009 | 481 | 394 | 0.819 | 0.895 | 0.738 |
| T3-016 | 259 | 214 | 0.826 | 0.902 | 0.814 |
| T3-028 | 166 | 138 | 0.831 | 0.906 | 0.770 |
| T3-075 | 74 | 62 | 0.838 | 0.911 | 0.759 |
| T3-014 | 278 | 242 | 0.871 | 0.928 | 0.787 |
| T3-054 | 143 | 136 | 0.951 | 0.974 | 0.924 |

**The theme the fleet handled worst** (lowest positive agreement on 30 or more items): T3-152, named on 42 items, both readers on 33% of them.

**The duplicate rate** beside it: see `position-B3.md`; the two copies never disagree, because readers recognised the repeat.

## The disagreement inventory (stage B4's workload)

Over 7825 items with both replicates: 5429 placed alike (same set, same primary), 2396 split. Of the splits, 1197 differ on the primary with different sets, 1130 share the primary and differ only on an additional theme, and 69 hold the same themes in another order. Corpus lines with more than one theme: 2467; lines flagged a bag: 673. The assembler's classes: class 1 2564, class 2 1984, class 3 2407, class 4 831, class 5 58 (1 and 2 stand; 3, 4 and 5 go to B4).

The next table gives the inventory per family.

| family | alike | split, primary | split, additional only | split, order only |
|---|---|---|---|---|
| G01 | 685 | 149 | 83 | 2 |
| G02 | 446 | 129 | 25 | 6 |
| G03 | 212 | 28 | 70 | 4 |
| G04 | 305 | 110 | 61 | 10 |
| G05 | 116 | 67 | 38 | 2 |
| G06 | 65 | 42 | 6 | 2 |
| G07 | 319 | 167 | 87 | 6 |
| G08 | 292 | 191 | 90 | 12 |
| G09 | 411 | 124 | 146 | 13 |
| G10 | 118 | 72 | 17 | 3 |
| G11 | 149 | 20 | 39 | 2 |
| G12 | 122 | 60 | 37 | 4 |
| G13 | 92 | 58 | 22 | 4 |
| G14 | 344 | 143 | 112 | 9 |
| G15 | 125 | 108 | 41 | 4 |
| G16 | 40 | 29 | 7 | 2 |
| G17 | 91 | 50 | 17 | 1 |
| G18 | 50 | 44 | 3 | 2 |
| G19 | 71 | 47 | 8 | 1 |
| G20 | 558 | 191 | 36 | 5 |
| G21 | 818 | 191 | 185 | 16 |

The per-theme inventory is in `out/_analysis/b3_check_*.json` (`inventory_themes`).

## Per-reader dispersion

**Variance components.** A linear mixed model with crossed random intercepts for room and reader (batch): multi: room 0.0067, reader 0.0120, residual 0.1141; nthemes: room 0.0105, reader 0.0172, residual 0.1718. The reader share is larger than the room share for both outcomes, and both are small beside the residual.

**The funnel.** Each reader's rate against its batch size, with limits at the fleet rate ± 3 binomial standard errors. Multi rate (fleet 0.158): 88 readers outside, all above. Themes per line (fleet 1.183): 49 outside, most of them the same readers. The empty rate is zero throughout.

**What the readers above the limits have in common.** The next table compares them with the fleet.

| readers | items | item bytes | arguable | seconds a packet | multi | multi of the other replicate, same items |
|---|---|---|---|---|---|---|
| above the limits (88) | 14.5 | 41185 | 0.549 | 199 | 0.531 | 0.287 |
| fleet (1208) | 14.6 | 34056 | 0.443 | 161 | 0.158 | 0.158 |

They held longer items, called more lines arguable and took longer. Their items also drew more second placements from the other replicate's readers than the fleet's items do, so part of the excess is in the items; the rest is the reader. Stage B4 needs their items named: the readers are listed below.

Readers above the multi limits (batch, lines, rate): B0021 13 0.46; B0023 13 0.46; B0032 13 0.46; B0053 13 0.46; B0099 13 0.46; B0105 13 0.54; B0142 13 0.46; B0158 13 0.85; B0164 13 0.46; B0169 13 0.54; B0198 13 0.62; B0222 13 0.62; B0226 13 0.46; B0232 13 0.54; B0248 13 0.46; B0263 13 0.46; B0321 13 0.54; B0334 13 0.62; B0343 13 0.54; B0352 13 0.46; B0382 13 0.46; B0390 13 0.54; B0420 13 0.46; B0421 13 0.54; B0428 13 0.46; B0452 13 0.46; B0454 13 0.54; B0460 13 0.62; B0476 13 0.46; B0481 13 0.54; B0485 13 0.46; B0487 13 0.69; B0491 13 0.62; B0504 13 0.46; B0519 13 0.46; B0520 13 0.54; B0525 13 0.46; B0554 13 0.46; B0596 13 0.46; B0604 13 0.46; B0616 13 0.54; B0617 13 0.54; B0621 13 0.69; B0644 13 0.46; B0646 13 0.62; B0667 13 0.62; B0680 13 0.62; B0697 13 0.54; B0716 13 0.46; B0753 13 0.54; B0757 13 0.46; B0770 13 0.77; B0771 13 0.46; B0785 13 0.54; B0794 13 0.46; B0803 13 0.46; B0812 8 0.62; B0820 13 0.54; B0833 13 0.46; B0835 13 0.46; B0843 13 0.46; B0855 13 0.54; B0862 13 0.46; B0868 13 0.54; B0886 13 0.85; B0895 13 0.46; B0899 13 0.46; B0935 13 0.77; B0944 13 0.62; B0961 13 0.46; B0966 13 0.54; B0977 13 0.77; B0978 13 0.46; B0988 13 0.46; B0992 13 0.69; B1014 13 0.46; B1015 13 0.46; B1019 13 0.46; B1022 13 0.62; B1067 13 0.62; B1116 13 0.46; B1121 13 0.54; B1122 13 0.62; B1129 13 0.46; B1141 13 0.62; B1190 13 0.46; B1205 13 0.46; B1209 13 0.54.

## families_opened

Families opened per placement line: median 1.0, mean 1.77. Distribution (families: lines): 1: 10582, 2: 3528, 3: 931, 4: 229, 5: 64, 6: 25, 7: 11, 8: 4, 10: 15, 11: 2, 12: 1, 21: 270. 61 of 18522 placements fall in a family the reader did not open; 270 lines opened all 21.

## The predicted confusions

1176 prediction lines over the returns (QB3-004 for the returns without one). 537 of the predicted pairs are among the nineteen of `confusions.md`. In 229 batches the predicted pair split the two replicates' primaries on at least one item of that batch.

The next table lists the pairs that split the two replicates' primaries most often, how many readers predicted each, and whether `confusions.md` names it.

| pair | primary splits | predicted by | in confusions.md |
|---|---|---|---|
| T3-005/T3-021 | 38 | 245 | yes |
| T3-017/T3-031 | 29 | 4 | no |
| T3-010/T3-149 | 24 | 58 | yes |
| T3-009/T3-073 | 22 | 24 | yes |
| T3-001/T3-023 | 20 | 25 | yes |
| T3-002/T3-038 | 19 | 8 | no |
| T3-002/T3-033 | 18 | 24 | yes |
| T3-010/T3-024 | 17 | 12 | yes |
| T3-001/T3-048 | 13 | 12 | no |
| T3-004/T3-041 | 12 | 7 | no |
| T3-001/T3-031 | 12 | 13 | no |
| T3-004/T3-070 | 12 | 8 | yes |
| T3-033/T3-041 | 12 | 0 | no |
| T3-023/T3-095 | 11 | 21 | no |
| T3-001/T3-095 | 11 | 48 | yes |

## Coverage

7825 of 7844 items have both replicates. Missing a replicate: 19 (MMA/t01, MMA/t02, MMA/t03, MMA/t04, MMA/t05, MMA/t06, MMA/t07, MMA/t08, greyblob/t01, greyblob/t02, greyblob/t03, greyblob/t04, hentai/t01, hentai/t02, hentai/t03, hentai/t04, hentai/t05, hentai/t06, ucf/t12).

**What these figures license.** The readers share an architecture with me and with each other, so a figure here bounds whether the written instrument decides, never whether it is right.
