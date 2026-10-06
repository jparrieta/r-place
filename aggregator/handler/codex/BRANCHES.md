# Fork an analysis

Target length: under 550 words.

An analysis branch continues from a verified native checkpoint. An interview is a separate conversation without study progression. Interviews and native archives stay outside Git.

## Boundary and history

To change C2, choose the last verified checkpoint before C2, normally the closing C1 leg. To change C1, choose the closing B4 checkpoint. Choosing a later checkpoint retains its later knowledge. Branching never erases that knowledge or reverses a verified stage.

Each branch gets independent files, native conversation ancestry, stage deliveries, validation records and checkpoints. It inherits the parent's model schedule and trusted validators. A revised card does not alter those validators. Changed upstream data may require an earlier restart if the existing checks reject it. Previous validation certifies the original inputs only.

## Phone or desktop panel

1. Select a verified saved aggregator in the conversation dropdown. Open **Fork as a new analysis**. Enter a new name and first leg, for example `C2a-01`.
2. **Create idle analysis branch** copies the checkpoint workspace and records ancestry. It sends no prompt.
3. Upload revised data and all future cards in **Analysis branch setup and Git lineage**. Choose delivery at branch start for immediate data, or a named stage for later delivery. For cards, selecting the file fills its stage and original destination path.
4. **Publish and prepare branch** seals the file changes, publishes the Git branch and restores the first leg. No model turn starts. Setup is then immutable; further variants need another branch.
5. Select **Start prepared leg**, or send your own first message. Later legs use the usual preparation/start controls or explicit handler instructions. Progression is not unattended.

Uploads use bounded chunks. A failed upload remains visible in `branch-status`. Set it aside at its destination path before uploading again; the unfinished bytes are preserved privately.

## Git structure

```text
shared closing C1 checkpoint
  + original C2, C3, ...
  + variant setup commit, revised C2, C3, ...
```

The new remote branch is `analysis/<name>`. Checkpoint tags identify common ancestor commits. The first new commit records the supplied changes. Each verified leg thereafter commits and pushes automatically. Sibling branches share the same checkpoint commit; nested branches preserve their actual parent.

Git publication uses a separate index. It does not switch the checkout, stage unrelated changes, update main or force-push. Published files use the original lineage's `aggregator/runs/<root-study>/` path for stable diffs; `LINEAGE.json` identifies the current analysis and archive hashes. Native histories, runtime archives and interviews remain private; credentials are excluded. Native checkpoints also retain the branch card set. Git alone cannot restore an agent.

A failed push preserves the verified local checkpoint and blocks advancement. Use **Retry Git publication** or `publish-branch`; do not repeat analysis. Existing remote changes are never overwritten. Files above 95 MiB are refused. Publication requires Git identity, authentication and network access.

## CLI

Use `run.py` from this controller directory:

```bash
python3 run.py branch PARENT CHECKPOINT VARIANT --leg C2a-01
python3 run.py branch-put VARIANT stages/STAGE-C2-model-the-loop.md --stage C2 --file /path/to/revised-card.md
python3 run.py branch-status VARIANT
python3 run.py prepare-branch VARIANT
python3 run.py start ACTOR
```

Branch creation and preparation return job IDs. Inspect each with `job JOB_ID` before the next command. Keep the existing card filename.

Deployment requires a safe controller restart. Tests do not constitute live research or phone acceptance.
