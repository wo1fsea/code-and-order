---
language: en-US
audience: mixed
doc_type: router
---

# Code & Order

Code & Order is a Codex skill for initializing and maintaining lightweight
engineering governance in human-agent software projects.

It helps repositories set up agent guidance, spec-first workflows, execution
status, validation rules, documentation standards, and code-quality review
gates without turning the project into a process shrine.

## Recommended Installation

Install Code & Order as a cloned global Codex skill.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/wo1fsea/code-and-order.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/code-and-order"
```

Use `git pull` to update the skill:

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/code-and-order" pull --ff-only
```

Prefer this clone-based install over copying files so the installed skill keeps
its Git history, can be updated safely, and can be inspected or pinned by
commit.

## Usage

Ask Codex to use the `code-and-order` skill when initializing or auditing repo
governance:

```text
Use code-and-order to initialize governance for this repository.
```

The skill entry point is `SKILL.md`; supporting workflows live under
`references/`, and the deterministic initializer lives at
`scripts/init_governance.py`.
