#!/usr/bin/env python3
"""Create a human-agent governance starter set for a repository."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SPEC_ID_RE = re.compile(
    r"^(?:gh-\d+|linear-[a-z0-9]+-\d+|jira-[a-z0-9]+-\d+|rfc-\d{4}|adhoc-\d{8})"
    r"-[a-z0-9]+(?:-[a-z0-9]+)*$"
)


def agents_md(tdd: str) -> str:
    tdd_row = (
        "| TDD work | `docs/governance/tdd-workflow.md` |\n"
        if tdd != "off"
        else ""
    )
    return f"""# AGENTS.md

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
| Ambiguous feature or cross-module change | `docs/governance/spec-workflow.md` |
| Choosing or reviewing a spec id | `docs/governance/spec-id-policy.md` |
{tdd_row}| Validation or test reporting | `docs/governance/validation-workflow.md` |
| PR or review prep | `docs/governance/review-workflow.md` |
| Agent context files | `docs/governance/agent-context.md` |
| Governance file changes | `docs/governance/governance-maintenance.md` |

## Non-Negotiables

- Do not duplicate detailed governance rules in this file or in agent adapter files.
- Thin adapter files such as `CLAUDE.md`, `GEMINI.md`, and `.github/copilot-instructions.md` must point here instead of copying rules.
- When adding, deleting, renaming, or moving governance documents, update this file in the same change.
- When changing which workflow applies to a task type, update the Governance Map in this file in the same change.
- Do not skip tests or validation silently. Record what ran and what did not.
- Do not revert user changes unless explicitly asked.
"""


CLAUDE = """# CLAUDE.md

@AGENTS.md
"""


GEMINI = """# GEMINI.md

@AGENTS.md
"""


COPILOT = """# GitHub Copilot Instructions

Follow `AGENTS.md` as the canonical repository guidance. Do not duplicate governance rules here.
"""


GOV_README = """# Governance

This directory holds the detailed engineering governance workflows.

`AGENTS.md` is the canonical router. If files here are added, removed, renamed, or moved, update `AGENTS.md` in the same change.
"""


AGENT_CONTEXT = """# Agent Context

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


DEVELOPMENT = """# Development Workflow

## Outer Loop

Use this loop for all non-trivial engineering work:

```text
Plan -> Develop -> Verify -> Fix
```

1. Plan: read the relevant governance docs, decide whether a spec is needed, identify risk, and choose the smallest coherent task shape.
2. Develop: make the change. When TDD applies, use `docs/governance/tdd-workflow.md` inside this phase.
3. Verify: run narrow validation first, broaden when behavior or shared contracts changed, and record evidence. When TDD applies, the broaden/validate/record steps come from `docs/governance/tdd-workflow.md`.
4. Fix: respond to failing tests, review feedback, or validation gaps. If reality changed, update specs or governance docs before repeating Develop/Verify.

TDD is not a competing workflow. It is the inner loop used inside Develop and Verify when behavior changes call for it.

## Default Steps

1. Read `AGENTS.md`.
2. Read the workflow file that matches the task.
3. Inspect the existing code and tests before editing.
4. Make the smallest coherent change.
5. Run the narrowest meaningful validation first.
6. Broaden validation when behavior, contracts, or shared modules changed.
7. Record tests run, tests skipped, and residual risk.

## Direct Implementation

Use direct implementation for narrow bug fixes, mechanical refactors, dependency bumps, documentation-only changes, or obvious single-file changes.

## Spec-Driven Implementation

Use `docs/governance/spec-workflow.md` when behavior is ambiguous, user-visible, cross-module, or high risk.
"""


