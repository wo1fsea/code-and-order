---
language: en-US
audience: agent
doc_type: normative
---

# Spec-First Delivery

Use this workflow for project work by default. Tiny mechanical changes and
emergency fixes may use direct implementation only when the exception is
explicitly recorded.

## Principle

Project delivery is spec first. The main session owns intent and acceptance.
Implementation work is delegated to subagents or worker sessions through
claimed workstreams. The main session validates the result before the spec can
move to review or done.

## Fixed Flow

```text
main session intake
-> PRODUCT.md
-> TECH.md
-> STATUS.md and workstreams
-> subagent implementation
-> subagent validation and handoff
-> main session acceptance
-> review or done
```

## Role Boundaries

### Main Session

The main session acts as coordinator and acceptor:

- Clarifies the request.
- Produces or revises the spec before implementation.
- Confirms `PRODUCT.md` behavior and non-goals.
- Confirms `TECH.md` is grounded in the current repo.
- Splits work into workstreams.
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
- The change is a tiny mechanical update with no behavior, contract, or
  governance effect.

Even with an exception, record the spec/workstream status and run a separate
acceptance pass before marking the work complete.
