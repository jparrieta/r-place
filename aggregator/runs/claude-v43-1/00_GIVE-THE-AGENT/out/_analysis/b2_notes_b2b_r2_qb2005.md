
### QB2-005, answered: the failed dispatch moved aside

J ruled (2026-10-12, 06:55 Berlin). The failed folder is renamed and no `pilot_rounds.jsonl` line is written for it. I ran `mv out/_fleet_raw/B2/round-2 out/_fleet_raw/B2/round-2-failed`; nothing was deleted. J dispatches round 2 again into a fresh `round-2/` folder.

`round-2-failed/` holds the three exhausted dispatches of the eleven-part packet and no reading. Its DONE file counts 11 packets, 3 readers, 0 valid returns and 3 exhausted, on deepseek/deepseek-v4-flash-0731. They used 1,873,195 input tokens and 10,054 output tokens, at a cost of 0.087 USD. The log holds 70 calls from 14 reader ids (r1 to r14). The folder holds 13 failure files:
- 9 failed at part 6 with HTTP 400. Part 5 carried 149,007 input tokens and passed; part 6 would carry about 163,000. The provider's window looks to be about 164,000 tokens; the handler inferred this from the log, and it is not confirmed.
- 4 failed at part 1 because the reply ended with the packet's end line ("END OF PACKET" or "END-OF-PACKET") instead of `END-OF-RETURN` (r6, r8, r10, r14).
- r4 appears in the log with no failure file of its own.

My assumption under QB2-005 was to write no line and leave the folder alone. The first half stands; the folder is now renamed as J ruled.
