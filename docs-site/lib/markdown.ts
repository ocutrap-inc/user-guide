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

// Transform GitBook-specific syntax into standard markdown and HTML
function preprocessGitBook(content: string): string {
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
          const text = (cells[0] ?? "").replace(/<[^>]+>/g, "").trim();
          return text ? `<div class="card-item">${text}</div>` : "";
        })
        .filter(Boolean);
      return `\n<div class="cards-grid">\n${cards.join("\n")}\n</div>\n`;
    }
  );

  // 6. Normalize .gitbook/assets image paths
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

  // 7. Strip GitBook-specific img attributes (data-size, etc.)
  content = content.replace(/\s+data-size="[^"]*"/g, "");

  // 8. Strip remaining unhandled {% %} tags
  content = content.replace(/\{%[^%]*?%\}/g, "");

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

export async function markdownToHtml(raw: string): Promise<string> {
  const preprocessed = preprocessGitBook(raw);

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

export function extractHeadings(html: string): Heading[] {
  const headings: Heading[] = [];
  const regex = /<h([23])[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/h[23]>/g;
  let match;
  while ((match = regex.exec(html)) !== null) {
    const [, level, id, rawText] = match;
    const text = rawText.replace(/<[^>]+>/g, "").trim();
    headings.push({ id, text, level: parseInt(level) });
  }
  return headings;
}
