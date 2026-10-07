# A1: measured cost and time per leg

Target length: under 400 words. Handler analysis; regenerate from `CONTROL/legs/actors/*/turns/*/result.json` (outside `.cc`). Cost is list price; `total_cost_usd` adds up across legs, so the increase is the leg's cost. The last row may be a leg still running.

| Leg | Minutes | Turns | Output | Cache read | Cache write | Cumulative | Leg cost |
|---|---|---|---|---|---|---|---|
| A1a | 14.2 | 148 | 68 k | 12 M | 0.25 M | $5.74 | $5.74 |
| A1b-01 | 35.5 | 364 | 155 k | 107 M | 1.16 M | $39.98 | $34.25 |
| A1b-02 | 41.4 | 300 | 132 k | 113 M | 0.66 M | $70.92 | $30.93 |
| A1b-03 | 37.9 | 377 | 175 k | 126 M | 0.61 M | $104.49 | $33.58 |
| A1b-04 | 39.4 | 283 | 162 k | 89 M | 0.61 M | $130.75 | $26.26 |
| A1b-05 | 26.5 | 234 | 130 k | 103 M | 0.42 M | $157.41 | $26.66 |
| A1b-06 | 34.7 | 292 | 159 k | 80 M | 0.49 M | $180.75 | $23.34 |
| A1b-07 | 31.3 | 309 | 153 k | 111 M | 0.41 M | $209.25 | $28.50 |
| A1b-08 | 32.2 | 277 | 149 k | 90 M | 0.42 M | $234.01 | $24.76 |
| A1b-09 | 51.0 | 429 | 234 k | 183 M | 0.61 M | $280.09 | $46.08 |
| A1b-10 | 43.5 | 456 | 207 k | 119 M | 0.57 M | $312.84 | $32.75 |
| A1b-11 | 20.1 | 220 | 101 k | 81 M | 0.29 M | $333.33 | $20.49 |
| A1b-12 | 34.3 | 365 | 164 k | 103 M | 0.49 M | $361.54 | $28.21 |
| A1b-13 | 2.2 | 29 | 11 k | 5 M | 0.05 M | $363.17 | $1.63 |

## Calibration against J's weekly meter

- 25% at 2026-10-06 18:08Z, 30% at 20:09Z; the run cost about $97 between them (18:08Z interpolated inside A1b-09).
- So 1% of a week is about $19 of list cost ($16 to $24 with the readings rounded); a full leg is about 1.5% of a week.
- The 59% J read at 16:27Z was another meter, likely the 5-hour window.

- 55% at 2026-10-07 09:02Z (J; some of it his own copy editing). Run cost then about $815 list; from 44% at 04:31Z ($656) that is about $160 for 11 points, at most $15 per point, less once J's and the handler's own use are taken out.