SPEC_WORKFLOW = """# Spec Workflow

## When To Write A Spec

Write a spec before implementation when at least one is true:

- Behavior is ambiguous or user-visible.
- The change spans multiple modules or ownership boundaries.
- The change affects persistence, permissions, security, billing, migration, or public APIs.
- A coding agent needs stable product intent before implementation.
- Reviewers need to approve direction before code churn begins.

Skip specs for narrow bug fixes, mechanical refactors, dependency bumps, or obvious single-file changes.

## Required Files

```text
specs/<spec-id>/
  PRODUCT.md
  TECH.md
```

`PRODUCT.md` describes user/API-visible behavior as testable invariants.

`TECH.md` describes current code context, proposed changes, validation, risks, and follow-ups.

## Keep Specs Current

If implementation changes user-visible behavior, update `PRODUCT.md`.

If implementation changes module boundaries, sequencing, validation, or risks, update `TECH.md`.
"""


SPEC_ID_POLICY = """# Spec ID Policy

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


def tdd_workflow(tdd: str) -> str:
    expectation = (
        "TDD evidence is expected for behavior changes."
        if tdd == "strict"
        else "TDD is recommended for behavior changes."
    )
    return f"""# TDD Workflow

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


VALIDATION = """# Validation Workflow

## Rule

Do not skip validation silently.

## Validation Ladder

1. Static checks or formatting.
2. Narrow unit tests.
3. Relevant integration tests.
4. End-to-end or manual checks for user-facing flows.
5. Screenshots, recordings, logs, or traces when they are the clearest proof.

## Reporting

Record:

- Commands run.
- Manual checks performed.
- Tests not run and why.
- Residual risk.
"""


REVIEW = """# Review Workflow

## Before Review

- Link the relevant spec when one exists.
- Summarize behavior changes and implementation shape.
- Include validation evidence.
- Call out risks, migrations, and follow-ups.

## PR Template Expectations

Use `.github/pull_request_template.md` when present.

If the template is missing, include at least: summary, spec link, validation, and risk.
"""


MAINTENANCE = """# Governance Maintenance

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
"""


SPECS_README = """# Specs

Use `docs/governance/spec-workflow.md` for the spec lifecycle and `docs/governance/spec-id-policy.md` for id format.

Each substantial spec should live under:

```text
specs/<source>-<id>-<short-slug>/
  PRODUCT.md
  TECH.md
```
"""


PRODUCT = """# <Feature> Product Spec

## Summary

## Goals / Non-goals

## Behavior

1. 

## Open Questions
"""


TECH = """# <Feature> Tech Spec

Product spec: `./PRODUCT.md`

## Context

## Proposed Changes

## Testing and Validation

## Risks and Follow-ups
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
    return f"""## Summary


## Spec

- Spec:

## Validation

- Commands run:
- Manual checks:
- Not run:
{tdd_section}
## Risk

- 
"""


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def planned_files(root: Path, suite: str, tdd: str, spec_id: str) -> list[tuple[Path, str]]:
    files = [
        (root / "AGENTS.md", agents_md(tdd)),
        (root / "docs" / "governance" / "README.md", GOV_README),
        (root / "docs" / "governance" / "agent-context.md", AGENT_CONTEXT),
        (root / "docs" / "governance" / "development-workflow.md", DEVELOPMENT),
        (root / "docs" / "governance" / "spec-workflow.md", SPEC_WORKFLOW),
        (root / "docs" / "governance" / "spec-id-policy.md", SPEC_ID_POLICY),
        (root / "docs" / "governance" / "validation-workflow.md", VALIDATION),
        (root / "docs" / "governance" / "review-workflow.md", REVIEW),
        (root / "docs" / "governance" / "governance-maintenance.md", MAINTENANCE),
        (root / "specs" / "README.md", SPECS_README),
        (root / "specs" / spec_id / "PRODUCT.md", PRODUCT),
        (root / "specs" / spec_id / "TECH.md", TECH),
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

    if not SPEC_ID_RE.match(args.spec_id):
        parser.error(
            "--spec-id must match examples like gh-123-feature, "
            "linear-app-123-feature, jira-core-42-feature, "
            "rfc-0001-feature, or adhoc-20260430-feature"
        )

    root = Path(args.repo).resolve()
    created = []
    skipped = []

    for path, content in planned_files(root, args.suite, args.tdd, args.spec_id):
        if write_if_missing(path, content):
            created.append(path)
        else:
            skipped.append(path)

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
