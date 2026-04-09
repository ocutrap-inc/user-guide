import fs from "fs";
import path from "path";
import matter from "gray-matter";

// Prefer content/ (committed copy used during Vercel deployment),
// fall back to ../ for local development where the KB dir is the parent.
function findKbRoot(): string {
  const candidates = [
    path.join(process.cwd(), "content"), // Vercel: committed copy
    path.join(process.cwd(), ".."), // Local: sibling of docs-site
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(path.join(candidate, "SUMMARY.md"))) return candidate;
  }
  // Default to content/ and let subsequent errors surface the real issue
  return path.join(process.cwd(), "content");
}

const KB_ROOT = findKbRoot();

export type NavItem = {
  title: string;
  href: string;
  filePath: string;
  children: NavItem[];
};

export type NavSection = {
  title: string | null;
  separator?: boolean;
  items: NavItem[];
};

export type DocData = {
  title: string;
  contentRaw: string;
  filePath: string;
  href: string;
  headings: { id: string; text: string; level: number }[];
  prev: { title: string; href: string } | null;
  next: { title: string; href: string } | null;
  section: string | null;
};

export type SearchDoc = {
  title: string;
  href: string;
  section: string | null;
  excerpt: string;
};

// Convert a file path like "getting-started/introduction.md" to URL href "/getting-started/introduction"
function filePathToHref(filePath: string): string {
  let href = filePath.replace(/\.md$/, "");
  if (href === "README") return "/";
  href = href.replace(/\/README$/, "");
  return "/" + href;
}

// Convert URL href to file path candidates
function hrefToFilePaths(href: string): string[] {
  const rel = href === "/" ? "" : href.replace(/^\//, "");
  if (!rel) return ["README.md"];
  return [`${rel}.md`, `${rel}/README.md`];
}

// Parse SUMMARY.md into a flat navigation structure
export function parseSummary(): NavSection[] {
  const summaryPath = path.join(KB_ROOT, "SUMMARY.md");
  const content = fs.readFileSync(summaryPath, "utf-8");
  const lines = content.split("\n");

  const sections: NavSection[] = [];
  let currentSection: NavSection = { title: null, items: [] };
  sections.push(currentSection);

  const lastItemByLevel = new Map<number, NavItem>();

  for (const line of lines) {
    // Section header ## Title
    const sectionMatch = line.match(/^##\s+(.+)/);
    if (sectionMatch) {
      currentSection = { title: sectionMatch[1].trim(), items: [] };
      sections.push(currentSection);
      lastItemByLevel.clear();
      continue;
    }

    // Nav item: * [Title](path) with optional leading spaces
    const itemMatch = line.match(/^(\s*)\*\s+\[([^\]]+)\]\(([^)]+)\)/);
    if (itemMatch) {
      const [, indent, title, filePath] = itemMatch;
      const level = Math.floor(indent.length / 2);
      const href = filePathToHref(filePath);
      const item: NavItem = { title, href, filePath, children: [] };

      if (level === 0) {
        currentSection.items.push(item);
      } else {
        const parent = lastItemByLevel.get(level - 1);
        if (parent) {
          parent.children.push(item);
        } else {
          currentSection.items.push(item);
        }
      }

      lastItemByLevel.set(level, item);
      // Clear deeper levels
      for (const k of Array.from(lastItemByLevel.keys())) {
        if (k > level) lastItemByLevel.delete(k);
      }
      continue;
    }

    // Separator ***
    if (line.trim() === "***") {
      currentSection = { title: null, separator: true, items: [] };
      sections.push(currentSection);
      lastItemByLevel.clear();
    }
  }

  return sections.filter((s) => s.items.length > 0);
}

// Flatten nav tree into an ordered list of items (for prev/next)
export function flattenNav(sections: NavSection[]): NavItem[] {
  const result: NavItem[] = [];
  function walk(items: NavItem[]) {
    for (const item of items) {
      result.push(item);
      if (item.children.length > 0) walk(item.children);
    }
  }
  for (const section of sections) walk(section.items);
  return result;
}

