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

function renderEmbed(url: string): string {
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

  // Generic external link
  return `<a href="${url}" class="embed-block" target="_blank" rel="noopener noreferrer">${url}</a>`;
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

// Transform GitBook-specific syntax into standard markdown and HTML.
// `sourcePath` (optional) is used only for build-time warnings.
function preprocessGitBook(content: string, sourcePath?: string): string {
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

  // 3. Embed blocks — render as video, iframe, or link based on URL type
  content = content.replace(
    /\{%\s*embed\s+url="([^"]+)"\s*%\}/g,
    (_, url) => `\n${renderEmbed(url)}\n`
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
