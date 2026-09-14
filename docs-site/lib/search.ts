import Fuse from "fuse.js";
import type { SearchDoc } from "./docs";

export function createSearchEngine(docs: SearchDoc[]) {
  return new Fuse(docs, {
    keys: [
      { name: "title", weight: 3 },
      { name: "section", weight: 1 },
      { name: "text", weight: 1 },
      { name: "excerpt", weight: 0.5 },
    ],
    threshold: 0.35,
    ignoreLocation: true,
    fieldNormWeight: 0.2,
  });
}

export function searchExcerpt(doc: SearchDoc, query: string): string {
  const text = doc.text || doc.excerpt;
  const normalized = text.toLowerCase();
  const phrase = query.trim().toLowerCase();
  let match = normalized.indexOf(phrase);
  if (match < 0) {
    const positions = phrase.split(/\s+/).filter((word) => word.length > 2)
      .map((word) => normalized.indexOf(word)).filter((index) => index >= 0);
    match = positions.length ? Math.min(...positions) : -1;
  }
  if (match < 0) return doc.excerpt;
  let start = Math.max(0, match - 50);
  if (start > 0) {
    const boundary = text.indexOf(" ", start);
    if (boundary < match) start = boundary + 1;
  }
  let end = Math.min(text.length, start + 210);
  if (end < text.length) {
    const boundary = text.lastIndexOf(" ", end);
    if (boundary > match + phrase.length) end = boundary;
  }
  return `${start ? "…" : ""}${text.slice(start, end).trim()}${end < text.length ? "…" : ""}`;
}

export function searchDocuments(engine: Fuse<SearchDoc>, query: string) {
  if (!query.trim()) return [];
  return engine.search(query.trim()).slice(0, 8).map(({ item }) => ({
    ...item,
    excerpt: searchExcerpt(item, query),
  }));
}
