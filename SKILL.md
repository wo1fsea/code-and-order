---
name: code-and-order
description: Initialize, audit, and organize engineering governance rules for human-agent software projects. Use when a user wants to set up or clean up repo-local guidance such as AGENTS.md, spec workflows, project standards, review rules, validation checklists, issue readiness labels, agent collaboration rules, or reusable engineering-governance templates.
---

# Code & Order

Use this skill to help a repository become easier for humans and coding agents to understand, change, review, and maintain.

The goal is lightweight governance: enough rules to reduce ambiguity, preserve decisions, and make validation repeatable, without turning the repo into a process shrine.

## Workflow

1. Inspect the existing repository before proposing rules.
   - Look for `AGENTS.md`, `CLAUDE.md`, `WARP.md`, `.cursor/rules`, `.github/`, `docs/`, `specs/`, `CONTRIBUTING.md`, test commands, build commands, and project-specific scripts.
   - Read existing instructions first and preserve their intent.
2. Classify the current governance state.
   - Missing: no clear agent or contributor instructions.
   - Fragmented: useful rules exist but are duplicated or scattered.
   - Heavy: rules exist but create unnecessary ceremony.
   - Healthy: rules are concise, current, and connected to validation.
3. Choose the smallest useful intervention.
   - Create or update `AGENTS.md` when agents need repo-local instructions.
   - Add a `specs/` workflow only for ambiguous or cross-module work.
   - Add templates or checklists only when they remove repeated judgment calls.
   - Move raw research and long examples into references rather than bloating the main rule file.
4. Separate product intent from implementation planning.
   - `PRODUCT.md`: user/API-visible behavior, testable invariants, goals, non-goals, open questions.
   - `TECH.md`: current code context, proposed changes, validation plan, risks, follow-ups.
5. Tie every rule to a decision point.
   - A good rule tells the next human or agent what to do differently.
   - Delete or compress rules that only restate common sense.
6. Validate the result.
   - Confirm links and paths work.
   - Confirm setup/test commands are discoverable.
   - Confirm the workflow says when to skip ceremony.
   - Summarize what changed and what remains intentionally undecided.

## Suggested File Set

Use this as a menu, not a mandate.

```text
AGENTS.md
CONTRIBUTING.md
specs/
  <issue-or-feature-id>/
    PRODUCT.md
    TECH.md
docs/
  governance/
    review-checklist.md
    validation-checklist.md
.github/
  ISSUE_TEMPLATE/
  pull_request_template.md
```

For small repos, start with only `AGENTS.md`.

## When To Add Specs

Add a spec before implementation when at least one is true:

- The behavior is ambiguous or user-visible.
- The change spans multiple modules or ownership boundaries.
- The change affects persistence, permissions, security, billing, migration, or public APIs.
- The implementation will likely be done by an agent that needs stable intent.
- Reviewers need to approve direction before code churn begins.

Skip specs for narrow bug fixes, mechanical refactors, dependency bumps, or obvious single-file changes.

## References

- Read `references/repo-governance.md` when designing or auditing a repo governance layout.
- Read `references/spec-templates.md` when creating `PRODUCT.md` / `TECH.md` templates.
- Use `scripts/init_governance.py` when a repo needs a deterministic starter structure.

