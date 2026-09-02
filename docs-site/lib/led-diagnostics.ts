// Single-source data model for the interactive LED diagnostic wizard (SITE-10
// / SW-333) AND the plain fallback table on the LED guide page.
//
// CONTENT SINGLE-SOURCE RULE (acceptance-critical): the color/pattern/meaning
// matrix is authored *once*, as a fenced ```led-diagnostics YAML block inside
// content/getting-started/led-guide.md. This module parses that block; the
// markdown pipeline (lib/markdown.ts) turns the same block into the visible
// fallback table, and the wizard component renders it interactively. There is
// no forked copy — editing the markdown block changes both the wizard and the
// table on the next build, with zero component-code changes.

import matter from "gray-matter";

// Fence info-string that marks the structured block. The markdown pipeline
// intercepts a ```<FENCE> code block and hands its body here instead of
// rendering it as a highlighted code block.
export const LED_DIAGNOSTICS_FENCE = "led-diagnostics";

// The one page the wizard mounts on. Matched by DocData.filePath in the page
// route so the wizard only hydrates where the data block lives.
export const LED_GUIDE_FILE = "getting-started/led-guide.md";

export type LedLink = {
  label: string;
  /** Site-absolute path (e.g. "/troubleshooting/trap-offline-or-wont-connect"),
   *  optionally with an #anchor. Absolute so it needs no source-relative
   *  resolution in either the React wizard or the injected HTML table. */
  href: string;
};

export type LedEntry = {
  /** Canonical color id, e.g. "cyan", "green", "no-light". */
  color: string;
  /** Human label for the color, defaults to a title-cased id. */
  colorLabel?: string;
  /** Canonical pattern id: solid | breathing | blinking | fast-blink | off. */
  pattern: string;
  /** What this color+pattern indicates. */
  meaning: string;
  /** Optional recommended action ("what to do"). */
  action?: string;
  /** Optional short qualifier, e.g. "on battery", "after a command". */
  context?: string;
  /** Links into the relevant troubleshooting sections. */
  links?: LedLink[];
};

export type LedMatrix = {
  entries: LedEntry[];
};

// Canonical pattern id → display label (presentation only; not content).
const PATTERN_LABELS: Record<string, string> = {
  solid: "Solid",
  breathing: "Breathing (slow fade)",
  blinking: "Blinking",
  "fast-blink": "Fast blinking",
  off: "No light",
};

