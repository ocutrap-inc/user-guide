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

## Docs Platform Migration (SITE)

> Added 2026-07-07. GitBook announced ~8× pricing; renewal is
> **2026-07-25** — the migration must be live and GitBook cancelled
> before that date.
> `docs.ocutrap.com` moves to the self-hosted `docs-site/` Next.js app
> already scaffolded in this repo. The current GitBook look is the design
> target — customers should not notice the platform change, except that
> AI search keeps working.

- [ ] **SITE-01**: Serve the full knowledge base from the `docs-site/`
  Next.js app, rendering the existing GitBook-flavored markdown in place
  (`SUMMARY.md` navigation, `{% hint %}` blocks, `{% content-ref %}` /
  card tables) with visual parity to the current GitBook theme at
  `docs.ocutrap.com`. Markdown files remain the single source of truth —
  no content forking.
- [ ] **SITE-02**: URL parity — every currently-published
  `docs.ocutrap.com` path resolves to the same content (same slug or 301
  redirect), with `sitemap.xml` and per-page title/description meta
  preserved so search rankings survive the cutover.
- [ ] **SITE-03**: Full-text search across all pages with a keyboard
  shortcut (`/` or `Cmd+K`). The existing client-side Fuse.js index in
  `docs-site/` is an acceptable implementation.
- [ ] **SITE-04**: AI search for users, replacing GitBook AI search:
  a customer can ask a natural-language question and get an answer
  grounded only in knowledge-base content, with linked citations to the
  source pages. No per-seat or per-page vendor pricing — build on our
  existing Convex + Claude API stack (or a comparable flat-cost service),
  with rate limiting and prompt-injection-resistant grounding.
- [ ] **SITE-05**: Publishing pipeline — merge to `main` auto-deploys the
  site (Vercel, matching `console`). The PDF pipeline
  (`build_kb_pdf.py` + CI) is unaffected; the AI search index rebuilds on
  deploy so answers never lag published content.
- [ ] **SITE-06**: Cutover — point `docs.ocutrap.com` DNS at the new
  host, verify SITE-01..05 in production, cancel the GitBook plan before
  the **2026-07-25** renewal, and document a rollback path (GitBook stays
  readable until cancellation).

## Docs Site Enhancements (SITE, continued)

> Added 2026-07-07 after the migration buildout. Post-launch improvements to
> the self-hosted docs site, sequenced: SITE-07 first (it tells us what else
> is worth building), then SITE-08/09 (small), then SITE-10/11 (bigger swings,
> after the SITE-06 cutover).

- [ ] **SITE-07**: Docs analytics + feedback loop. PostHog (existing OcuTrap
  workspace) captures: pageviews, full-text search queries with result
  counts (zero-result queries especially), AI-ask questions with outcome
  (answered / declined / rate-limited / error), and a per-page
  "Was this helpful? 👍👎" widget (vote + page path). No PII beyond
  PostHog defaults; key via env. Output: a PostHog dashboard showing
  top zero-result searches, top asked questions, and lowest-rated pages —
  the content-gap queue.
- [ ] **SITE-08**: Live system-status indicator. Fetch the public
  Statuspage API (`ocutrap.statuspage.io/api/v2/status.json`) and render a
  live status pill (● operational / degraded / outage) on the home
  "System status" card and troubleshooting pages. Cached/edge-friendly,
  graceful fallback to the plain bookmark card if unreachable.
- [ ] **SITE-09**: AI-consumable docs. Build-generated `/llms.txt` (page
  index per the llms.txt convention) and `/llms-full.txt` (full markdown
  corpus), plus a per-page "Copy page as Markdown" button beside the print
  icon. Source from the existing content pipeline; rebuilt every deploy.
- [ ] **SITE-10**: Interactive LED diagnostic wizard. On the LED guide /
  troubleshooting flow: pick the LED color → pick the pattern → get the
  diagnosis and linked fix pages. Content derived from the LED guide
  markdown (single source of truth — no forked copy); works on mobile;
  usable offline once SITE-11 lands. After cutover.
- [ ] **SITE-11**: Offline docs (PWA). Service worker + manifest caching
  the KB pages, LED guide, and assets needed in the field; offline
  indicator banner; `/api/*` excluded. Verified in airplane mode on a
  phone. Rationale: customers operate traps in low-coverage areas.
  After cutover.

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
| SITE-01 | Docs Platform Migration        |
| SITE-02 | Docs Platform Migration        |
| SITE-03 | Docs Platform Migration        |
| SITE-04 | Docs Platform Migration        |
| SITE-05 | Docs Platform Migration        |
| SITE-06 | Docs Platform Migration        |
| SITE-07 | Docs Enhancements (post-launch)|
| SITE-08 | Docs Enhancements (post-launch)|
| SITE-09 | Docs Enhancements (post-launch)|
| SITE-10 | Docs Enhancements (post-cutover)|
| SITE-11 | Docs Enhancements (post-cutover)|
