import type { Metadata } from "next";
import "./globals.css";
import { parseSummary } from "@/lib/docs";
import SidebarClient from "@/components/sidebar-client";
import SearchDialog from "@/components/search-dialog";
import PrintButton from "@/components/print-button";
import Link from "next/link";

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

  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <div className="layout">
          <SidebarClient sections={sections} />

          <div className="main-wrapper">
            <header className="site-header">
              {/* Hamburger rendered inside SidebarClient — spacer to push content */}
              <div style={{ width: 32, display: "none" }} aria-hidden="true" className="hamburger-spacer" />
              <Link href="/" className="site-logo" style={{ marginRight: "auto" }}>
                <span className="site-logo-icon">O</span>
                OcuTrap Docs
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
