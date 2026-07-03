# Requirements

> Source of truth for v1 requirements. Each REQ-ID is referenced from
> ROADMAP.md (traceability table at the bottom of this file).

## v1 Requirements

### Audit (AUD)

- [ ] **AUD-01**: Produce a written audit comparing every page in `SUMMARY.md`
  to the current Bubble web app at `app.ocutrap.com`. Output is a checklist
  of drifted UI labels, screens, and workflows with the affected markdown
  file path for each item.
- [ ] **AUD-02**: Produce a written audit comparing user guide content to
  the current shipping firmware (Particle B-Series + camera) — specifically
  the v598 / v633 / v644 / v672 / v675 / v700–v706 feature table referenced
  in `pdf-docs/MAINTENANCE.md`, plus current product version 665. Output is
  a checklist of firmware-gated features that are missing or out-of-date in
  the docs, with the affected markdown file path for each item.
- [ ] **AUD-03**: Produce a written audit of the two hand-coded PDFs
  (`R1_Quick_Start.pdf`, `R1_Operation_Cheat_Sheet.pdf`) — list every line of
  hardcoded copy in `scripts/build_quick_start.py` and
  `scripts/build_cheat_sheet.py` that disagrees with current product reality.

### Content Update (DOC)

- [ ] **DOC-01**: Update affected GitBook markdown pages so terminology
  matches the current web app — at minimum: "Captures" → "Detections", the
  three-mode arm system (off / monitor / armed), the new ControlBar, per-trap
  audit log, and `trapIdLabel`.
- [ ] **DOC-02**: Update GitBook markdown to remove or correct any
  description of features that have been removed from the product
  (e.g. post-detection-delay knob — ADR-0002).
- [ ] **DOC-03**: Update screenshots and images for any pages whose UI has
  visually changed in the redesign. Images are committed as plain Git blobs
  (no LFS) so GitBook sync picks them up.
- [ ] **DOC-04**: Update GitBook markdown so firmware-gated behavior matches
  what current firmware actually does (covering the AUD-02 checklist).

### PDF Regeneration (PDF)

- [ ] **PDF-01**: If `R1_Quick_Start.pdf` content drifted, edit
  `scripts/build_quick_start.py` and regenerate the PDF; commit script and
  PDF in the same commit.
- [ ] **PDF-02**: If `R1_Operation_Cheat_Sheet.pdf` content drifted, edit
  `scripts/build_cheat_sheet.py` and regenerate the PDF; commit script and
  PDF in the same commit.
- [ ] **PDF-03**: Regenerate `OcuTrap_Knowledge_Base.pdf` locally via
  `scripts/build_kb_pdf.py` and confirm it builds cleanly from the updated
  markdown. (CI will rebuild on push to `main`; we just need to know it
  works.)
- [ ] **PDF-04**: Run `scripts/verify_kb_pdf.py` (and `source_hash.py` if
  applicable) to confirm there is no remaining drift between the markdown
  source and the committed PDF.

### Tracker Update (TRK)

- [ ] **TRK-01**: Update `pdf-docs/MAINTENANCE.md` "Pending updates" section
  to reflect items resolved in this milestone, the date of the sync, and any
  newly-identified pending items.

## v2 Requirements

<!-- Deferred. Captured here so we don't lose them. -->

- Continuous / automated docs-sync (drift bot) — surface a CI check that
  fails when web-app or firmware repos add features without a matching
  user-guide page.
- Add firmware release notes PDF and hardware/setup PDFs to the sync scope.

## Out of Scope

- **Editing the website or firmware to match docs** — Product is canonical
  in this milestone. If product is wrong, that's a separate engineering
  ticket.
- **Replacing the existing PDF build pipeline** — `build_kb_pdf.py` + CI
  workflow is working as of 2026-05-04; we use it as-is.
- **Rewriting the GitBook information architecture** — `SUMMARY.md` table
  of contents stays as-is unless a specific drift item demands a new page.

## Traceability

| REQ-ID  | Phase                          |
|---------|--------------------------------|
| AUD-01  | Phase 1: Audit                 |
| AUD-02  | Phase 1: Audit                 |
| AUD-03  | Phase 1: Audit                 |
| DOC-01  | Phase 2: Patch                 |
| DOC-02  | Phase 2: Patch                 |
| DOC-03  | Phase 2: Patch                 |
| DOC-04  | Phase 2: Patch                 |
| PDF-01  | Phase 3: Regenerate & Verify   |
| PDF-02  | Phase 3: Regenerate & Verify   |
| PDF-03  | Phase 3: Regenerate & Verify   |
| PDF-04  | Phase 3: Regenerate & Verify   |
| TRK-01  | Phase 3: Regenerate & Verify   |
