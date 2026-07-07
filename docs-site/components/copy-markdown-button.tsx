"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

// "Copy page as Markdown" — copies the pre-cleaned markdown for the current
// page (produced server-side by markdownToPlain, identical to /llms-full.txt)
// to the clipboard. Shows a check icon for ~2s on success. Sits beside the
// per-page print icon in the article topbar (SITE-09).
export default function CopyMarkdownButton({ markdown }: { markdown: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(markdown);
    } catch {
      // Fallback for browsers/contexts without the async clipboard API.
      const ta = document.createElement("textarea");
      ta.value = markdown;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
      } catch {
        // give up silently
      }
      document.body.removeChild(ta);
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  }

  return (
    <button
      className="print-btn print-btn--icon copy-md-btn"
      onClick={handleCopy}
      aria-label="Copy this page as Markdown"
      title={copied ? "Copied!" : "Copy page as Markdown"}
    >
      {copied ? <Check size={16} /> : <Copy size={16} />}
    </button>
  );
}
