import { parseSummary, flattenNav, getDocBySlug, getHomeDoc } from "@/lib/docs";
import { markdownToHtml } from "@/lib/markdown";
import DocContent from "@/components/doc-content";
import PrintButton from "@/components/print-button";
import TabsInit from "@/components/tabs-init";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Full Manual — OcuTrap Docs",
  description: "Complete OcuTrap documentation in one printable page.",
};

export default async function ManualPage() {
  const sections = parseSummary();
  const flatItems = flattenNav(sections);

  // Resolve and render every doc in nav order
  const pages = (
    await Promise.all(
      flatItems.map(async (item) => {
        const slug = item.href === "/" ? [] : item.href.replace(/^\//, "").split("/");
        const doc = slug.length === 0 ? getHomeDoc() : getDocBySlug(slug);
        if (!doc) return null;
        const html = await markdownToHtml(doc.contentRaw);
        return { title: item.title, href: item.href, section: doc.section, html };
      })
    )
  ).filter(Boolean) as { title: string; href: string; section: string | null; html: string }[];

  return (
    <>
      {/* Screen-only header */}
      <div className="manual-header">
        <div>
          <h1>OcuTrap — Complete Manual</h1>
          <p>
            {pages.length} pages · Use your browser&rsquo;s Print / Save as PDF to export
          </p>
        </div>
        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center", flexWrap: "wrap" }}>
          <a
            href="/"
            style={{
              padding: "0.5rem 1rem",
              border: "1px solid var(--color-border)",
              borderRadius: "6px",
              fontSize: "0.875rem",
              textDecoration: "none",
              color: "var(--color-muted)",
            }}
          >
            ← Back to docs
          </a>
          <PrintButton />
        </div>
      </div>

      <div className="manual-body">
        {pages.map((page, i) => (
          <section key={page.href} className="manual-page" id={`page-${i}`}>
            <div className="manual-page-header">
              {page.section && (
                <span className="manual-section-label">{page.section}</span>
              )}
              <h1 className="manual-page-title">{page.title}</h1>
            </div>
            <DocContent html={page.html} />
          </section>
        ))}
      </div>

      <TabsInit />
    </>
  );
}
