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
