#!/usr/bin/env python3
"""Create a human-agent governance starter set for a repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SPEC_ID_RE = re.compile(
    r"^(?:gh-\d+|linear-[a-z0-9]+-\d+|jira-[a-z0-9]+-\d+|rfc-\d{4}|adhoc-\d{8})"
    r"-[a-z0-9]+(?:-[a-z0-9]+)*$"
)

LOCK_RELATIVE_PATH = Path("docs/governance/code-and-order.lock.json")
LOCK_SCHEMA_VERSION = 1
SOURCE_REPO_FALLBACK = "https://github.com/wo1fsea/code-and-order"
SOURCE_REF = "main"


GITIGNORE = """.out/
"""


def agents_md(tdd: str) -> str:
    tdd_row = (
        "| TDD work | `docs/governance/tdd-workflow.md` |\n"
        if tdd != "off"
        else ""
    )
    return f"""---
language: en-US
audience: agent
doc_type: router
---

# AGENTS.md

This is the canonical routing file for all coding agents.

Keep this file short. Put detailed rules in `docs/governance/` and use this file to route agents to the right workflow.

## Read Order

1. Read this file first.
2. Read the relevant workflow under `docs/governance/` before acting.
3. If instructions conflict, prefer the more specific workflow file.
4. If a workflow file is missing or stale, update it before relying on it.

## Governance Map

| Situation | Read |
|---|---|
| Any code change | `docs/governance/development-workflow.md` |
| New or changed API, command, config, dependency, adapter, workflow doc, template, or agent entrypoint | `docs/governance/change-gate.md` |
| Code structure, interfaces, dead code, dependencies, or compatibility layers | `docs/governance/code-quality.md` |
| README, docs, examples, generated docs, specs, contributor guidance, or agent instructions | `docs/governance/documentation-standards.md` |
| Screenshots, recordings, traces, logs, reports, debug dumps, or scratch files | `docs/governance/temp-artifacts.md` |
| Bug fixes, small behavior tweaks, or direct implementation exceptions | `docs/governance/compact-specs.md` |
| Spec-first project delivery, implementation handoff, or main-session acceptance | `docs/governance/spec-first-delivery.md` |
| Ambiguous feature or cross-module change | `docs/governance/spec-workflow.md` |
| Creating or revising specs | `docs/governance/spec-production.md` |
| Choosing or reviewing a spec id | `docs/governance/spec-id-policy.md` |
| Spec execution status or parallel workstreams | `docs/governance/spec-execution-status.md` |
| Multi-agent parallel spec implementation | `docs/governance/multi-agent-spec-flow.md` |
{tdd_row}| Validation or test reporting | `docs/governance/validation-workflow.md` |
| PR or review prep | `docs/governance/review-workflow.md` |
| Agent context files | `docs/governance/agent-context.md` |
| Governance file changes, Code & Order version checks, or drift audits | `docs/governance/governance-maintenance.md` |

## Non-Negotiables

- Do not duplicate detailed governance rules in this file or in agent adapter files.
- Thin adapter files such as `CLAUDE.md`, `GEMINI.md`, and `.github/copilot-instructions.md` must point here instead of copying rules.
- When adding, deleting, renaming, or moving governance documents, update this file in the same change.
- When changing which workflow applies to a task type, update the Governance Map in this file in the same change.
- New or substantially changed durable docs must declare `language`, `audience`, and `doc_type` near the top.
- Agent-facing docs use English by default unless a local exception is explicit.
- Do not duplicate long-lived documentation; keep one source of truth and route to it.
- Bug fixes and small tweaks use compact specs unless the change is purely mechanical with no behavior, contract, data, UI, test, or governance impact.
- Subagents or worker sessions implement spec work; the main session accepts it.
- Do not skip tests or validation silently. Record what ran and what did not.
- Do not preserve dead code, stale flags, or compatibility paths without an owner and deletion condition.
- Do not scatter temporary artifacts through the repo. Use `.out/` unless local rules say otherwise.
- Do not hand-edit `docs/governance/code-and-order.lock.json`; use the Code & Order initializer audit, adopt, or update modes.
- Do not revert user changes unless explicitly asked.
"""


CLAUDE = """---
language: en-US
audience: agent
doc_type: router
---

# CLAUDE.md

@AGENTS.md
"""


GEMINI = """---
language: en-US
audience: agent
doc_type: router
---

# GEMINI.md

@AGENTS.md
"""


COPILOT = """---
language: en-US
audience: agent
doc_type: router
---

# GitHub Copilot Instructions

Follow `AGENTS.md` as the canonical repository guidance. Do not duplicate governance rules here.
"""


GOV_README = """---
language: en-US
audience: agent
doc_type: router
---

# Governance

This directory holds the detailed engineering governance workflows.

`AGENTS.md` is the canonical router. If files here are added, removed, renamed, or moved, update `AGENTS.md` in the same change.

`code-and-order.lock.json` records which Code & Order version initialized or last updated managed governance files.
"""


AGENT_CONTEXT = """---
language: en-US
audience: agent
doc_type: normative
---

# Agent Context

## Canonical Rule

`AGENTS.md` is the canonical routing file for all coding agents.

## Thin Adapters

- `CLAUDE.md` imports `AGENTS.md`.
- `GEMINI.md` imports `AGENTS.md`.
- `.github/copilot-instructions.md` points to `AGENTS.md`.

Adapter files must not duplicate detailed workflow rules. Add tool-specific notes only when the tool truly requires them.

## Maintenance

When an adapter is added, removed, renamed, or moved, update this file and `AGENTS.md` in the same change.
"""


DEVELOPMENT = """---
language: en-US
audience: agent
doc_type: normative
---

# Development Workflow

## Outer Loop

Use this loop for all non-trivial engineering work:

```text
Plan -> Develop -> Verify -> Fix
```

1. Plan: read the relevant governance docs, create or update the spec, identify risk, and choose the smallest coherent task shape.
2. Develop: hand implementation to a subagent or worker session through `docs/governance/spec-first-delivery.md`. When TDD applies, use `docs/governance/tdd-workflow.md` inside this phase.
3. Verify: the worker runs narrow validation, then the main session verifies and broadens when behavior or shared contracts changed. When TDD applies, the broaden/validate/record steps come from `docs/governance/tdd-workflow.md`.
4. Fix: respond to failing tests, review feedback, or validation gaps. If reality changed, update specs or governance docs before repeating Develop/Verify.

TDD is not a competing workflow. It is the inner loop used inside Develop and Verify when behavior changes call for it.

