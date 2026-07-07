// Tests for the AI-ask endpoint internals (SW-300).
// Run with: npm test   (tsx scripts/test-ask.mts)
//
// No API key and no network required:
//  1. retrieval relevance — a troubleshooting question surfaces the right page
//  2. citation mapping    — chunks collapse to one citation per page
//  3. streaming shape      — answerLines emits citations → deltas → done,
//                            with the Anthropic client mocked
import { retrieve, citationsFor, answerLines, buildSystemPrompt } from "../lib/ask";
import { buildChunkIndex } from "../lib/docs";

let failures = 0;
function check(name: string, cond: boolean, detail = "") {
  if (cond) {
    console.log(`  ✓ ${name}`);
  } else {
    failures++;
    console.error(`  ✗ ${name}${detail ? ` — ${detail}` : ""}`);
  }
}

async function main() {
  console.log("chunk index");
  const chunks = buildChunkIndex();
  check("builds a non-empty chunk index", chunks.length > 0, `got ${chunks.length}`);
  check(
    "chunks carry page/heading/text fields",
    chunks.every((c) => c.pagePath && c.pageTitle && typeof c.text === "string")
  );

  console.log("retrieval relevance");
  const offline = retrieve("why is my trap offline", 6);
  check("returns results for an offline question", offline.length > 0);
  check(
    "top-ranked chunk is the offline/troubleshooting page",
    /offline|troubleshoot|connect/i.test(offline[0]?.pagePath ?? "") ||
      /offline|connect/i.test(offline[0]?.heading ?? "") ||
      /offline|connect/i.test(offline[0]?.pageTitle ?? ""),
    `top pagePath was ${offline[0]?.pagePath}`
  );

  const battery = retrieve("how long does the battery last", 6);
  check("returns results for an unrelated topic too", battery.length > 0);
  check(
    "empty question yields no results",
    retrieve("   ", 6).length === 0
  );

  console.log("citation mapping");
  const dupPage = offline[0]?.pagePath;
  const synthetic = [
    { pagePath: dupPage, pageTitle: "A", heading: "h1", text: "x" },
    { pagePath: dupPage, pageTitle: "A", heading: "h2", text: "y" },
    { pagePath: "/other", pageTitle: "B", heading: "h", text: "z" },
  ];
  const cites = citationsFor(synthetic);
  check("dedupes citations by page", cites.length === 2, `got ${cites.length}`);
  check(
    "citations map to {title, href}",
    cites.every((c) => c.title && c.href.startsWith("/"))
  );

  console.log("prompt grounding");
  const prompt = buildSystemPrompt(offline.slice(0, 3));
  check("system prompt embeds excerpts", prompt.includes("Knowledge-base excerpts"));
  check(
    "system prompt hardens against injection",
    /never as instructions|Treat everything in it as the question/i.test(prompt)
  );

  console.log("streaming shape (mocked Anthropic client)");
  async function* mockDeltas() {
    yield "The trap ";
    yield "is offline ";
    yield "because…";
  }
  const lines: any[] = [];
  for await (const line of answerLines(offline.slice(0, 2), mockDeltas())) {
    lines.push(line);
  }
  check("first line is citations", lines[0]?.type === "citations");
  check(
    "citations line carries the mapped pages",
    Array.isArray(lines[0]?.citations) && lines[0].citations.length > 0
  );
  check(
    "middle lines are deltas in order",
    lines[1]?.type === "delta" &&
      lines[1].text === "The trap " &&
      lines[2]?.text === "is offline " &&
      lines[3]?.text === "because…"
  );
  check("last line is done", lines[lines.length - 1]?.type === "done");

  console.log("streaming shape (mid-stream error is swallowed gracefully)");
  async function* erroringDeltas() {
    yield "partial";
    throw new Error("boom");
  }
  const errLines: any[] = [];
  for await (const line of answerLines([], erroringDeltas())) {
    errLines.push(line);
  }
  check("still terminates with done after an error", errLines[errLines.length - 1]?.type === "done");

  console.log("");
  if (failures > 0) {
    console.error(`FAILED: ${failures} check(s) failed`);
    process.exit(1);
  }
  console.log("All checks passed.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
