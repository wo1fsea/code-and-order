---
name: code-and-order
description: Initialize, audit, and organize engineering governance rules for human-agent software projects. Use when a user wants to set up or clean up repo-local guidance such as AGENTS.md, spec workflows, project standards, review rules, validation checklists, issue readiness labels, agent collaboration rules, or reusable engineering-governance templates.
---

# Code & Order

Use this skill to help a repository become easier for humans and coding agents to understand, change, review, and maintain.

The goal is lightweight governance: enough rules to reduce ambiguity, preserve decisions, and make validation repeatable, without turning the repo into a process shrine.

## Default Design

Use this governance shape unless the repo already has a stronger local convention:

```text
AGENTS.md                         # canonical router, not a long handbook
CLAUDE.md                         # thin adapter pointing to AGENTS.md
GEMINI.md                         # thin adapter pointing to AGENTS.md
.github/copilot-instructions.md   # thin Copilot adapter pointing to AGENTS.md
docs/governance/
  README.md
  agent-context.md
  development-workflow.md
  spec-workflow.md
  spec-id-policy.md
  spec-execution-status.md
  tdd-workflow.md
  validation-workflow.md
  review-workflow.md
  governance-maintenance.md
specs/
  README.md
  <spec-id>/
    PRODUCT.md
    TECH.md
    STATUS.md
    workstreams/
      01-implementation.md
```

`AGENTS.md` is the canonical entry point, but it should stay short. It routes task types to the detailed governance files. Do not duplicate the detailed workflow text into `AGENTS.md` or the adapter files.

## Workflow

1. Inspect the existing repository before proposing rules.
   - Look for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `WARP.md`, `.cursor/rules`, `.github/copilot-instructions.md`, `.github/instructions/`, `.github/`, `docs/`, `specs/`, `CONTRIBUTING.md`, test commands, build commands, and project-specific scripts.
   - Read existing instructions first and preserve their intent.
2. Classify the current governance state.
   - Missing: no clear agent or contributor instructions.
   - Fragmented: useful rules exist but are duplicated or scattered.
   - Heavy: rules exist but create unnecessary ceremony.
   - Healthy: rules are concise, current, and connected to validation.
3. Choose the smallest useful intervention.
   - Create or update `AGENTS.md` as a router when agents need repo-local instructions.
   - Put detailed rules in `docs/governance/`.
   - Create thin adapter files only when a tool expects them.
   - Add a `specs/` workflow only for ambiguous or cross-module work.
   - Add templates or checklists only when they remove repeated judgment calls.
4. Separate product intent from implementation planning.
   - `PRODUCT.md`: user/API-visible behavior, testable invariants, goals, non-goals, open questions.
   - `TECH.md`: current code context, proposed changes, validation plan, risks, follow-ups.
5. Use concrete spec ids.
   - Preferred shape: `specs/<source>-<id>-<short-slug>/`.
   - Examples: `gh-123-open-file-tilde`, `linear-app-1066-agent-autonomy`, `rfc-0001-repo-governance`, `adhoc-20260430-tdd-bootstrap`.
   - Read `references/spec-id-policy.md` before inventing a new policy.
6. Manage execution status explicitly.
   - Do not encode status in directory names.
   - Use `STATUS.md` for the overall spec board and `workstreams/*.md` for parallel execution.
   - Agents claim and update their own workstream files, then synchronize only their row in `STATUS.md`.
   - Read `references/spec-execution-status.md` when a spec has not started, is partially complete, is blocked, or has multiple agents working in parallel.
7. Treat TDD as a workflow, not a slogan.
   - The outer engineering loop is Plan -> Develop -> Verify -> Fix.
   - TDD is the inner loop inside Develop/Verify: product behavior -> test plan -> red -> green -> refactor -> broaden -> validate -> record.
   - Do not present TDD as a competing workflow.
   - Read `references/tdd-workflow.md` when defining or auditing TDD rules.
8. Tie every rule to a decision point.
   - A good rule tells the next human or agent what to do differently.
   - Delete or compress rules that only restate common sense.
9. Maintain the router.
   - When adding, deleting, renaming, or moving governance files, update `AGENTS.md` in the same change.
   - When changing which workflow applies to a task type, update the `AGENTS.md` governance map in the same change.
10. Validate the result.
   - Confirm links and paths work.
   - Confirm setup/test commands are discoverable.
   - Confirm the workflow says when to skip ceremony.
   - Summarize what changed and what remains intentionally undecided.

## Initialization Modes

Use `scripts/init_governance.py` for deterministic starter files:

```bash
python scripts/init_governance.py . \
  --suite universal \
  --tdd strict \
  --spec-id rfc-0001-initial-governance
```

Modes:

- `--suite minimal`: `AGENTS.md`, core governance docs, and starter specs.
- `--suite universal`: minimal plus `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, and pull request template.
- `--tdd off`: no TDD-specific workflow.
- `--tdd standard`: TDD guidance is recommended.
- `--tdd strict`: TDD evidence is expected for behavior changes.

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
- Read `references/spec-id-policy.md` when defining or reviewing spec id format.
- Read `references/spec-execution-status.md` when managing spec lifecycle, partial implementation, or multi-agent workstreams.
- Read `references/tdd-workflow.md` when adding TDD expectations.
- Read `references/universal-agent-init.md` when initializing Codex, Copilot, Claude, and Gemini context files together.
- Use `scripts/init_governance.py` when a repo needs a deterministic starter structure.
