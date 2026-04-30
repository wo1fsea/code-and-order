# Validation Patterns

Use this reference when defining validation expectations for a repository or a specific governance profile. Validation should be concrete enough that another human or agent can repeat it.

## Validation Weights

### minimal

Use for small tools, docs-heavy repos, and low-risk changes.

Expected evidence:
- Formatting, lint, typecheck, build, or a narrow smoke command when available.
- Link, formatting, or example checks for documentation changes when available.
- Manual check only when automation is not meaningful.
- Record commands skipped and why.

### standard

Use for most product, app, library, and multi-agent work.

Expected evidence:
- Static checks or formatting.
- Relevant unit tests.
- Build or typecheck.
- Targeted integration, browser, or manual checks for touched behavior.
- Documentation checks for changed README, examples, generated docs, specs, or contributor guidance.
- Visual evidence for UI-visible changes.

### strict

Use for public contracts, protocol surfaces, long-running services, migrations, security-sensitive work, or critical UI flows.

Expected evidence:
- Narrow tests plus broader regression tests.
- Contract, schema, migration, or compatibility checks when relevant.
- Documentation source-of-truth, generated-output, public example, and link checks when docs are public or normative.
- Observability, rollback, or failure-path checks for services.
- Screenshots or recordings for critical UI flows and responsive states.

## UI / Visual Evidence Gate

For UI-visible changes, visual evidence is required unless explicitly marked not applicable.

This applies when a change affects:
- Rendering, layout, spacing, sizing, typography, color, imagery, or responsive behavior.
- User-visible copy.
- Interaction flows, menus, dialogs, forms, hover/focus/selected states, loading, empty, disabled, success, or error states.
- Canvas, Three.js, charts, maps, animation, generated images, or other non-trivial visual output.

Default evidence:
- At least one screenshot or short recording of the changed flow.
- Relevant UI states, chosen by risk: normal, loading, empty, error, disabled, hover, focus, selected, expanded, collapsed, or success.
- Desktop viewport for most changes.
- Mobile viewport when layout, responsive behavior, touch interaction, or narrow-screen content may be affected.

Store screenshots, recordings, traces, and other validation artifacts according to `references/temp-artifacts.md`.

For canvas, Three.js, charts, maps, or animation:
- Confirm the surface is nonblank.
- Confirm primary elements render in frame.
- Confirm text and controls do not overlap.
- Confirm the scene or animation moves or responds when interactivity matters.

## Not Applicable Format

Use this when visual evidence is not required:

```markdown
## Visual Evidence

- Required: no
- Reason:
- Substitute evidence:
```

Common valid reasons:
- Backend-only change.
- Test, lint, type, build, dependency, or infrastructure-only change with no visible UI effect.
- UI-adjacent logic covered by automated tests and no rendering, copy, or interaction behavior changed.

## Reporting Format

```markdown
## Validation

- Commands run:
- Automated checks:
- Manual checks:
- Visual evidence:
- Not run:
- Residual risk:
```
