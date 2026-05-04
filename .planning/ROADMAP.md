# Roadmap — OcuTrap User Guide Docs Sync

> One-shot milestone to bring `docs.ocutrap.com` and the customer-downloadable
> PDFs back into alignment with the current OcuTrap web app and shipping
> firmware. Coarse granularity: audit → patch → regenerate-and-verify.

## Milestone

**Docs Sync 2026-05** — Patch GitBook markdown, hand-coded PDFs, and the
auto-built Knowledge Base PDF so a customer reading the guide never sees UI,
terminology, or firmware behavior that disagrees with the product.

## Phases

- [ ] **Phase 1: Audit** — Produce written checklists of every drift between docs and product (web app, firmware, hand-coded PDFs).
- [ ] **Phase 2: Patch** — Apply the audit checklists to GitBook markdown and screenshots so the source-of-truth docs match the product.
- [ ] **Phase 3: Regenerate & Verify** — Rebuild the hand-coded PDFs, rebuild the Knowledge Base PDF, verify drift is zero, and update the maintenance tracker.

## Phase Details

### Phase 1: Audit
**Goal**: Three concrete written checklists exist on disk that name every drifted item, the affected file path, and the corrective action — so Phase 2 has executable work, not a research task.
**Depends on**: Nothing (first phase)
**Requirements**: AUD-01, AUD-02, AUD-03
**Success Criteria** (what must be TRUE):
  1. A written web-app audit checklist exists in `.planning/audits/` that lists every drifted UI label, screen, and workflow (including "Captures" → "Detections", three-mode arm system off/monitor/armed, ControlBar, analytics heatmaps, per-trap audit log, `trapIdLabel`) with the affected markdown file path for each item.
  2. A written firmware audit checklist exists in `.planning/audits/` that lists every firmware-gated feature from the v598 / v633 / v644 / v672 / v675 / v700–v706 table (and current product version 665) that is missing or out-of-date in the docs, with the affected markdown file path for each item — and explicitly flags the post-detection-delay knob (ADR-0002 rejected) for removal.
  3. A written PDF copy audit checklist exists in `.planning/audits/` that lists every line of hardcoded copy in `scripts/build_quick_start.py` and `scripts/build_cheat_sheet.py` that disagrees with current product reality.
  4. Every item in all three checklists has an unambiguous corrective action (rename / rewrite / replace screenshot / delete section / add page) so Phase 2 can execute without re-deciding.
**Plans**: TBD

### Phase 2: Patch
**Goal**: The GitBook markdown source of truth (and its images) matches the current product — every item from the Phase 1 checklists is resolved in the markdown tree.
**Depends on**: Phase 1
**Requirements**: DOC-01, DOC-02, DOC-03, DOC-04
**Success Criteria** (what must be TRUE):
  1. Every web-app drift item from the Phase 1 audit is resolved in GitBook markdown — terminology matches the current app (Detections, three-mode arm, ControlBar, per-trap audit log, `trapIdLabel`) and the audit checklist is fully ticked off.
  2. No GitBook markdown page describes a feature that no longer exists in the product (post-detection-delay knob and any other ADR-rejected behavior is removed or corrected).
  3. Every screenshot/image whose UI visually changed in the redesign is replaced; replacements are committed as plain Git blobs (no LFS) per the GitBook sync constraint.
  4. Every firmware-gated behavior item from the Phase 1 firmware audit is reflected in markdown so the docs match what current firmware (through v706, product 665) actually does — including the cellular-only constraint (no WiFi) and notify-only-on-captured policy.
**Plans**: TBD
**UI hint**: yes

### Phase 3: Regenerate & Verify
**Goal**: All three customer-facing PDFs are rebuilt from the patched sources, drift verification passes, and the maintenance tracker reflects the new state-of-the-world.
**Depends on**: Phase 2
**Requirements**: PDF-01, PDF-02, PDF-03, PDF-04, TRK-01
**Success Criteria** (what must be TRUE):
  1. If the Phase 1 PDF audit flagged drift in `R1_Quick_Start.pdf`, `scripts/build_quick_start.py` is updated and `python3 scripts/build_quick_start.py` produces the regenerated PDF; both the script and the PDF are committed in the same commit. (If the audit found no drift, the phase records that explicitly.)
  2. If the Phase 1 PDF audit flagged drift in `R1_Operation_Cheat_Sheet.pdf`, `scripts/build_cheat_sheet.py` is updated and `python3 scripts/build_cheat_sheet.py` produces the regenerated PDF; both the script and the PDF are committed in the same commit. (If the audit found no drift, the phase records that explicitly.)
  3. `python3 scripts/build_kb_pdf.py` exits 0 locally and produces an updated `.gitbook/assets/OcuTrap_Knowledge_Base.pdf` plus its `.sources.sha` sidecar, both committed in the same PR as the Phase 2 markdown changes.
  4. `python3 scripts/verify_kb_pdf.py` exits 0 against the committed PDF and sidecar, confirming zero remaining drift between the markdown source and the committed Knowledge Base PDF.
  5. `pdf-docs/MAINTENANCE.md` "Pending updates" section is updated: items resolved in this milestone are ticked with the 2026-05 sync date, and any newly-identified pending items are added.
**Plans**: TBD

## Progress

| Phase | Plans Complete | Status      | Completed |
|-------|----------------|-------------|-----------|
| 1. Audit                  | 0/0 | Not started | -    |
| 2. Patch                  | 0/0 | Not started | -    |
| 3. Regenerate & Verify    | 0/0 | Not started | -    |

## Coverage

All 12 v1 requirements mapped to exactly one phase. No orphans.

| Phase | REQ-IDs |
|-------|---------|
| 1. Audit                  | AUD-01, AUD-02, AUD-03 |
| 2. Patch                  | DOC-01, DOC-02, DOC-03, DOC-04 |
| 3. Regenerate & Verify    | PDF-01, PDF-02, PDF-03, PDF-04, TRK-01 |