## Default Steps

1. Read `AGENTS.md`.
2. Read the workflow file that matches the task.
3. Create or update the relevant spec before implementation, unless an explicit tiny or emergency exception applies.
4. Split work into workstreams and hand implementation to a subagent or worker session.
5. If adding or expanding project surface, apply `docs/governance/change-gate.md`.
6. For code changes, apply `docs/governance/code-quality.md`.
7. For docs, examples, generated docs, specs, contributor guidance, or agent instructions, apply `docs/governance/documentation-standards.md`.
8. If producing temporary artifacts, apply `docs/governance/temp-artifacts.md`.
9. Make the smallest coherent change in the worker/subagent pass.
10. Run the narrowest meaningful validation first.
11. Return a worker completion report.
12. Main session reviews, validates, and accepts before marking the spec ready-review or done.
13. Record tests run, docs checked, tests skipped, and residual risk.

## Direct Implementation Exceptions

Direct main-session implementation is an exception. Use it only for emergency fixes, unavailable subagent tooling with an explicit note, or tiny mechanical changes with no behavior, contract, or governance effect.

## Spec-Driven Implementation

Use `docs/governance/spec-workflow.md` when behavior is ambiguous, user-visible, cross-module, or high risk.

Use `docs/governance/spec-first-delivery.md` for the fixed coordinator -> worker -> acceptance flow.
"""


CHANGE_GATE = """---
language: en-US
audience: agent
doc_type: normative
---

# Change Gate

Use this gate before adding or expanding project surface. Every new surface must prove that it deserves to exist.

## What Counts As Surface

- API endpoint or route.
- Public or exported function, class, component, package export, or module.
- CLI command, option, flag, or output format.
- Configuration field, environment variable, feature flag, or runtime mode.
- Dependency, adapter, integration, provider, or compatibility shim.
- File format, schema, database shape, event format, or protocol message.
- Workflow document, governance file, template, agent entrypoint, or generated starter file.
- Plugin extension point, hook, callback, or user-facing customization point.

## When Required

Run the gate when a change adds, expands, renames, replaces, deprecates, or removes surface.

## Gate Questions

```markdown
## Change Gate

- Problem:
- Existing path considered:
- Why existing path is insufficient:
- Smallest new surface:
- What will be deleted or replaced:
- Owner:
- Validation:
- Temporary or permanent:
- Removal condition:
```

## Rules

- Prefer reuse before adding surface.
- Keep new surface minimal.
- Delete superseded paths in the same change unless compatibility requires retention.
- New configs, flags, adapters, dependencies, workflows, and templates need owners.
- New surface needs validation tied to the surface.
- Temporary surface needs a concrete removal condition.
- Public surface needs compatibility notes.
- Documentation surface counts.
- Dependencies count.

## Compatibility Exception

```markdown
## Compatibility Exception

- Old path:
- New path:
- Why retained:
- Owner:
- Remove when:
- Tracking issue/spec:
- Validation:
```
"""


CODE_QUALITY = """---
language: en-US
audience: agent
doc_type: normative
---

# Code Quality

Use these rules as review gates for code changes. Violations should be fixed or recorded as explicit, owned exceptions.

## Related Gates

- Before adding or expanding project surface, apply `docs/governance/change-gate.md`.
- When producing screenshots, recordings, traces, logs, generated reports, debug dumps, or scratch files, apply `docs/governance/temp-artifacts.md`.

## Required Rules

1. Remove dead code.
   - Delete unused functions, exports, classes, components, routes, flags, configs, unreachable branches, stale adapters, and obsolete compatibility paths.
   - Keep legacy code only when it has an owner, a reason, and a deletion condition.

2. Keep capability interfaces orthogonal.
   - Each public function, API, command, option, or configuration field should represent one independent concept.
   - Do not combine unrelated behavior behind positional flags, mode strings, or overloaded parameters.
   - If parameters constrain each other, introduce a named options object, split the interface, or model the valid states explicitly.

3. Separate commands from queries.
   - Query-shaped APIs must not mutate durable state, create records, emit irreversible side effects, or hide refresh/write behavior.
   - Mutating APIs should be named as commands and document their side effects.

4. Model state explicitly.
   - Do not represent complex lifecycle state with loose boolean clusters.
   - Prefer a single status enum, tagged union, state machine, or domain object that makes invalid states unrepresentable.

5. Keep side effects at boundaries.
   - Core logic should not directly read the network, database, filesystem, environment, current time, randomness, process state, or global mutable state.
   - Pass side-effectful dependencies through parameters, adapters, services, or dependency injection points that are easy to test.

6. Maintain one source of truth.
   - Do not store the same business state in multiple fields, caches, configs, or services without a documented owner.
   - If denormalization or caching is required, define invalidation, precedence, and conflict resolution.

7. Collapse duplicate business rules.
   - When the same business rule appears a third time, centralize it or record why duplication is safer for now.

8. Reject speculative abstractions.
   - Do not add frameworks, base classes, plugin systems, generic engines, or extension points for hypothetical future use.
   - Abstract from real repetition, separate ownership, or proven variation.

9. Name code by its real behavior.
   - Function and module names must expose meaningful side effects.
   - `validateUser` must not write records. `formatConfig` must not read environment.

10. Design lifecycle APIs as a set.
    - If a capability has `create`, decide whether `update`, `delete`, `archive`, `restore`, `list`, and `get` exist.
    - If an operation is intentionally absent, record the product or domain reason.

11. Use distinguishable errors.
    - Callers should be able to distinguish validation, permission, not-found, conflict, timeout, dependency failure, and internal failure when those cases require different handling.

12. Govern dependencies.
    - New dependencies need a reason, an owner, and a note on why the standard library or existing dependency is not enough.

13. Govern TODOs and incomplete code.
    - `TODO`, `FIXME`, temporary flags, and partial compatibility paths must include an owner or issue/spec id.

14. Govern configuration and feature flags.
    - Every config or flag needs a default, scope, owner, and removal or review condition.
    - Expired flags and unused config are dead code.

15. Give compatibility layers an exit plan.
    - Migration paths, adapters, legacy branches, fallbacks, and shims must state why they exist and when they can be deleted.

## Exception Format

```markdown
## Code Quality Exception

- Rule:
- Reason:
- Owner:
- Remove or revisit when:
- Tracking issue/spec:
- Validation:
```
"""


DOCUMENTATION_STANDARDS = """---
language: en-US
audience: agent
doc_type: normative
---

# Documentation Standards

Documentation is project surface. It should have a clear source of truth, audience, scope, validation path, and retirement path.

