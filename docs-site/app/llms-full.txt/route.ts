import { parseSummary, flattenNav, getDocByHref } from "@/lib/docs";
import { markdownToPlain } from "@/lib/markdown";
import { absoluteUrl, SITE_DESCRIPTION } from "@/lib/site";

// Build-generated /llms-full.txt — the entire knowledge base as one clean
// markdown corpus in navigation order, for AI assistants that can ingest the
// whole thing. Each page's GitBook syntax is normalized to portable CommonMark
// by the shared markdownToPlain() helper (identical to the per-page copy
// button). Regenerated on every deploy from SUMMARY.md.
export const dynamic = "force-static";

function buildLlmsFull(): string {
  const sections = parseSummary();
  const items = flattenNav(sections);

  // Home ("/") first, then every nav entry, de-duped in order.
  const hrefs: string[] = ["/"];
  for (const item of items) {
    if (!hrefs.includes(item.href)) hrefs.push(item.href);
  }

  const parts: string[] = [];
  parts.push("# OcuTrap Knowledge Base");
  parts.push("");
  parts.push(`> ${SITE_DESCRIPTION}`);
  parts.push("");
  parts.push(
    `This file is the full markdown corpus of the OcuTrap knowledge base. ` +
      `For a link index of every page, see ${absoluteUrl("/llms.txt")}.`
  );
  parts.push("");

  for (const href of hrefs) {
    const doc = getDocByHref(href);
    if (!doc) continue;
    const body = markdownToPlain(doc.contentRaw);
    parts.push("---");
    parts.push(`# ${doc.title}`);
    parts.push(`URL: ${absoluteUrl(doc.href)}`);
    parts.push("");
    parts.push(body);
    parts.push("");
  }

  return parts.join("\n").replace(/\n{4,}/g, "\n\n\n").trimEnd() + "\n";
}

export function GET(): Response {
  return new Response(buildLlmsFull(), {
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
}