// Get all slugs for static params
export function getAllSlugs(): string[][] {
  const sections = parseSummary();
  const items = flattenNav(sections);
  return items
    .filter((item) => item.href !== "/")
    .map((item) => item.href.replace(/^\//, "").split("/"));
}

// Find which file to read for a given href
function resolveFilePath(href: string): string | null {
  const candidates = hrefToFilePaths(href);
  for (const candidate of candidates) {
    const full = path.join(KB_ROOT, candidate);
    if (fs.existsSync(full)) return candidate;
  }
  return null;
}

// Get section title for a given href
function getSectionTitle(
  sections: NavSection[],
  href: string
): string | null {
  for (const section of sections) {
    function search(items: NavItem[]): boolean {
      for (const item of items) {
        if (item.href === href) return true;
        if (search(item.children)) return true;
      }
      return false;
    }
    if (search(section.items)) return section.title;
  }
  return null;
}

export function getDocBySlug(slug: string[]): DocData | null {
  const href = "/" + slug.join("/");
  const sections = parseSummary();
  const flatItems = flattenNav(sections);

  const filePath = resolveFilePath(href);
  if (!filePath) return null;

  const fullPath = path.join(KB_ROOT, filePath);
  const raw = fs.readFileSync(fullPath, "utf-8");
  const { content, data } = matter(raw);

  // Determine title: frontmatter, first h1 in content, or filename
  let title: string = data.title ?? "";
  if (!title) {
    const h1Match = content.match(/^#\s+(.+)/m);
    title = h1Match ? h1Match[1] : slug[slug.length - 1];
  }

  // Find prev/next
  const currentIndex = flatItems.findIndex((item) => item.href === href);
  const prev = currentIndex > 0 ? flatItems[currentIndex - 1] : null;
  const next =
    currentIndex < flatItems.length - 1 ? flatItems[currentIndex + 1] : null;

  const section = getSectionTitle(sections, href);

  return {
    title,
    contentRaw: content,
    filePath,
    href,
    headings: [], // populated after HTML processing
    prev: prev ? { title: prev.title, href: prev.href } : null,
    next: next ? { title: next.title, href: next.href } : null,
    section,
  };
}

export function getHomeDoc(): DocData | null {
  const filePath = "README.md";
  const fullPath = path.join(KB_ROOT, filePath);
  if (!fs.existsSync(fullPath)) return null;

  const raw = fs.readFileSync(fullPath, "utf-8");
  const { content, data } = matter(raw);

  const sections = parseSummary();
  const flatItems = flattenNav(sections);
  const next = flatItems.length > 0 ? flatItems[0] : null;

  return {
    title: data.title ?? "OcuTrap Knowledge Base",
    contentRaw: content,
    filePath,
    href: "/",
    headings: [],
    prev: null,
    next: next ? { title: next.title, href: next.href } : null,
    section: null,
  };
}

// Build search index from all docs
export function buildSearchIndex(): SearchDoc[] {
  const sections = parseSummary();
  const flatItems = flattenNav(sections);
  const results: SearchDoc[] = [];

  for (const item of flatItems) {
    const filePath = resolveFilePath(item.href);
    if (!filePath) continue;

    try {
      const fullPath = path.join(KB_ROOT, filePath);
      const raw = fs.readFileSync(fullPath, "utf-8");
      const { content } = matter(raw);

      // Strip markdown syntax and HTML entities for plain text excerpt
      const plainText = content
        .replace(/\{%[\s\S]*?%\}/g, "")
        .replace(/#+\s+/g, "")
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
        .replace(/[*_`~]/g, "")
        .replace(/<[^>]+>/g, "")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#x[0-9a-fA-F]+;/g, " ")
        .replace(/&[a-z]+;/g, " ")
        .replace(/\s+/g, " ")
        .trim();

      const section = getSectionTitle(sections, item.href);
      // Trim to ~160 chars at word boundary, skip the page title if it starts the excerpt
      let rawExcerpt = plainText.startsWith(item.title)
        ? plainText.slice(item.title.length).trimStart()
        : plainText;
      if (rawExcerpt.length > 160) {
        rawExcerpt = rawExcerpt.slice(0, 160).replace(/\s\S*$/, "") + "…";
      }
      const excerpt = rawExcerpt;

      results.push({
        title: item.title,
        href: item.href,
        section,
        excerpt,
      });
    } catch {
      // Skip unreadable files
    }
  }

  return results;
}
