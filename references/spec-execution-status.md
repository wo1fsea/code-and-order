# Spec Execution Status

## Principle

Status is code. Status changes must be explicit file changes, reviewable in diffs, and tied to evidence.

Never encode status in directory names. Keep `specs/<spec-id>/` stable so links from commits, PRs, and notes do not break.

## Required Structure

```text
specs/<spec-id>/
  PRODUCT.md
  TECH.md
  STATUS.md
  workstreams/
    01-implementation.md
```

`STATUS.md` is the global board. It records the overall lifecycle, the Spec Decision Gate, the Parallelization Gate, implementation progress, validation progress, and a summary table of workstreams.

`workstreams/*.md` files are the concurrency unit. Agents should primarily update their own workstream file and synchronize only their row in `STATUS.md`.

Use `references/spec-first-delivery.md` for coordinator handoff, subagent implementation, and main-session acceptance.

Use `references/multi-agent-spec-flow.md` when multiple agents or branches implement the same spec in parallel.

## Spec Decision Gate

When a spec exists or is being created, `STATUS.md` should record the decision
that made code-changing work eligible to proceed:

```markdown
## Spec Decision Gate

- Request:
- Code change expected: yes/no
- Existing spec:
- Decision: new-full-spec / update-existing-spec / compact-spec / direct-exception / no-code-change
- Reason:
- Behavior, contract, data, UI, configuration, permissions, security, test, docs, or governance impact:
- Next workflow:
- Recorded in:
```

## Parallelization Gate

Before any workstream is claimed, `STATUS.md` should record:

```markdown
## Parallelization Gate

- Can run in parallel: yes/no
- Reason:
- Shared contract needed first: yes/no
- Workstream split:
- Sequential dependencies:
- Conflict risk:
- Implementation agents to launch:
- Main-session acceptance checks:
```

Default to `yes` for non-trivial specs. Record a serial exception when the
task is atomic, highly conflict-prone, blocked on unresolved shared contracts,
a tiny or emergency exception, or cheaper to complete directly than to
coordinate.

## Overall Spec Status

Use these values for the frontmatter `status` field in `STATUS.md`:

- `draft`: product or technical direction is still being shaped; implementation should not start.
- `ready`: spec is accepted enough to begin; implementation has not started.
- `active`: at least one workstream is claimed or in progress.
- `blocked`: work is stopped on an external decision, dependency, or failing prerequisite.
- `ready-review`: implementation and validation are complete enough for review, but not merged.
- `done`: implementation is merged or shipped, validation is complete, and specs match reality.
- `superseded`: replaced by another spec or decision.
- `cancelled`: explicitly abandoned.

Use these values for progress fields:

- `not_started`
- `partial`
- `complete`

Common combinations:

- Not started: `status: ready`, `implementation: not_started`, `validation: not_started`.
- Partially complete: `status: active`, `implementation: partial`, `validation: partial`.
- Complete: `status: done`, `implementation: complete`, `validation: complete`.

## Workstream Status

Use this state machine for each `workstreams/*.md` file:

```text
ready -> claimed -> in_progress -> implemented -> validating -> validated -> merged
           |             |              |
           v             v              v
        released      blocked        blocked
```

Rules:

- `implemented` means code is written but validation is not complete.
- `validated` means validation evidence exists but the work may not be merged.
- `merged` means the workstream has landed in the target branch.
- `released` means the claim was intentionally given up and the work can return to `ready`.
- Do not use `done` for workstreams; it is too ambiguous.
- Do not jump from `ready` to `merged`.

## Claiming Work

Before starting implementation, an agent must claim a workstream by updating its frontmatter:

```yaml
status: claimed
owner: codex
branch: codex/parser-work
claimed_at: 2026-04-30T10:00:00+08:00
lease_expires_at: 2026-04-30T12:00:00+08:00
updated: 2026-04-30
```

If the agent starts immediately, `in_progress` is acceptable. The claim must include owner, branch when known, and a lease for parallel work.

Do not take over another owner’s workstream unless the previous owner released it, the coordinator reassigned it, or the workstream is clearly stale by project policy.

## Evidence

Every status transition must add an Activity Log entry:

```markdown
## Activity Log

- 2026-04-30 codex: claimed workstream; branch `codex/parser-work`.
- 2026-04-30 codex: implemented parser path; narrow test `cargo test parser` passes.
- 2026-04-30 codex: blocked on UI decision; unblock when product confirms empty-state copy.
```

For `blocked`, include:

```markdown
## Blocked

Reason:
Unblock when:
Owner to unblock:
```

## STATUS.md Sync Rules

When updating a workstream:

1. Update the workstream file first.
2. Update only that workstream’s row in `STATUS.md`.
3. Update `STATUS.md` summary fields only when the aggregate status changed.
4. Do not rewrite unrelated rows or reformat the whole table.

## Completion Criteria

A spec can be marked `done` only when:

- Required implementation workstreams are `merged`.
- Validation is complete and recorded.
- The main session accepted the worker output and recorded acceptance evidence.
- `PRODUCT.md` describes the behavior that shipped.
- `TECH.md` describes the implementation shape that landed.
- Follow-ups are either complete, moved to a new spec/issue, or explicitly deferred.
