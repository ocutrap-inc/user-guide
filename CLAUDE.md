# OcuTrap Agent Alignment — user-guide

**Read [`../internal-docs/orchestrator/agents.md`](../internal-docs/orchestrator/agents.md) first** — the company-wide rules every agent follows (north star + `exit-impact:` tags, spec-first, Linear/ClickUp split, and the §4 shared-contract solidarity rule). Repo specifics: [`AGENTS.md`](AGENTS.md).

- **Requirements home (spec-first):** `.planning/REQUIREMENTS.md`.
- **Tracking:** ClickUp — **Internal Documentation**. Every task: `spec: REQ-ID` + `exit-impact:`.
- **Docs follow product:** terminology home is `app/requirements.md`; don't skip user-guide for customer-visible changes (agents.md §7).

*(The GSD blocks below are tool-generated and mirror `AGENTS.md` by design.)*

<!-- GSD:project-start source:PROJECT.md -->
## Project

**OcuTrap User Guide — Docs Sync**

A one-shot effort to bring `docs.ocutrap.com` (the GitBook user guide) and its
downloadable PDFs back into alignment with the **current state of the customer
app** (`app.ocutrap.com`, post-redesign) and the **current Particle + camera
firmware**. The output is patched markdown in this repo plus regenerated PDFs
that customers actually receive.

**Core Value:** **A customer reading the user guide should never see UI, terminology, or
firmware behavior that doesn't match what they actually have in their hands or
on their screen.** When the docs and the product disagree, the docs lose.

### Constraints

- **Tech stack**: Markdown (GitBook flavor) for docs source of truth;
  Python + ReportLab for hand-coded PDFs; `scripts/build_kb_pdf.py` for
  auto-compiled KB PDF; CI via GitHub Actions (`build-kb-pdf.yml`).
- **Workflow**: Branch + PR required; no direct push to `main`. PRs go
  through harness pre-commit hooks.
- **Image storage**: Plain Git blobs only (no LFS) so GitBook's sync
  picks them up.
- **Source of truth direction**: Product (web app + firmware) is
  canonical. Docs follow product. We do not change product to match docs.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
