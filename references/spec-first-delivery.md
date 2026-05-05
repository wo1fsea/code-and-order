---
language: en-US
audience: agent
doc_type: normative
---

# Spec-First Delivery

Use this workflow for project work by default. Tiny mechanical changes and
emergency fixes may use direct implementation only when the exception is
explicitly recorded.

Run `references/spec-decision-gate.md` before this workflow to decide whether
the task needs a new spec, an existing spec update, a compact spec, or a direct
implementation exception.

Use `references/compact-specs.md` for bug fixes and small tweaks that need a
thin spec rather than a full feature spec.

## Principle

Project delivery is spec first. The main session owns intent and acceptance.
Implementation is parallel-first: before work starts, the main session must run
a Parallelization Gate and prefer independent workstreams delegated to
subagents or worker sessions. Serial implementation is allowed only when the
task is atomic, highly conflict-prone, blocked on unresolved shared contracts,
an explicit tiny or emergency exception, or cheaper to complete directly than
to coordinate. The main session validates the result before the spec can move
to review or done.

## Fixed Flow

```text
main session intake
-> Spec Decision Gate
-> PRODUCT.md
-> TECH.md
-> Parallelization Gate
-> STATUS.md and workstreams
-> subagent implementation
-> subagent validation and handoff
-> main session acceptance
-> review or done
```

## Parallelization Gate

Before implementation starts, record this gate in `STATUS.md`. The handoff may
repeat the relevant decision, but it does not replace the status record:

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

Default to parallel workstreams for non-trivial specs. Use one serial
workstream only when the scope is atomic, the same files would be edited by
multiple agents, a shared contract must be resolved first, the change is a
recorded direct-implementation exception, or coordination cost is higher than
the work itself.

## Role Boundaries

### Main Session

The main session acts as coordinator and acceptor:

- Clarifies the request.
- Produces or revises the spec before implementation.
- Confirms `PRODUCT.md` behavior and non-goals.
- Confirms `TECH.md` is grounded in the current repo.
- Runs the Parallelization Gate and records why any serial path is acceptable.
- Splits work into independent workstreams with clear ownership, dependencies,
  and validation expectations.
- Assigns or launches subagents/worker sessions when implementation starts.
- Reviews changed files and workstream evidence.
- Runs or delegates broad validation, then verifies the result directly.
- Moves the overall spec to `ready-review` or `done`.

The main session should not quietly implement substantial spec work itself. If
subagent execution is unavailable, record an explicit exception and keep the
implementation pass separate from the acceptance pass.

### Subagent Or Worker Session

The subagent or worker session owns execution for a claimed workstream:

- Reads `AGENTS.md`, the spec, and relevant governance docs.
- Claims exactly one workstream before editing.
- Implements only the assigned scope.
- Runs narrow validation for its work.
- Updates its workstream file first.
- Updates only its row in `STATUS.md`.
- Reports changed files, validation, blockers, conflicts, residual risk, and
  handoff notes.

The subagent does not mark the overall spec `done`.

## Spec Readiness Gate

Implementation cannot start until the spec has:

- `PRODUCT.md` with observable behavior and non-goals.
- `TECH.md` with current code context, proposed change shape, risks, and
  validation plan.
- `STATUS.md` with `status: ready` or an explicitly accepted `active` state.
- A recorded Parallelization Gate.
- At least one workstream with owner, files or scope, dependencies, and
  validation expectations.
- A main-session handoff note naming the worker/subagent scope.

## Subagent Handoff

Use this handoff when assigning work:

```markdown
## Subagent Handoff

- Spec:
- Workstream:
- Scope:
- Files or modules:
- Must preserve:
- Validation to run:
- Do not touch:
- Handoff back with:
```

## Worker Completion Report

The subagent should return:

```markdown
## Worker Completion

- Workstream:
- Status:
- Files changed:
- Validation run:
- Validation not run:
- Behavior/spec changes:
- Conflicts or blockers:
- Residual risk:
- Suggested acceptance checks:
```

## Main Session Acceptance

The main session accepts the work only after:

- Reviewing the diff against `PRODUCT.md` and `TECH.md`.
- Checking that workstream scope was respected.
- Running the narrow validation again when practical.
- Running broader validation when behavior, contracts, persistence, UI, or
  shared modules changed.
- Checking docs, temp artifacts, change gate, and code-quality evidence.
- Updating `STATUS.md` and activity logs.

Acceptance output:

```markdown
## Main Session Acceptance

- Spec:
- Workstreams accepted:
- Diff reviewed:
- Validation run:
- Additional fixes required:
- Status update:
- Residual risk:
```

## Exceptions

Direct main-session implementation is allowed only when one is true:

- The change is an emergency fix and delay would be riskier than process.
- Subagent tooling is unavailable and the exception is recorded.
- The change is a tiny mechanical update with no behavior, contract, data, UI,
  configuration, permissions, security, test, docs, or governance impact.

Even with an exception, record the spec/workstream status and run a separate
acceptance pass before marking the work complete.

Bug fixes and small tweaks are not direct-implementation exceptions by default.
If they affect behavior, contracts, UI, data, configuration, permissions,
security, tests, docs, or governance, create a compact spec.
