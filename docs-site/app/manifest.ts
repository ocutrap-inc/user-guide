import type { MetadataRoute } from "next";
import { SITE_NAME, SITE_DESCRIPTION } from "@/lib/site";

// Web app manifest (SITE-11 / SW-334). Next serves this at
// /manifest.webmanifest and auto-injects the <link rel="manifest"> tag.
//
// Installability contract (Lighthouse PWA): name + short_name, start_url,
// display "standalone", and 192px + 512px icons. Icons reuse the existing
// OcuTrap raccoon mark (public/ocutrap-mark.png → icon-192/512.png). theme /
// background colors are brand navy #1f3c6b (internal-docs brand tokens),
// matching the light-mode header bar so the OS chrome blends in.
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: SITE_NAME,
    short_name: "OcuTrap Docs",
    description: SITE_DESCRIPTION,
    start_url: "/",
    scope: "/",
    display: "standalone",
    orientation: "portrait-primary",
    background_color: "#ffffff",
    theme_color: "#1f3c6b",
    icons: [
      {
        src: "/icon-192.png",
        sizes: "192x192",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "/icon-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "any",
      },
      {
        // Same raccoon mark declared maskable so Android adaptive icons and
        // the install prompt have a maskable candidate.
        src: "/icon-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };
}
