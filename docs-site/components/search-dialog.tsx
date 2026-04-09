"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Search, X } from "lucide-react";
import Fuse from "fuse.js";
import type { SearchDoc } from "@/lib/docs";

export default function SearchDialog() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchDoc[]>([]);
  const [focused, setFocused] = useState(0);
  const [docs, setDocs] = useState<SearchDoc[]>([]);
  const [fuse, setFuse] = useState<Fuse<SearchDoc> | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  // Load search index once when dialog first opens
  useEffect(() => {
    if (!open || docs.length > 0) return;
    fetch("/api/search")
      .then((r) => r.json())
      .then((data: SearchDoc[]) => {
        setDocs(data);
        setFuse(
          new Fuse(data, {
            keys: [
              { name: "title", weight: 2 },
              { name: "section", weight: 1 },
              { name: "excerpt", weight: 0.5 },
            ],
            threshold: 0.35,
            includeScore: true,
          })
        );
      })
      .catch(() => {});
  }, [open, docs.length]);

  // Keyboard shortcut Cmd+K / Ctrl+K
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, []);

  // Focus input when dialog opens
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery("");
      setResults([]);
      setFocused(0);
    }
  }, [open]);

  const handleSearch = useCallback(
    (q: string) => {
      setQuery(q);
      setFocused(0);
      if (!fuse || !q.trim()) {
        setResults([]);
        return;
      }
      const hits = fuse.search(q.trim()).slice(0, 8);
      setResults(hits.map((h) => h.item));
    },
    [fuse]
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setFocused((v) => Math.min(v + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocused((v) => Math.max(v - 1, 0));
    } else if (e.key === "Enter" && results[focused]) {
      setOpen(false);
      router.push(results[focused].href);
    }
  };

  const navigate = (href: string) => {
    setOpen(false);
    router.push(href);
  };

  const displayResults =
    results.length > 0
      ? results
      : query.trim() && docs.length > 0
        ? []
        : docs.slice(0, 6);

  return (
    <>
      <button
        className="search-trigger"
        onClick={() => setOpen(true)}
        aria-label="Search documentation"
      >
        <Search size={14} />
        <span>Search docs...</span>
        <span className="search-kbd">⌘K</span>
      </button>

      {open && (
        <div
          className="search-overlay"
          onClick={(e) => e.target === e.currentTarget && setOpen(false)}
          role="dialog"
          aria-modal="true"
          aria-label="Search"
        >
          <div className="search-dialog">
            <div className="search-input-wrap">
              <Search size={18} color="var(--color-muted)" />
              <input
                ref={inputRef}
                className="search-input"
                placeholder="Search documentation..."
                value={query}
                onChange={(e) => handleSearch(e.target.value)}
                onKeyDown={handleKeyDown}
                autoComplete="off"
                spellCheck={false}
              />
              {query && (
                <button
                  onClick={() => handleSearch("")}
                  aria-label="Clear search"
                  style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-muted)", display: "flex" }}
                >
                  <X size={16} />
                </button>
              )}
            </div>

            <div className="search-results" role="listbox">
              {displayResults.length === 0 && query.trim() ? (
                <div className="search-empty">No results for &ldquo;{query}&rdquo;</div>
              ) : displayResults.length === 0 ? (
                <div className="search-empty">Start typing to search…</div>
              ) : (
                <>
                  {!query.trim() && (
                    <div style={{ padding: "0.375rem 1.125rem 0.125rem", fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-muted)" }}>
                      Recent pages
                    </div>
                  )}
                  {displayResults.map((doc, i) => (
                    <button
                      key={doc.href}
                      className={`search-result${i === focused ? " search-result--focused" : ""}`}
                      onClick={() => navigate(doc.href)}
                      onMouseEnter={() => setFocused(i)}
                      role="option"
                      aria-selected={i === focused}
                    >
                      {doc.section && (
                        <div className="search-result-section">{doc.section}</div>
                      )}
                      <div className="search-result-title">{doc.title}</div>
                      {doc.excerpt && (
                        <div className="search-result-excerpt">{doc.excerpt}</div>
                      )}
                    </button>
                  ))}
                </>
              )}
            </div>

            <div className="search-footer">
              <span className="search-shortcut">
                <kbd>↑↓</kbd> navigate
              </span>
              <span className="search-shortcut">
                <kbd>↵</kbd> open
              </span>
              <span className="search-shortcut">
                <kbd>Esc</kbd> close
              </span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
