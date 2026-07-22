import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow images from any source in the docs
  images: {
    unoptimized: true,
  },
  // Transpile nothing extra needed
  output: undefined,

  // Ensure the OG route's raccoon mark is bundled into its serverless function
  // (it is read from disk via fs at request time — SITE-01).
  outputFileTracingIncludes: {
    "/api/og": ["./public/ocutrap-mark.png"],
  },

  // URL parity with the old GitBook site (SW-299 / spec SITE-02).
  // GitBook serves canonical, non-trailing-slash URLs (e.g.
  // /getting-started/introduction). Next.js' default is also
  // trailingSlash: false — a request to /foo/ 308-redirects to /foo — but we
  // set it explicitly so the contract survives future config edits.
  trailingSlash: false,

  // 301 redirects for any legacy GitBook URL whose slug does NOT match a
  // current app route. The full live GitBook sitemap (sitemap-pages.xml, 92
  // URLs) was diffed against the SUMMARY.md-derived routes and matched 1:1.
  // Add { source, destination, permanent: true } entries here when a slug is
  // renamed so customer bookmarks and search results keep resolving.
  async redirects() {
    return [
      // Bug reporting page renamed support-1 → bug-reporting (SW-341).
      {
        source: "/support/support-1",
        destination: "/support/bug-reporting",
        permanent: true,
      },
      // LED pages consolidated to getting-started/led-guide (SW-575 / DOC-11).
      {
        source: "/troubleshooting/led-light-guide",
        destination: "/getting-started/led-guide",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
