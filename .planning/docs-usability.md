# Docs usability corrections

exit-impact: ops
spec: SITE-14, SITE-15, SITE-16, SITE-17, DOC-24

Based on the September 12–13 live-site review and public Mobbin references:
On iOS FAQ Page (6e6184a1-50fb-4536-9e07-3b5e70966a10) and Linear Web Initial
Help Window (e4f5c37e-834c-4996-b0b3-f10c40b7ca67).

Plan: correct full-text indexing and snippets; add accessible search/menu
dialogs; preserve article space with responsive TOC and scrollable tables;
promote homepage search/tasks; correct scouting copy and rebuild its PDF.

Validation: focused search/navigation regressions, existing AI/LED tests,
TypeScript and production build, source/content equality, PDF source check,
and browser checks at 1440, 1024, 390, and 320px with keyboard and themes.

Tracker route: ClickUp Internal Documentation (901318828640). No ClickUp
connector is available in this session; the native ClickUp app is signed out.
Tracker creation remains pending authenticated access; no task was fabricated.

Base: origin/main dc9d9b6. Isolated branch: fix/docs-usability.

Implemented SITE-14–17 and DOC-24. Added full-text search with relevant
snippets, first-result Enter behavior, loading/error recovery, native modal
focus/scroll management, 44px controls, responsive TOC and table regions,
homepage search/common tasks, and the corrected scouting event copy.
The generated content refresh also picks up the already-merged camera-status
copy from origin/main, restoring equality with its canonical markdown.

Validation completed:
- Search regression suite: four missing terms, typo, no match, legacy index,
  homepage Next → Setup. AI retrieval/streaming and LED matrix suites pass.
- TypeScript and production Next build pass (93 generated pages).
- Python: 25 passed, 1 existing optional integration test skipped.
- KB PDF regenerated: 214 pages, 16.2 MB; source hash matches. Rendered and
  visually reviewed homepage and scouting pages 7, 59, 60.
- Browser: 1440×1000 and 1024×900 desktop; 390×844 and 320×740 mobile;
  light/dark themes. Settings document width equals viewport at both mobile
  sizes; tables scroll within 358px/288px regions. At 1024px the article is
  692px wide and the inline TOC replaces the right rail.
- Keyboard: closed drawer skipped, native modal containment/scroll lock,
  visible Close/Escape restores trigger focus, mobile TOC closes and focuses
  its heading, table arrow-key scrolling, search Enter opens the first page.
  AI unavailable fallback and Back/Close checked; LED cyan/breathing diagnosis
  still works. PDF print rendering and table overflow print overrides checked.
- Added docs-site-checks CI for TypeScript and search/AI/LED regressions.

References:
- https://mobbin.com/explore/screens/6e6184a1-50fb-4536-9e07-3b5e70966a10
- https://mobbin.com/explore/screens/e4f5c37e-834c-4996-b0b3-f10c40b7ca67


## Compact context follow-up (SITE-18)

User screenshot: the Daily use breadcrumb repeats the site and page title,
wrapping above the H1. Replaced it with the section label for top-level pages
and one immediate-parent link for nested articles, derived from SUMMARY's
hierarchy. Removed the homepage's redundant label and aligned the action row.
No content or PDF source changed; existing tracker access limitation persists.

Validation: production build/typecheck pass; PDF source hash still matches.
Reviewed Daily use at 390px, Settings reference at 320px (44px row, no
horizontal overflow), and nested parent navigation at 1440px in both themes.
Parent links resolve to authored navigation parents, not URL-folder guesses.
