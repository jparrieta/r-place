#!/usr/bin/env python3
"""Immutable, content-addressed checkpoints for a managed room. Standard library only.

The store's stable paths are part of the checkpoint contract. Restoring materializes
workspace/, native/, and state/ at their ORIGINAL paths. Branches sharing a store run
serially. A checkpoint never rewrites an agent's files, history, or instrument hashes.
"""
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import uuid


class CheckpointError(RuntimeError):
    pass


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        dfd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def json_write(path, obj):
    atomic(path, encoded(obj))


def read_json(path):
    return json.loads(Path(path).read_text())


def name(value):
    import re
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", value):
        raise CheckpointError("Use a simple name (letters, numbers, dot, dash, underscore)")
    return value


@contextlib.contextmanager
def locked(store):
    store = Path(store).resolve()
    store.mkdir(parents=True, exist_ok=True)
    with (store / ".lock").open("a+") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise CheckpointError("This managed room is busy; branches/agents share stable paths")
        try:
            yield store
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


ROOTS = ("workspace", "native", "state")


def excluded(rel):
    """Only runtime-local secrets and disposable runtime files are excluded.

    Workspace files, including hidden/untracked files, are ALWAYS captured.
    No authentication material is copied into the object store or checkpoints.
    """
    p = Path(rel)
    if p.parts[0] != "native":
        return False
    parts = p.parts[2:]  # native/<agent>/...
    return bool(parts) and (parts[0] in {"auth.json", "log", "logs", "tmp", "otel"}
                           or p.name.endswith((".sock", ".lock")))


