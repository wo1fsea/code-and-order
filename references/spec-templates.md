# Spec Templates

## PRODUCT.md

```markdown
# <Feature> Product Spec

## Summary

One to three sentences describing the desired outcome.

## Goals / Non-goals

- Goal:
- Non-goal:

## Behavior

1. Describe the default behavior.
2. Describe each user-visible state.
3. Describe inputs, outputs, errors, empty states, cancellation, permissions, accessibility, and edge cases.

## Open Questions

- 
```

## TECH.md

```markdown
# <Feature> Tech Spec

Product spec: `./PRODUCT.md`

## Context

- Current system behavior.
- Relevant files, commands, APIs, and ownership boundaries.

## Proposed Changes

- Modules to change.
- New types, files, state, data flow, or migration steps.
- Tradeoffs and why this shape fits the repo.

## Testing and Validation

- Behavior 1 -> automated test or manual validation.
- Behavior 2 -> automated test or manual validation.

## Risks and Follow-ups

- Risk:
- Follow-up:
```

## STATUS.md

```markdown
---
spec_id: <spec-id>
status: ready
implementation: not_started
validation: not_started
coordinator:
updated: YYYY-MM-DD
---

# Status

## Summary

## Workstreams

| ID | Scope | Status | Owner | Branch / PR | Depends on | Updated |
|---|---|---|---|---|---|---|
| 01 | Implementation | ready | unassigned | | | |

## Activity Log

- YYYY-MM-DD: status initialized.
```

## Workstream

```markdown
---
id: 01-implementation
status: ready
owner: unassigned
branch:
pr:
files: []
depends_on: []
claimed_at:
lease_expires_at:
updated: YYYY-MM-DD
---

# Implementation Workstream

## Scope

## Plan

## Progress

## Validation

## Blocked

Reason:
Unblock when:
Owner to unblock:

## Activity Log

- YYYY-MM-DD: workstream initialized.
```

## Spec ID Examples

Use `specs/<source>-<id>-<short-slug>/`.

```text
specs/gh-123-open-file-tilde/
specs/linear-app-1066-agent-autonomy/
specs/jira-core-42-auth-retry/
specs/rfc-0001-repo-governance/
specs/adhoc-20260430-tdd-bootstrap/
```

See `references/spec-id-policy.md` for the full policy.

See `references/spec-execution-status.md` for lifecycle and workstream status rules.

See `references/spec-production.md` for spec authoring flow.

See `references/multi-agent-spec-flow.md` for parallel implementation flow.
