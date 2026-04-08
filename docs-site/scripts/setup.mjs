/**
 * Pre-build setup:
 * 1. Copies .gitbook/assets/ → public/gitbook-assets/
 * 2. Copies all KB markdown content → content/
 *    (makes the content self-contained for Vercel deployment)
 */
import {
  cpSync,
  existsSync,
  mkdirSync,
  rmSync,
  readdirSync,
  statSync,
  copyFileSync,
} from "fs";
import { join, dirname, relative } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const docsRoot = join(__dirname, ".."); // docs-site/
const kbRoot = join(docsRoot, ".."); // OcuTrap_Knowledge_Base/

// Directories to skip when copying content
const SKIP_DIRS = new Set(["docs-site", "convex-tutorial", "node_modules", ".git"]);

// ── 1. Copy .gitbook/assets ───────────────────────────────────
const assetsSource = join(kbRoot, ".gitbook/assets");
const assetsDest = join(docsRoot, "public/gitbook-assets");

if (existsSync(assetsSource)) {
  if (existsSync(assetsDest)) rmSync(assetsDest, { recursive: true });
  mkdirSync(assetsDest, { recursive: true });
  cpSync(assetsSource, assetsDest, { recursive: true });
  console.log("✓ Copied .gitbook/assets → public/gitbook-assets");
} else {
  console.log("ℹ .gitbook/assets not found, skipping asset copy");
}

// ── 2. Copy markdown content ──────────────────────────────────
const contentDest = join(docsRoot, "content");

if (existsSync(kbRoot) && existsSync(join(kbRoot, "SUMMARY.md"))) {
  if (existsSync(contentDest)) rmSync(contentDest, { recursive: true });
  mkdirSync(contentDest, { recursive: true });

  function copyMarkdown(srcDir, destDir) {
    const entries = readdirSync(srcDir, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = join(srcDir, entry.name);
      const destPath = join(destDir, entry.name);
      if (entry.isDirectory()) {
        if (SKIP_DIRS.has(entry.name) || entry.name.startsWith(".")) continue;
        mkdirSync(destPath, { recursive: true });
        copyMarkdown(srcPath, destPath);
      } else if (entry.name.endsWith(".md")) {
        copyFileSync(srcPath, destPath);
      }
    }
  }

  copyMarkdown(kbRoot, contentDest);
  const mdCount = readdirSync(contentDest, { recursive: true }).filter(
    (f) => typeof f === "string" && f.endsWith(".md")
  ).length;
  console.log(`✓ Copied ${mdCount} markdown files → content/`);
} else {
  console.log("ℹ KB root not found, skipping content copy (using existing content/)");
}
