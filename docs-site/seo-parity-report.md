# SEO / URL Parity Report — GitBook → Next.js docs-site

**Spec:** SITE-02 · **Linear:** SW-299 · **exit-impact:** ops
**Generated:** 2026-07-07
**Live GitBook source:** `https://docs.ocutrap.com/sitemap.xml` → `https://docs.ocutrap.com/sitemap-pages.xml` (reachable from this environment; **92 URLs**)
**New app under test:** `docs-site/` built with `npm run build` and served via `npx next start` (99 static routes)

## Summary

| Metric | Count |
|---|---|
| Live GitBook URLs (from `sitemap-pages.xml`) | **92** |
| Resolve on new app at the **same path** (HTTP 200) | **92** |
| Mapped via **301 redirect** | **0** |
| **Missing / 404** | **0** |

**Result: full parity.** Every published GitBook URL resolves to the identical
path on the new app with a 200. Zero redirects were required because
`docs-site` derives its routes from the same `SUMMARY.md` that GitBook
publishes, and `lib/docs.ts#filePathToHref` reproduces GitBook's slug rules
(strip `.md`, collapse `/README`). Diff of the 92-URL GitBook inventory against
the 92 SUMMARY-derived routes was empty in both directions.

## Verification method

1. Fetched the live GitBook sitemap index (`sitemap.xml`) → single child
   `sitemap-pages.xml` (GitBook serves one), yielding 92 `<loc>` URLs.
2. Derived the new app's route set from `SUMMARY.md` via the same
   `filePathToHref` transform → 92 routes. `comm` diff = 0 differences.
3. Built the app (`npm run build`, clean) and served it with `npx next start`,
   then requested every one of the 92 GitBook paths — all returned **200**.
4. **Trailing slash:** GitBook serves canonical **non-trailing-slash** URLs.
   The app matches: `/getting-started/introduction` → **200**,
   `/getting-started/introduction/` → **308** redirect to the non-slash form
   (Next.js default, pinned via `trailingSlash: false` in `next.config.ts`).
5. **Canonical + Open Graph:** confirmed rendered in page `<head>`, e.g.
   `/getting-started/introduction` emits
   `<link rel="canonical" href="https://docs.ocutrap.com/getting-started/introduction">`
   plus `og:title` / `og:description` / `og:url` / `og:type=article`, and the
   home page emits the origin canonical `https://docs.ocutrap.com`.

## Per-URL results

Every row below was verified live against the running build.

