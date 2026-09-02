import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkRehype from "remark-rehype";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeHighlight from "rehype-highlight";
import rehypeStringify from "rehype-stringify";
import { absoluteUrl } from "./site";
import {
  ledFenceRegex,
  ledMatrixToMarkdownTable,
  parseLedDiagnostics,
} from "./led-diagnostics";

export type Heading = {
  id: string;
  text: string;
  level: number;
};

const VIDEO_EXTENSIONS = /\.(mp4|webm|mov|ogg|m4v)(\?[^"]*)?$/i;
const YOUTUBE_REGEX =
  /(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
const VIMEO_REGEX = /vimeo\.com\/(\d+)/;

function isVideoUrl(url: string): boolean {
  return VIDEO_EXTENSIONS.test(url);
}

// Best-effort hostname for a bookmark-card title fallback. Strips the
// protocol and a leading "www.", e.g. "https://ocutrap.statuspage.io/" →
// "ocutrap.statuspage.io". Never throws on malformed input.
function hostnameFromUrl(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    const stripped = url.replace(/^[a-z]+:\/\//i, "").replace(/^www\./, "");
    return stripped.split(/[/?#]/)[0] || url;
  }
}

// Host whose bookmark card gets upgraded with a live system-status pill
// (SW-331 / spec SITE-08). Kept narrow so only the OcuTrap status page hydrates.
const STATUSPAGE_HOST = "ocutrap.statuspage.io";

// Render a non-video external URL as a GitBook-style bookmark card: a single
// clickable card (opens in a new tab) with a globe icon, a title line (the
// embed caption if present, else the URL hostname) and the URL as a muted
// second line. No remote fetch — titles are derived locally at build time.
//
// For the OcuTrap Statuspage URL we additionally emit a `data-status-url`
// attribute (the summary JSON endpoint) and a hidden `.bookmark-card__status`
// pill placeholder. A client hydrator (components/status-pill.tsx) fills and
// reveals it at runtime; with JS off — or if the fetch fails — the pill stays
// hidden and the card renders exactly as it did before, so graceful
// degradation is preserved and there is no layout shift (the pill is appended
// after the URL line and takes no space until shown).
function renderBookmarkCard(url: string, caption?: string): string {
  const title = caption && caption.trim() ? caption.trim() : hostnameFromUrl(url);
  const isStatuspage = hostnameFromUrl(url) === STATUSPAGE_HOST;
  const statusAttr = isStatuspage
    ? ` data-status-url="https://${STATUSPAGE_HOST}/api/v2/status.json"`
    : "";
  const statusPill = isStatuspage
    ? `\n<span class="bookmark-card__status" data-status-pill hidden><span class="bookmark-card__status-dot" aria-hidden="true"></span><span class="bookmark-card__status-text"></span></span>`
    : "";
  return `<a href="${url}" class="bookmark-card"${statusAttr} target="_blank" rel="noopener noreferrer">
<span class="bookmark-card__icon" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></span>
<span class="bookmark-card__body">
<span class="bookmark-card__title">${title}</span>
<span class="bookmark-card__url">${url}</span>${statusPill}
</span>
</a>`;
}

function renderEmbed(url: string, caption?: string): string {
  // YouTube
  const ytMatch = url.match(YOUTUBE_REGEX);
  if (ytMatch) {
    return `<div class="video-embed video-embed--youtube">
<iframe
  src="https://www.youtube.com/embed/${ytMatch[1]}"
  title="YouTube video"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen
  loading="lazy"
></iframe>
</div>`;
  }

  // Vimeo
  const vimeoMatch = url.match(VIMEO_REGEX);
  if (vimeoMatch) {
    return `<div class="video-embed video-embed--vimeo">
<iframe
  src="https://player.vimeo.com/video/${vimeoMatch[1]}"
  title="Vimeo video"
  frameborder="0"
  allow="autoplay; fullscreen; picture-in-picture"
  allowfullscreen
  loading="lazy"
></iframe>
</div>`;
  }

  // Direct video file
  if (isVideoUrl(url)) {
    return `<div class="video-embed video-embed--native">
<video controls preload="metadata" playsinline>
  <source src="${url}" type="video/mp4">
  <p>Your browser does not support HTML5 video. <a href="${url}" target="_blank" rel="noopener noreferrer">Download the video</a>.</p>
</video>
<p class="video-embed__open"><a href="${url}" target="_blank" rel="noopener noreferrer">Open video in a new tab</a></p>
</div>`;
  }

  // Any other URL → GitBook-style bookmark card (never an empty box).
  return renderBookmarkCard(url, caption);
}

// Rewrite a GitBook asset path (".gitbook/assets/X") to the served
// "/gitbook-assets/X" path, matching the image handling. Non-asset paths
// (external URLs, etc.) are returned unchanged.
function toAssetHref(src: string): string {
  const marker = ".gitbook/assets/";
  const idx = src.indexOf(marker);
  if (idx === -1) return src.trim();
  return "/gitbook-assets/" + src.slice(idx + marker.length).trim();
}

// Render a `{% file %}` block as a download card/link, styled to match the
// existing content-ref-card. `caption` (block form) overrides the filename
// as the visible label.
function renderFileCard(src: string, caption?: string): string {
  const href = toAssetHref(src);
  const rawName = href.split("/").pop() || href;
  let filename = rawName;
  try {
    filename = decodeURIComponent(rawName);
  } catch {
    // rawName contained a stray "%"; keep it as-is
  }
  // Block-form caption: first line is the card title, an optional second
  // line replaces the default "Download <filename>" hint.
  const lines = (caption ?? "")
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);
  const label = lines[0] ?? filename;
  const hint = lines[1] ?? `Download ${filename}`;
  return `\n<a href="${href}" class="file-card" download>\n<span class="file-card__icon" aria-hidden="true">↓</span>\n<span class="file-card__body">\n<span class="file-card__name">${label}</span>\n<span class="file-card__hint">${hint}</span>\n</span>\n</a>\n`;
}

// GitBook's markdown export sprinkles numeric HTML character references into
// prose as typographic guards — a leading `&#x20;` (space) or `&#x53;` (the
// letter it escapes, e.g. "S") so an adjacent `_emphasis_` marker parses, plus
// an invalid `&#xNAN;` line-start sentinel (sometimes backslash-escaped as
// `\&#xNAN;`). Standard CommonMark decodes the *valid* references, but the
// invalid `&#xNAN;` survives and rehype escapes its `&` to `&#x26;`, so
// customers see a literal "&#xNAN;". Normalize both here — in the pipeline, not
// by editing the GitBook-canonical content — so future exports stay clean too.
//
// Runs on raw markdown but skips fenced code blocks and inline code spans, so
// a literal entity shown as code (or code that merely contains `&#…;`) is left
// untouched.
function normalizeEntity(text: string): string {
  // 1. Drop the invalid GitBook sentinel (with an optional escaping backslash).
  text = text.replace(/\\?&#x?NAN;/gi, "");
  // 2. Decode valid numeric character references (hex then decimal).
  text = text.replace(/&#x([0-9A-Fa-f]+);/g, (_, h) =>
    String.fromCodePoint(parseInt(h, 16))
  );
  text = text.replace(/&#(\d+);/g, (_, d) =>
    String.fromCodePoint(parseInt(d, 10))
  );
  return text;
}

// Apply `fn` to the prose of `content`, leaving fenced code blocks (``` / ~~~)
// and inline code spans untouched. Shared by the entity decoders and the
// residual-HTML stripper so neither mangles literal markup shown as code.
function applyOutsideCode(
  content: string,
  fn: (chunk: string) => string
): string {
  const codePattern = /(```[\s\S]*?```|~~~[\s\S]*?~~~|(`+)[\s\S]*?\2)/g;
  let result = "";
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = codePattern.exec(content)) !== null) {
    result += fn(content.slice(last, m.index));
    result += m[0];
    last = m.index + m[0].length;
  }
  result += fn(content.slice(last));
  return result;
}

function decodeGitBookEntities(content: string): string {
  return applyOutsideCode(content, normalizeEntity);
}

// Transform GitBook-specific syntax into standard markdown and HTML.
// `sourcePath` (optional) is used only for build-time warnings.
function preprocessGitBook(content: string, sourcePath?: string): string {
  // 0. Normalize GitBook's HTML-entity guards before anything else parses.
  content = decodeGitBookEntities(content);

  // 0.5. LED diagnostic block (SW-333 / SITE-10). The ```led-diagnostics fenced
  //      block is structured data, not display content: the interactive wizard
  //      (rendered above the article by the page route) owns the on-page
  //      rendering — it shows an accessible fallback table built from this same
  //      data when JS is off. So strip the block here rather than letting it
  //      render as a raw YAML code block. The plain-markdown pipeline
  //      (markdownToPlain) instead expands it into a real markdown table for
  //      llms.txt / copy-as-markdown / search / print corpora.
  content = content.replace(ledFenceRegex(), "");

  // 1. Hint/callout blocks
  content = content.replace(
    /\{%\s*hint\s+style="(\w+)"\s*%\}([\s\S]*?)\{%\s*endhint\s*%\}/g,
    (_, style, inner) =>
      `\n<div class="hint hint-${style}">\n\n${inner.trim()}\n\n</div>\n`
  );

  // 2. Content-ref blocks → styled reference link. URLs are relative to the
  //    source page's directory (same SW-336 bug class as inline links —
  //    rooting the raw value turns `setting-up.md` into a 404 at /setting-up),
  //    so resolve through resolveKbHref; the fallback keeps old behavior for
  //    already-absolute paths.
  content = content.replace(
    /\{%\s*content-ref\s+url="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endcontent-ref\s*%\}/g,
    (_, url, inner) => {
      const linkMatch = inner.match(/\[([^\]]+)\]/);
      const title = linkMatch ? linkMatch[1] : url;
      const href =
        resolveKbHref(url, sourcePath) ??
        "/" +
          url
            .replace(/\.md$/, "")
            .replace(/\/README$/, "")
            .replace(/^\//, "");
      return `\n<a href="${href}" class="content-ref-card">${title}</a>\n`;
    }
  );

  // 3. Embed blocks — render as video, iframe, or bookmark card based on URL
  //    type. Both forms are handled and an optional `caption="…"` attribute
  //    (or the inner text of the block form) becomes the bookmark-card title.
  //    The attribute blob is captured with a tempered pattern that allows `%`
  //    inside URL-encoded URLs (e.g. GitBook `…spaces%2F…`) but stops at the
  //    closing `%}` delimiter.
  const embedAttrs = "((?:[^%]|%(?!\\}))*?)";
  //    Block form first: {% embed url="…" %}caption{% endembed %}.
  content = content.replace(
    new RegExp(`\\{%\\s*embed\\s+${embedAttrs}\\s*%\\}([\\s\\S]*?)\\{%\\s*endembed\\s*%\\}`, "g"),
    (_, attrs, inner) => {
      const url = (attrs.match(/url="([^"]+)"/) || [])[1];
      if (!url) return "";
      const caption = (attrs.match(/caption="([^"]*)"/) || [])[1] || inner.trim();
      return `\n${renderEmbed(url, caption)}\n`;
    }
  );
  //    Then the self-closing form: {% embed url="…" (caption="…")? %}.
  content = content.replace(
    new RegExp(`\\{%\\s*embed\\s+${embedAttrs}\\s*%\\}`, "g"),
    (_, attrs) => {
      const url = (attrs.match(/url="([^"]+)"/) || [])[1];
      if (!url) return "";
      const caption = (attrs.match(/caption="([^"]*)"/) || [])[1];
      return `\n${renderEmbed(url, caption)}\n`;
    }
  );

  // 4. Tab groups → data-attribute tab structure
  content = content.replace(
    /\{%\s*tabs\s*%\}([\s\S]*?)\{%\s*endtabs\s*%\}/g,
    (_, tabsContent) => {
      const tabs: { title: string; content: string }[] = [];
      const tabRegex =
        /\{%\s*tab\s+title="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endtab\s*%\}/g;
      let match;
      while ((match = tabRegex.exec(tabsContent)) !== null) {
        tabs.push({ title: match[1], content: match[2].trim() });
      }
      if (tabs.length === 0) return "";

      const buttons = tabs
        .map(
          (t, i) =>
            `<button class="tab-btn${i === 0 ? " tab-btn--active" : ""}" data-tab="${i}">${t.title}</button>`
        )
        .join("\n");

      const panels = tabs
        .map(
          (t, i) =>
            `<div class="tab-panel${i === 0 ? "" : " tab-panel--hidden"}" data-panel="${i}">\n\n${t.content}\n\n</div>`
        )
        .join("\n");

      return `\n<div class="tabs-container">\n<div class="tabs-nav">\n${buttons}\n</div>\n${panels}\n</div>\n`;
    }
  );

  // 5. GitBook card tables → card grid
  content = content.replace(
    /<table[^>]*data-view="cards"[^>]*>([\s\S]*?)<\/table>/g,
    (_, inner) => {
      const rows = inner.match(/<tr>([\s\S]*?)<\/tr>/g) ?? [];
      const cards = rows
        .slice(1)
        .map((row: string) => {
          const cells = row.match(/<td[^>]*>([\s\S]*?)<\/td>/g) ?? [];
          if (cells.length === 0) return "";

          const strip = (html: string) =>
            html.replace(/<[^>]+>/g, "").trim();
          const title = strip(cells[0] ?? "");
          if (!title) return "";

          let description = "";
          let href = "";
          for (const cell of cells.slice(1)) {
            const linkMatch = cell.match(/href="([^"]+)"/);
            if (linkMatch) {
              href = linkMatch[1];
            } else if (!description) {
              const text = strip(cell);
              if (text) description = text;
            }
          }
          if (!href) return "";

          const url =
            "/" +
            href
              .replace(/\.md$/, "")
              .replace(/\/README$/, "")
              .replace(/^\//, "")
              .replace(/\/$/, "");

          const descHtml = description
            ? `<span class="card-item__desc">${description}</span>`
            : "";
          return `<a href="${url}" class="card-item"><span class="card-item__title">${title}</span>${descHtml}</a>`;
        })
        .filter(Boolean);
      return `\n<div class="cards-grid">\n${cards.join("\n")}\n</div>\n`;
    }
  );

  // 6. File download blocks → download card/link
  //    Block form first (inner text is used as the caption), then the
  //    self-closing form. Runs before image-path normalization; asset
  //    paths are rewritten to /gitbook-assets/ inside renderFileCard.
  content = content.replace(
    /\{%\s*file\s+src="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endfile\s*%\}/g,
    (_, src, caption) => renderFileCard(src, caption)
  );
  content = content.replace(
    /\{%\s*file\s+src="([^"]+)"\s*%\}/g,
    (_, src) => renderFileCard(src)
  );

  // 7. Normalize .gitbook/assets image paths
  content = content.replace(
    /src="[^"]*\.gitbook\/assets\/([^"]+)"/g,
    (_, filename) => {
      // If it's a video file, will be handled post-processing
      return `src="/gitbook-assets/${filename}"`;
    }
  );
  content = content.replace(
    /srcset="[^"]*\.gitbook\/assets\/([^"]+)"/g,
    'srcset="/gitbook-assets/$1"'
  );

  // 8. Strip GitBook-specific img attributes (data-size, etc.)
  content = content.replace(/\s+data-size="[^"]*"/g, "");

  // 9. Fallback for any remaining unhandled GitBook tags.
  //    Instead of silently deleting them (which made new GitBook constructs
  //    vanish without a trace), preserve the inner content of paired tags,
  //    drop only the tag markup of self-closing tags, and emit a build-time
  //    warning naming the tag and the source file so it gets a real transform.
  const warnUnhandled = (tag: string) =>
    console.warn(
      `[markdown] Unhandled GitBook tag {% ${tag} %} in ${
        sourcePath ?? "unknown file"
      } — content preserved; add a transform in lib/markdown.ts`
    );

  // Paired tags: {% x ... %}...{% endx %} → keep inner content, warn.
  content = content.replace(
    /\{%\s*([\w-]+)[^%]*%\}([\s\S]*?)\{%\s*end\1\s*%\}/g,
    (_, tag, inner) => {
      warnUnhandled(tag);
      return inner;
    }
  );

  // Remaining self-closing / orphan tags → drop markup, keep surrounding text, warn.
  content = content.replace(/\{%\s*([\w-]+)[^%]*%\}/g, (_, tag) => {
    warnUnhandled(tag);
    return "";
  });

  return content;
}

/** Post-process HTML: convert <img src="*.mp4"> to <video> elements */
function convertVideoImgs(html: string): string {
  return html.replace(
    /<img([^>]*?)src="([^"]+\.(?:mp4|webm|mov|ogg|m4v)[^"]*)"([^>]*?)>/gi,
    (_, before, src, after) => {
      const altMatch = (before + after).match(/alt="([^"]*)"/);
      const altText = altMatch ? altMatch[1] : "";
      return `<div class="video-embed video-embed--native">
<video controls preload="metadata" playsinline title="${altText}">
  <source src="${src}" type="video/mp4">
  <p><a href="${src}" target="_blank" rel="noopener noreferrer">Download video</a></p>
</video>
<p class="video-embed__open"><a href="${src}" target="_blank" rel="noopener noreferrer">Open video in a new tab</a></p>
</div>`;
    }
  );
}

/**
 * Post-process HTML: rewrite relative inline links (`set-up-tutorial.md`,
 * `../faqs/battery.md`, `trap-settings/README.md#x`) into absolute site
 * routes, resolved against the source page's directory. GitBook resolved
 * these itself; without this pass they leak into hrefs and 404 on click.
 * Absolute paths, schemes (`https:`, `mailto:`), and pure anchors pass
 * through untouched.
 */
/**
 * Resolve a relative doc/asset reference against the source page's KB
 * directory into a site-absolute path ("/getting-started/faqs/battery",
 * "/gitbook-assets/pic.png"). Returns null for hrefs that need no rewrite
 * (absolute paths, schemes, pure anchors). Anchors/queries are preserved.
 */
function resolveKbHref(href: string, sourcePath?: string): string | null {
  if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|#|\/)/i.test(href)) return null;
  const dir = sourcePath ? sourcePath.split("/").slice(0, -1).join("/") : "";
  const cut = href.search(/[#?]/);
  const relPath = cut === -1 ? href : href.slice(0, cut);
  const suffix = cut === -1 ? "" : href.slice(cut);
  const stack: string[] = [];
  for (const seg of `${dir}/${relPath}`.split("/")) {
    if (!seg || seg === ".") continue;
    if (seg === "..") stack.pop();
    else stack.push(seg);
  }
  let resolved = stack.join("/");
  // Assets referenced relatively map to the copied public dir.
  const assetIdx = resolved.indexOf(".gitbook/assets/");
  if (assetIdx !== -1) {
    return `/gitbook-assets/${resolved.slice(assetIdx + ".gitbook/assets/".length)}${suffix}`;
  }
  resolved = resolved
    .replace(/\.md$/i, "")
    .replace(/(^|\/)README$/i, "$1")
    .replace(/\/+$/, "");
  return `/${resolved}${suffix}`;
}

function resolveInternalLinks(html: string, sourcePath?: string): string {
  return html.replace(
    /(<a\b[^>]*?\shref=")([^"]+)(")/g,
    (whole, pre, href, post) => {
      const resolved = resolveKbHref(href, sourcePath);
      return resolved === null ? whole : `${pre}${resolved}${post}`;
    }
  );
}

// Same rewrite for image/video sources. The preprocessor's src= pass only
// sees raw-HTML tags in the markdown source; markdown-syntax images
// (`![](../.gitbook/assets/x.png)`) become <img> only after remark renders
// them, so their relative asset paths reached prod unrewritten and 404'd.
function resolveImageSrcs(html: string, sourcePath?: string): string {
  return html.replace(
    /(<(?:img|source)\b[^>]*?\ssrc=")([^"]+)(")/g,
    (whole, pre, src, post) => {
      const resolved = resolveKbHref(src, sourcePath);
      return resolved === null ? whole : `${pre}${resolved}${post}`;
    }
  );
}

export async function markdownToHtml(
  raw: string,
  sourcePath?: string
): Promise<string> {
  const preprocessed = preprocessGitBook(raw, sourcePath);

  const result = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
    .use(rehypeAutolinkHeadings, {
      behavior: "wrap",
      properties: { class: "heading-anchor" },
    })
    .use(rehypeHighlight, { detect: true, ignoreMissing: true })
    .use(rehypeStringify)
    .process(preprocessed);

  return resolveImageSrcs(
    resolveInternalLinks(convertVideoImgs(String(result)), sourcePath),
    sourcePath
  );
}

// Decode the HTML entities rehype emits (numeric + the common named ones) back
// to their characters. Heading text is pulled from *rendered* HTML where `&`
// becomes `&#x26;` etc.; the TOC prints it as a plain React string (no browser
// decode), so without this it shows the raw entity. (B10)
function decodeEntities(s: string): string {
  return s
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) =>
      String.fromCodePoint(parseInt(h, 16))
    )
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)))
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&");
}

export function extractHeadings(html: string): Heading[] {
  const headings: Heading[] = [];
  const regex = /<h([23])[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/h[23]>/g;
  let match;
  while ((match = regex.exec(html)) !== null) {
    const [, level, id, rawText] = match;
    const text = decodeEntities(rawText.replace(/<[^>]+>/g, "")).trim();
    headings.push({ id, text, level: parseInt(level) });
  }
  return headings;
}

// ── Plain-markdown pipeline (SITE-09) ────────────────────────────────
// Convert GitBook-flavored source markdown into clean, portable CommonMark
// with no GitBook `{% … %}` tags, no numeric/HTML-entity artifacts, and no
// leftover HTML — suitable for feeding to AI assistants (`/llms-full.txt`)
// and for the per-page "Copy page as Markdown" button. Both consumers call
// this single helper so their output is byte-identical.

// GitBook hint style → GitHub-flavored alert keyword.
const HINT_ALERT: Record<string, string> = {
  info: "NOTE",
  success: "TIP",
  warning: "WARNING",
  danger: "CAUTION",
};

// Resolve an image/asset reference to an absolute, portable URL. GitBook
// asset paths ("../.gitbook/assets/X") become absolute /gitbook-assets/ URLs
// (spaces percent-encoded so the link stays valid); other URLs pass through.
function plainAssetUrl(src: string): string {
  const clean = src.replace(/^</, "").replace(/>$/, "").trim();
  if (clean.includes(".gitbook/assets/")) {
    return absoluteUrl(toAssetHref(clean).replace(/ /g, "%20"));
  }
  return clean;
}

// A `{% file %}` reference → a plain markdown download link line.
function plainFileLink(src: string, caption?: string): string {
  const url = plainAssetUrl(src);
  const rawName = url.split("/").pop() || url;
  let filename = rawName;
  try {
    filename = decodeURIComponent(rawName);
  } catch {
    // keep rawName as-is if it contains a stray "%"
  }
  const label = caption && caption.trim() ? caption.trim() : filename;
  return `\n[${label}](${url})\n`;
}

// Decode numeric + the common named HTML entities for plain output. (The HTML
// pipeline lets rehype decode named entities; plain text has no renderer, so
// we do it here.) Runs on prose only, via applyOutsideCode.
function normalizePlainEntity(text: string): string {
  text = normalizeEntity(text); // NAN sentinel + numeric refs
  return text
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, "&");
}

// Drop residual inline/block HTML tags (keeping their text) so the output is
// pure markdown. Runs on prose only so `<tags>` shown inside code survive.
function stripResidualHtml(text: string): string {
  return text
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/?(?:figure|picture|figcaption|source|div|span)[^>]*>/gi, "")
    .replace(/<\/?[a-zA-Z][^>]*>/g, "");
}

export function markdownToPlain(content: string, sourcePath?: string): string {
  // 0. LED diagnostic block (SW-333 / SITE-10) → real markdown table so the
  //    AI corpus, "Copy as Markdown", search index and print all carry the
  //    color/pattern/meaning matrix. Same single source as the wizard.
  content = content.replace(ledFenceRegex(), (block) => {
    const matrix = parseLedDiagnostics(block);
    return matrix ? `\n${ledMatrixToMarkdownTable(matrix)}\n` : "";
  });

  // 1. Hint/callout → GitHub-flavored alert blockquote.
  content = content.replace(
    /\{%\s*hint\s+style="(\w+)"\s*%\}([\s\S]*?)\{%\s*endhint\s*%\}/g,
    (_, style, inner) => {
      const alert = HINT_ALERT[style] ?? "NOTE";
      const body = inner
        .trim()
        .split("\n")
        .map((line: string) => `> ${line}`.replace(/\s+$/, ""))
        .join("\n");
      return `\n> [!${alert}]\n${body}\n`;
    }
  );

  // 2. Content-ref → plain markdown link (absolute URL). URLs resolve against
  //    the source page's directory via resolveKbHref (same SW-336 bug class as
  //    inline links — prefix-stripping alone 404s same-dir refs), and a
  //    filename-style link label is humanized ("support.md" → "Support").
  content = content.replace(
    /\{%\s*content-ref\s+url="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endcontent-ref\s*%\}/g,
    (_, url, inner) => {
      const href =
        resolveKbHref(url, sourcePath) ??
        "/" +
          url
            .replace(/\.md$/, "")
            .replace(/\/README$/, "")
            .replace(/^(?:\.\.?\/)+/, "")
            .replace(/^\//, "");
      const linkMatch = inner.match(/\[([^\]]+)\]/);
      let title = linkMatch ? linkMatch[1].trim() : href;
      if (/\.md$/i.test(title)) {
        title = (title.replace(/\.md$/i, "").split("/").pop() || title)
          .replace(/[-_]/g, " ")
          .replace(/\b\w/g, (c: string) => c.toUpperCase());
      }
      return `\n[${title}](${absoluteUrl(href)})\n`;
    }
  );

  // 3. Embed → a URL line (or `[caption](url)` when captioned). Same tempered
  //    attribute pattern as the HTML pipeline so URL-encoded `%` survives.
  const embedAttrs = "((?:[^%]|%(?!\\}))*?)";
  content = content.replace(
    new RegExp(
      `\\{%\\s*embed\\s+${embedAttrs}\\s*%\\}([\\s\\S]*?)\\{%\\s*endembed\\s*%\\}`,
      "g"
    ),
    (_, attrs, inner) => {
      const url = (attrs.match(/url="([^"]+)"/) || [])[1];
      if (!url) return "";
      const caption = (attrs.match(/caption="([^"]*)"/) || [])[1] || inner.trim();
      return caption ? `\n[${caption}](${url})\n` : `\n${url}\n`;
    }
  );
  content = content.replace(
    new RegExp(`\\{%\\s*embed\\s+${embedAttrs}\\s*%\\}`, "g"),
    (_, attrs) => {
      const url = (attrs.match(/url="([^"]+)"/) || [])[1];
      if (!url) return "";
      const caption = (attrs.match(/caption="([^"]*)"/) || [])[1];
      return caption ? `\n[${caption}](${url})\n` : `\n${url}\n`;
    }
  );

  // 4. Tab groups → flattened sections, each tab label a bold line.
  content = content.replace(
    /\{%\s*tabs\s*%\}([\s\S]*?)\{%\s*endtabs\s*%\}/g,
    (_, tabsContent) => {
      const parts: string[] = [];
      const tabRegex =
        /\{%\s*tab\s+title="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endtab\s*%\}/g;
      let match;
      while ((match = tabRegex.exec(tabsContent)) !== null) {
        const body = match[2].trim();
        parts.push(body ? `**${match[1].trim()}**\n\n${body}` : `**${match[1].trim()}**`);
      }
      return parts.length ? `\n${parts.join("\n\n")}\n` : "";
    }
  );

  // 5. File download blocks → link line (block form carries a caption).
  content = content.replace(
    /\{%\s*file\s+src="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endfile\s*%\}/g,
    (_, src, caption) => plainFileLink(src, caption)
  );
  content = content.replace(
    /\{%\s*file\s+src="([^"]+)"\s*%\}/g,
    (_, src) => plainFileLink(src)
  );

  // 6. HTML `<figure>` (incl. `<picture>`) → a markdown image, preferring the
  //    figcaption then the img alt as the label.
  content = content.replace(/<figure>[\s\S]*?<\/figure>/gi, (block) => {
    const src = (block.match(/<img[^>]*\ssrc="([^"]+)"/i) || [])[1];
    if (!src) return "";
    const alt = (block.match(/<img[^>]*\salt="([^"]*)"/i) || [])[1] || "";
    const cap = (block.match(/<figcaption>([\s\S]*?)<\/figcaption>/i) || [])[1]
      ?.replace(/<[^>]+>/g, "")
      .trim();
    return `\n![${cap || alt}](${plainAssetUrl(src)})\n`;
  });

  // 7. Any remaining bare `<img>` → markdown image.
  content = content.replace(/<img\b[^>]*>/gi, (tag) => {
    const src = (tag.match(/\ssrc="([^"]+)"/i) || [])[1];
    if (!src) return "";
    const alt = (tag.match(/\salt="([^"]*)"/i) || [])[1] || "";
    return `![${alt}](${plainAssetUrl(src)})`;
  });

  // 8. Markdown images pointing at GitBook assets → absolute URLs. Handles the
  //    angle-bracket form GitBook uses for paths containing spaces.
  content = content.replace(
    /(!\[[^\]]*\]\()<?([^)>]*\.gitbook\/assets\/[^)>]*)>?(\))/g,
    (_, pre, src, post) => `${pre}${plainAssetUrl(src)}${post}`
  );

  // 9. Fallback for any unhandled GitBook tags: keep inner content of paired
  //    tags, drop self-closing markup. (Silent here — the HTML pipeline already
  //    emits the build-time warning for unknown tags.)
  content = content.replace(
    /\{%\s*([\w-]+)[^%]*%\}([\s\S]*?)\{%\s*end\1\s*%\}/g,
    (_, _tag, inner) => inner
  );
  content = content.replace(/\{%\s*[\w-]+[^%]*%\}/g, "");

  // 10. Strip residual HTML, then decode entities (order matters: a decoded
  //     `<` from `&lt;` must not then be treated as a tag).
  content = applyOutsideCode(content, stripResidualHtml);
  content = applyOutsideCode(content, normalizePlainEntity);

  // 11. Resolve relative inline links/images against the source page's
  //     directory and emit absolute site URLs — same bug class as the HTML
  //     pipeline's resolveInternalLinks (SW-335): GitBook resolved these
  //     itself, and an AI assistant quoting the corpus would otherwise hand
  //     users dead `../foo.md` links.
  if (sourcePath) {
    content = applyOutsideCode(content, (chunk) =>
      chunk.replace(
        /(!?)\[([^\]]*)\]\(([^)\s]+)((?:\s+"[^"]*")?)\)/g,
        (whole, bang, label, target, title) => {
          const resolved = resolveKbHref(target, sourcePath);
          if (resolved === null) return whole;
          // Drop GitBook's editor-only `"mention"` titles; keep real ones.
          const keptTitle = title.trim() === '"mention"' ? "" : title;
          return `${bang}[${label}](${absoluteUrl(resolved.replace(/ /g, "%20"))}${keptTitle})`;
        }
      )
    );
  }

  // 12. Tidy whitespace.
  return content
    .replace(/[ \t]+$/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}
