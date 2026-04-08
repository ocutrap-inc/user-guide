"use client";

import { useEffect, useState } from "react";
import type { Heading } from "@/lib/markdown";

export default function TableOfContents({ headings }: { headings: Heading[] }) {
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    if (headings.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        }
      },
      { rootMargin: "-80px 0px -60% 0px" }
    );

    for (const heading of headings) {
      const el = document.getElementById(heading.id);
      if (el) observer.observe(el);
    }

    return () => observer.disconnect();
  }, [headings]);

  if (headings.length === 0) return null;

  return (
    <div className="toc">
      <div className="toc-title">On this page</div>
      <nav aria-label="Table of contents">
        {headings.map((h) => (
          <a
            key={h.id}
            href={`#${h.id}`}
            className={`toc-link${h.level === 3 ? " toc-link--h3" : ""}${activeId === h.id ? " toc-link--active" : ""}`}
          >
            {h.text}
          </a>
        ))}
      </nav>
    </div>
  );
}
