import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

// Build-generated robots.txt. Allow full crawl and advertise the sitemap so
// search engines re-index the migrated pages at the same URLs.
export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
    },
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
