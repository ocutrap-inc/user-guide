/**
 * Fixture test for the GitBook markdown pipeline (SITE-01 / SW-298).
 *
 * Exercises lib/markdown.ts directly (Node 22+/24 strips the TS types):
 *   1. An unrecognized `{% foo %}...{% endfoo %}` tag renders its inner
 *      content and emits a build-time warning naming the tag and file.
 *   2. A `{% file %}` block renders a working download link with the
 *      .gitbook/assets path rewritten to /gitbook-assets/.
 *
 * No test framework — run with `node scripts/test-unknown-tag.mjs`.
 * Exits non-zero on any failed assertion.
 */
import { markdownToHtml } from "../lib/markdown.ts";

let failures = 0;
function check(name, cond) {
  if (cond) {
    console.log(`  ok   ${name}`);
  } else {
    console.error(`  FAIL ${name}`);
    failures++;
  }
}

// Capture build-time warnings.
const warnings = [];
const origWarn = console.warn;
console.warn = (...args) => {
  warnings.push(args.join(" "));
};

const fixture = `# Fixture

{% foo bar="baz" %}
This paragraph must survive an unknown block tag.
{% endfoo %}

{% widget id="42" %}

{% file src="../.gitbook/assets/OcuTrap_Knowledge_Base.pdf" %}

{% file src="../.gitbook/assets/OcuTrap_PDF.pdf" %}Marketing one-pager{% endfile %}

{% embed url="https://ocutrap.statuspage.io/" %}

{% embed url="https://files.example.com/clip.mp4?token=abc" %}

{% embed url="https://example.com/page" caption="Custom title" %}

> &#xNAN;_&#x53;ettings → Trap Info → Firmware_ should show v706.

> \&#xNAN;_Settings → Device Info_ shows the build.

Inline code keeps entities literal: \`&#x53;ettings\`.
`;

const html = await markdownToHtml(fixture, "scripts/fixtures/unknown-tag.md");
console.warn = origWarn;

console.log("Unknown-tag guard:");
check(
  "inner content of unknown paired tag is preserved",
  html.includes("This paragraph must survive an unknown block tag.")
);
check(
  "raw {% %} markup does not leak into output",
  !html.includes("{%") && !html.includes("%}")
);
check(
  "warning names the unknown paired tag 'foo' and the source file",
  warnings.some((w) => w.includes("{% foo %}") && w.includes("scripts/fixtures/unknown-tag.md"))
);
check(
  "warning names the unknown self-closing tag 'widget'",
  warnings.some((w) => w.includes("{% widget %}"))
);

console.log("File download blocks:");
check(
  "self-closing {% file %} renders a download link",
  html.includes('class="file-card"') && html.includes('download')
);
check(
  ".gitbook/assets path is rewritten to /gitbook-assets/",
  html.includes('href="/gitbook-assets/OcuTrap_Knowledge_Base.pdf"')
);
check(
  "self-closing file uses the filename as its label",
  html.includes("OcuTrap_Knowledge_Base.pdf")
);
check(
  "block-form {% file %} caption overrides the filename label",
  html.includes("Marketing one-pager") &&
    html.includes('href="/gitbook-assets/OcuTrap_PDF.pdf"')
);

console.log("Embed blocks:");
check(
  "non-video {% embed %} renders a bookmark card (not an empty box)",
  html.includes('class="bookmark-card"') &&
    html.includes('href="https://ocutrap.statuspage.io/"')
);
check(
  "bookmark card without a caption falls back to the URL hostname",
  html.includes('class="bookmark-card__title">ocutrap.statuspage.io<')
);
check(
  "video-URL {% embed %} still renders a <video>, not a bookmark card",
  html.includes("video-embed--native") &&
    html.includes('src="https://files.example.com/clip.mp4?token=abc"')
);
check(
  "{% embed %} caption attribute becomes the bookmark-card title",
  html.includes('class="bookmark-card__title">Custom title<')
);
check(
  "no leftover empty embed-block from the old fallback",
  !html.includes('class="embed-block"')
);

console.log("GitBook HTML-entity guards:");
check(
  "invalid &#xNAN; sentinel is stripped from prose (no visible &#x)",
  !html.includes("#xNAN")
);
check(
  "valid &#x53; decodes so escaped emphasis reads 'Settings'",
  html.includes("<em>Settings → Trap Info → Firmware</em>")
);
check(
  "backslash-escaped \\&#xNAN; is also removed",
  html.includes("<em>Settings → Device Info</em>")
);
check(
  "entities inside inline code are left literal (not decoded)",
  html.includes("<code>&#x26;#x53;ettings</code>")
);

console.log("Relative inline-link resolution:");
const linkMd = [
  "[sibling](set-up-tutorial.md)",
  "[up](../../faqs/battery.md#top)",
  "[dir index](trap-settings/README.md)",
  "[abs kept](/troubleshooting/common-issues)",
  "[ext kept](https://example.com/a.md)",
  "[asset](../../.gitbook/assets/pic.png)",
].join("\n\n");
const linkHtml = await markdownToHtml(linkMd, "getting-started/app/logs.md");
check(
  "sibling .md resolves against the page's directory",
  linkHtml.includes('href="/getting-started/app/set-up-tutorial"')
);
check(
  "../ traversal resolves and preserves the anchor",
  linkHtml.includes('href="/faqs/battery#top"')
);
check(
  "README.md maps to the directory route",
  linkHtml.includes('href="/getting-started/app/trap-settings"')
);
check(
  "absolute path passes through untouched",
  linkHtml.includes('href="/troubleshooting/common-issues"')
);
check(
  "external URL passes through untouched",
  linkHtml.includes('href="https://example.com/a.md"')
);
check(
  "relative asset link maps to /gitbook-assets/",
  linkHtml.includes('href="/gitbook-assets/pic.png"')
);

if (failures > 0) {
  console.error(`\n${failures} assertion(s) failed.`);
  process.exit(1);
}
console.log("\nAll assertions passed.");
