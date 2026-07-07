import { getHomeDoc } from "@/lib/docs";
import { markdownToHtml, markdownToPlain, extractHeadings } from "@/lib/markdown";
import DocContent from "@/components/doc-content";
import TableOfContents from "@/components/toc";
import TabsInit from "@/components/tabs-init";
import StatusPill from "@/components/status-pill";
import PrintButton from "@/components/print-button";
import CopyMarkdownButton from "@/components/copy-markdown-button";
import Link from "next/link";
import { notFound } from "next/navigation";

export default async function HomePage() {
  const doc = getHomeDoc();
  if (!doc) return notFound();

  const html = await markdownToHtml(doc.contentRaw, doc.filePath);
  const headings = extractHeadings(html);
  const pageMarkdown = `# ${doc.title}\n\n${markdownToPlain(doc.contentRaw)}\n`;

  return (
    <div className="page-content">
      <article className="doc-body">
        <div className="doc-topbar">
          <div className="breadcrumb">
            <span>OcuTrap Knowledge Base</span>
          </div>
          <div className="doc-actions">
            <CopyMarkdownButton markdown={pageMarkdown} />
            <PrintButton variant="icon" />
          </div>
        </div>

        <header className="page-header">
          <h1 className="page-title">{doc.title}</h1>
          {doc.description && (
            <p className="page-subtitle">{doc.description}</p>
          )}
        </header>

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
        <StatusPill />
      </article>

      <aside className="toc-sidebar" aria-label="On this page">
        <TableOfContents headings={headings} />
      </aside>
    </div>
  );
}
