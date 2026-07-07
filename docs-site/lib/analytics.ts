// Client-side product analytics for the docs site (SITE-07 / SW-330).
//
// PostHog is the "sensor" that turns docs usage into a content-gap signal:
// pageviews, search queries (esp. zero-result), AI-ask outcomes, and per-page
// "was this helpful?" votes. No PII beyond PostHog defaults; autocapture and
// session recording are off. Everything here no-ops cleanly when the key is
// an empty string so the site still builds/runs without analytics configured.

import posthog from "posthog-js";

// OcuTrap workspace publishable (client) token — safe to commit; this key can
// only *write* events, not read data. An env override wins when present.
const DEFAULT_KEY = "phc_n7JwWoHYFJdkiJgcs7PBxSgCqc4BQjE7WW3vSA8aZpkb";

export const POSTHOG_KEY =
  process.env.NEXT_PUBLIC_POSTHOG_KEY ?? DEFAULT_KEY;
const POSTHOG_HOST = "https://us.i.posthog.com";

let started = false;

/** Initialize PostHog once, client-side. No-ops if the key is empty. */
export function initAnalytics(): void {
  if (started) return;
  if (typeof window === "undefined") return;
  if (!POSTHOG_KEY) return; // empty key → analytics disabled, cleanly
  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    // App Router: we send $pageview / $pageleave ourselves on route changes.
    capture_pageview: false,
    capture_pageleave: true,
    autocapture: false,
    disable_session_recording: true,
    // Keep the person graph minimal — no PII beyond PostHog defaults.
    person_profiles: "identified_only",
  });
  started = true;
}

export function analyticsEnabled(): boolean {
  return started;
}

/** Fire a custom event. No-ops until PostHog has been initialized. */
export function capture(
  event: string,
  properties?: Record<string, unknown>
): void {
  if (!started) return;
  posthog.capture(event, properties);
}

/** Send a manual $pageview for the current route (App Router). */
export function capturePageview(url: string): void {
  if (!started) return;
  posthog.capture("$pageview", { $current_url: url });
}
