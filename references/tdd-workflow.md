# TDD Workflow

## Loop

Use this loop for behavior changes:

```text
Product behavior -> test plan -> red -> green -> refactor -> broaden -> validate -> record
```

## Steps

1. Write or update behavior invariants in `PRODUCT.md`.
2. Map important invariants to tests in `TECH.md`.
3. Add the smallest failing test that proves the behavior is not implemented.
4. Run the narrow test command and record the red result.
5. Implement the smallest change that makes the test pass.
6. Run the same narrow command and record the green result.
7. Refactor only while the tests are green.
8. Broaden validation to the relevant unit, integration, e2e, or manual checks.
9. Record commands run, checks skipped, and residual risk in the PR or implementation log.

## PR Evidence

For non-trivial behavior changes, capture:

```markdown
## TDD Evidence

- Red:
- Green:
- Broader validation:
- Tests not run:
```

## When TDD Can Be Light

Use a lighter loop for documentation-only edits, mechanical renames, dependency bumps, generated code updates, or changes where the repository has no realistic automated test seam. Still record manual validation or explain why no validation was run.

