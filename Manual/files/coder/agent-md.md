# The operating notes (AGENT.md)

The first file every coder and case lead reads: where it is, whether it is resuming, and what to call.

**What it holds**

A STATE block (instrument, contract hash, role, batch, slice, community, corpus counts, record, brief, openings, outputs, window). The first command to run, `read.py CORPUS state`, whose cursor says whether the run is starting or resuming. The rule that scratch files stay inside the run directory, not in a scratchpad the environment names. The rule not to read the tools' source. The three tools and how to set them up. What the harness observes (served reading against declared reading). What to do if interrupted. The outputs and the preflight check.

**Who writes it, and when**

The instrument's author wrote the template. `newrun.py` fills it for the case lead and `newrun.build_fleet()` fills it for each fleet batch.

**Why it exists**

It "says whether you are resuming". The scratch rule exists because a shared scratch path "can be read or overwritten by something that is not you", and a coder who writes there "has left its slice where another coder can read it". If it and the contracts disagree, the contracts win.

**Where**

[AGENT.v32.md](../../../coder/instrument/v32/AGENT.v32.md); filled copies at `run/AGENT.md` and `run/fleet/batch_NN/AGENT.md` in each run archive.

Checked against: AGENT.v32.md, newrun.py