## When Required

Apply this when a change:

- Adds, moves, renames, deletes, or substantially rewrites a doc.
- Changes user/API-visible behavior that existing docs describe.
- Changes commands, configuration, environment variables, file formats, schemas, setup, deployment, validation, or troubleshooting steps.
- Adds or changes examples, snippets, templates, generated docs, screenshots, diagrams, or public contributor guidance.
- Changes agent instructions, governance files, specs, or routing docs such as `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, or `docs/README.md`.

If a behavior change does not require documentation, record why in the PR, workstream, or change note.

## Language And Audience

Every new or substantially changed durable doc must declare its language near the top.

```yaml
---
language: en-US
audience: agent
doc_type: normative
---
```

Rules:

- Use `en-US` for agent-facing docs by default.
- Use the target reader's language for user-facing or team-facing docs.
- Use `mixed` only when multiple languages are intentional, and label sections clearly.
- Do not mix languages casually inside normative instructions.
- Code identifiers, commands, paths, flags, API names, and error strings remain literal.
- Use a hidden comment metadata block when YAML frontmatter would leak into generated output.

Existing docs without metadata should be backfilled when touched, moved, audited, or promoted.

## Required Rules

1. Define one source of truth.
   - Do not copy the same rule, command, API shape, or setup instruction into multiple long-lived docs.
   - If multiple entrypoints need the same information, make one canonical and point the others to it.

2. State audience and scope early.
   - A reader should quickly know whether the doc is for users, contributors, maintainers, operators, reviewers, or agents.

3. Keep routers thin.
   - Entry files such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions, root README sections, and docs indexes should route, not duplicate.
   - When adding, deleting, renaming, or moving canonical docs, update the router in the same change.

4. Update docs with behavior.
   - Code changes that alter documented behavior must update the relevant docs in the same change or record why no doc update is needed.

5. Validate examples and commands.
   - Commands should include working directory, required environment, expected output shape, or validation context when not obvious.
   - Snippets and examples must either be runnable/verified or clearly marked illustrative.

6. Treat generated docs as generated.
   - Record the generator or source.
   - Update the source and regenerate instead of hand-editing generated output, unless the repo documents an exception.

7. Delete or supersede stale docs.
   - When a doc is obsolete, remove it or mark it superseded with the replacement path.
   - Do not preserve old docs without owner and review condition.

8. Separate durable docs from working notes.
   - Drafts, raw agent notes, debug output, screenshots, recordings, traces, and generated reports stay in `.out/` until accepted or promoted.

## Documentation Evidence

```markdown
## Documentation Evidence

- Docs updated / N/A:
- Language/audience/doc type declared:
- Source of truth:
- Routers or indexes updated:
- Links checked:
- Examples or commands checked:
- Generated docs regenerated / N/A:
- Stale docs removed or superseded:
```
"""


TEMP_ARTIFACTS = """---
language: en-US
audience: agent
doc_type: normative
---

# Temp Artifacts

Temporary artifacts are useful during work, but they must not pollute formal repo knowledge.

## Default Directory

Use `.out/` by default:

```text
.out/
  screenshots/
  recordings/
  traces/
  logs/
  reports/
  scratch/
```

`.out/` should be gitignored unless the repo has a stronger local convention.

## Artifact Classes

- `ephemeral`: temporary debugging output. Default: do not commit.
- `evidence`: validation evidence referenced by a PR, spec, or workstream. Default: cite the path, do not commit.
- `promoted`: artifact that must be retained long term. Move it into an owned docs/spec location.

## Rules

- Put temporary artifacts in `.out/`.
- Do not commit `.out/` by default.
- Evidence can be referenced without being committed.
- Promote long-term artifacts into owned locations such as `docs/assets/`, `docs/reports/`, or `specs/<spec-id>/evidence/`.
- Do not place unpromoted artifacts in repo root, `docs/`, `specs/`, `src/`, or `tests/`.
- Raw agent drafts stay in `.out/scratch/` until explicitly accepted.
- Cleanup is part of done.
- Do not write secrets, tokens, private customer data, or sensitive logs into `.out/`.

## Reporting

```markdown
## Temp Artifacts

- Created:
- Referenced as evidence:
- Promoted:
- Cleaned:
- Intentionally retained:
```
"""


COMPACT_SPECS = """---
language: en-US
audience: agent
doc_type: normative
---

# Compact Specs

Use compact specs for bug fixes and small behavior tweaks. They keep spec-first delivery lightweight while preserving intent, boundaries, and validation evidence.

## Rule

Bug fixes and small tweaks still use spec-first when they affect behavior, contracts, UI, data, configuration, permissions, tests, or governance.

Use a direct implementation exception only for purely mechanical changes with no behavior, contract, data, UI, test, or governance effect.

## Shape

Keep the normal spec directory, but make the content short:

```text
specs/<spec-id>/
  PRODUCT.md
  TECH.md
  STATUS.md
  workstreams/
    01-fix.md
```

For small tweaks, use `workstreams/01-tweak.md` when clearer.

## Bug Fix PRODUCT.md

Write bug fix specs as restored behavior, not as new functionality:

```markdown
# Bugfix Behavior Spec

## Observed

What currently fails.

## Expected

What behavior should be restored.

## Regression Invariant

The condition that must not break again.

## Reproduction

1. Step.
2. Step.

## Non-Goals

- Do not redesign unrelated behavior.
- Do not change public contracts unless explicitly required.
```

## Bug Fix TECH.md

```markdown
# Bugfix Tech Spec

## Suspected Area

- Files, modules, commands, or contracts likely involved.

## Change Shape

- Smallest intended fix.
- Regression test to add or update.
- Public API, data, UI, and config surfaces that must stay unchanged.

## Validation

- Narrow command:
- Regression command:
- Manual or visual check:

## Risk

- Why this fix could break adjacent behavior.
```

## Small Tweak PRODUCT.md

Use for copy, default values, narrow UI states, sorting, labels, small interaction changes, and other intentional but limited behavior changes.

```markdown
# Small Tweak Behavior Spec

## Current

Existing behavior.

## Desired

New narrow behavior.

## Acceptance

- Observable result.
- Existing behavior to preserve.

## Affected Surface

- UI, API, config, docs, or command surface affected.

## Non-Goals

- Do not expand scope.
- Do not redesign or refactor unrelated areas.
```

## Small Tweak TECH.md

```markdown
# Small Tweak Tech Spec

## Files Or Modules

- Expected touch points.

## Change Shape

