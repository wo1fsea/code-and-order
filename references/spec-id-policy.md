# Spec ID Policy

## Canonical Shape

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
- Keep the external tracker id stable; treat the slug as human-readable context.
- Use `gh-<number>-<slug>` for GitHub issues.
- Use `linear-<team>-<number>-<slug>` for Linear tickets.
- Use `jira-<project>-<number>-<slug>` for Jira tickets.
- Use `rfc-<4-digit-number>-<slug>` for governance, architecture, or process decisions that are not tied to an issue.
- Use `adhoc-<YYYYMMDD>-<slug>` only for short-lived exploration. Promote accepted work to `rfc-*` or a tracker-backed id.

## Directory Contents

Required:

```text
PRODUCT.md
TECH.md
```

Optional when useful:

```text
DECISIONS.md
VALIDATION.md
ROLLBACK.md
```

## Lifecycle

1. Create the spec directory before implementation when behavior or architecture is ambiguous.
2. Keep `PRODUCT.md` aligned with shipped behavior.
3. Keep `TECH.md` aligned with the implementation that actually landed.
4. If the source ticket changes, prefer updating links inside the spec over renaming a directory that has already been referenced in commits or PRs.

