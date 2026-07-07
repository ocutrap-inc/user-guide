"use client";

// Initializes PostHog on the client and emits a manual $pageview on every
// App Router navigation (Next has no per-route callback, so we wire it via
// the pathname). Renders nothing. See lib/analytics.ts (SITE-07 / SW-330).

import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { initAnalytics, capturePageview } from "@/lib/analytics";

export default function PostHogProvider() {
  const pathname = usePathname();

  useEffect(() => {
    initAnalytics();
  }, []);

  useEffect(() => {
    if (!pathname) return;
    // Absolute URL keeps PostHog's path/host breakdowns accurate. We omit the
    // query string on purpose — docs routes are static and carry no PII.
    capturePageview(window.location.origin + pathname);
  }, [pathname]);

  return null;
}
