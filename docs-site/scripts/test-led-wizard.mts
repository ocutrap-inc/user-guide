// Build-time assertions for the interactive LED diagnostic wizard (SW-333 /
// SITE-10). Run with: npm run test:led   (tsx scripts/test-led-wizard.mts)
//
// Guards the CONTENT SINGLE-SOURCE RULE and acceptance criteria:
//  1. the LED guide markdown carries a parseable ```led-diagnostics block
//  2. every color+pattern combo the wizard exposes also appears in the
//     generated fallback table (wizard data == table content — no drift)
//  3. every "what to do" link points at a real KB page (working links)
//  4. patterns use the canonical vocabulary the wizard's UI understands
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import {
  parseLedDiagnostics,
  ledMatrixToHtmlTable,
  ledMatrixToMarkdownTable,
  colorsInOrder,
  patternsForColor,
  entriesFor,
  patternLabel,
  colorLabelOf,
  LED_GUIDE_FILE,
} from "../lib/led-diagnostics";

let failures = 0;
function check(name: string, cond: boolean, detail = "") {
  if (cond) {
    console.log(`  ✓ ${name}`);
  } else {
    failures++;
    console.error(`  ✗ ${name}${detail ? ` — ${detail}` : ""}`);
  }
}

const CONTENT_ROOT = path.join(process.cwd(), "content");
const CANONICAL_PATTERNS = new Set([
  "solid",
  "breathing",
  "blinking",
  "fast-blink",
  "off",
]);

// Resolve a site-absolute KB href ("/troubleshooting/foo#bar") to a markdown
// file, mirroring the route's hrefToFilePaths logic.
function hrefResolvesToFile(href: string): boolean {
  const clean = href.replace(/[#?].*$/, "").replace(/^\//, "");
  if (!clean) return true;
  return (
    fs.existsSync(path.join(CONTENT_ROOT, `${clean}.md`)) ||
    fs.existsSync(path.join(CONTENT_ROOT, clean, "README.md"))
  );
}

function main() {
  console.log("LED diagnostic single-source");

  const raw = fs.readFileSync(path.join(CONTENT_ROOT, LED_GUIDE_FILE), "utf-8");
  const { content } = matter(raw);
  const matrix = parseLedDiagnostics(content);

  check("LED guide carries a parseable led-diagnostics block", !!matrix);
  if (!matrix) {
    console.error("\nFATAL: no matrix — aborting.");
    process.exit(1);
  }

  const colors = colorsInOrder(matrix);
  const combos = new Set<string>();
  for (const c of colors)
    for (const p of patternsForColor(matrix, c)) combos.add(`${c}/${p}`);

  console.log(
    `  · ${colors.length} colors, ${combos.size} color+pattern combos, ${matrix.entries.length} diagnosis entries`
  );

  check("matrix is non-empty", matrix.entries.length > 0);

  // 2. Every combo the wizard reaches also appears in the fallback table (both
  //    HTML and markdown renderers), so the JS-off / print / AI views match.
  const htmlTable = ledMatrixToHtmlTable(matrix);
  const mdTable = ledMatrixToMarkdownTable(matrix);
  let comboCovered = true;
  let meaningCovered = true;
  for (const entry of matrix.entries) {
    const color = colorLabelOf(entry);
    const pat = patternLabel(entry.pattern);
    // The table lists this color and pattern label…
    if (!htmlTable.includes(color) || !htmlTable.includes(pat)) {
      comboCovered = false;
    }
    // …and the exact meaning text reaches the same guidance as the wizard.
    const meaningInHtml = htmlTable.includes(
      entry.meaning
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
    );
    const meaningInMd = mdTable.includes(entry.meaning.replace(/\|/g, "\\|"));
    if (!meaningInHtml || !meaningInMd) meaningCovered = false;
  }
  check("every color+pattern appears in the fallback table", comboCovered);
  check("every wizard meaning appears in the fallback table", meaningCovered);

  // 3. Working links.
  const badLinks: string[] = [];
  for (const entry of matrix.entries) {
    for (const l of entry.links ?? []) {
      if (!hrefResolvesToFile(l.href)) badLinks.push(l.href);
    }
  }
  check(
    "every result link resolves to a real KB page",
    badLinks.length === 0,
    badLinks.join(", ")
  );

  // 4. Canonical pattern vocabulary (so the wizard UI renders known labels).
  const badPatterns = [
    ...new Set(
      matrix.entries.map((e) => e.pattern).filter((p) => !CANONICAL_PATTERNS.has(p))
    ),
  ];
  check(
    "all patterns use the canonical vocabulary",
    badPatterns.length === 0,
    badPatterns.join(", ")
  );

  // 5. Sanity: at least one combo carries multiple meanings (the LEDs reuse
  //    combinations) — proves the multi-entry path is exercised.
  const hasMultiMeaning = [...combos].some(
    (k) => entriesFor(matrix, k.split("/")[0], k.split("/")[1]).length > 1
  );
  check("multi-meaning combos are represented", hasMultiMeaning);

  if (failures) {
    console.error(`\n${failures} check(s) failed.`);
    process.exit(1);
  }
  console.log("\nAll LED wizard checks passed.");
}

main();
