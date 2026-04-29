# Repo Governance Notes

## Governance Layers

Prefer a small number of clear layers:

1. `AGENTS.md` for agent-facing operating rules.
2. `CONTRIBUTING.md` for contributor flow and review expectations.
3. `specs/` for substantial feature design and implementation plans.
4. `.github/` templates for issue and pull request intake.
5. `docs/governance/` for longer checklists that should not crowd the main instructions.

## Good Governance Properties

- Local: rules live near the repo they govern.
- Executable: rules tell an agent or human what to do next.
- Current: rules are updated in the same change as workflow changes.
- Minimal: rules avoid ceremony for simple changes.
- Verifiable: important behavior maps to tests or manual validation.

## Common Smells

- The repo has several instruction files that contradict each other.
- Specs describe implementation before product behavior is agreed.
- Pull requests require checkboxes no one actually uses.
- Agent rules mention stale commands or old directory names.
- Validation is left as "run tests" without naming which tests matter.

## Useful Readiness States

- `needs-triage`: the issue exists but scope is not understood.
- `ready-to-spec`: the problem is understood but behavior or design is open.
- `ready-to-implement`: implementation can begin.
- `needs-mocks`: UI work is blocked on design artifacts.
- `blocked`: an external dependency or decision is missing.

