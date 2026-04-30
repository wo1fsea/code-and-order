---
language: en-US
audience: agent
doc_type: normative
---

# Documentation Standards

Use this governance when creating, changing, or reviewing documentation, examples, agent instructions, contributor guidance, user-facing help, generated docs, or specs.

## Principle

Documentation is project surface. It should have a clear source of truth, audience, scope, validation path, and retirement path. A stale doc is worse than no doc because it trains humans and agents to distrust the repo.

## When Required

Apply this when a change:

- Adds, moves, renames, deletes, or substantially rewrites a doc.
- Changes user/API-visible behavior that existing docs describe.
- Changes commands, configuration, environment variables, file formats, schemas, setup, deployment, validation, or troubleshooting steps.
- Adds or changes examples, snippets, templates, generated docs, screenshots, diagrams, or public contributor guidance.
- Changes agent instructions, governance files, specs, or routing docs such as `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, or `docs/README.md`.

If a behavior change does not require documentation, record why in the PR, workstream, or change note.

## Documentation Types

- `router`: Short entrypoints that point to canonical docs, such as `AGENTS.md`, root `README.md`, and docs indexes.
- `normative`: Rules people should follow, such as governance docs, contributor docs, runbooks, and API contracts.
- `explanatory`: Architecture notes, guides, design docs, and tutorials.
- `spec`: Product, technical, status, and workstream docs under `specs/`.
- `example`: Runnable examples, snippets, fixtures, screenshots, and diagrams.
- `template`: Templates that are copied or rendered into future docs, issues, PRs, or specs.
- `generated`: Docs produced from source, schemas, code, comments, or tooling.
- `historical`: ADRs, decision records, incident notes, and superseded plans.

Name the type implicitly in the location or explicitly near the top when ambiguity would affect maintenance.

## Language And Audience

Every new or substantially changed durable doc must declare its language near the top. Prefer YAML frontmatter when the file supports it:

```yaml
---
language: en-US
audience: agent
doc_type: normative
---
```

Use these values unless the repo defines a tighter local set:

- `language`: `en-US`, `zh-CN`, or `mixed`.
- `audience`: `agent`, `human`, or `mixed`.
- `doc_type`: `router`, `normative`, `explanatory`, `spec`, `example`, `template`, `generated`, or `historical`.

Rules:

1. Use `en-US` for agent-facing docs by default.
   - This includes `AGENTS.md`, agent adapters, governance docs, technical specs, status boards, workstreams, validation docs, and review workflows.

2. Use the target reader's language for user-facing or team-facing docs.
   - Product docs, project notes, public user docs, and team research can use the language of their primary human audience.

3. Use `mixed` only when multiple languages are intentional.
   - Label sections clearly when a doc mixes languages.
   - Do not mix languages casually inside normative instructions.

4. Keep code and tool literals unchanged.
   - Code identifiers, commands, paths, flags, API names, error strings, and copied output remain literal even when surrounding prose uses another language.

5. Use a comment metadata block when YAML frontmatter would leak into generated output.
   - Templates that render directly into PRs, issues, or user-facing content may use a hidden HTML comment with `language`, `audience`, and `doc_type`.

Existing docs without metadata should be backfilled when they are touched, moved, audited, or promoted.

## Required Rules

1. Define one source of truth.
   - Do not copy the same rule, command, API shape, or setup instruction into multiple long-lived docs.
   - If multiple entrypoints need the same information, make one canonical and point the others to it.

2. State audience and scope early.
   - A reader should quickly know whether the doc is for users, contributors, maintainers, operators, reviewers, or agents.
   - Say what the doc covers and what it intentionally does not cover when scope is easy to misunderstand.

3. Keep routers thin.
   - Entry files such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions, root README sections, and docs indexes should route, not duplicate.
   - When adding, deleting, renaming, or moving canonical docs, update the router in the same change.

4. Update docs with behavior.
   - Code changes that alter documented behavior must update the relevant docs in the same change or record why no doc update is needed.
   - Public APIs, CLI output, configs, environment variables, schema, setup, deployment, and validation changes count as documented behavior.

5. Validate examples and commands.
   - Commands should include working directory, required environment, expected output shape, or validation context when not obvious.
   - Snippets and examples must either be runnable/verified or clearly marked illustrative.
   - Do not leave copied examples that no longer match the current API.

6. Treat generated docs as generated.
   - Record the generator or source.
   - Update the source and regenerate instead of hand-editing generated output, unless the repo documents an exception.

7. Delete or supersede stale docs.
   - When a doc is obsolete, remove it or mark it superseded with the replacement path.
   - Do not preserve old docs "just in case" without owner and review condition.

8. Keep links and names stable.
   - Prefer lowercase kebab-case for new governance and docs files unless the repo already has a convention.
   - Update inbound links when moving or renaming docs.
   - Use relative links inside the repo when practical.

9. Separate durable docs from working notes.
   - Drafts, raw agent notes, debug output, screenshots, recordings, traces, and generated reports stay in `.out/` until accepted or promoted.
   - Promoted artifacts need an owned destination and a reason to retain them.

10. Preserve historical records honestly.
    - Do not silently rewrite accepted decisions, ADRs, incident timelines, or completed specs to hide prior context.
    - Append correction, superseded, or follow-up notes when history matters.

## Documentation Evidence

Use this in PRs, workstreams, or review notes:

```markdown
## Documentation Evidence

- Docs updated / N/A:
- Language/audience/doc type declared:
- Source of truth:
- Routers or indexes updated:
- Links checked:
- Examples or commands checked:
- Generated docs regenerated / N/A:
- Stale docs removed or superseded:
```

## Reviewer Checklist

- Is there one clear source of truth?
- Does each new or changed durable doc declare language, audience, and doc type?
- Are agent-facing docs written in English unless a local exception is explicit?
- Did behavior, command, config, setup, schema, or validation changes update docs?
- Are routers and indexes current?
- Are examples, snippets, screenshots, and commands still accurate?
- Are generated docs updated from their source?
- Were stale docs deleted or explicitly superseded?
- Are temporary artifacts kept out of durable docs unless promoted?
