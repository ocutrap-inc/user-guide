import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow images from any source in the docs
  images: {
    unoptimized: true,
  },
  // Transpile nothing extra needed
  output: undefined,

  // URL parity with the old GitBook site (SW-299 / spec SITE-02).
  // GitBook serves canonical, non-trailing-slash URLs (e.g.
  // /getting-started/introduction). Next.js' default is also
  // trailingSlash: false — a request to /foo/ 308-redirects to /foo — but we
  // set it explicitly so the contract survives future config edits.
  trailingSlash: false,

  // 301 redirects for any legacy GitBook URL whose slug does NOT match a
  // current app route. The full live GitBook sitemap (sitemap-pages.xml, 92
  // URLs) was diffed against the SUMMARY.md-derived routes and matched 1:1,
  // so no redirects are required today (see docs-site/seo-parity-report.md).
  // Add { source, destination, permanent: true } entries here if a slug is
  // ever renamed so customer bookmarks and search results keep resolving.
  async redirects() {
    return [];
  },
};

export default nextConfig;
