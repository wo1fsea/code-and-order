# Temp Artifacts

Use this governance when humans or agents create screenshots, recordings, traces, logs, debug dumps, generated reports, benchmark output, downloaded fixtures, or scratch files while working.

## Principle

Temporary artifacts are useful during work, but they must not pollute formal repo knowledge. Keep them contained, ignored by default, and promote them only when they need long-term ownership.

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

1. Put temporary artifacts in `.out/`.
   - Use it for screenshots, recordings, browser traces, debug logs, generated reports, benchmark output, scratch JSON, downloaded fixtures, and one-off agent output.

2. Do not commit `.out/` by default.
   - It is a local work area, not a formal knowledge location.

3. Evidence can be referenced without being committed.
   - Example: `Visual evidence: .out/screenshots/login-mobile-error.png`.

4. Promote long-term artifacts.
   - If an artifact is part of durable documentation or a spec, move it to an owned location such as `docs/assets/`, `docs/reports/`, or `specs/<spec-id>/evidence/`.
   - Explain why it is retained.

5. Do not pollute formal directories.
   - Do not place unpromoted artifacts in repo root, `docs/`, `specs/`, `src/`, or `tests/`.

6. Agent drafts are not specs.
   - Raw analysis, scratch notes, dumps, and one-off generated files stay in `.out/scratch/` until explicitly accepted into `docs/` or `specs/`.

7. Cleanup is part of done.
   - Before finishing, delete useless artifacts or confirm they are in an ignored temp location.

8. Protect sensitive data.
   - Do not write secrets, tokens, private customer data, or sensitive logs into `.out/`.
   - If sensitive evidence must be captured, redact it and record the handling note.

## Promotion Format

```markdown
## Artifact Promotion

- Artifact:
- From:
- To:
- Reason retained:
- Owner:
- Remove or review when:
```

## Reporting

Use this in PRs, workstreams, or validation notes:

```markdown
## Temp Artifacts

- Created:
- Referenced as evidence:
- Promoted:
- Cleaned:
- Intentionally retained:
```