export function patternLabel(pattern: string): string {
  return (
    PATTERN_LABELS[pattern] ??
    pattern.replace(/[-_]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
  );
}

// Stable ordering so the fallback table and the wizard's swatch/pattern rows
// read the same top-to-bottom regardless of authoring order.
const PATTERN_ORDER = ["solid", "breathing", "blinking", "fast-blink", "off"];

export function patternRank(pattern: string): number {
  const i = PATTERN_ORDER.indexOf(pattern);
  return i === -1 ? PATTERN_ORDER.length : i;
}

function titleCase(id: string): string {
  return id.replace(/[-_]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function colorLabelOf(entry: LedEntry): string {
  return entry.colorLabel ?? titleCase(entry.color);
}

// Global matcher for the whole ```led-diagnostics fenced block (fence lines
// included). Used by the markdown pipeline to strip/replace it.
export function ledFenceRegex(): RegExp {
  return new RegExp(
    "```+\\s*" + LED_DIAGNOSTICS_FENCE + "\\s*\\r?\\n[\\s\\S]*?\\r?\\n```+",
    "g"
  );
}

// Extract the raw body of the ```led-diagnostics fenced block from a markdown
// string, or null if absent. Tolerant of extra spaces and CRLF.
export function extractLedDiagnosticsBlock(markdown: string): string | null {
  const fence = new RegExp(
    "```+\\s*" + LED_DIAGNOSTICS_FENCE + "\\s*\\r?\\n([\\s\\S]*?)\\r?\\n```+",
    "m"
  );
  const m = markdown.match(fence);
  return m ? m[1] : null;
}

// Parse the LED matrix out of a page's raw markdown. Returns null when the
// block is missing or malformed (callers degrade gracefully). Uses gray-matter
// (already a dependency) as the YAML engine so we add no new parser.
export function parseLedDiagnostics(markdown: string): LedMatrix | null {
  const body = extractLedDiagnosticsBlock(markdown);
  if (body == null) return null;
  let data: unknown;
  try {
    data = matter(`---\n${body}\n---\n`).data;
  } catch {
    return null;
  }
  if (!data || typeof data !== "object") return null;
  const rawEntries = (data as { entries?: unknown }).entries;
  if (!Array.isArray(rawEntries)) return null;

  const entries: LedEntry[] = [];
  for (const raw of rawEntries) {
    if (!raw || typeof raw !== "object") continue;
    const e = raw as Record<string, unknown>;
    if (typeof e.color !== "string" || typeof e.pattern !== "string") continue;
    if (typeof e.meaning !== "string") continue;
    const links: LedLink[] = [];
    if (Array.isArray(e.links)) {
      for (const l of e.links) {
        if (l && typeof l === "object") {
          const lo = l as Record<string, unknown>;
          if (typeof lo.label === "string" && typeof lo.href === "string") {
            links.push({ label: lo.label, href: lo.href });
          }
        }
      }
    }
    entries.push({
      color: e.color,
      colorLabel: typeof e.colorLabel === "string" ? e.colorLabel : undefined,
      pattern: e.pattern,
      meaning: e.meaning,
      action: typeof e.action === "string" ? e.action : undefined,
      context: typeof e.context === "string" ? e.context : undefined,
      links: links.length ? links : undefined,
    });
  }
  return entries.length ? { entries } : null;
}

// Ordered, de-duplicated color ids in the matrix (first-seen order).
export function colorsInOrder(matrix: LedMatrix): string[] {
  const seen: string[] = [];
  for (const e of matrix.entries) if (!seen.includes(e.color)) seen.push(e.color);
  return seen;
}

// Patterns available for a given color, ranked.
export function patternsForColor(matrix: LedMatrix, color: string): string[] {
  const seen: string[] = [];
  for (const e of matrix.entries) {
    if (e.color === color && !seen.includes(e.pattern)) seen.push(e.pattern);
  }
  return seen.sort((a, b) => patternRank(a) - patternRank(b));
}

// All entries matching a color+pattern (may be more than one — the LEDs reuse
// combinations, e.g. blinking green means both "seeking signal" and "closing
// the door").
export function entriesFor(
  matrix: LedMatrix,
  color: string,
  pattern: string
): LedEntry[] {
  return matrix.entries.filter(
    (e) => e.color === color && e.pattern === pattern
  );
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function actionCellHtml(entry: LedEntry): string {
  const parts: string[] = [];
  if (entry.action) parts.push(escapeHtml(entry.action));
  if (entry.links && entry.links.length) {
    const links = entry.links
      .map(
        (l) =>
          `<a href="${escapeHtml(l.href)}">${escapeHtml(l.label)}</a>`
      )
      .join(" · ");
    parts.push(links);
  }
  return parts.join("<br>") || "—";
}

// Render the matrix as a GitBook-style HTML table for the article body — this
// is the JS-off fallback that the markdown pipeline injects where the fenced
// block sat. Rows are grouped by color, then pattern, matching the wizard.
export function ledMatrixToHtmlTable(matrix: LedMatrix): string {
  const rows: string[] = [];
  for (const color of colorsInOrder(matrix)) {
    for (const pattern of patternsForColor(matrix, color)) {
      for (const entry of entriesFor(matrix, color, pattern)) {
        const ctx = entry.context
          ? ` <span class="led-table__context">(${escapeHtml(
              entry.context
            )})</span>`
          : "";
        rows.push(
          `<tr><td>${escapeHtml(colorLabelOf(entry))}</td>` +
            `<td>${escapeHtml(patternLabel(entry.pattern))}</td>` +
            `<td>${escapeHtml(entry.meaning)}${ctx}</td>` +
            `<td>${actionCellHtml(entry)}</td></tr>`
        );
      }
    }
  }
  return (
    `<table class="led-table">\n` +
    `<thead><tr><th>Light color</th><th>Pattern</th><th>What it means</th><th>What to do</th></tr></thead>\n` +
    `<tbody>\n${rows.join("\n")}\n</tbody>\n</table>`
  );
}

// Render the matrix as a GitHub-flavored markdown table for the plain-text
// pipeline (llms.txt, "Copy page as Markdown", search index, print corpus).
export function ledMatrixToMarkdownTable(matrix: LedMatrix): string {
  const esc = (s: string) => s.replace(/\|/g, "\\|").replace(/\n/g, " ");
  const lines: string[] = [
    "| Light color | Pattern | What it means | What to do |",
    "| --- | --- | --- | --- |",
  ];
  for (const color of colorsInOrder(matrix)) {
    for (const pattern of patternsForColor(matrix, color)) {
      for (const entry of entriesFor(matrix, color, pattern)) {
        const meaning =
          entry.meaning + (entry.context ? ` (${entry.context})` : "");
        const actionParts: string[] = [];
        if (entry.action) actionParts.push(entry.action);
        if (entry.links && entry.links.length) {
          actionParts.push(
            entry.links.map((l) => `[${l.label}](${l.href})`).join(" · ")
          );
        }
        lines.push(
          `| ${esc(colorLabelOf(entry))} | ${esc(patternLabel(entry.pattern))} | ${esc(
            meaning
          )} | ${esc(actionParts.join(" · ") || "–")} |`
        );
      }
    }
  }
  return lines.join("\n");
}