- Smallest change.
- Surfaces that must remain unchanged.

## Validation

- Automated check:
- Manual check:
- Visual evidence when UI-visible:
```

## Direct Implementation Exception

Do not create a full spec only when the change is purely mechanical. Record the exception in the handoff, PR, or implementation log:

```markdown
## Direct Implementation Exception

- Reason: tiny mechanical change
- Behavior impact: none
- Contract impact: none
- Data/UI/test/governance impact: none
- Files:
- Validation:
- Main-session acceptance:
```

If any impact field is not `none`, use a compact spec.

## Acceptance

The main session accepts compact spec work by checking:

- The fix or tweak matches `PRODUCT.md`.
- The implementation stayed within `TECH.md` and non-goals.
- Regression or acceptance evidence was recorded.
- No extra surface, refactor, or behavior expansion slipped in.
"""


SPEC_FIRST_DELIVERY = """---
language: en-US
audience: agent
doc_type: normative
---

# Spec-First Delivery

Project delivery is spec first by default. The main session owns intent, coordination, and acceptance. Subagents or worker sessions implement claimed workstreams and hand back evidence. Tiny mechanical changes and emergency fixes may use direct implementation only when the exception is explicitly recorded.

Use `docs/governance/compact-specs.md` for bug fixes and small tweaks that need a thin spec rather than a full feature spec.

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

## Main Session

The main session acts as coordinator and acceptor:

- Clarify the request.
- Produce or revise the spec before implementation.
- Confirm `PRODUCT.md` behavior and non-goals.
- Confirm `TECH.md` is grounded in the current repo.
- Split work into workstreams.
- Assign or launch subagents/worker sessions when implementation starts.
- Review changed files and workstream evidence.
- Run broad validation or verify that it was run.
- Move the overall spec to `ready-review` or `done`.

The main session should not quietly implement substantial spec work itself. If subagent execution is unavailable, record an exception and keep implementation and acceptance as separate passes.

## Subagent Or Worker Session

The subagent or worker session owns execution for a claimed workstream:

- Read `AGENTS.md`, the spec, and relevant governance docs.
- Claim exactly one workstream before editing.
- Implement only the assigned scope.
- Run narrow validation for the work.
- Update the workstream file first.
- Update only that row in `STATUS.md`.
- Report changed files, validation, blockers, conflicts, residual risk, and handoff notes.

The subagent does not mark the overall spec `done`.

## Spec Readiness Gate

Implementation cannot start until the spec has:

- `PRODUCT.md` with observable behavior and non-goals.
- `TECH.md` with current code context, proposed change shape, risks, and validation plan.
- `STATUS.md` with `status: ready` or an explicitly accepted `active` state.
- At least one workstream with owner, scope, dependencies, and validation expectations.
- A main-session handoff note naming the worker/subagent scope.

## Subagent Handoff

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

## Worker Completion

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

Direct main-session implementation is allowed only for emergency fixes, unavailable subagent tooling with an explicit note, or tiny mechanical changes with no behavior, contract, or governance effect. Even then, run a separate acceptance pass before marking work complete.

Bug fixes and small tweaks are not direct-implementation exceptions by default. If they affect behavior, contracts, UI, data, configuration, permissions, tests, or governance, create a compact spec.
"""


SPEC_WORKFLOW = """---
language: en-US
audience: agent
doc_type: normative
---

# Spec Workflow

## When To Write A Spec

Write a spec before implementation when at least one is true:

- Behavior is ambiguous or user-visible.
- The change spans multiple modules or ownership boundaries.
- The change affects persistence, permissions, security, billing, migration, or public APIs.
- A coding agent needs stable product intent before implementation.
- Reviewers need to approve direction before code churn begins.

Use `docs/governance/compact-specs.md` for bug fixes and small behavior tweaks. Skip full specs only for direct implementation exceptions: purely mechanical changes with no behavior, contract, data, UI, test, or governance effect.

## Required Files

```text
specs/<spec-id>/
  PRODUCT.md
  TECH.md
  STATUS.md
  workstreams/
    01-implementation.md
