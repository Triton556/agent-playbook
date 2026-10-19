# Local quality ledger

`scripts/quality_ledger.py` uses Python's standard library. It reads only declared files inside `--root`, performs no shell/network/model calls, and writes only the explicitly requested report. Use a ledger when a series or recurring-defect task needs machine validation of evidence/dependencies, or the project already requires it; otherwise the existing acceptance record is enough.

```text
python <skill-root>/scripts/quality_ledger.py snapshot --root <project> --path tools/generator.py --path output/model.vox
python <skill-root>/scripts/quality_ledger.py validate <project>/quality-ledger.json --root <project> --require-ready --output <project>/quality-report.json
```

Exit 0: structurally valid and the requested readiness condition passed. Exit 1: malformed input or a false ready/complete declaration. Exit 2: a structurally valid in-progress ledger is not ready when `--require-ready` was requested. Default validate permits a valid draft and reports `ready_to_complete=false`; callers must inspect that field or use `--require-ready` before claiming completion.

## Schema version 1

- `task`: `{id, status}` where status is `in_progress`, `blocked`, `ready` or `complete`.
- `contract`: nonempty `objective`, `style`, `functional`, `context`.
- `subjects`: `{id, files:[{path,sha256}]}`. Include relevant generator dependencies and actual outputs. `snapshot` returns `files` and a canonical `digest` independent of path order. Paths are relative to root, use forward slashes and cannot escape it.
- `requirements`: `{id, kind, blocking, status, criterion, subject_ids, evidence_ids?}`. Kinds: `technical`, `semantic`, `visual`, `human`. Statuses: `pass`, `fail`, `pending`, `not_applicable`, `deferred`. Nonapplicable and deferred need `rationale`. A blocking deferral does not satisfy acceptance. A pass needs compatible fresh passing evidence covering every declared subject. Optional `required_views:[{id,subject_id,min_width,min_height}]` records useful image coverage.
- `evidence`: `{id,kind,verdict,method,reviewer:{kind,name},observed_at,observation,subject_hashes:{subject_id:digest},files:[{path,sha256}],views?}`. Review verdict: `pass`, `fail` or `observed`. Timestamp has a timezone. Reviewer kind: `automated`, `agent` or `human`; a human record needs human kind. Visual/human records require `inspected:true`. A view is `{id,subject_id,path,width,height}` with a hashed PNG/JPEG file. Actual header dimensions must match and meet the requirement.
- `issues`: `{id,subject_ids,severity,status,description}`. Severity: `blocking` or `advisory`; status: `open`, `fixed` or `deferred`. A fixed issue needs `verification_kind` and fresh compatible `resolved_evidence_ids` covering its subjects. A deferred issue needs `rationale`; a blocking one still blocks.
- `preserve`: `{path,sha256,rationale}` for approved immutable baselines. An intentional new version does not overwrite those paths.

Technical evidence cannot fulfill visual acceptance. A new source/artifact or changed render invalidates its receipt; rehashing the subject does not refresh the old review. Keep failed receipts and open issue history, then link the passing repair/recheck. An unused stale receipt is disclosed as advisory; it cannot satisfy a current criterion.

The validator verifies the record, hashes, references and image dimensions. It does **not** prove a source dependency list is complete, a photo depicts the declared angle, an image was inspected, or a reviewer is the named human. Its report explicitly preserves these limits. It is a local tool, not an installed platform hook and not a trained aesthetic judge.

## Completeness, dependencies and interpretation

Declare the expected outputs before generation, in the existing plan or task-state v2. The ledger validates declared subjects; it cannot detect an object that was never declared. `agent-worklog.mjs inspect` checks the output/stage manifest beside it, then invokes this validator when a ledger is linked.

The plan owns requirements, task-state owns progress when used, and this ledger owns detailed evidence. Required schema summaries refer to that basis; they do not create another specification. One compatible fresh evidence record can serve multiple requirements. Keep the existing schema compatible. Style, context, comprehension and use from [human-perspective-review](human-perspective-review.md) become applicable technical/semantic/visual/human requirements with concrete evidence, not a new compulsory kind. Bind source, render, labels and rules that influence the criterion. Unknown independence retains conservative rechecking; independently described and tested closures can be separated. A current hash is a binding, not proof that a person inspected the file.
