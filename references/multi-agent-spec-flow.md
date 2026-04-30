# Multi-Agent Spec Flow

Use this workflow when multiple agents, branches, or owners may implement the same spec in parallel.

## Model

```text
Spec = product and technical intent plus overall status
Workstream = concurrency unit owned by one agent or owner at a time
Agent = claims and updates one workstream
Integrator = coordinates conflicts, merge order, and final validation
```

## Directory Shape

```text
specs/<spec-id>/
  PRODUCT.md
  TECH.md
  STATUS.md
  workstreams/
    01-contract.md
    02-core.md
    03-ui.md
    04-tests.md
```

Use one `01-implementation.md` workstream for small tasks. Split only when parallelism reduces risk or wait time.

## Overall Spec Status

`STATUS.md` owns the global board:

```yaml
---
spec_id: gh-123-example
status: active
implementation: partial
validation: partial
coordinator: alice
updated: 2026-04-30
---
```

The workstream table should summarize, not replace, workstream files:

```markdown
| ID | Scope | Status | Owner | Branch / PR | Depends on | Updated |
|---|---|---|---|---|---|---|
| 01 | API contract | in_progress | agent-a | codex/gh-123/01-contract | | 2026-04-30 |
| 02 | UI flow | blocked | agent-b | codex/gh-123/02-ui | 01 | 2026-04-30 |
```

## Workstream Status Machine

```text
ready -> claimed -> in_progress -> implemented -> validating -> validated -> merged
           |             |              |
           v             v              v
        released      blocked        blocked
```

Rules:

- `ready`: available to claim.
- `claimed`: reserved, not yet actively changed.
- `in_progress`: implementation is underway.
- `implemented`: code or docs are written, validation incomplete.
- `validating`: validation is underway.
- `validated`: validation evidence exists, not necessarily merged.
- `merged`: landed in target branch.
- `blocked`: cannot continue until a named condition is resolved.
- `released`: claim was intentionally given up and can return to `ready`.

Do not use `done` for workstreams.

## Claim And Lease

Each workstream frontmatter should include:

```yaml
---
id: 01-contract
status: claimed
owner: agent-a
branch: codex/gh-123/01-contract
pr:
files:
  - src/api/*
depends_on: []
claimed_at: 2026-04-30T10:00:00+08:00
lease_expires_at: 2026-04-30T12:00:00+08:00
updated: 2026-04-30
---
```

Rules:

- Claim before editing.
- Use a lease for parallel work so stale claims can be recovered.
- Update `lease_expires_at` when continuing substantial work.
- Do not take over another owner’s active lease without coordinator action or clear stale-policy evidence.
- When releasing work, set status to `released`, record why, then coordinator or next owner can move it to `ready`.

## Agent Update Rules

- Update your workstream file first.
- Update only your row in `STATUS.md`.
- Do not rewrite the entire `STATUS.md` table.
- Do not edit another agent’s workstream except for coordinator-approved handoff or mechanical conflict resolution.
- Do not modify another workstream’s declared files without recording the conflict or requesting a split.
- Add an Activity Log entry for every status transition.

## Dependency And Conflict Rules

- Use `depends_on` for ordered work.
- Shared contracts should usually be their own workstream, such as `01-contract.md`.
- If UI depends on API, UI can be `blocked` or work against a documented mock until contract validation exists.
- If two agents need the same files, split the workstream or appoint an integrator.
- Contract changes must update `TECH.md` before dependent workstreams rely on them.

## Recommended Workstream Split

Use only what the spec needs:

```text
01-contract    API, schema, shared types, file formats, public surface
02-core        domain, backend, core implementation
03-ui          UI, interaction, visual states
04-tests       integration, e2e, regression coverage
05-docs        docs, migration notes, release notes
```

## Integrator Flow

```text
draft/ready spec
-> coordinator splits workstreams
-> agents claim with leases
-> agents implement and validate
-> workstreams reach validated
-> integrator checks conflicts and merge order
-> workstreams merge
-> full validation runs
-> STATUS.md moves to ready-review
-> review/merge
-> STATUS.md moves to done
```

Integrator responsibilities:

- Confirm `PRODUCT.md` still describes intended behavior.
- Confirm `TECH.md` matches implementation shape.
- Resolve cross-workstream conflicts.
- Run broad validation.
- Move unresolved follow-ups to new specs/issues or explicit deferrals.

## Done Criteria

The overall spec can be `done` only when:

- Required workstreams are `merged`.
- Validation is complete and recorded.
- `PRODUCT.md` matches shipped behavior.
- `TECH.md` matches landed implementation.
- Follow-ups are complete, tracked elsewhere, or explicitly deferred.
- `STATUS.md` has a final Activity Log entry.
