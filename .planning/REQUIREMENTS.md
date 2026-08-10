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
  (no LFS) so docs-site and the PDF build read them from the repo.
  (Originally a GitBook-sync constraint; GitBook retired 2026-07-10.)
- [ ] **DOC-04**: Update GitBook markdown so firmware-gated behavior matches
  what current firmware actually does (covering the AUD-02 checklist).
- [x] **DOC-05** (SW-355): Rewrite the trap delete/transfer lifecycle pages to
  the shipped React app. `deleting-a-trap.md` describes the real flow (trap →
  Settings tab → Danger zone → Remove trap → confirm dialog; owner-only; web
  only) and the cancel-subscription-first requirement enforced by the app
  (SW-475 / app PR #273 — publish after it deploys). No auto-cancel, no
  confirmation email (both were Bubble-era). `selling-or-transferring-a-trap.md`
  leads with the explicit order — cancel subscription → remove trap → new
  owner adds + subscribes — and states that images/history are deleted, not
  transferred. Both pages cross-link each other, managing-your-subscription,
  adding-a-trap, and support (for the "Device ID already registered" dead end,
  SW-476). Nav: "Deleting a Trap" moves from the orphan `***` block into
  `## Device Management` beside the transfer page (drift item justifying the
  TOC exception; URL slug unchanged). Root and `docs-site/content/` copies stay
  byte-identical.
- [x] **DOC-06** (SW-479 / SW-476): Sync two customer-visible app changes.
  Scout-mode notifications (SW-479 / app PR #288, ADR 0003 Amendment 1): Scout
  Alert / Scout Trigger events are now recorded in the trap's activity feed
  only — they never send push or email, never appear in the Inbox, and never
  affect the notification-bell count (outdoor-temperature/weather alerts are
  unaffected). Patched `getting-started/app/scouting-mode.md` (Scouting vs.
  Armed table, What-to-expect bullets, 5-minute cadence reframed as feed
  cadence, troubleshooting item) and `getting-started/app/notification-settings.md`
  (In-app channel exception, Mobile Device-alerts scope, closing note).
  Second-hand trap claim (SW-476 / app PR #290): the Add flow now self-serve
  transfers a parked unit when the entered Trap ID matches the Device ID pair
  printed on the unit; added a "Buying a trap second-hand" section to
  `device-management/selling-or-transferring-a-trap.md` and replaced the
  outdated "contact us to release the device" hint. Aggregate
  `OcuTrap_Knowledge_Base_Complete.md` synced (scout glossary + Recent Updates +
  transfer note). Root and `docs-site/content/` copies byte-identical; KB PDF
  regenerated. Publishes only when app PRs #288 and #290 deploy.
- [x] **DOC-07** (SW-517): Add a customer-facing billing-continuity page for the
  cutover to the new app, backed by CUT-04 in
  `internal-docs/specs/2026-07-bubble-app-cutover.md` (billing transfers) and its
  §5 billing invariants. New page
  `account-and-billing/billing-when-you-move-to-the-new-app.md` states only what
  CUT-04 establishes: the trap's existing Stripe subscription continues
  uninterrupted (same customer, same payment method, same price, same renewal
  date), no new checkout, no second subscription, no lapse. Claiming repoints
  `subscriptions.userId` only; Stripe-side objects are never touched (spec §2
  CUT-D5), so invoice history and the billing account survive the move. Leads
  customers to the §5 invariant "zero new checkouts from migrated customers" as
  an actionable instruction: if the app prompts a checkout for an already-paid
  trap, stop and contact support rather than starting a second subscription
  (the app-side guard for this is SW-148 / app PR #307). Deliberately omits any
  refund promise, any absolute "cannot be double-charged" guarantee, and any
  bank-dispute instruction: the spec establishes none of the three. No dates
  (CUT-D4 dates are gate-conditioned); the retire date is deferred to the
  customer's email. Nav under `## Account and Billing`; cross-linked from
  `subscription-overview.md`. Root and `docs-site/content/` copies
  byte-identical; KB PDF regenerated. Publishes with the cutover comms.
- [ ] **DOC-08** (SW-536): Publish a sign-in troubleshooting page,
  `troubleshooting/cant-sign-in.md` ("Can't Sign In to Your Account"), shaped
  as one section per failure mode: forgot password, reset code didn't arrive,
  sign-in errors, lost email access, coming from the old app
  (base.ocutrap.com), escalation to support. Password path ONLY — no Magic
  Auth, SSO, or 2FA (those buttons render for nobody on the logged-out page,
  SW-535) and no invented policy (we have no 2FA and no inactive-account
  purge). Every UI label matches the shipped auth code (SignInForm /
  ForgotPassword / ResetPassword). Cross-links: resetting-password,
  password-policy-for-users, account-deletion, support. Nav: new bullet at the
  end of `## Troubleshooting` in SUMMARY.md. Root and `docs-site/content/`
  copies stay byte-identical; KB PDF regenerated. Ships docs-first, paired
  with the app login-page help link (REQ-AUTH-HELP-01, app repo).
- [x] **DOC-09** (FW-305): Document the new firmware motor-direction setting,
  Actuator Inverse. It reverses the door motor drive direction for traps built
  with reversed motor wiring, where the door drives open when it should close;
  firmware corrects it with no hardware rework. Bool, default Off, set by
  OcuTrap support (not exposed to customers in the current app UI). Added a row
  to the "Hardware & Feedback Settings" table in
  `getting-started/app/trap-settings/settings-reference.md` (directly after
  Enhanced Door Closing), a matching row to the settings table in
  `OcuTrap_Knowledge_Base_Complete.md`, and an `### Actuator Inverse`
  subsection under `## Trap Settings` (after Enhanced Door Closing). Copy stays
  telegraphic: turn it On if your motor is going the wrong way (support-copy dropped 07-21 per Graham).
  KB PDF regenerated. `more-settings-overview.md` / `advanced-settings.md` left
  untouched (they document the current app UI, which does not surface this
  setting).
- [x] **DOC-10** (SW-574 / user-guide#93): Publish a mobile-app reset page,
  `troubleshooting/resetting-the-mobile-app.md` ("Resetting the Mobile App"),
  with iOS and Android steps for force-quit, optional Android cache clear,
  delete + reinstall, and post-reinstall sign-in / notification permissions.
  Clarify that traps, images, and subscription stay on the account (cloud).
  Cross-links: using-the-mobile-app, notification-settings, cant-sign-in,
  support. Nav: new bullet at the end of `## Troubleshooting` in SUMMARY.md.
  Root and `docs-site/content/` copies stay byte-identical; KB PDF
  regenerated. exit-impact: ops. Merged 2026-07-21.
- [x] **DOC-11** (SW-575): High-ROI docs simplify from the 2026-07-21 audit —
  LED consolidation + dual Trap Settings nav labels + Getting Started regroup.
  Does **not** include FAQ triage, billing/password stub removal, thin-page
  merges, or marketing appendix drops (deferred; account-deletion docs left
  alone for SW-570 / user-guide#90). Acceptance checklist:
  - [x] Canonical LED page remains `getting-started/led-guide.md` (interactive
    diagnostic + reference table; FW-218 SCOUT row still lands here later).
  - [x] `troubleshooting/led-light-guide.md` is a stub pointing at the
    canonical LED Guide; `docs-site/next.config.ts` 301-redirects
    `/troubleshooting/led-light-guide` → `/getting-started/led-guide`;
    removed from Troubleshooting nav; `common-issues.md` links to led-guide.
  - [x] `getting-started/app/led-modes.md` no longer claims rapid red =
    SOS/system error (conflicts with power-down); retitled LED Pattern
    Animations, keeps connection GIFs, defers red/no-light to led-guide;
    nested under LED Guide in SUMMARY (not under App).
  - [x] Dual Trap Settings trees have distinct sidebar labels: **Settings in
    the App** (`getting-started/app/trap-settings/`) vs **Door & Capture
    Features** (`getting-started/trap-settings/`); H1s match; feature hub
    cross-links the app settings hub.
  - [x] Getting Started SUMMARY regrouped under Setup · Daily use ·
    Reference · Care hub pages (`setup.md`, `daily-use.md`, `reference.md`,
    `care.md`) without moving billing/password stubs or dropping appendix.
  - [x] Root and `docs-site/content/` twins byte-identical for every touched
    markdown page + SUMMARY. exit-impact: ops.
- [x] **DOC-12** (SW-575 follow-on): FAQ triage + billing/password nav unify.
  Deferred from DOC-11 so SW-570 / user-guide#90 could stay isolated.
  Acceptance checklist:
  - [x] `faqs/common-questions.md` cut from ~79 marketing FAQs to ~17 ops
    FAQs; stale “does not require a subscription” answers corrected to match
    `account-and-billing/subscription-overview.md`; deep how-tos link out.
  - [x] Billing + Resetting Password removed from App nav in SUMMARY; stubs
    remain as move notices; `docs-site/next.config.ts` 301-redirects
    `/getting-started/app/billing` → subscription-overview and
    `/getting-started/app/resetting-password` → account resetting-password.
  - [x] Root and `docs-site/content/` twins byte-identical for touched pages +
    SUMMARY. exit-impact: ops.
- [x] **DOC-13** (SW-575 leftover): thin-page merges + marketing appendix drop.
  Acceptance checklist:
  - [x] Motor connector video folded into
    `troubleshooting/motor-connector-tightness-check.md`;
    `motor-connector-use.md` is a stub; 301 redirect; removed from nav.
  - [x] Camera FAQ trio consolidated into `faqs/manually-taking-an-image.md`
    (retitled Requesting photos); seeing-camera-view +
    taking-higher-quality-images are stubs with 301s; nav has one entry.
  - [x] Appendix nav keeps Downloads + Updates only; media kit /
    testimonials / case study / news removed from SUMMARY with 301s to
    ocutrap.com; source files remain (pdf-exclude already).
  - [x] Root and `docs-site/content/` twins byte-identical for touched pages +
    SUMMARY. exit-impact: ops.
- [x] **DOC-14**: Document the fast-blinking-blue LED as a cellular-network
  join failure. Support was fielding this pattern with no page to point at,
  and the guide only covered blue as "door open" (solid) and "opening the
  door" (blinking after a command). Acceptance checklist:
  - [x] `led-diagnostics` entry in `getting-started/led-guide.md`:
    `blue` / `fast-blink`, context "idle, not after a command", meaning =
    cannot join the cellular network and keeps retrying, action = move to
    better coverage, wait 10 minutes, then contact support with the Trap ID.
    Links to trap-offline, connectivity-and-coverage, support. The wizard and
    the on-page reference table both pick it up from this one entry.
  - [x] Row added to the Step 3 LED table in
    `troubleshooting/trap-offline-or-wont-connect.md`, plus a warning hint in
    Step 4 (Check Cellular Coverage) naming it as the escalate-to-support
    signal rather than a field-fixable one.
  - [x] Row added to the System Status LEDs table in
    `OcuTrap_Knowledge_Base_Complete.md` (hand-maintained; feeds the KB PDF).
  - [x] Root and `docs-site/content/` twins byte-identical for all three
    touched pages. exit-impact: ops.
- [ ] **DOC-17**: Give the on-trap buttons their own page. The button
  sequences were scattered across a shortcut table in
  `getting-started/tips-and-tricks.md` and a partial how-to in
  `getting-started/led-guide.md`, so a customer standing at a trap with no
  signal had nowhere to be sent. Acceptance checklist:
  - [ ] New page `getting-started/using-the-trap-buttons.md` covers status
    check, door open/close hold sequence, arm (including the three refusal
    LED patterns), unarm, power off/on, and a "no signal, buttons still
    work" section. No em dashes; no internal hardware brand names.
  - [ ] `SUMMARY.md` lists it under **Daily use** immediately after the
    **App** block and before **Tips and Tricks**, at the same 2-space level.
    It therefore also enters the SUMMARY-driven KB PDF assembly.
  - [ ] Cross-links added from `getting-started/app/arm-un-arm-button.md`
    (info hint), `getting-started/app/after-capture.md` (On-trap buttons
    section), `getting-started/handling-a-captured-animal.md` (release
    section hint), `getting-started/hardware-features.md` (Manual control
    bullet), `getting-started/tips-and-tricks.md` (Button Shortcuts), and
    `getting-started/led-guide.md` (User Button Interactions).
  - [ ] Page summarized in `OcuTrap_Knowledge_Base_Complete.md`
    (hand-maintained) at the matching SUMMARY position.
  - [ ] Root and `docs-site/content/` twins byte-identical for the new page,
    every touched page, and `SUMMARY.md`. exit-impact: ops.
- [ ] **DOC-18**: Weak-cellular-signal troubleshooting page plus
  multi-network connectivity copy. Support had no page describing what
  actually helps in marginal coverage, and repeated power cycling was making
  network searches worse. Acceptance checklist:
  - [ ] New page `troubleshooting/improving-a-weak-cellular-signal.md`
    explains multi-network 4G LTE selection, what weak signal looks like, the
    ordered field ladder (antenna, move, raise, one power cycle, wait an
    hour, then support), and trapping while disconnected.
  - [ ] `SUMMARY.md` lists it in **Troubleshooting** immediately after
    **Trap Offline or Won't Connect**.
  - [ ] `getting-started/connectivity-and-coverage.md` gains a short
    multi-network paragraph pointing at the new page;
    `troubleshooting/trap-offline-or-wont-connect.md` Step 4 (Check Cellular
    Coverage) links to it.
  - [ ] `faqs/safe-mode.md` brand fix: "the Particle module inside the POD"
    becomes "the cellular module inside the POD".
  - [ ] Page summarized in `OcuTrap_Knowledge_Base_Complete.md`
    (hand-maintained) at the matching SUMMARY position.
  - [ ] Root and `docs-site/content/` twins byte-identical for the new page,
    every touched page, and `SUMMARY.md`. exit-impact: ops.

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
> **Status 2026-07-10: COMPLETE — docs.ocutrap.com serves the Vercel
> docs-site and the GitBook plan is cancelled (SITE-06 done, SW-297
> closed). Rollback is redeploy-only: `docs-site/CUTOVER-ROLLBACK.md`.**
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
  After cutover. Acceptance (SW-334): (a) `app/manifest.ts` serves an
  installable web manifest (name/short_name, `start_url`, `display:
  standalone`, 192 + 512 icons from the existing raccoon mark, brand-navy
  `theme_color`); Lighthouse installability passes. (b) A build-generated
  service worker (`scripts/generate-sw.mjs` → `public/sw.js`, run in
  pre(dev|build)) precaches the app shell + every KB route + critical
  images (LED status GIFs especially), with the route/asset list derived
  from the content itself (SUMMARY.md + markdown image refs) — no
  hardcoded lists that drift. (c) Repeat visits are stale-while-revalidate;
  content-hashed `/_next/static/*` is cache-first. (d) Cache names are
  keyed by a per-deploy build id (Vercel commit SHA, else a content hash);
  `activate` deletes every older cache so a stale docs cache can't persist.
  (e) `/api/*` is network-only EXCEPT `/api/search` (precached so full-text
  search works offline); videos are network-only with the poster falling
  through the image path; the AI ask shows a friendly "needs connection"
  state offline. (f) A slim "Offline — showing saved docs" banner renders
  while the browser is offline; an `/offline` fallback route is precached.
  (g) Real-phone airplane-mode validation is the remaining manual step
  (checklist in the SW-334 PR).
- [ ] **SITE-12**: Brand alignment + visual polish. The site shipped on a
  generic bright SaaS blue (`#0050ff`) and Outfit/Manrope type — both
  off-brand per `internal-docs/orchestrator/brand/index.md` ("Don't:
  generic bright SaaS blue"; docs typography follows web marketing).
  Acceptance: (a) primary/accent/link colors derive from brand navy
  `#1f3c6b` (light) and `#6291d4` (dark — the documented
  `app_web.primary_dark`; the previous dark accent `#5a8dff` claimed to
  match that token but didn't); (b) headings Work Sans, body Inter, mono
  JetBrains Mono per brand §4; (c) neutrals are the brand's warm stone
  ramp, not blue-gray; (d) semantic hint/status colors unchanged;
  (e) visible `:focus-visible` ring on interactive elements; (f) mobile
  article top bar doesn't crowd breadcrumbs into the action buttons;
  (g) verified by screenshot on desktop (~1440px) and mobile (390px) in
  light + dark themes with no regressions to search, sidebar, TOC,
  hints, cards, tables, or print styles.
- [ ] **SITE-13**: Unique per-page meta descriptions. A Semrush audit
  (2026-08-02) found 27 duplicate meta descriptions: pages with no
  `description:` frontmatter fall back to `<Section> — OcuTrap Knowledge
  Base`, so every page in a section shares one string. Acceptance: every
  published KB page (each `.md` referenced from `SUMMARY.md`) carries a
  unique `description:` frontmatter block, read by `docs-site/lib/docs.ts`
  and used for both the meta description tag and the visible page subtitle
  under the H1; no page falls back to the section-level default.
  Descriptions summarize what the page actually says (no invented features
  or numbers), 80–155 characters, no em dashes, varied openings — they are
  customer-visible copy, not keyword filler. External links point at the
  apex `https://ocutrap.com`, never the `www.` host (which 301-redirects),
  and link anchor text is descriptive rather than a raw URL. Root and
  `docs-site/content/` copies stay byte-identical. exit-impact: ops.

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
| DOC-05  | Post-launch drift (SW-355)     |
| DOC-06  | Post-launch drift (SW-479/476)  |
| DOC-07  | Cutover comms (SW-517)         |
| DOC-08  | Post-launch drift (SW-536)     |
| DOC-09  | Post-launch drift (FW-305)     |
| DOC-10  | Post-launch drift (mobile reset) |
| DOC-11  | Docs simplify / nav cleanup (SW-575) |
| DOC-12  | FAQ triage + billing/password nav (SW-575) |
| DOC-13  | Thin-page merges + appendix drop (SW-575) |
| DOC-17  | On-trap buttons page + cross-links |
| DOC-18  | Weak cellular signal page + multi-network copy |
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
| SITE-12 | Docs Enhancements (post-launch)|
| SITE-13 | Docs Enhancements (post-launch)|
