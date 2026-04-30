# Change Gate

Use this gate before adding or expanding project surface. The goal is to make every new surface prove that it deserves to exist.

## What Counts As Surface

Surface includes:

- API endpoint or route.
- Public or exported function, class, component, package export, or module.
- CLI command, option, flag, or output format.
- Configuration field, environment variable, feature flag, or runtime mode.
- Dependency, adapter, integration, provider, or compatibility shim.
- File format, schema, database shape, event format, or protocol message.
- Workflow document, governance file, template, agent entrypoint, or generated starter file.
- Plugin extension point, hook, callback, or user-facing customization point.

## When Required

Run the gate when a change:

- Adds new surface.
- Expands existing surface with new modes, parameters, states, options, or behavior.
- Renames, replaces, deprecates, or removes surface.
- Adds a compatibility layer, fallback path, migration path, or temporary feature flag.

## Gate Questions

Record these answers in the PR, spec, workstream, or nearby decision record:

```markdown
## Change Gate

- Problem:
- Existing path considered:
- Why existing path is insufficient:
- Smallest new surface:
- What will be deleted or replaced:
- Owner:
- Validation:
- Temporary or permanent:
- Removal condition:
```

## Rules

1. Prefer reuse before adding surface.
   - If an existing path can solve the problem, use it.

2. Keep new surface minimal.
   - Do not add future-looking parameters, modes, configuration, wrappers, extension points, or abstractions without an immediate need.

3. Delete superseded paths in the same change.
   - When a new path replaces an old one, delete the old code, command, config, document, adapter, test, and routing entry unless compatibility requires retention.

4. Require ownership.
   - New configs, flags, adapters, dependencies, workflows, and templates need an owner for future changes.

5. Require validation.
   - API surface needs contract or integration checks.
   - CLI surface needs smoke or usage checks.
   - Config surface needs default and override checks.
   - Agent or workflow docs need routing or generated-output checks.

6. Temporary surface needs a removal condition.
   - `temporary` is not enough. State exactly when the surface can be deleted.

7. Public surface needs compatibility notes.
   - Public APIs, CLIs, schemas, file formats, agent entrypoints, and templates must explain whether old behavior remains compatible.

8. Documentation surface counts.
   - New governance docs, README sections, templates, and agent instructions must define their boundary and avoid duplicating an existing source of truth.

9. Dependencies count.
   - New dependencies must explain why the standard library or existing dependency is insufficient, plus maintenance health, license, size/runtime impact, and security surface when relevant.

## Compatibility Exception

Use this when old and new paths must coexist:

```markdown
## Compatibility Exception

- Old path:
- New path:
- Why retained:
- Owner:
- Remove when:
- Tracking issue/spec:
- Validation:
```

## Reviewer Checklist

- Is the new surface necessary?
- Is it the smallest useful surface?
- Did the change delete or deprecate superseded paths?
- Is ownership clear?
- Is validation tied to the new surface?
- If temporary or compatibility-related, is the removal condition concrete?
