import { getAllSlugs, getDocBySlug } from "@/lib/docs";
import { markdownToHtml, extractHeadings } from "@/lib/markdown";
import DocContent from "@/components/doc-content";
import TableOfContents from "@/components/toc";
import TabsInit from "@/components/tabs-init";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";

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
  return {
    title: doc.title,
    description: `${doc.section ? doc.section + " — " : ""}OcuTrap Documentation`,
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

  const html = await markdownToHtml(doc.contentRaw);
  const headings = extractHeadings(html);

  return (
    <div className="page-content">
      <article className="doc-body">
        {/* Breadcrumb */}
        <nav className="breadcrumb" aria-label="Breadcrumb">
          <Link href="/" style={{ color: "var(--color-muted)", textDecoration: "none" }}>
            OcuTrap Docs
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

        <DocContent html={html} />

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
      </article>

      <aside className="toc-sidebar" aria-label="On this page">
        <TableOfContents headings={headings} />
      </aside>
    </div>
  );
}
