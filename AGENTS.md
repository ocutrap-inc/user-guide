# OcuTrap Agent Alignment — user-guide

**Read [`../internal-docs/orchestrator/agents.md`](../internal-docs/orchestrator/agents.md) first** — the company-wide rules every agent follows (north star + `exit-impact:` tags, spec-first, Linear/ClickUp split, and the §4 shared-contract solidarity rule). Don't restate them here; this header adds only user-guide-specific detail.

- **Requirements home (spec-first):** `.planning/REQUIREMENTS.md`.
- **Tracking:** ClickUp — **Internal Documentation** (Engineering space). Every task: `spec: REQ-ID` + `exit-impact:`.
- **Docs follow product:** terminology home is `app/requirements.md`; notification behavior is ADR 0003 (firmware-sourced). Every customer-visible `app`/firmware change needs a pass through this repo (agents.md §7 — don't skip user-guide).
- **Repo rules:** this file owns the documentation workflow; `CLAUDE.md` points here. Canonical source is git; the published site is the target.


## Documentation workflow

GSD is retired. Ignore legacy GSD commands, generated blocks, profile prompts,
and `.planning/config.json`; they are historical tooling, not prerequisites.
Do not install or run GSD or ask for a GSD bypass before editing.

For authorized work, read the company routing and relevant specification, edit
files directly, keep planning notes current, run the applicable checks, and use
a branch and pull request. Preserve the existing product-before-docs publication
order. These instructions are maintained directly; no generator is required.

See `.planning/PROJECT.md` for project context and `.planning/REQUIREMENTS.md`
for acceptance criteria (including REQ-DOC-WORKFLOW-01).

## Project

**OcuTrap User Guide — Docs Sync**

A one-shot effort to bring `docs.ocutrap.com` (the user guide, self-hosted
from `docs-site/` on Vercel since the 2026-07-10 GitBook cutover, SITE-06) and
its downloadable PDFs back into alignment with the **current state of the
customer app** (`app.ocutrap.com`, post-redesign) and the **current Particle +
camera firmware**. The output is patched markdown in this repo plus
regenerated PDFs that customers actually receive.

**Core Value:** **A customer reading the user guide should never see UI, terminology, or
firmware behavior that doesn't match what they actually have in their hands or
on their screen.** When the docs and the product disagree, the docs lose.

### Constraints

- **Tech stack**: Markdown (GitBook flavor, rendered by the `docs-site/`
  Next.js app — the published site since the 2026-07-10 cutover) for docs
  source of truth; Python + ReportLab for hand-coded PDFs;
  `scripts/build_kb_pdf.py` for auto-compiled KB PDF; CI via GitHub Actions
  (`build-kb-pdf.yml`).
- **Workflow**: Branch + PR required; no direct push to `main`. PRs go
  through harness pre-commit hooks.
- **Image storage**: Plain Git blobs only (no LFS) — `docs-site` serves
  images straight from the repo (`.gitbook/assets/` → `/gitbook-assets/`),
  and the KB PDF build reads them locally. Large media (video) does NOT go
  in git — upload to the `ocutrap-docs-media` Vercel Blob store and embed
  the blob URL.
- **Source of truth direction**: Product (web app + firmware) is
  canonical. Docs follow product. We do not change product to match docs.
