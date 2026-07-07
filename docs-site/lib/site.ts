// Canonical public origin for the docs site.
// Env-overridable so preview/staging deployments can point elsewhere,
// but defaults to the production GitBook domain we are migrating onto so
// sitemap/canonical/OG URLs stay identical to the old GitBook site.
export const SITE_URL = (
  process.env.NEXT_PUBLIC_SITE_URL ?? "https://docs.ocutrap.com"
).replace(/\/+$/, "");

// Absolute URL for a site-relative href ("/" → origin, "/foo" → origin + "/foo").
export function absoluteUrl(href: string): string {
  if (!href || href === "/") return SITE_URL;
  return `${SITE_URL}${href.startsWith("/") ? href : `/${href}`}`;
}

export const SITE_NAME = "OcuTrap Knowledge Base";
// GitBook's site tagline — used verbatim for parity (SITE-01/SITE-02).
export const SITE_DESCRIPTION =
  "Set up, operate, and troubleshoot your OcuTrap smart trap.";

// Site-relative path to the dynamic OG card for a page (SITE-01). Passed to
// Next metadata `images`, which resolves it against `metadataBase` (SITE_URL)
// into the absolute URL crawlers require.
export function ogImagePath(title?: string, section?: string | null): string {
  const params = new URLSearchParams();
  if (title) params.set("title", title);
  if (section) params.set("section", section);
  const qs = params.toString();
  return `/api/og${qs ? `?${qs}` : ""}`;
}
