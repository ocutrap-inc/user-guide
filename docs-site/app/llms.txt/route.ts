import { parseSummary, getDocByHref, type NavItem, type NavSection } from "@/lib/docs";
import { absoluteUrl, SITE_DESCRIPTION } from "@/lib/site";

// Build-generated /llms.txt (the llms.txt convention: https://llmstxt.org).
// A curated, link-first index of the whole knowledge base so AI assistants can
// discover every page. Regenerated on every deploy from SUMMARY.md — the same
// source of truth the sitemap and nav use — so it never drifts from the site.
export const dynamic = "force-static";

// Flatten a section's nested nav tree into an ordered list (children inline).
function flatten(items: NavItem[]): NavItem[] {
  const out: NavItem[] = [];
  const walk = (list: NavItem[]) => {
    for (const item of list) {
      out.push(item);
      if (item.children.length) walk(item.children);
    }
  };
  walk(items);
  return out;
}

// Heading for a section: its SUMMARY.md title, or a sensible fallback for the
// two untitled groups (the home entry and the post-separator entry).
function headingFor(section: NavSection): string {
  if (section.title) return section.title;
  return section.items.some((i) => i.href === "/") ? "Overview" : "More";
}

function buildLlmsTxt(): string {
  const sections = parseSummary();
  const lines: string[] = [];

  lines.push("# OcuTrap Knowledge Base");
  lines.push("");
  lines.push(`> ${SITE_DESCRIPTION}`);
  lines.push("");

  for (const section of sections) {
    const items = flatten(section.items);
    if (!items.length) continue;
    lines.push(`## ${headingFor(section)}`);
    lines.push("");
    for (const item of items) {
      const doc = getDocByHref(item.href);
      const desc = doc?.description;
      const suffix = desc ? `: ${desc}` : "";
      lines.push(`- [${item.title}](${absoluteUrl(item.href)})${suffix}`);
    }
    lines.push("");
  }

  return lines.join("\n").replace(/\n{3,}/g, "\n\n").trimEnd() + "\n";
}

export function GET(): Response {
  return new Response(buildLlmsTxt(), {
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
}
