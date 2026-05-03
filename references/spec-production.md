# Spec Production

Use this workflow when turning a fuzzy request, issue, or product idea into a repo-native spec.

## Principle

Produce stable intent before implementation. A spec is not ready because files exist; it is ready when behavior, implementation context, status, ownership, and validation are clear enough for a human or agent to execute.

## Flow

```text
intake -> clarify -> classify -> assign spec id -> PRODUCT -> behavior review -> code inspection -> TECH -> STATUS/workstreams -> validation plan -> draft or ready
```

## Intake

Capture:

- Source request, issue, ticket, or decision.
- User or API-visible outcome.
- Scope and non-goals.
- Known constraints, deadlines, and owners.
- Whether UI, API, data, permissions, security, migration, or agent workflows are affected.

## Clarify Before Writing

Ask concise questions when answers would change the spec:

- Who is the user or caller?
- What behavior changes?
- What must not change?
- What are the success criteria?
- What failure, empty, loading, permission, cancellation, or rollback paths matter?
- Which repo pattern and validation weight apply?
- Does this need one workstream or parallel workstreams?

Do not invent product intent when the answer would affect implementation.

## Classify

Classify the spec:

- `feature`: new user/API-visible behavior.
- `bugfix`: incorrect existing behavior with reproduction evidence.
- `refactor`: implementation change intended to preserve behavior.
- `migration`: data, schema, storage, or compatibility transition.
- `governance`: repo rules, workflow, templates, or agent guidance.
- `research`: investigation whose implementation path is not yet known.

## Assign Spec ID

Use `references/spec-id-policy.md`.

Default shape:

```text
specs/<source>-<id>-<short-slug>/
```

If no external tracker exists, use `rfc-<4-digit-number>-<slug>` for accepted governance/architecture work or `adhoc-<YYYYMMDD>-<slug>` for short-lived exploration.

## Write PRODUCT.md First

`PRODUCT.md` describes testable behavior, not implementation.

Required sections:

- Summary.
- Goals and non-goals.
- Behavior invariants as a numbered list.
- States and edge cases.
- Open questions.

Good behavior invariant:

```markdown
1. When a signed-out user opens the billing page, the app redirects to sign-in and preserves the return URL.
```

Weak behavior statement:

```markdown
- Make billing better.
```

## Review Behavior

Before writing `TECH.md`, check:

- Each behavior item is observable or testable.
- Non-goals prevent obvious scope creep.
- Open questions are explicit.
- UI-visible behavior references visual evidence expectations.
- API or contract behavior references compatibility expectations.

If product intent is not stable, keep the spec `draft`.

## Inspect Code Before TECH.md

`TECH.md` must be grounded in the actual repo.

Inspect:

- Existing files, modules, commands, tests, and ownership boundaries.
- Current behavior and relevant failure paths.
- Existing abstractions and contracts.
- Migration, compatibility, security, or validation risks.

Do not write implementation plans purely from memory or preference.

## Write TECH.md

Required sections:

- Context.
- Proposed changes.
- Touched files or modules.
- Contract, data, config, dependency, and migration impact.
- Workstream split when parallel work is useful.
- Testing and validation.
- Risks and follow-ups.

Apply `references/change-gate.md` before adding new surface.

## Initialize STATUS.md And Workstreams

Use `references/spec-execution-status.md` for status values.

For incomplete specs:

```yaml
status: draft
implementation: not_started
validation: not_started
```

For accepted specs that are ready to implement:

```yaml
status: ready
implementation: not_started
validation: not_started
```

Small specs can use:

```text
workstreams/01-implementation.md
```

Parallel specs should split by ownership or dependency boundary, for example:

```text
workstreams/01-contract.md
workstreams/02-core.md
workstreams/03-ui.md
workstreams/04-tests.md
workstreams/05-docs.md
```

Use `references/spec-first-delivery.md` before implementation handoff.

Use `references/multi-agent-spec-flow.md` when more than one agent may implement work in parallel.

## Define Validation

Validation should map back to behavior invariants.

Record:

- Narrow commands.
- Broader regression commands.
- Manual checks.
- Visual evidence for UI-visible behavior.
- Contract, migration, rollback, or observability checks when relevant.

## Handoff Output

After producing or revising a spec, summarize:

```markdown
## Spec Handoff

- Spec path:
- Status:
- Spec type:
- Open questions:
- Workstreams:
- Next owner:
- Validation expectation:
- Ready to implement: yes/no
- Subagent handoff required: yes/no
```
