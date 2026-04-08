import { getHomeDoc } from "@/lib/docs";
import { markdownToHtml, extractHeadings } from "@/lib/markdown";
import DocContent from "@/components/doc-content";
import TableOfContents from "@/components/toc";
import TabsInit from "@/components/tabs-init";
import Link from "next/link";
import { notFound } from "next/navigation";

export default async function HomePage() {
  const doc = getHomeDoc();
  if (!doc) return notFound();

  const html = await markdownToHtml(doc.contentRaw);
  const headings = extractHeadings(html);

  return (
    <div className="page-content">
      <article className="doc-body">
        <div className="breadcrumb">
          <span>OcuTrap Docs</span>
        </div>

        <h1 className="prose" style={{ fontSize: "1.875rem", fontWeight: 700, marginBottom: "1.5rem", color: "var(--color-heading)" }}>
          {doc.title}
        </h1>

        <DocContent html={html} />

        {doc.next && (
          <nav className="doc-nav" aria-label="Page navigation">
            <div style={{ flex: 1 }} />
            <Link href={doc.next.href} className="doc-nav-btn doc-nav-btn--next">
              <span className="doc-nav-label">Next →</span>
              <span className="doc-nav-title">{doc.next.title}</span>
            </Link>
          </nav>
        )}

        <TabsInit />
      </article>

      <aside className="toc-sidebar" aria-label="On this page">
        <TableOfContents headings={headings} />
      </aside>
    </div>
  );
}
