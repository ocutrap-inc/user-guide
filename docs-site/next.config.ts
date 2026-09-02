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
      // App-nav billing/password stubs → Account and Billing (SW-575 / DOC-12).
      {
        source: "/getting-started/app/billing",
        destination: "/account-and-billing/subscription-overview",
        permanent: true,
      },
      {
        source: "/getting-started/app/resetting-password",
        destination: "/account-and-billing/resetting-password",
        permanent: true,
      },
      // Thin-page merges (SW-575 / DOC-13).
      {
        source: "/faqs/seeing-camera-view",
        destination: "/faqs/manually-taking-an-image",
        permanent: true,
      },
      {
        source: "/faqs/taking-higher-quality-images",
        destination: "/faqs/manually-taking-an-image",
        permanent: true,
      },
      {
        source: "/troubleshooting/motor-connector-use",
        destination: "/troubleshooting/motor-connector-tightness-check",
        permanent: true,
      },
      // Marketing appendix pages removed from customer KB nav (DOC-13).
      {
        source: "/appendix-and-resources/media-kit",
        destination: "https://ocutrap.com",
        permanent: true,
      },
      {
        source: "/appendix-and-resources/testimonials",
        destination: "https://ocutrap.com",
        permanent: true,
      },
      {
        source: "/appendix-and-resources/case-study",
        destination: "https://ocutrap.com",
        permanent: true,
      },
      {
        source: "/appendix-and-resources/ocutrap-in-news",
        destination: "https://ocutrap.com",
        permanent: true,
      },
      // Trap Test / demo mode was dropped from the app (SW-117); the page is
      // gone, so send bookmarks to the field-test step (DOC-25).
      {
        source: "/device-management/trap-test-mode",
        destination: "/getting-started/deploying-in-the-field",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