def inventory(store, save=False):
    """Record bytes, modes, empty directories, and mtimes; refuse unsafe special files.

    Symlinks are rejected rather than silently depending on files outside the capture.
    Reads must be quiescent; compare before/after and re-scan at commit.
    """
    store = Path(store)
    result = {}
    for root in ROOTS:
        base = store / root
        if not base.exists():
            continue
        for p in [base, *sorted(base.rglob("*"))]:
            rel = p.relative_to(store).as_posix()
            if excluded(rel) or any(excluded(x.relative_to(store)) for x in p.parents if x != store and store in x.parents):
                continue
            st = p.lstat()
            mode = stat.S_IMODE(st.st_mode)
            if stat.S_ISDIR(st.st_mode):
                result[rel] = {"kind": "dir", "mode": mode}
            elif stat.S_ISREG(st.st_mode):
                data = p.read_bytes()
                after = p.stat()
                if (st.st_size, st.st_mtime_ns, st.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                    raise CheckpointError("File changed during capture: " + rel)
                sha = digest(data)
                result[rel] = {"kind": "file", "mode": mode, "size": len(data),
                               "mtime_ns": st.st_mtime_ns, "sha256": sha}
                if save:
                    blob = store / "objects" / sha[:2] / sha[2:]
                    if blob.exists():
                        if digest(blob.read_bytes()) != sha:
                            raise CheckpointError("Corrupt existing object: " + sha)
                    else:
                        atomic(blob, data)
                        blob.chmod(0o400)
            else:
                raise CheckpointError("Cannot snapshot symlink/socket/device: " + rel)
    return result


def capture(store, metadata, label=None):
    store = Path(store).resolve()
    if label:
        label = name(label)
        if (store / "refs" / (label + ".json")).exists():
            raise CheckpointError("Checkpoint label already exists: " + label)
    entries = inventory(store, save=True)
    if entries != inventory(store):
        raise CheckpointError("Room changed while checkpointing; no checkpoint committed")
    obj = {"format": "atlas-agent-checkpoint-v1", "store_path": str(store),
           "created_utc": now(), "metadata": metadata, "entries": entries}
    data = encoded(obj)
    cid = digest(data)
    dst = store / "checkpoints" / (cid + ".json")
    atomic(dst, data)
    dst.chmod(0o400)
    if label:
        label = name(label)
        ref = store / "refs" / (label + ".json")
        json_write(ref, {"checkpoint": cid})
    json_write(store / "HEAD.json", {"checkpoint": cid})
    return cid


def load(store, ref):
    store = Path(store).resolve()
    if ref == "HEAD":
        ref = read_json(store / "HEAD.json")["checkpoint"]
    elif (store / "refs" / (name(ref) + ".json")).exists():
        ref = read_json(store / "refs" / (ref + ".json"))["checkpoint"]
    if len(ref) != 64 or any(c not in "0123456789abcdef" for c in ref):
        raise CheckpointError("Unknown checkpoint: " + ref)
    data = (store / "checkpoints" / (ref + ".json")).read_bytes()
    if digest(data) != ref:
        raise CheckpointError("Checkpoint manifest hash mismatch")
    obj = json.loads(data)
    if obj.get("format") != "atlas-agent-checkpoint-v1":
        raise CheckpointError("Unsupported checkpoint format")
    if obj["store_path"] != str(store) and Path(obj["store_path"]).name != store.name:
        raise CheckpointError("Restore requires the original store path: " + obj["store_path"])
    for rel, e in obj["entries"].items():
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts or not p.parts or p.parts[0] not in ROOTS:
            raise CheckpointError("Unsafe checkpoint path: " + rel)
        if e["kind"] == "file":
            sha = e["sha256"]
            if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
                raise CheckpointError("Invalid object digest")
            blob = store / "objects" / sha[:2] / sha[2:]
            if not blob.is_file() or digest(blob.read_bytes()) != sha:
                raise CheckpointError("Missing/corrupt object: " + rel)
        elif e["kind"] != "dir":
            raise CheckpointError("Invalid entry kind: " + rel)
    return ref, obj


def restore(store, ref):
    """Validate and stage everything first. Save displaced trees; journal interruptions.

    No running server may own these paths (the runner holds the room lock until exit).
    A power failure between renames leaves RESTORE.json and recoverable trees, never
    a checkpoint falsely marked restored. `recover_restore` rolls the operation back.
    """
    store = Path(store).resolve()
    if (store / "RESTORE.json").exists():
        raise CheckpointError("Interrupted restore; run recover before continuing")
    cid, obj = load(store, ref)
    tx = store / "displaced" / uuid.uuid4().hex
    stage = tx / "incoming"
    stage.mkdir(parents=True)
    for rel, e in obj["entries"].items():
        p = stage / rel
        if e["kind"] == "dir":
            p.mkdir(parents=True, exist_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            sha = e["sha256"]
            shutil.copyfile(store / "objects" / sha[:2] / sha[2:], p)
            os.utime(p, ns=(e["mtime_ns"], e["mtime_ns"]))
        p.chmod(e["mode"])
    plan = {"checkpoint": cid, "transaction": str(tx),
            "previous_head": read_json(store / "HEAD.json") if (store / "HEAD.json").exists() else None,
            "had": {r: (store / r).exists() for r in ROOTS}}
    json_write(store / "RESTORE.json", plan)
    for root in ROOTS:
        old = store / root
        if old.exists():
            old.rename(tx / root)
        if (stage / root).exists():
            (stage / root).rename(old)
    if inventory(store) != obj["entries"]:
        raise CheckpointError("Restore verification failed; recover before continuing")
    json_write(store / "HEAD.json", {"checkpoint": cid})
    (store / "RESTORE.json").unlink()
    return cid, obj


def recover_restore(store):
    store = Path(store).resolve()
    p = store / "RESTORE.json"
    plan = read_json(p)
    tx = Path(plan["transaction"])
    if tx.parent != store / "displaced":
        raise CheckpointError("Invalid restore transaction")
    for r in ROOTS:
        old, current = tx / r, store / r
        if old.exists():
            if current.exists():
                current.rename(tx / (r + ".incomplete"))
            old.rename(current)
        elif not plan["had"][r] and current.exists():
            current.rename(tx / (r + ".incomplete"))
    if plan.get("previous_head") is not None:
        json_write(store / "HEAD.json", plan["previous_head"])
    else:
        (store / "HEAD.json").unlink(missing_ok=True)
    p.unlink()


def require_clean_transaction(store):
    if (Path(store) / "RESTORE.json").exists():
        raise CheckpointError("Interrupted restore; run recover first")
    if (Path(store) / "RUNNING.json").exists():
        raise CheckpointError("Unfinished agent operation. Inspect RUNNING.json; use recover-run only after its processes have exited")
