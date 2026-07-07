import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkRehype from "remark-rehype";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeHighlight from "rehype-highlight";
import rehypeStringify from "rehype-stringify";

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

// Render a non-video external URL as a GitBook-style bookmark card: a single
// clickable card (opens in a new tab) with a globe icon, a title line (the
// embed caption if present, else the URL hostname) and the URL as a muted
// second line. No remote fetch — titles are derived locally at build time.
function renderBookmarkCard(url: string, caption?: string): string {
  const title = caption && caption.trim() ? caption.trim() : hostnameFromUrl(url);
  return `<a href="${url}" class="bookmark-card" target="_blank" rel="noopener noreferrer">
<span class="bookmark-card__icon" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></span>
<span class="bookmark-card__body">
<span class="bookmark-card__title">${title}</span>
<span class="bookmark-card__url">${url}</span>
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
  <source src="${url}">
  <p>Your browser does not support HTML5 video. <a href="${url}" target="_blank" rel="noopener noreferrer">Download the video</a>.</p>
</video>
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
  const label = caption && caption.trim() ? caption.trim() : filename;
  return `\n<a href="${href}" class="file-card" download>\n<span class="file-card__icon" aria-hidden="true">↓</span>\n<span class="file-card__body">\n<span class="file-card__name">${label}</span>\n<span class="file-card__hint">Download ${filename}</span>\n</span>\n</a>\n`;
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

function decodeGitBookEntities(content: string): string {
  // Preserve fenced blocks (``` / ~~~) and inline code spans verbatim; apply
  // the entity normalization only to the prose between them.
  const codePattern = /(```[\s\S]*?```|~~~[\s\S]*?~~~|(`+)[\s\S]*?\2)/g;
  let result = "";
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = codePattern.exec(content)) !== null) {
    result += normalizeEntity(content.slice(last, m.index));
    result += m[0];
    last = m.index + m[0].length;
  }
  result += normalizeEntity(content.slice(last));
  return result;
}

// Transform GitBook-specific syntax into standard markdown and HTML.
// `sourcePath` (optional) is used only for build-time warnings.
function preprocessGitBook(content: string, sourcePath?: string): string {
  // 0. Normalize GitBook's HTML-entity guards before anything else parses.
  content = decodeGitBookEntities(content);

  // 1. Hint/callout blocks
  content = content.replace(
    /\{%\s*hint\s+style="(\w+)"\s*%\}([\s\S]*?)\{%\s*endhint\s*%\}/g,
    (_, style, inner) =>
      `\n<div class="hint hint-${style}">\n\n${inner.trim()}\n\n</div>\n`
  );

  // 2. Content-ref blocks → styled reference link
  content = content.replace(
    /\{%\s*content-ref\s+url="([^"]+)"\s*%\}([\s\S]*?)\{%\s*endcontent-ref\s*%\}/g,
    (_, url, inner) => {
      const linkMatch = inner.match(/\[([^\]]+)\]/);
      const title = linkMatch ? linkMatch[1] : url;
      const href =
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
  <source src="${src}">
  <p><a href="${src}" target="_blank" rel="noopener noreferrer">Download video</a></p>
</video>
</div>`;
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

  return convertVideoImgs(String(result));
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
