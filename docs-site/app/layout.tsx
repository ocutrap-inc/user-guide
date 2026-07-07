import type { Metadata } from "next";
import "./globals.css";
import { parseSummary } from "@/lib/docs";
import { SITE_URL, SITE_NAME, SITE_DESCRIPTION, ogImagePath } from "@/lib/site";
import SidebarClient from "@/components/sidebar-client";
import SearchDialog from "@/components/search-dialog";
import ThemeToggle from "@/components/theme-toggle";
import Link from "next/link";
import Image from "next/image";
import { Outfit, Manrope, JetBrains_Mono } from "next/font/google";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
  weight: ["400", "500", "600", "700", "800"],
});

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope",
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
  weight: ["400", "500"],
});

const OG_IMAGE = {
  url: ogImagePath(),
  width: 1200,
  height: 630,
  alt: SITE_NAME,
};

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: SITE_NAME, template: `%s | ${SITE_NAME}` },
  description: SITE_DESCRIPTION,
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    siteName: SITE_NAME,
    url: SITE_URL,
    title: SITE_NAME,
    description: SITE_DESCRIPTION,
    images: [OG_IMAGE],
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_NAME,
    description: SITE_DESCRIPTION,
    images: [OG_IMAGE.url],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const sections = parseSummary();
  const fontVars = `${outfit.variable} ${manrope.variable} ${jetbrainsMono.variable}`;

  return (
    <html lang="en" suppressHydrationWarning className={fontVars}>
      <head>
        {/* No-flash theme: apply a stored manual preference before first paint.
            With no stored preference, CSS @media (prefers-color-scheme) drives the default. */}
        <script
          dangerouslySetInnerHTML={{
            __html:
              "(function(){try{var t=localStorage.getItem('theme');if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();",
          }}
        />
      </head>
      <body>
        <div className="layout">
          <SidebarClient sections={sections} />

          <div className="main-wrapper">
            <header className="site-header">
              {/* Spacer for mobile hamburger */}
              <div style={{ width: 32, display: "none" }} aria-hidden="true" className="hamburger-spacer" />
              <Link href="/" className="site-logo" style={{ marginRight: "auto" }}>
                <span className="site-logo-chip">
                  <Image
                    src="/ocutrap-mark.png"
                    alt="OcuTrap"
                    width={26}
                    height={26}
                    priority
                  />
                </span>
                <span className="site-logo-word">
                  OcuTrap
                  <span className="site-logo-sub">Knowledge Base</span>
                </span>
              </Link>
              <SearchDialog />
              <ThemeToggle />
            </header>

            <main>{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
