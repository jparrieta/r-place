# The scheduler's contract (CONTRACT-scheduler.md)

What the scheduler does between the agents: launch, check, keep the record, and ask J.

**What it holds**

What the scheduler may read and write (§1). The cycle for one room: brief, build, the lead's first launch, the branch-B loop of coder, check and collect, the fork point, the close (§2). The checks F1 to F6 after a brief, B1 to B7 after a coder, E1 to E6 after the close (§3). What agents do wrong (§4), what to do when a check fails (§5), the record the scheduler keeps in `STATE.json` and the transcripts (§6), snapshots and forks, including native case-lead continuation (§7), order and the four giant rooms (§8), and what is J's to decide (§9).

**Who writes it, and when**

The study's owner. It says it is "the job that was done by hand on v29, written down". The scheduler may be a person or an agent.

**Why it exists**

So that "any agent, on any provider, can do it the same way". The scheduler "is not a reader": it never judges a reading and never lets one agent's output reach another except through the files the instrument names. "A failure is never fixed by editing an agent's output."

**Where**

[CONTRACT-scheduler.md](../../../coder/handler/CONTRACT-scheduler.md). Its header still reads "run yard v31".

Checked against: CONTRACT-scheduler.md, yard/README.md
