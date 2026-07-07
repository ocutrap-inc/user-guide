import type { MetadataRoute } from "next";
import { parseSummary, flattenNav } from "@/lib/docs";
import { absoluteUrl } from "@/lib/site";

// Build-generated sitemap.xml. URLs are derived from SUMMARY.md (the single
// source of truth for the docs navigation) so the published inventory always
// matches what the site actually serves — preserving the GitBook URL set that
// search engines already indexed.
export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const sections = parseSummary();
  const items = flattenNav(sections);
  const now = new Date();

  // Home ("/") plus every nav entry. flattenNav already excludes nothing,
  // so we dedupe via a Set (README parents resolve to their section href).
  const hrefs = new Set<string>(["/"]);
  for (const item of items) hrefs.add(item.href);

  return Array.from(hrefs).map((href) => ({
    url: absoluteUrl(href),
    lastModified: now,
    changeFrequency: "weekly",
    priority: href === "/" ? 1 : 0.7,
  }));
}
