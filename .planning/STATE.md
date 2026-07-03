# STATE — OcuTrap User Guide Docs Sync

## Project Reference

- **Repo**: `~/ocutrapinc/user-guide` on branch `feat/docs-sync-update`
- **Core value**: A customer reading the user guide should never see UI,
  terminology, or firmware behavior that doesn't match what they actually have
  in their hands or on their screen. Product is canonical; docs follow.
- **Current focus**: Phase 1 — Audit (produce three written drift checklists)
- **Granularity**: coarse (3 phases)
- **Workflow**: Branch + PR. Direct push to `main` blocked by harness hook.

## Current Position

- **Milestone**: Docs Sync 2026-05
- **Phase**: 1 of 3 — Audit
- **Plan**: not yet planned
- **Status**: roadmap approved, awaiting `/gsd-plan-phase 1`
- **Progress**: `[░░░░░░░░░░] 0%` (0/3 phases complete)

## Phase Map

| # | Phase | Status | REQ-IDs |
|---|-------|--------|---------|
| 1 | Audit                | Not started | AUD-01, AUD-02, AUD-03 |
| 2 | Patch                | Not started | DOC-01, DOC-02, DOC-03, DOC-04 |
| 3 | Regenerate & Verify  | Not started | PDF-01, PDF-02, PDF-03, PDF-04, TRK-01 |

## Performance Metrics

- Phases complete: 0/3
- Plans complete: 0/0 (no plans drafted yet)
- Requirements covered: 0/12 (all mapped, none yet executed)

## Accumulated Context

### Decisions

- **One-shot sync, not automation** — User explicitly scoped "update once now".
  A continuous drift-bot is captured as a v2 backlog seed.
- **User guide PDFs only** — Firmware release notes, hardware/setup PDFs, and
  translations are out of scope this milestone.
- **Coarse granularity, 3 phases** — Audit → Patch → Regenerate & Verify. The
  shape was inevitable from the requirement structure (AUD / DOC / PDF+TRK).
- **Audits land on disk before patching** — Phase 1 produces concrete checklists
  in `.planning/audits/` so Phase 2 executes against artifacts, not memory.
- **Existing build infra is canonical** — `build_quick_start.py`,
  `build_cheat_sheet.py`, `build_kb_pdf.py`, `verify_kb_pdf.py`, and
  `.github/workflows/build-kb-pdf.yml` are used as-is. We do not replace them.

### Standing Constraints

- Images committed as plain Git blobs only (no LFS) — GitBook sync skips LFS.
- Cellular-only firmware (Particle B-Series); no WiFi anywhere in docs.
- Notification policy: notify only when `detectionType === "captured"`.
- ADR-0002 rejected post-detection-delay; R1 closes on first verified
  detection. Docs must not describe the removed knob.
- Direction is one-way: product → docs. We do not edit product to match docs.

### Todos / Carry-Forward

- (none yet — populated by `/gsd-plan-phase 1`)

### Blockers

- (none)

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260616-q22 | Image-cadence page + v915 distance/zone/cadence reconciliation | 2026-06-16 | 2f3473c | [260616-q22-add-image-cadence-user-guide-page-and-co](./quick/260616-q22-add-image-cadence-user-guide-page-and-co/) |

## Session Continuity

- **Last session**: 2026-05-04 — `/gsd-new-project` created PROJECT.md,
  REQUIREMENTS.md, ROADMAP.md, STATE.md.
- **Next action**: `/gsd-plan-phase 1` to decompose the Audit phase into a
  concrete plan that produces the three drift checklists.
- **Files of interest for next session**:
  - `.planning/ROADMAP.md` (phase definitions)
  - `.planning/REQUIREMENTS.md` (REQ-IDs and traceability)
  - `SUMMARY.md` (GitBook table of contents — input to AUD-01)
  - `pdf-docs/MAINTENANCE.md` (drift tracker — input to AUD-02 and TRK-01)
  - `scripts/build_quick_start.py`, `scripts/build_cheat_sheet.py` (input to
    AUD-03 and Phase 3 regeneration)