```

`PRODUCT.md` describes user/API-visible behavior as testable invariants.

`TECH.md` describes current code context, proposed changes, validation, risks, and follow-ups.

Use `docs/governance/spec-first-delivery.md` for coordinator handoff, subagent implementation, and main-session acceptance.

Use `docs/governance/compact-specs.md` for bug fix and small tweak specs.

Use `docs/governance/spec-production.md` when creating or revising spec files.

## Keep Specs Current

If implementation changes user-visible behavior, update `PRODUCT.md`.

If implementation changes module boundaries, sequencing, validation, or risks, update `TECH.md`.

Use `docs/governance/spec-execution-status.md` to manage not-started, partial, blocked, ready-review, and completed execution states.

Use `docs/governance/multi-agent-spec-flow.md` when multiple agents or branches implement the same spec in parallel.
"""


SPEC_PRODUCTION = """---
language: en-US
audience: agent
doc_type: normative
---

# Spec Production

Use this workflow when turning a fuzzy request, issue, or product idea into a repo-native spec.

Use `docs/governance/compact-specs.md` when the request is a bug fix or small tweak.

## Flow

```text
intake -> clarify -> classify -> assign spec id -> PRODUCT -> behavior review -> code inspection -> TECH -> STATUS/workstreams -> validation plan -> draft or ready
```

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

## PRODUCT First

`PRODUCT.md` describes testable behavior, not implementation.

Required sections:

- Summary.
- Goals and non-goals.
- Behavior invariants as a numbered list.
- States and edge cases.
- Open questions.

If product intent is not stable, keep the spec `draft`.

For bug fixes, write restored behavior: observed, expected, regression invariant, reproduction, and non-goals.

For small tweaks, write current behavior, desired behavior, acceptance, affected surface, and non-goals.

## Inspect Code Before TECH

`TECH.md` must be grounded in the actual repo.

Inspect existing files, commands, tests, contracts, ownership boundaries, risks, and validation paths before proposing implementation.

Apply `docs/governance/change-gate.md` before adding new surface.

## STATUS And Workstreams

For incomplete specs:

```yaml
status: draft
implementation: not_started
validation: not_started
```

For accepted specs ready to implement:

```yaml
status: ready
implementation: not_started
validation: not_started
```

Small specs can use `workstreams/01-implementation.md`.

Parallel specs should split by ownership or dependency boundary, for example:

```text
workstreams/01-contract.md
workstreams/02-core.md
workstreams/03-ui.md
workstreams/04-tests.md
workstreams/05-docs.md
```

Use `docs/governance/multi-agent-spec-flow.md` when more than one agent may implement work in parallel.

Use `docs/governance/compact-specs.md` for compact bug fix and small tweak templates.

## Handoff

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
"""


SPEC_ID_POLICY = """---
language: en-US
audience: agent
doc_type: normative
---

# Spec ID Policy

## Format

Use:

```text
specs/<source>-<id>-<short-slug>/
```

Examples:

```text
specs/gh-123-open-file-tilde/
specs/linear-app-1066-agent-autonomy/
specs/jira-core-42-auth-retry/
specs/rfc-0001-repo-governance/
specs/adhoc-20260430-tdd-bootstrap/
```

## Rules

- Use lowercase kebab-case.
- Use `gh-<number>-<slug>` for GitHub issues.
- Use `linear-<team>-<number>-<slug>` for Linear tickets.
- Use `jira-<project>-<number>-<slug>` for Jira tickets.
- Use `rfc-<4-digit-number>-<slug>` for governance, architecture, or process decisions.
- Use `adhoc-<YYYYMMDD>-<slug>` only for short-lived exploration.
- Treat the source id as stable and the slug as human-readable context.
"""


SPEC_EXECUTION_STATUS = """---
language: en-US
audience: agent
doc_type: normative
---

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

`STATUS.md` is the global board. It records the overall lifecycle, implementation progress, validation progress, and a summary table of workstreams.

`workstreams/*.md` files are the concurrency unit. Agents should primarily update their own workstream file and synchronize only their row in `STATUS.md`.

Use `docs/governance/multi-agent-spec-flow.md` when multiple agents or branches implement the same spec in parallel.

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

Before starting implementation, an agent must claim a workstream by updating its frontmatter with status, owner, branch when known, and updated date.

For parallel work, include `claimed_at` and `lease_expires_at`.

Do not take over another owner’s workstream unless the previous owner released it, the coordinator reassigned it, or the workstream is clearly stale by project policy.

## Evidence

Every status transition must add an Activity Log entry.

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
- `PRODUCT.md` describes the behavior that shipped.
- `TECH.md` describes the implementation shape that landed.
- Follow-ups are either complete, moved to a new spec/issue, or explicitly deferred.
"""


MULTI_AGENT_SPEC_FLOW = """---
language: en-US
audience: agent
doc_type: normative
---

# Multi-Agent Spec Flow

Use this workflow when multiple agents, branches, or owners may implement the same spec in parallel.

## Model

```text
Spec = product and technical intent plus overall status
Workstream = concurrency unit owned by one agent or owner at a time
Agent = claims and updates one workstream
Integrator = coordinates conflicts, merge order, and final validation
```

## Workstream Status Machine

```text
ready -> claimed -> in_progress -> implemented -> validating -> validated -> merged
           |             |              |
           v             v              v
        released      blocked        blocked
```

Do not use `done` for workstreams.

## Claim And Lease

Each workstream frontmatter should include:

```yaml
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
```

Rules:

- Claim before editing.
- Use a lease so stale claims can be recovered.
- Update `lease_expires_at` when continuing substantial work.
- Do not take over another owner’s active lease without coordinator action or clear stale-policy evidence.
- When releasing work, set status to `released`, record why, then coordinator or next owner can move it to `ready`.

## Agent Update Rules

- Update your workstream file first.
- Update only your row in `STATUS.md`.
- Do not rewrite the entire `STATUS.md` table.
- Do not edit another agent’s workstream except for coordinator-approved handoff or mechanical conflict resolution.
- Add an Activity Log entry for every status transition.

## Dependency And Conflict Rules

- Use `depends_on` for ordered work.
- Shared contracts should usually be their own workstream, such as `01-contract.md`.
- If two agents need the same files, split the workstream or appoint an integrator.
- Contract changes must update `TECH.md` before dependent workstreams rely on them.

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

The overall spec can be `done` only when required workstreams are `merged`, validation is complete, specs match reality, and follow-ups are tracked or explicitly deferred.
"""


def tdd_workflow(tdd: str) -> str:
    expectation = (
        "TDD evidence is expected for behavior changes."
        if tdd == "strict"
        else "TDD is recommended for behavior changes."
    )
    return f"""---
language: en-US
audience: agent
doc_type: normative
---

# TDD Workflow

{expectation}

## Loop

TDD is the inner loop inside the broader `Plan -> Develop -> Verify -> Fix` engineering cycle in `development-workflow.md`.

```text
Product behavior -> test plan -> red -> green -> refactor -> broaden -> validate -> record
```

## Steps

1. Write or update behavior invariants in `PRODUCT.md`.
2. Map important invariants to tests in `TECH.md`.
3. Add the smallest failing test that proves the behavior is not implemented.
4. Run the narrow test command and record the red result.
5. Implement the smallest change that makes the test pass.
6. Run the same narrow command and record the green result.
7. Refactor only while tests are green.
8. Broaden validation to relevant unit, integration, e2e, or manual checks.
9. Record commands run, checks skipped, and residual risk in the PR or implementation log.

## PR Evidence

```markdown
## TDD Evidence

- Red:
- Green:
- Broader validation:
- Tests not run:
```
"""


VALIDATION = """---
language: en-US
audience: agent
doc_type: normative
---

# Validation Workflow

## Rule

Do not skip validation silently.

For UI-visible changes, visual evidence is required unless explicitly marked not applicable.

## Validation Ladder

1. Static checks or formatting.
2. Narrow unit tests.
3. Relevant integration tests.
4. End-to-end or manual checks for user-facing flows.
5. Screenshots, recordings, logs, or traces when they are the clearest proof.

## UI / Visual Evidence

Use this gate when a change affects rendering, layout, spacing, sizing, typography, color, imagery, responsive behavior, user-visible copy, interaction flows, visual states, canvas, Three.js, charts, maps, or animation.

Default evidence:

- At least one screenshot or short recording of the changed flow.
- Relevant states chosen by risk: normal, loading, empty, error, disabled, hover, focus, selected, expanded, collapsed, or success.
- Desktop viewport for most changes.
- Mobile viewport when layout, responsive behavior, touch interaction, or narrow-screen content may be affected.

If visual evidence is not applicable, record why and provide substitute evidence.

Store screenshots, recordings, traces, and other validation artifacts according to `docs/governance/temp-artifacts.md`.

## Reporting

Record:

- Commands run.
- Manual checks performed.
- Visual evidence or why it is not applicable.
- Tests not run and why.
- Residual risk.
"""


REVIEW = """---
language: en-US
audience: agent
doc_type: normative
---

# Review Workflow

## Before Review

- Link the relevant spec when one exists.
- Summarize behavior changes and implementation shape.
- Check `docs/governance/change-gate.md` when adding or expanding project surface.
- Check `docs/governance/code-quality.md` for structural code-quality issues.
- Check `docs/governance/documentation-standards.md` when docs, examples, generated docs, specs, contributor guidance, or agent instructions changed.
- Check `docs/governance/temp-artifacts.md` when temporary outputs were produced.
- Check `docs/governance/spec-first-delivery.md` when implementation was delegated to subagents or worker sessions.
- Include validation evidence.
- Call out risks, migrations, and follow-ups.

## PR Template Expectations

Use `.github/pull_request_template.md` when present.

If the template is missing, include at least: summary, spec link, validation, and risk.
"""


MAINTENANCE = """---
language: en-US
audience: agent
doc_type: normative
---

# Governance Maintenance

## Mandatory AGENTS.md Updates

Update `AGENTS.md` in the same change when you:

- Add a governance document.
- Delete a governance document.
- Rename or move a governance document.
- Change which workflow applies to a task type.
- Add or remove an agent adapter file.
- Add a new mandatory workflow.

## Usually No AGENTS.md Update Needed

- Typo fixes.
- Examples inside an existing governance document.
- Wording changes that do not alter routing, scope, or mandatory workflow.

## Code & Order Provenance

`docs/governance/code-and-order.lock.json` records:

- Code & Order source repo, branch, and commit.
- Initializer config such as suite, TDD mode, and starter spec id.
- Managed governance files with template hashes and local hashes at write time.

Use the initializer to manage the lockfile:

```bash
python scripts/init_governance.py . --audit
python scripts/init_governance.py . --adopt
python scripts/init_governance.py . --update --dry-run
python scripts/init_governance.py . --update
```

## Drift Status

- `current`: local file matches the managed template.
- `upstream-available`: local file is unchanged locally and a newer template is available.
- `local-customized`: local file differs from the managed template, while the template has not changed.
- `needs-merge`: local file was customized and the template also changed.
- `missing`: managed file is absent locally.
- `new-template`: current Code & Order has a managed file not present in the lockfile.

Safe updates may automatically refresh `upstream-available` files and create missing `new-template` files. They must not overwrite `local-customized` or `needs-merge` files.
"""


SPECS_README = """---
language: en-US
audience: agent
doc_type: router
---

# Specs

Use `docs/governance/spec-first-delivery.md` for the fixed coordinator -> worker -> acceptance flow, `docs/governance/compact-specs.md` for bug fix and small tweak specs, `docs/governance/spec-production.md` for creating specs, `docs/governance/spec-workflow.md` for the spec lifecycle, `docs/governance/spec-id-policy.md` for id format, `docs/governance/spec-execution-status.md` for execution status, and `docs/governance/multi-agent-spec-flow.md` for parallel implementation.

Each substantial spec should live under:

```text
specs/<source>-<id>-<short-slug>/
  PRODUCT.md
  TECH.md
  STATUS.md
  workstreams/
    01-implementation.md
```
"""


PRODUCT = """---
language: en-US
audience: mixed
doc_type: spec
---

# <Feature> Product Spec

## Summary

## Goals / Non-goals

## Behavior

1. 

## Open Questions
"""


TECH = """---
language: en-US
audience: agent
doc_type: spec
---

# <Feature> Tech Spec

Product spec: `./PRODUCT.md`

## Context

## Proposed Changes

## Testing and Validation

## Risks and Follow-ups
"""


STATUS = """---
spec_id: <spec-id>
language: en-US
audience: agent
doc_type: spec
status: ready
implementation: not_started
validation: not_started
coordinator:
updated: YYYY-MM-DD
---

# Status

## Summary

Implementation has not started.

## Workstreams

| ID | Scope | Status | Owner | Branch / PR | Depends on | Updated |
|---|---|---|---|---|---|---|
| 01 | Implementation | ready | unassigned | | | |

## Activity Log

- YYYY-MM-DD: status initialized.

## Main Session Acceptance

- Accepted by:
- Diff reviewed:
- Validation run:
- Residual risk:
"""


WORKSTREAM = """---
id: 01-implementation
language: en-US
audience: agent
doc_type: spec
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
"""


def pr_template(tdd: str) -> str:
    tdd_section = (
        """
## TDD Evidence

- Red:
- Green:
- Broader validation:
- Tests not run:
"""
        if tdd != "off"
        else ""
    )
    return f"""<!--
language: en-US
audience: mixed
doc_type: template
-->

## Summary


## Spec

- Spec:
- Compact spec or direct exception:
- Spec-first workflow used:
- Implementing subagent/workstream:
- Main-session acceptance:

## Code Quality

- Dead code removed / N/A:
- Interface, state, dependency, config, or compatibility-layer exceptions:

## Change Gate

- Required:
- Gate answered:
- Compatibility exception:

## Documentation

- Docs updated / N/A:
- Language/audience/doc type declared:
- Source of truth:
- Routers or indexes updated:
- Examples, commands, links, or generated docs checked:
- Stale docs removed or superseded:

## Temp Artifacts

- Created / N/A:
- Referenced as evidence:
- Promoted:
- Cleaned or intentionally retained:

## Validation

- Commands run:
- Manual checks:
- Visual evidence / N/A:
- Not run:
{tdd_section}
## Risk

- 
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def git_output(args: list[str], cwd: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    output = completed.stdout.strip()
    return output or None


def current_source_commit() -> str:
    return git_output(["rev-parse", "HEAD"], skill_root()) or "unknown"


def current_source_dirty() -> bool:
    return git_output(["status", "--porcelain"], skill_root()) is not None


def current_source_repo() -> str:
    return (
        git_output(["config", "--get", "remote.origin.url"], skill_root())
        or SOURCE_REPO_FALLBACK
    )


def latest_source_commit(source_repo: str) -> str | None:
    output = git_output(["ls-remote", source_repo, f"refs/heads/{SOURCE_REF}"], skill_root())
    if not output:
        return None
    return output.split()[0]


def hash_text(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


def hash_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def template_id_for(relative_path: str) -> str:
    return relative_path.replace("/", ":")


def lock_path(root: Path) -> Path:
    return root / LOCK_RELATIVE_PATH


def load_lock(root: Path) -> dict[str, Any] | None:
    path = lock_path(root)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_lock(root: Path, lock: dict[str, Any]) -> None:
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def planned_entries(root: Path, suite: str, tdd: str, spec_id: str) -> list[dict[str, Any]]:
    entries = []
    for path, content in planned_files(root, suite, tdd, spec_id):
        relative_path = path.relative_to(root).as_posix()
        entries.append(
            {
                "path": relative_path,
                "template_id": template_id_for(relative_path),
                "content": content,
                "base_hash": hash_text(content),
            }
        )
    return entries


def lock_config(args: argparse.Namespace, existing: dict[str, Any] | None = None) -> dict[str, str]:
    config = (existing or {}).get("config", {})
    return {
        "suite": config.get("suite", args.suite),
        "tdd": config.get("tdd", args.tdd),
        "spec_id": config.get("spec_id", args.spec_id),
    }


def managed_entry(
    root: Path,
    entry: dict[str, Any],
    source_commit: str,
    action: str,
    base_hash: str | None = None,
    base_source_commit: str | None = None,
) -> dict[str, Any]:
    path = root / entry["path"]
    return {
        "path": entry["path"],
        "template_id": entry["template_id"],
        "base_source_commit": base_source_commit or source_commit,
        "base_hash": base_hash or entry["base_hash"],
        "local_hash_at_write": hash_file(path),
        "last_action": action,
    }


def build_lock(
    root: Path,
    args: argparse.Namespace,
    actions: dict[str, str],
    adopted: bool = False,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = lock_config(args, existing)
    source_commit = current_source_commit()
    now = utc_now()
    entries = [
        managed_entry(root, entry, source_commit, actions.get(entry["path"], "tracked"))
        for entry in planned_entries(root, config["suite"], config["tdd"], config["spec_id"])
    ]
    return {
        "schema_version": LOCK_SCHEMA_VERSION,
        "tool": "code-and-order",
        "source_repo": current_source_repo(),
        "source_ref": SOURCE_REF,
        "source_commit": source_commit,
        "source_dirty": current_source_dirty(),
        "initialized_at": (existing or {}).get("initialized_at", now),
        "last_updated_at": now,
        "adopted": adopted or (existing or {}).get("adopted", False),
        "config": config,
        "managed_files": entries,
    }


def analyze_lock(
    root: Path,
    lock: dict[str, Any],
    config: dict[str, str],
) -> list[dict[str, Any]]:
    old_entries = {entry["path"]: entry for entry in lock.get("managed_files", [])}
    results = []
    for entry in planned_entries(root, config["suite"], config["tdd"], config["spec_id"]):
        old = old_entries.get(entry["path"])
        path = root / entry["path"]
        local_hash = hash_file(path)
        latest_hash = entry["base_hash"]
        if old is None:
            if local_hash is None:
                status = "new-template"
            elif local_hash == latest_hash:
                status = "lock-outdated"
            else:
                status = "needs-adopt"
        else:
            old_hash = old.get("base_hash")
            if local_hash is None:
                status = "missing"
            elif old_hash == latest_hash:
                status = "current" if local_hash == latest_hash else "local-customized"
            elif local_hash == old_hash:
                status = "upstream-available"
            elif local_hash == latest_hash:
                status = "lock-outdated"
            else:
                status = "needs-merge"
        results.append(
            {
                "path": entry["path"],
                "template_id": entry["template_id"],
                "content": entry["content"],
                "latest_hash": latest_hash,
                "local_hash": local_hash,
                "old_entry": old,
                "status": status,
            }
        )
    return results


def print_audit(root: Path, lock: dict[str, Any], config: dict[str, str]) -> None:
    source_repo = lock.get("source_repo") or current_source_repo()
    latest_commit = latest_source_commit(source_repo)
    running_commit = current_source_commit()
    print("Code & Order audit")
    print(f"- Lockfile: {LOCK_RELATIVE_PATH.as_posix()}")
    print(f"- Locked source: {lock.get('source_commit', 'unknown')}")
    if lock.get("source_dirty"):
        print("- Locked source dirty: true")
    print(f"- Running source: {running_commit}")
    if current_source_dirty():
        print("- Running source dirty: true")
    print(f"- Latest {SOURCE_REF}: {latest_commit or 'unknown'}")
    if latest_commit and lock.get("source_commit") != latest_commit:
        print("- Upstream: latest main differs from the lockfile source")
    elif latest_commit:
        print("- Upstream: lockfile source matches latest main")
    else:
        print("- Upstream: latest main could not be checked")

    results = analyze_lock(root, lock, config)
    counts: dict[str, int] = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1

    print("\nStatus summary:")
    for status in sorted(counts):
        print(f"- {status}: {counts[status]}")

    print("\nManaged files:")
    for result in results:
        print(f"- [{result['status']}] {result['path']}")


def update_from_lock(
    root: Path,
    lock: dict[str, Any],
    config: dict[str, str],
    dry_run: bool,
) -> tuple[dict[str, Any], dict[str, int]]:
    source_commit = current_source_commit()
    old_entries = {entry["path"]: entry for entry in lock.get("managed_files", [])}
    results = analyze_lock(root, lock, config)
    counts: dict[str, int] = {}
    new_entries = []

    for result in results:
        status = result["status"]
        counts[status] = counts.get(status, 0) + 1
        path = root / result["path"]
        should_write = status in {"upstream-available", "new-template"}

        if should_write and not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(result["content"], encoding="utf-8")
            status = "updated" if result["old_entry"] else "created"

        if status in {"updated", "created", "current", "lock-outdated"}:
            new_entries.append(
                managed_entry(
                    root,
                    {
                        "path": result["path"],
                        "template_id": result["template_id"],
                        "base_hash": result["latest_hash"],
                    },
                    source_commit,
                    status,
                )
            )
        else:
            old = old_entries.get(result["path"])
            if old:
                new_entries.append(
                    managed_entry(
                        root,
                        {
                            "path": result["path"],
                            "template_id": result["template_id"],
                            "base_hash": result["latest_hash"],
                        },
                        source_commit,
                        status,
                        base_hash=old.get("base_hash"),
                        base_source_commit=old.get("base_source_commit"),
                    )
                )
            else:
                new_entries.append(
                    managed_entry(
                        root,
                        {
                            "path": result["path"],
                            "template_id": result["template_id"],
                            "base_hash": result["latest_hash"],
                        },
                        source_commit,
                        status,
                    )
                )

    new_lock = {
        "schema_version": LOCK_SCHEMA_VERSION,
        "tool": "code-and-order",
        "source_repo": lock.get("source_repo") or current_source_repo(),
        "source_ref": lock.get("source_ref") or SOURCE_REF,
        "source_commit": source_commit,
        "source_dirty": current_source_dirty(),
        "initialized_at": lock.get("initialized_at", utc_now()),
        "last_updated_at": utc_now(),
        "adopted": lock.get("adopted", False),
        "config": config,
        "managed_files": new_entries,
    }
    return new_lock, counts


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def planned_files(root: Path, suite: str, tdd: str, spec_id: str) -> list[tuple[Path, str]]:
    files = [
        (root / ".gitignore", GITIGNORE),
        (root / "AGENTS.md", agents_md(tdd)),
        (root / "docs" / "governance" / "README.md", GOV_README),
        (root / "docs" / "governance" / "agent-context.md", AGENT_CONTEXT),
        (root / "docs" / "governance" / "development-workflow.md", DEVELOPMENT),
        (root / "docs" / "governance" / "change-gate.md", CHANGE_GATE),
        (root / "docs" / "governance" / "code-quality.md", CODE_QUALITY),
        (root / "docs" / "governance" / "documentation-standards.md", DOCUMENTATION_STANDARDS),
        (root / "docs" / "governance" / "temp-artifacts.md", TEMP_ARTIFACTS),
        (root / "docs" / "governance" / "compact-specs.md", COMPACT_SPECS),
        (root / "docs" / "governance" / "spec-first-delivery.md", SPEC_FIRST_DELIVERY),
        (root / "docs" / "governance" / "spec-production.md", SPEC_PRODUCTION),
        (root / "docs" / "governance" / "spec-workflow.md", SPEC_WORKFLOW),
        (root / "docs" / "governance" / "spec-id-policy.md", SPEC_ID_POLICY),
        (root / "docs" / "governance" / "spec-execution-status.md", SPEC_EXECUTION_STATUS),
        (root / "docs" / "governance" / "multi-agent-spec-flow.md", MULTI_AGENT_SPEC_FLOW),
        (root / "docs" / "governance" / "validation-workflow.md", VALIDATION),
        (root / "docs" / "governance" / "review-workflow.md", REVIEW),
        (root / "docs" / "governance" / "governance-maintenance.md", MAINTENANCE),
        (root / "specs" / "README.md", SPECS_README),
        (root / "specs" / spec_id / "PRODUCT.md", PRODUCT),
        (root / "specs" / spec_id / "TECH.md", TECH),
        (root / "specs" / spec_id / "STATUS.md", STATUS.replace("<spec-id>", spec_id)),
        (
            root / "specs" / spec_id / "workstreams" / "01-implementation.md",
            WORKSTREAM,
        ),
    ]

    if tdd != "off":
        files.append((root / "docs" / "governance" / "tdd-workflow.md", tdd_workflow(tdd)))

    if suite == "universal":
        files.extend(
            [
                (root / "CLAUDE.md", CLAUDE),
                (root / "GEMINI.md", GEMINI),
                (root / ".github" / "copilot-instructions.md", COPILOT),
                (root / ".github" / "pull_request_template.md", pr_template(tdd)),
            ]
        )

    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Report Code & Order lockfile drift without writing files",
    )
    parser.add_argument(
        "--adopt",
        action="store_true",
        help="Write a lockfile for existing governance files without changing them",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Safely update unchanged managed governance files to this Code & Order version",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview --update without writing managed files or the lockfile",
    )
    parser.add_argument(
        "--suite",
        choices=["minimal", "universal"],
        default="universal",
        help="Governance starter suite",
    )
    parser.add_argument(
        "--tdd",
        choices=["off", "standard", "strict"],
        default="strict",
        help="TDD workflow strictness",
    )
    parser.add_argument(
        "--spec-id",
        default="rfc-0001-initial-governance",
        help="Starter spec directory id",
    )
    args = parser.parse_args()

    selected_modes = sum([args.audit, args.adopt, args.update])
    if selected_modes > 1:
        parser.error("choose only one of --audit, --adopt, or --update")
    if args.dry_run and not args.update:
        parser.error("--dry-run only applies to --update")

    if not SPEC_ID_RE.match(args.spec_id):
        parser.error(
            "--spec-id must match examples like gh-123-feature, "
            "linear-app-123-feature, jira-core-42-feature, "
            "rfc-0001-feature, or adhoc-20260430-feature"
        )

    root = Path(args.repo).resolve()

    existing_lock = load_lock(root)
    config = lock_config(args, existing_lock)

    if args.audit:
        if not existing_lock:
            print(
                "No Code & Order lockfile found. "
                "Run with --adopt to start tracking existing governance files."
            )
            return 0
        print_audit(root, existing_lock, config)
        return 0

    if args.adopt:
        actions = {}
        for entry in planned_entries(root, config["suite"], config["tdd"], config["spec_id"]):
            actions[entry["path"]] = "adopted" if (root / entry["path"]).exists() else "missing"
        write_lock(root, build_lock(root, args, actions, adopted=True, existing=existing_lock))
        print(f"Adopted governance tracking in {LOCK_RELATIVE_PATH.as_posix()}")
        print_audit(root, load_lock(root) or {}, config)
        return 0

    if args.update:
        if not existing_lock:
            print(
                "No Code & Order lockfile found. "
                "Run with --adopt before using --update."
            )
            return 1
        new_lock, counts = update_from_lock(root, existing_lock, config, args.dry_run)
        if not args.dry_run:
            write_lock(root, new_lock)
        print("Update summary:" if not args.dry_run else "Update dry run summary:")
        for status in sorted(counts):
            print(f"- {status}: {counts[status]}")
        if args.dry_run:
            print("No files written.")
        else:
            print(f"Updated {LOCK_RELATIVE_PATH.as_posix()}")
        return 0

    created = []
    skipped = []
    actions = {}

    for path, content in planned_files(root, args.suite, args.tdd, args.spec_id):
        relative_path = path.relative_to(root).as_posix()
        if write_if_missing(path, content):
            created.append(path)
            actions[relative_path] = "created"
        else:
            skipped.append(path)
            actions[relative_path] = "skipped"

    if not existing_lock:
        write_lock(root, build_lock(root, args, actions))
        created.append(lock_path(root))
    else:
        print(
            f"Existing {LOCK_RELATIVE_PATH.as_posix()} left unchanged. "
            "Use --audit or --update for managed governance maintenance."
        )

    if created:
        print("Created:")
        for path in created:
            print(f"- {path.relative_to(root)}")
    else:
        print("No files created; starter files already exist.")

    if skipped:
        print("Skipped existing files:")
        for path in skipped:
            print(f"- {path.relative_to(root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
