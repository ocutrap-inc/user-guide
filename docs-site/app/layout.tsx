import type { Metadata } from "next";
import "./globals.css";
import { parseSummary } from "@/lib/docs";
import SidebarClient from "@/components/sidebar-client";
import SearchDialog from "@/components/search-dialog";
import PrintButton from "@/components/print-button";
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

export const metadata: Metadata = {
  title: { default: "OcuTrap Knowledge Base", template: "%s | OcuTrap Docs" },
  description: "Documentation and support for OcuTrap trap management.",
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
      <body>
        <div className="layout">
          <SidebarClient sections={sections} />

          <div className="main-wrapper">
            <header className="site-header">
              {/* Spacer for mobile hamburger */}
              <div style={{ width: 32, display: "none" }} aria-hidden="true" className="hamburger-spacer" />
              <Link href="/" className="site-logo" style={{ marginRight: "auto" }}>
                <Image
                  src="/gitbook-assets/Removed Background logo.png"
                  alt="OcuTrap"
                  width={120}
                  height={30}
                  className="site-logo-img"
                  priority
                  style={{ height: 30, width: "auto" }}
                />
              </Link>
              <SearchDialog />
              <PrintButton />
            </header>

            <main>{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
