# Repo Governance Notes

## Governance Layers

Prefer a small number of clear layers:

1. `AGENTS.md` as the canonical router for all coding agents.
2. Thin adapters (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`) that import or point to `AGENTS.md`.
3. `docs/governance/` for detailed workflows and checklists.
4. `specs/` for substantial feature design and implementation plans.
5. `.github/` templates for issue and pull request intake.
6. `CONTRIBUTING.md` for public contributor flow and review expectations when the repo is open to contributors.

## Good Governance Properties

- Local: rules live near the repo they govern.
- Executable: rules tell an agent or human what to do next.
- Current: rules are updated in the same change as workflow changes.
- Minimal: rules avoid ceremony for simple changes.
- Verifiable: important behavior maps to tests or manual validation.
- Visual: UI-visible changes require screenshots or recordings unless explicitly not applicable.
- Routed: `AGENTS.md` points to the current workflow files without duplicating them.
- Coordinated: active specs use `STATUS.md` and `workstreams/*.md` instead of hidden chat state.
- Structural: code-quality rules require change gates before adding surface and reject dead code, non-orthogonal interfaces, hidden side effects, duplicate business rules, and permanent temporary layers.
- Contained: temporary artifacts stay in ignored temp locations unless intentionally promoted.
- Spec-producing: fuzzy requests become specs through clarification, product behavior, code inspection, technical planning, status initialization, and validation handoff.
- Parallel-aware: multi-agent work uses claim, lease, release, blocked, validation, merge, and integrator handoff rules.

## Common Smells

- The repo has several instruction files that contradict each other.
- `AGENTS.md` becomes a long handbook instead of a routing file.
- Claude, Gemini, or Copilot adapter files copy rules that belong in `docs/governance/`.
- A governance file was added, moved, or renamed without updating `AGENTS.md`.
- Specs describe implementation before product behavior is agreed.
- Spec execution status is tracked in chat, branch names, or moved directories instead of committed status files.
- Pull requests require checkboxes no one actually uses.
- Agent rules mention stale commands or old directory names.
- Validation is left as "run tests" without naming which tests matter.
- UI-visible changes merge with no screenshot, recording, or not-applicable note.
- Code-quality guidance says "keep code clean" but does not say when to delete, split, rename, or block a change.
- New APIs, commands, configs, dependencies, docs, adapters, or agent entrypoints appear without explaining why existing paths were insufficient.
- Screenshots, traces, logs, debug dumps, and scratch files appear in repo root or formal docs without promotion.
- Compatibility layers, feature flags, configs, and TODOs have no owner or deletion condition.
- Specs are created from implementation guesses before product behavior is clarified.
- Multiple agents edit the same spec or files without claim, lease, dependency, or handoff records.

## Useful Readiness States

- `needs-triage`: the issue exists but scope is not understood.
- `ready-to-spec`: the problem is understood but behavior or design is open.
- `ready-to-implement`: implementation can begin.
- `needs-mocks`: UI work is blocked on design artifacts.
- `blocked`: an external dependency or decision is missing.
