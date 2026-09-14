"use client";

import { useEffect, useState, useRef } from "react";
import type { Heading } from "@/lib/markdown";

export default function TableOfContents({ headings, compact = false }: { headings: Heading[]; compact?: boolean }) {
  const [activeId, setActiveId] = useState<string>("");
  const detailsRef = useRef<HTMLDetailsElement>(null);

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

  const links = (
      <nav aria-label="Table of contents">
        {headings.map((h) => (
          <a
            key={h.id}
            href={`#${h.id}`}
            onClick={(event) => {
              if (!compact) return;
              const heading = document.getElementById(h.id);
              if (!heading) return;
              event.preventDefault();
              if (detailsRef.current) detailsRef.current.open = false;
              heading.tabIndex = -1;
              heading.focus({ preventScroll: true });
              heading.scrollIntoView({ block: "start" });
              history.replaceState(null, "", `#${h.id}`);
              setActiveId(h.id);
            }}
            className={`toc-link${h.level === 3 ? " toc-link--h3" : ""}${activeId === h.id ? " toc-link--active" : ""}`}
          >
            {h.text}
          </a>
        ))}
      </nav>
  );

  if (compact) return (
    <details ref={detailsRef} className="mobile-toc">
      <summary>On this page</summary>
      {links}
    </details>
  );

  return (
    <div className="toc">
      <div className="toc-title">On this page</div>
      {links}
    </div>
  );
}
