# OcuTrap User Guide — Docs Sync

## What This Is

A one-shot effort to bring `docs.ocutrap.com` (the GitBook user guide) and its
downloadable PDFs back into alignment with the **current state of the customer
app** (`app.ocutrap.com`, post-redesign) and the **current Particle + camera
firmware**. The output is patched markdown in this repo plus regenerated PDFs
that customers actually receive.

## Core Value

**A customer reading the user guide should never see UI, terminology, or
firmware behavior that doesn't match what they actually have in their hands or
on their screen.** When the docs and the product disagree, the docs lose.

## Requirements

### Validated

<!-- Capabilities that already exist and are working in this repo. -->

- ✓ GitBook markdown structure (`SUMMARY.md` table of contents) — existing
- ✓ Auto-compiled `OcuTrap_Knowledge_Base.pdf` from `SUMMARY.md` via
  `scripts/build_kb_pdf.py` + `.github/workflows/build-kb-pdf.yml` — existing
- ✓ Hand-coded `R1_Quick_Start.pdf` via `scripts/build_quick_start.py` —
  existing
- ✓ Hand-coded `R1_Operation_Cheat_Sheet.pdf` via
  `scripts/build_cheat_sheet.py` — existing
- ✓ Drift tracker at `pdf-docs/MAINTENANCE.md` — existing
- ✓ Source-hash drift detection via `scripts/source_hash.py` and
  `scripts/verify_kb_pdf.py` — existing

### Active

<!-- Current scope. The hypotheses we're shipping. -->

- [ ] Audit `docs.ocutrap.com` content against the current Bubble web app at
  `app.ocutrap.com` — list every UI label, mode name, screen, and workflow
  that has drifted (e.g. "Captures" → "Detections", arm modes
  off / monitor / armed, ControlBar, analytics heatmaps, per-trap audit log,
  trapIdLabel)
- [ ] Audit user guide content against the current shipping firmware
  (Particle B-Series + camera) — confirm coverage of features through
  product version 665 and the v598/v633/v644/v672/v675/v700–v706 feature
  table referenced in `pdf-docs/MAINTENANCE.md`
- [ ] Patch the affected GitBook markdown pages so screenshots, labels, and
  step-by-step flows match the current app and firmware
- [ ] Regenerate the two hand-coded PDFs (`R1_Quick_Start.pdf`,
  `R1_Operation_Cheat_Sheet.pdf`) if any of their hardcoded copy drifted
- [ ] Verify `OcuTrap_Knowledge_Base.pdf` rebuilds cleanly from the updated
  markdown (CI on push to main, plus local `verify_kb_pdf.py`)
- [ ] Update `pdf-docs/MAINTENANCE.md` "Pending updates" tracker so it
  reflects the new state-of-the-world

### Out of Scope

- **Continuous / automated docs-sync tooling** — User answered "Update docs
  once now"; we are not building a watcher / drift bot in this milestone.
  Capture as a backlog seed if drift recurs.
- **Re-architecting the PDF build pipeline** — The existing
  `build_kb_pdf.py` + CI workflow is working; we use it, we do not replace
  it.
- **Firmware release notes PDF, hardware/setup PDFs** — User scoped this to
  *user guide PDF only*. Other PDFs are not in this milestone.
- **Translations** (`translate_repo.py` exists) — Not part of this sync;
  English source-of-truth only.
- **Editing the website or firmware to match the docs** — Direction is
  one-way: product is canonical, docs follow.

## Context

- **Repo**: `~/ocutrapinc/user-guide` on branch `feat/docs-sync-update`.
  Owned by `ocutrap-inc` GitHub org; harness blocks direct push to `main`,
  so all changes ship via PR.
- **GitBook ↔ Git LFS gotcha**: GitBook's GitHub sync does **not** pull LFS,
  so PNG/JPG/JPEG/GIF in this repo are kept as plain Git blobs (de-LFS'd
  2026-04-27). Any image updates we make must follow the same rule.
- **Web app reality** (per recent OcuTrap redesign, PRs #2–#8 on
  `ocutrap-inc/app`): three-mode arm system (off / monitor / armed),
  Captures renamed to **Detections**, new **ControlBar**, analytics
  heatmaps, per-trap audit log, `trapIdLabel`. The user guide largely
  predates this redesign.
- **Firmware reality**: WiFi is not supported (cellular-only Particle
  B-Series SoM). Current product version is 665. `pdf-docs/MAINTENANCE.md`
  already lists firmware-gated features through v700–v706 and notes they
  were captured in GitBook on 2026-05-04.
- **Notification policy**: notify only on real trap captures
  (`detectionType === "captured"`), not on every image — docs must reflect
  this.
- **Post-detection delay**: ADR-0002 rejected post-detection-delay; R1
  closes on first verified detection. Docs must not describe a knob that
  no longer exists.
- **Rebuild ethos**: minimalism, maintainability, compartmentalization
  above all else — applies to anything we add, including new doc pages.

## Constraints

- **Tech stack**: Markdown (GitBook flavor) for docs source of truth;
  Python + ReportLab for hand-coded PDFs; `scripts/build_kb_pdf.py` for
  auto-compiled KB PDF; CI via GitHub Actions (`build-kb-pdf.yml`).
- **Workflow**: Branch + PR required; no direct push to `main`. PRs go
  through harness pre-commit hooks.
- **Image storage**: Plain Git blobs only (no LFS) so GitBook's sync
  picks them up.
- **Source of truth direction**: Product (web app + firmware) is
  canonical. Docs follow product. We do not change product to match docs.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| One-shot sync, not automation | User explicitly scoped "update once now"; automation can come later if drift recurs | — Pending |
| User guide PDF only | User answered "User guide PDF" to the PDF-scope question; other PDFs deferred | — Pending |
| Skip codebase mapping | This is a content / docs repo, not an architecture decision; mapping the markdown tree adds no value | — Pending |
| Skip domain research | The drift surface (web app + firmware) is in adjacent repos we already know; web research can't tell us what's in our own product | — Pending |
| Coarse granularity | Audit → patch → regen → verify is naturally 3–4 phases | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-04 after initialization*
