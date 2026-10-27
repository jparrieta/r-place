# The reconstruction return (stage E1)

Written at E1c, 27 October 2026. This is the specification for the readers of `_packets-E1/`. Each packet holds one room's skeleton (the global model at the frozen version, with the room's supported accepted, modified and particular lines, and its pending lines, evidence states and version uncertainty stated), the coder's account of the room (`case.md`) and the room's second-order themes. It holds no model-D account, no canvas figure and no analyst's note.

## The task

Read the coder's account claim by claim. For each claim, say whether the skeleton accounts for it.

- **A claim** is one sentence, or one part of a sentence, of the coder's account that states what members of the room did, in what order, with whom, or why. A sentence about the coder's evidence (what was read, what could not be seen, what the record does not show) is not a claim. Number the claims in the order they appear.
- **yes**: an element or arrow of the skeleton, with the room's lines on it, states what the claim says.
- **partly**: the skeleton states part of it, such as the act but not its order or its condition.
- **no**: nothing in the skeleton states it.
- **unresolved**: the skeleton's only lines on it are pending, or its evidence state is unresolved, or the version is uncertain. Say which.
- A pending or rejected line is not support. Silence is not negative evidence: a claim the skeleton does not mention is "no", not a contradiction. A claim the skeleton states the opposite of is "no", with "contradicts" at the head of the reason.

## The file

Write one file per room, `_fleet_raw/E1/<sub>.jsonl`. It has one JSON line per claim, then one summary line.

A claim line:

    {"sub": "<room>", "claim": 1, "text": "<the claim, in the account's own words, at most 200 characters>",
     "accounted": "yes" | "partly" | "no" | "unresolved", "element": "<element or arrow id, or none>",
     "reason": "<one sentence: what in the skeleton states it, or what is missing>"}

The summary line, last:

    {"sub": "<room>", "summary": true, "model_version": "<the version the skeleton states>",
     "local_status": "<the room's local status as the skeleton states it>", "claims": <n>,
     "yes": <n>, "partly": <n>, "no": <n>, "unresolved": <n>, "contradicted": <n>}

The counts in the summary must equal the claim lines. Write nothing else in the file.

## How the return is read

At the check leg, each room's **fidelity** is computed as yes plus half of partly, over yes, partly and no. Unresolved claims are reported apart, never counted as failures. Fidelity is reported by branch and by verdict. A low score is then separated by its cause:
- a claim the room's record does not support;
- missing evidence;
- a particular the skeleton omits;
- a shared account that does not hold.
