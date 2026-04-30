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
- Routed: `AGENTS.md` points to the current workflow files without duplicating them.
- Coordinated: active specs use `STATUS.md` and `workstreams/*.md` instead of hidden chat state.
- Structural: code-quality rules reject dead code, non-orthogonal interfaces, hidden side effects, duplicate business rules, and permanent temporary layers.

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
- Code-quality guidance says "keep code clean" but does not say when to delete, split, rename, or block a change.
- Compatibility layers, feature flags, configs, and TODOs have no owner or deletion condition.

## Useful Readiness States

- `needs-triage`: the issue exists but scope is not understood.
- `ready-to-spec`: the problem is understood but behavior or design is open.
- `ready-to-implement`: implementation can begin.
- `needs-mocks`: UI work is blocked on design artifacts.
- `blocked`: an external dependency or decision is missing.
