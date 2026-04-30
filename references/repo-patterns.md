# Repo Patterns

Use this reference before initializing governance for a new, unfamiliar, or mixed repository. The goal is to choose the smallest useful governance set for the repo's actual shape.

## Initialization Clarification

Inspect the repo first. If the pattern or desired governance weight is unclear, ask concise questions before generating files.

Ask only what changes the output. Good questions:

1. Which repo pattern should governance optimize for: `small-tool`, `web-app`, `monorepo`, `plugin-sdk-protocol`, `long-running-service`, `docs-heavy`, or `mixed`?
2. Should governance be `minimal`, `standard`, or `strict`?
3. Which agent adapters are required: Codex `AGENTS.md`, Claude `CLAUDE.md`, Gemini `GEMINI.md`, GitHub Copilot, Cursor, or other?
4. What are the canonical validation commands for this repo?
5. Should specs and workstreams be created by default, or only when a task is ambiguous, cross-module, or high-risk?

If the user asks for non-interactive initialization, infer a pattern from repo signals, state the assumption, and choose the lightest viable governance.

## Pattern Summary

| Pattern | Typical repo | Default weight |
|---|---|---|
| `small-tool` | CLI, script, local utility, single package | minimal |
| `web-app` | product UI, dashboard, frontend/backend app | standard |
| `monorepo` | multiple packages, apps, owners, or workspaces | standard to strict |
| `plugin-sdk-protocol` | plugin, SDK, API client, MCP/JSON-RPC/protocol surface | strict on contracts |
| `long-running-service` | service, worker, infra automation, operator console | strict on runtime safety |
| `docs-heavy` | documentation site, knowledge repo, prompt/skill repo | standard on source-of-truth |
| `mixed` | repo matches multiple patterns | ask for primary pattern |

## Patterns

### small-tool

Signals:
- One main package, CLI, script, or local utility.
- Validation is usually one test/build/smoke command.
- Few maintainers or agents operate in the repo.

Default governance:
- `AGENTS.md` as the canonical router.
- Development, validation, and code-quality workflows.
- Temp artifact rule when the tool produces logs, screenshots, traces, scratch files, or generated files.

Enable when needed:
- TDD for behavior changes.
- Specs only for ambiguous behavior, public CLI/API changes, or cross-module work.

Avoid by default:
- Full spec workstream boards.
- Heavy ADR process.
- Multiple adapter files unless the tools are actually used.

### web-app

Signals:
- UI routes, components, assets, screenshots, browser flows, or frontend/backend integration.
- User-visible behavior and visual regressions matter.

Default governance:
- Development, validation, TDD, code-quality, and review workflows.
- Validation should include build/typecheck plus targeted UI or browser checks when behavior is visual.
- UI-visible changes require visual evidence unless explicitly not applicable: screenshots or recordings for relevant states and viewports.

Enable when needed:
- Visual governance for design-sensitive products.
- E2E or screenshot gates for critical flows.
- Specs for user-visible or cross-module features.

Avoid by default:
- Protocol-versioning rules unless the app exposes a stable external API.

### monorepo

Signals:
- Multiple packages, workspaces, apps, services, owners, or build systems.
- A change can easily affect unrelated packages.

Default governance:
- Fixed read order and package-scope rules.
- Command entrypoints for narrow package validation and broader workspace validation.
- Specs and workstreams for cross-package work.

Enable when needed:
- Ownership maps.
- Capability matrices.
- Root wrapper commands.

Avoid by default:
- Whole-repo rewrites or broad formatting in feature changes.
- Rules that assume one package manager, runtime, or release flow without inspection.

### plugin-sdk-protocol

Signals:
- Public APIs, plugin contracts, SDK exports, schemas, JSON-RPC, MCP, GraphQL, REST, CLI contracts, or extension points.

Default governance:
- Change gate before adding surface.
- Contract compatibility and migration notes.
- Distinguishable error types.
- Validation for public examples, schema, or protocol fixtures.

Enable when needed:
- Capability matrix.
- Versioning policy.
- Deprecation and compatibility-layer governance.

Avoid by default:
- Silent defaults or ambiguous optional parameters.
- Renaming or removing public surface without migration guidance.

### long-running-service

Signals:
- Background workers, servers, schedulers, queues, databases, deployment, infrastructure, or operator consoles.

Default governance:
- Runtime safety, failure strategy, observability, validation, and code-quality workflows.
- Explicit handling for retries, timeouts, partial success, migrations, and rollback.

Enable when needed:
- Runbooks.
- Incident notes.
- Deployment and rollback checklists.

Avoid by default:
- Treating local unit tests as sufficient proof for runtime changes.

### docs-heavy

Signals:
- Main output is docs, specs, prompts, skills, or knowledge organization.
- Correct source-of-truth and stale content control matter more than runtime behavior.

Default governance:
- Canonical entrypoint and source-of-truth rules.
- Documentation sync and stale-content deletion.
- Lightweight validation for links, formatting, examples, and generated outputs.

Enable when needed:
- Audience-split docs.
- Index or resume snapshot for long-running knowledge projects.
- Publication checklist.

Avoid by default:
- Code-heavy spec/workstream ceremony unless docs are produced by a substantial software system.

## Selection Output

After classification, summarize the choice before editing:

```markdown
## Governance Initialization Choice

- Repo pattern:
- Governance weight:
- Required agent adapters:
- Validation commands:
- Specs/workstreams:
- Enabled modules:
- Intentionally skipped modules:
- Assumptions:
```
