import assert from "node:assert/strict";
import { buildSearchIndex, getHomeDoc } from "../lib/docs.ts";
import { createSearchEngine, searchDocuments } from "../lib/search.ts";

const docs = buildSearchIndex();
assert.ok(docs.length > 50, "Load the published documentation corpus");
const engine = createSearchEngine(docs);
for (const query of ["Actuator Inverse", "Camera Quality", "Dark Lux Threshold", "Maximum IR Brightness"]) {
  const hits = searchDocuments(engine, query);
  const settings = hits.find((doc) => doc.href.endsWith("/settings-reference"));
  assert.ok(settings, `${query}: settings reference appears among the first eight matches`);
  assert.ok(settings.excerpt.toLowerCase().includes(query.toLowerCase()), `${query}: show a relevant snippet`);
  console.log(`PASS ${query}: ${hits[0].title}`);
}
assert.ok(searchDocuments(engine, "Actuator Inveres").some((doc) => doc.href.endsWith("/settings-reference")), "Tolerate a typo in a deep article term");
assert.equal(searchDocuments(engine, "").length, 0);
assert.equal(searchDocuments(engine, "zzzzqqqqvvvvxxxx").length, 0);
const oldCache = createSearchEngine([{ title: "Battery overview", href: "/battery", section: "Getting started", excerpt: "Charge the battery before setup." }]);
assert.equal(searchDocuments(oldCache, "battery")[0].href, "/battery", "Old offline indexes without full text still work");
assert.equal(getHomeDoc()?.next?.href, "/getting-started/setup", "Home Next advances to setup");
console.log("PASS typo, no-match, legacy cache, homepage navigation");
