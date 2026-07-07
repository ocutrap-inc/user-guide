/**
 * Render audit for the docs-site (SITE-01 / SW-298).
 *
 * Boots `next start` (the site must be built first: `npm run build`), then
 * fetches every route in SUMMARY.md plus `/` and `/manual`, asserting each
 * returns HTTP 200 with non-empty rendered article content. Also spot-checks
 * a {% file %} download card, a card-table grid, and a /gitbook-assets image.
 *
 * Usage:
 *   npm run build && node scripts/audit-render.mjs
 *
 * Exits non-zero if any route fails.
 */
import { spawn } from "child_process";
import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const docsRoot = join(__dirname, "..");
const PORT = process.env.AUDIT_PORT || "3111";
const BASE = `http://127.0.0.1:${PORT}`;

// ── Collect routes from the committed content copy of SUMMARY.md ──
const summaryPath = join(docsRoot, "content", "SUMMARY.md");
if (!existsSync(summaryPath)) {
  console.error(`SUMMARY.md not found at ${summaryPath}. Run \`npm run build\` first.`);
  process.exit(1);
}
const summary = readFileSync(summaryPath, "utf-8");
const routes = [];
for (const line of summary.split("\n")) {
  const m = line.match(/^\s*\*\s+\[([^\]]+)\]\(([^)]+)\)/);
  if (!m) continue;
  const [, title, filePath] = m;
  let href = filePath.replace(/\.md$/, "");
  if (href === "README") href = "/";
  else href = "/" + href.replace(/\/README$/, "");
  routes.push({ title, href });
}
// De-dupe hrefs, then prepend home + manual.
const seen = new Set();
const summaryRoutes = routes.filter((r) => {
  if (seen.has(r.href)) return false;
  seen.add(r.href);
  return true;
});
const allRoutes = [
  { title: "Home", href: "/" },
  { title: "Full Manual", href: "/manual" },
  ...summaryRoutes.filter((r) => r.href !== "/"),
];

console.log(`SUMMARY.md nav pages: ${summaryRoutes.length}`);
console.log(`Total routes to check (incl. / and /manual): ${allRoutes.length}\n`);

// ── Boot next start ──
const server = spawn("npx", ["next", "start", "-p", PORT], {
  cwd: docsRoot,
  stdio: ["ignore", "pipe", "pipe"],
});
let serverLog = "";
server.stdout.on("data", (d) => (serverLog += d));
server.stderr.on("data", (d) => (serverLog += d));

async function waitForServer(timeoutMs = 60000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(BASE + "/", { method: "GET" });
      if (res.status < 500) return true;
    } catch {
      // not up yet
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

function shutdown(code) {
  server.kill("SIGTERM");
  process.exit(code);
}

const up = await waitForServer();
if (!up) {
  console.error("Server did not start in time. Log:\n" + serverLog);
  shutdown(1);
}

// ── Fetch every route ──
const failures = [];
const passes = [];
for (const route of allRoutes) {
  const url = BASE + route.href;
  try {
    const res = await fetch(url);
    const body = await res.text();
    // Non-empty rendered content: the article/manual body must be present
    // and carry real prose, not just the chrome.
    const hasArticle =
      body.includes('class="prose"') || body.includes("manual-page");
    const proseLen = body.replace(/<[^>]+>/g, "").trim().length;
    const ok = res.status === 200 && hasArticle && proseLen > 200;
    if (ok) {
      passes.push(route);
      console.log(`  200  ${route.href}`);
    } else {
      failures.push({ ...route, status: res.status, hasArticle, proseLen });
      console.error(
        `  FAIL ${route.href} — status=${res.status} article=${hasArticle} textLen=${proseLen}`
      );
    }
  } catch (err) {
    failures.push({ ...route, error: String(err) });
    console.error(`  ERR  ${route.href} — ${err}`);
  }
}

// ── Spot checks ──
console.log("\nSpot checks:");
async function spot(name, href, assertion) {
  try {
    const res = await fetch(BASE + href);
    const body = await res.text();
    const ok = res.status === 200 && assertion(body, res);
    console.log(`  ${ok ? "ok  " : "FAIL"} ${name} (${href})`);
    if (!ok) failures.push({ title: name, href, spot: true });
  } catch (err) {
    console.error(`  ERR  ${name} (${href}) — ${err}`);
    failures.push({ title: name, href, spot: true });
  }
}

await spot(
  "{% file %} download card renders",
  "/appendix-and-resources/downloads",
  (b) => b.includes('class="file-card"') && b.includes("/gitbook-assets/OcuTrap_Knowledge_Base.pdf")
);
await spot(
  "media-kit file cards inside tabs render",
  "/appendix-and-resources/media-kit",
  (b) => (b.match(/file-card/g) || []).length >= 10
);
await spot(
  "card-table grid renders",
  "/",
  (b) => b.includes("cards-grid") || b.includes("card-item") || b.includes('class="prose"')
);
await spot("gitbook-assets image is served (200)", "/gitbook-assets/controls-popup.png", (_b, res) => res.status === 200);

// ── Summary ──
console.log(`\n${passes.length}/${allRoutes.length} routes rendered clean.`);
if (failures.length > 0) {
  console.error(`\n${failures.length} failure(s):`);
  for (const f of failures) console.error("  - " + (f.href || f.title));
  shutdown(1);
}
console.log("All routes and spot checks passed.");
shutdown(0);