| Live GitBook URL | New app path | HTTP | Status |
|---|---|---|---|
| https://docs.ocutrap.com | `/` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/account-deletion | `/account-and-billing/account-deletion` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/billing | `/account-and-billing/billing` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/billing/changing-your-subscription-payment-method | `/account-and-billing/billing/changing-your-subscription-payment-method` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/managing-your-subscription | `/account-and-billing/managing-your-subscription` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/resetting-password | `/account-and-billing/resetting-password` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/subscription-overview | `/account-and-billing/subscription-overview` | 200 | same-path 200 |
| https://docs.ocutrap.com/account-and-billing/update-individual-trap-subscriptions | `/account-and-billing/update-individual-trap-subscriptions` | 200 | same-path 200 |
| https://docs.ocutrap.com/appendix-and-resources/case-study | `/appendix-and-resources/case-study` | 200 | same-path 200 |
| https://docs.ocutrap.com/appendix-and-resources/downloads | `/appendix-and-resources/downloads` | 200 | same-path 200 |
| https://docs.ocutrap.com/appendix-and-resources/media-kit | `/appendix-and-resources/media-kit` | 200 | same-path 200 |
| https://docs.ocutrap.com/appendix-and-resources/ocutrap-in-news | `/appendix-and-resources/ocutrap-in-news` | 200 | same-path 200 |
| https://docs.ocutrap.com/appendix-and-resources/testimonials | `/appendix-and-resources/testimonials` | 200 | same-path 200 |
| https://docs.ocutrap.com/appendix-and-resources/updates | `/appendix-and-resources/updates` | 200 | same-path 200 |
| https://docs.ocutrap.com/deleting-a-trap | `/deleting-a-trap` | 200 | same-path 200 |
| https://docs.ocutrap.com/device-management/selling-or-transferring-a-trap | `/device-management/selling-or-transferring-a-trap` | 200 | same-path 200 |
| https://docs.ocutrap.com/device-management/trap-test-mode | `/device-management/trap-test-mode` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/accessory-button-port | `/faqs/accessory-button-port` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/battery | `/faqs/battery` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/camera | `/faqs/camera` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/cold-weather | `/faqs/cold-weather` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/common-questions | `/faqs/common-questions` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/gps | `/faqs/gps` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/manually-taking-an-image | `/faqs/manually-taking-an-image` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/miscellaneous | `/faqs/miscellaneous` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/miscellaneous/password-policy-for-users | `/faqs/miscellaneous/password-policy-for-users` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/power-modes | `/faqs/power-modes` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/safe-mode | `/faqs/safe-mode` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/seeing-camera-view | `/faqs/seeing-camera-view` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/sharing-traps | `/faqs/sharing-traps` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/sharing-traps/user-levels | `/faqs/sharing-traps/user-levels` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/taking-higher-quality-images | `/faqs/taking-higher-quality-images` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/target-animals | `/faqs/target-animals` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/updating-firmware | `/faqs/updating-firmware` | 200 | same-path 200 |
| https://docs.ocutrap.com/faqs/weather-and-environmental-guidelines | `/faqs/weather-and-environmental-guidelines` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app | `/getting-started/app` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/adding-a-trap-to-your-account | `/getting-started/app/adding-a-trap-to-your-account` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/after-capture | `/getting-started/app/after-capture` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/arm-un-arm-button | `/getting-started/app/arm-un-arm-button` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/billing | `/getting-started/app/billing` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/deleting-an-image | `/getting-started/app/deleting-an-image` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/image-cadence | `/getting-started/app/image-cadence` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/image-recognition | `/getting-started/app/image-recognition` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/interface-views | `/getting-started/app/interface-views` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/led-modes | `/getting-started/app/led-modes` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/logs | `/getting-started/app/logs` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/notification-settings | `/getting-started/app/notification-settings` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/open-closed-button | `/getting-started/app/open-closed-button` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/other-app-information | `/getting-started/app/other-app-information` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/resetting-password | `/getting-started/app/resetting-password` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/scouting-mode | `/getting-started/app/scouting-mode` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/trap-control | `/getting-started/app/trap-control` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/trap-settings | `/getting-started/app/trap-settings` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/trap-settings/advanced-settings | `/getting-started/app/trap-settings/advanced-settings` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/trap-settings/more-settings-overview | `/getting-started/app/trap-settings/more-settings-overview` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/trap-settings/settings-reference | `/getting-started/app/trap-settings/settings-reference` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/app/using-the-mobile-app | `/getting-started/app/using-the-mobile-app` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/battery-overview | `/getting-started/battery-overview` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/connectivity-and-coverage | `/getting-started/connectivity-and-coverage` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/deploying-in-the-field | `/getting-started/deploying-in-the-field` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/handling-a-captured-animal | `/getting-started/handling-a-captured-animal` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/hardware-features | `/getting-started/hardware-features` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/introduction | `/getting-started/introduction` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/led-guide | `/getting-started/led-guide` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/maintenance | `/getting-started/maintenance` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/set-up-tutorial | `/getting-started/set-up-tutorial` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/setting-up | `/getting-started/setting-up` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/technical-specifications | `/getting-started/technical-specifications` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/tips-and-tricks | `/getting-started/tips-and-tricks` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/trap-settings | `/getting-started/trap-settings` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/trap-settings/distance-safety-and-alerts | `/getting-started/trap-settings/distance-safety-and-alerts` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/trap-settings/enhanced-door-closing | `/getting-started/trap-settings/enhanced-door-closing` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/trap-settings/pre-capture-notification | `/getting-started/trap-settings/pre-capture-notification` | 200 | same-path 200 |
| https://docs.ocutrap.com/getting-started/video-assembly | `/getting-started/video-assembly` | 200 | same-path 200 |
| https://docs.ocutrap.com/legal-and-compliance/data-and-privacy | `/legal-and-compliance/data-and-privacy` | 200 | same-path 200 |
| https://docs.ocutrap.com/legal-and-compliance/legal-disclaimers-and-compliance-information | `/legal-and-compliance/legal-disclaimers-and-compliance-information` | 200 | same-path 200 |
| https://docs.ocutrap.com/legal-and-compliance/responsible-and-legal-use | `/legal-and-compliance/responsible-and-legal-use` | 200 | same-path 200 |
| https://docs.ocutrap.com/legal-and-compliance/warranty-information | `/legal-and-compliance/warranty-information` | 200 | same-path 200 |
| https://docs.ocutrap.com/support/nonprofit-and-501-c-program | `/support/nonprofit-and-501-c-program` | 200 | same-path 200 |
| https://docs.ocutrap.com/support/purchases | `/support/purchases` | 200 | same-path 200 |
| https://docs.ocutrap.com/support/safety-information | `/support/safety-information` | 200 | same-path 200 |
| https://docs.ocutrap.com/support/support | `/support/support` | 200 | same-path 200 |
| https://docs.ocutrap.com/support/support-1 | `/support/support-1` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/common-issues | `/troubleshooting/common-issues` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/condensation-on-the-camera | `/troubleshooting/condensation-on-the-camera` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/led-light-guide | `/troubleshooting/led-light-guide` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/motor-connector-tightness-check | `/troubleshooting/motor-connector-tightness-check` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/motor-connector-use | `/troubleshooting/motor-connector-use` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/motor-to-pin-connection-too-tight | `/troubleshooting/motor-to-pin-connection-too-tight` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/trap-not-sending-commands | `/troubleshooting/trap-not-sending-commands` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/trap-offline-or-wont-connect | `/troubleshooting/trap-offline-or-wont-connect` | 200 | same-path 200 |
| https://docs.ocutrap.com/troubleshooting/wire-exposed | `/troubleshooting/wire-exposed` | 200 | same-path 200 |

## Notes for cutover (SITE-06)

- `sitemap.xml` and `robots.txt` are build-generated (`app/sitemap.ts`,
  `app/robots.ts`) and emit absolute URLs from `SITE_URL`
  (`lib/site.ts`, env-overridable via `NEXT_PUBLIC_SITE_URL`, default
  `https://docs.ocutrap.com`). The new sitemap carries the same 92 URLs.
- No 301 redirects are needed today. `next.config.ts#redirects()` is in place
  (currently empty) so any future slug rename can be mapped without a code
  restructure — add `{ source, destination, permanent: true }` entries there.
- This report was generated against the **live** GitBook sitemap, so it does
  not need a re-run for inventory. Re-verify the 200 checks once against the
  production Vercel deployment immediately before the DNS swap, since this run
  used a local `next start`.
