# docs.ocutrap.com cutover — rollback path (SITE-06 / SW-304)

`docs.ocutrap.com` was cut over from GitBook to this Vercel-hosted docs-site
on **2026-07-10** (Vercel project `ocutrap-docs`, team `grahampaticos-projects`).

## Phase 1 — GitBook plan still active (until cancellation)

Rollback is a **pure DNS revert**: the GitBook space is intact and still
serves the old content, so pointing `docs.ocutrap.com` back at GitBook
(re-add the custom domain in GitBook, remove it from the Vercel project)
fully restores the old site. No data restore needed.

## Phase 2 — after the GitBook plan is cancelled (**point of no return**)

The GitBook space (and its `files.gitbook.com` file storage) is gone.
Rollback then means **redeploy-only**:

- The site content is fully reproducible from this repo: markdown at the
  repo root, rendered by `docs-site/` (`npm run build`), deployed by Vercel
  on push to `main`.
- If the Vercel project is lost, re-import the repo as a new Next.js
  project — config gotchas are recorded in Linear SW-302 (Framework Preset
  must be **Next.js**; "Skip deployments when no changes to root dir" must
  be **OFF** because KB markdown lives at the repo root).
- The only assets NOT in git are the 9 tutorial videos, which were
  downloaded from GitBook before cancellation and now live in the
  `ocutrap-docs-media` Vercel Blob store (public). Originals are archived
  offline at `~/ocutrapinc/media-archive/user-guide-videos/` on Graham's
  machine — re-upload from there if the Blob store is ever lost
  (`vercel blob put <file> --pathname videos/<slug> --access public`).

## Pre-cancellation checklist

- [x] 92/92 GitBook-inventory URLs return 200 on docs.ocutrap.com (2026-07-10)
- [x] AI ask (`/api/ask`) live-verified with citations (2026-07-10)
- [x] sitemap/robots/canonical/OG all on docs.ocutrap.com (2026-07-10)
- [x] No content references `files.gitbook.com` (videos moved to Vercel Blob)
- [ ] GitBook plan cancelled, no auto-renew charge confirmed (Graham, before 07-25)
