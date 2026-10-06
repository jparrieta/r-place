#!/usr/bin/env python3
"""Verify the saved Dorset demonstration without running a model or changing its store."""
import argparse
import json
from pathlib import Path
from checkpoints import CheckpointError, load, locked, read_json


def blob(store, checkpoint, rel):
    entry = checkpoint["entries"][rel]
    sha = entry["sha256"]
    return (store / "objects" / sha[:2] / sha[2:]).read_bytes()


def verify(store, marker):
    refs = ["dorset-complete", "alternative-a", "alternative-a-reply", "alternative-b", "alternative-b-reply"]
    checkpoints = {r: load(store, r) for r in refs}
    parent = checkpoints["dorset-complete"][1]
    metadata = parent["metadata"]
    counts = json.loads(blob(store, parent, "workspace/room/run/out/_run.json"))
    threads = {metadata["thread_id"]}
    ignored = {"workspace/room/run/out/_transcript.jsonl", "workspace/room/run/out/final_message.md",
               "workspace/room/run/out/_resume_probe.json"}

    def research_files(cp):
        return {p: e for p, e in cp["entries"].items() if p.startswith("workspace/") and p not in ignored}

    branches = {}
    for letter in "ab":
        fork_id, fork = checkpoints["alternative-" + letter]
        reply_id, reply = checkpoints["alternative-" + letter + "-reply"]
        fm, rm = fork["metadata"], reply["metadata"]
        assert fm["thread_id"] not in threads, "Fork reused a native thread ID"
        threads.add(fm["thread_id"])
        assert fm["turn_id"] == metadata["turn_id"], "Wrong fork boundary"
        assert fm["final_message"] == metadata["final_message"], "Final reply changed at fork"
        assert rm["thread_id"] == fm["thread_id"], "Continuation started a fresh agent"
        assert rm["turn_id"] != fm["turn_id"], "No continuation turn"
        assert fm["forked_from"]["checkpoint"] == checkpoints["dorset-complete"][0]
        assert "workspace/room/run/out/_resume_probe.json" not in fork["entries"], "Sibling file leaked into fork"
        assert research_files(fork) == research_files(parent), "Fork changed research files"
        assert research_files(reply) == research_files(parent), "Continuation changed research files"
        probe = json.loads(blob(store, reply, "workspace/room/run/out/_resume_probe.json"))
        assert probe["branch"].lower() == letter, "Wrong branch file restored"
        assert probe["cwd"] == metadata["configuration"]["cwd"], "Working path changed"
        assert probe["n_codes"] == counts["n_codes"] and probe["n_themes"] == counts["n_themes"]
        assert probe["verdict"] == counts["verdict"]
        # Audit the continuation's actual stream: remembered marker before its first tool.
        evidence = None
        for log in sorted((store / "audit").glob("*/rpc.jsonl")):
            events = [json.loads(l)["message"] for l in log.read_text().splitlines()]
            if not any(m.get("method") == "turn/completed" and
                       m.get("params", {}).get("turn", {}).get("id") == rm["turn_id"] for m in events):
                continue
            first_tool = None
            remembered = None
            for i, m in enumerate(events):
                if m.get("method") != "item/completed":
                    continue
                item = m.get("params", {}).get("item", {})
                if item.get("type") == "agentMessage" and marker in item.get("text", "") and remembered is None:
                    remembered = i
                if item.get("type") in ("commandExecution", "fileChange", "mcpToolCall", "dynamicToolCall") and first_tool is None:
                    first_tool = i
            assert remembered is not None and first_tool is not None and remembered < first_tool, "Marker not recalled before tools"
            assert any(m.get("method") == "thread/resume" and m.get("params", {}).get("threadId") == fm["thread_id"] for m in events)
            evidence = str(log)
        assert evidence, "No native continuation trace"
        branches[letter] = {"fork_checkpoint": fork_id, "reply_checkpoint": reply_id,
                            "thread_id": fm["thread_id"], "probe": probe,
                            "continuity_before_tools": True, "audit": evidence}
    return {"result": "PASSED", "subreddit": "Dorset", "store": str(store),
            "model": metadata["configuration"]["model"],
            "reasoning_effort": metadata["configuration"]["reasoningEffort"],
            "parent_checkpoint": checkpoints["dorset-complete"][0],
            "parent_thread_id": metadata["thread_id"], "parent_turn_id": metadata["turn_id"],
            "verdict": counts["verdict"], "codes": counts["n_codes"], "themes": counts["n_themes"],
            "checks": ["all checkpoint manifests and objects verified", "three independent native thread IDs",
                       "forks preserve the final completed turn and reply", "native cold resume used for both continuations",
                       "conversation-only marker recalled before tools", "same absolute working directory",
                       "no sibling probe file at either branch start", "all research files unchanged"],
            "branches": branches}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", required=True)
    p.add_argument("--marker-file", required=True, help="JSON file with the original continuity marker")
    a = p.parse_args()
    with locked(a.store) as store:
        print(json.dumps(verify(store, read_json(a.marker_file)["marker"]), indent=2))
