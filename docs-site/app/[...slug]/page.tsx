import { getAllSlugs, getDocBySlug } from "@/lib/docs";
import { markdownToHtml, markdownToPlain, extractHeadings } from "@/lib/markdown";
import DocContent from "@/components/doc-content";
import TableOfContents from "@/components/toc";
import TabsInit from "@/components/tabs-init";
import StatusPill from "@/components/status-pill";
import StatusBanner from "@/components/status-banner";
import PrintButton from "@/components/print-button";
import Feedback from "@/components/feedback";
import CopyMarkdownButton from "@/components/copy-markdown-button";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ogImagePath } from "@/lib/site";

// Pages that surface the live system-status banner under the title when
// OcuTrap systems are degraded (SW-331 / spec SITE-08). Kept as an explicit
// href allow-list — these are the two troubleshooting pages a customer lands
// on when a trap looks "offline", where an active incident is the likely
// cause. Add an href here to opt another page in.
const STATUS_BANNER_HREFS = new Set([
  "/troubleshooting/trap-offline-or-wont-connect",
  "/troubleshooting/common-issues",
]);

export async function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const doc = getDocBySlug(slug);
  if (!doc) return {};
  const description =
    doc.description ??
    `${doc.section ? doc.section + " — " : ""}OcuTrap Knowledge Base`;
  const ogImage = ogImagePath(doc.title, doc.section);
  return {
    title: doc.title,
    description,
    alternates: { canonical: doc.href },
    openGraph: {
      type: "article",
      url: doc.href,
      title: doc.title,
      description,
      images: [{ url: ogImage, width: 1200, height: 630, alt: doc.title }],
    },
    twitter: {
      card: "summary_large_image",
      title: doc.title,
      description,
      images: [ogImage],
    },
  };
}

export default async function DocPage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;
  const doc = getDocBySlug(slug);
  if (!doc) return notFound();

  const html = await markdownToHtml(doc.contentRaw, doc.filePath);
  const headings = extractHeadings(html);
  const pageMarkdown = `# ${doc.title}\n\n${markdownToPlain(doc.contentRaw)}\n`;

  return (
    <div className="page-content">
      <article className="doc-body">
        {/* Breadcrumb + per-page copy/print affordances */}
        <div className="doc-topbar">
          <nav className="breadcrumb" aria-label="Breadcrumb">
            <Link href="/" style={{ color: "var(--color-muted)", textDecoration: "none" }}>
              OcuTrap Knowledge Base
            </Link>
            {doc.section && (
              <>
                <span className="breadcrumb-sep">/</span>
                <span>{doc.section}</span>
              </>
            )}
            <span className="breadcrumb-sep">/</span>
            <span style={{ color: "var(--color-heading)" }}>{doc.title}</span>
          </nav>
          <div className="doc-actions">
            <CopyMarkdownButton markdown={pageMarkdown} />
            <PrintButton variant="icon" />
          </div>
        </div>

        <header className="page-header">
          {doc.section && <div className="page-eyebrow">{doc.section}</div>}
          <h1 className="page-title">{doc.title}</h1>
          {doc.description && (
            <p className="page-subtitle">{doc.description}</p>
          )}
        </header>

        {STATUS_BANNER_HREFS.has(doc.href) && <StatusBanner />}

        <DocContent html={html} />

        {/* "Was this helpful?" feedback (SITE-07) — bottom of every article. */}
        <Feedback path={doc.href} />

        {/* Prev / Next navigation */}
        {(doc.prev || doc.next) && (
          <nav className="doc-nav" aria-label="Page navigation">
            {doc.prev ? (
              <Link href={doc.prev.href} className="doc-nav-btn">
                <span className="doc-nav-label">← Previous</span>
                <span className="doc-nav-title">{doc.prev.title}</span>
              </Link>
            ) : (
              <div />
            )}
            {doc.next ? (
              <Link href={doc.next.href} className="doc-nav-btn doc-nav-btn--next">
                <span className="doc-nav-label">Next →</span>
                <span className="doc-nav-title">{doc.next.title}</span>
              </Link>
            ) : (
              <div />
            )}
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
