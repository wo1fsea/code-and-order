# Universal Agent Initialization

## Principle

Use one canonical router and thin adapters:

```text
AGENTS.md                         # canonical router
CLAUDE.md                         # imports or points to AGENTS.md
GEMINI.md                         # imports or points to AGENTS.md
.github/copilot-instructions.md   # points to AGENTS.md
```

`AGENTS.md` should tell agents what to read next. It should not duplicate detailed workflow docs.

## Thin Adapter Examples

`CLAUDE.md`:

```markdown
# CLAUDE.md

@AGENTS.md
```

`GEMINI.md`:

```markdown
# GEMINI.md

@AGENTS.md
```

`.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Instructions

Follow `AGENTS.md` as the canonical repository guidance. Do not duplicate governance rules here.
```

## Maintenance Rule

When an adapter is added, removed, or moved, update `AGENTS.md` and `docs/governance/agent-context.md` in the same change.
