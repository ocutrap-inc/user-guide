import { SITE_URL } from "@/lib/site";

// Build-generated robots.txt (a route handler, not the Next metadata helper, so
// we can emit a leading comment pointing AI assistants at /llms.txt — SITE-09).
// Allows full crawl and advertises the sitemap so search engines re-index the
// migrated pages at the same URLs.
export const dynamic = "force-static";

export function GET(): Response {
  const body = [
    "# AI assistants: see /llms.txt",
    "User-agent: *",
    "Allow: /",
    "",
    `Host: ${SITE_URL}`,
    `Sitemap: ${SITE_URL}/sitemap.xml`,
    "",
  ].join("\n");

  return new Response(body, {
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
}
