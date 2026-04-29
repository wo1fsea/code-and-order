#!/usr/bin/env python3
"""Create a minimal human-agent governance starter set for a repository."""

from __future__ import annotations

import argparse
from pathlib import Path


AGENTS = """# AGENTS.md

This repository supports lightweight human + agent collaboration.

## Read First

- Read this file before making changes.
- Prefer existing project patterns over new abstractions.
- Keep edits scoped to the requested behavior.
- Do not revert user changes unless explicitly asked.

## Workflow

- Straightforward bug fix or small change -> implement directly.
- Ambiguous feature or cross-module change -> write a spec under `specs/<id>/`.
- Update governance docs in the same change when workflow rules change.

## Validation

- Run the narrowest meaningful tests first.
- For user-facing changes, include manual validation steps or screenshots when useful.
- State any tests that were not run and why.
"""


PRODUCT = """# <Feature> Product Spec

## Summary

## Goals / Non-goals

## Behavior

1. 

## Open Questions
"""


TECH = """# <Feature> Tech Spec

Product spec: `./PRODUCT.md`

## Context

## Proposed Changes

## Testing and Validation

## Risks and Follow-ups
"""


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".", help="Repository root")
    parser.add_argument("--spec-id", default="example-feature", help="Starter spec directory id")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    created = []

    for path, content in [
        (root / "AGENTS.md", AGENTS),
        (root / "specs" / args.spec_id / "PRODUCT.md", PRODUCT),
        (root / "specs" / args.spec_id / "TECH.md", TECH),
    ]:
        if write_if_missing(path, content):
            created.append(path)

    if created:
        print("Created:")
        for path in created:
            print(f"- {path.relative_to(root)}")
    else:
        print("No files created; starter files already exist.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
