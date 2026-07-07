"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Search, X, Sparkles, CornerDownLeft } from "lucide-react";
import Fuse from "fuse.js";
import type { SearchDoc } from "@/lib/docs";

type Citation = { title: string; href: string };
type AskStatus =
  | "idle"
  | "loading"
  | "streaming"
  | "done"
  | "error"
  | "ratelimited"
  | "unconfigured";

// A row in the keyboard-navigable list: the "Ask AI" action or a search hit.
type NavItem = { kind: "ask" } | { kind: "result"; doc: SearchDoc };

export default function SearchDialog() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchDoc[]>([]);
  const [focused, setFocused] = useState(0);
  const [docs, setDocs] = useState<SearchDoc[]>([]);
  const [fuse, setFuse] = useState<Fuse<SearchDoc> | null>(null);

  // Answer ("ask AI") mode state.
  const [mode, setMode] = useState<"search" | "answer">("search");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [askStatus, setAskStatus] = useState<AskStatus>("idle");

  const inputRef = useRef<HTMLInputElement>(null);
  const modeRef = useRef(mode);
  const abortRef = useRef<AbortController | null>(null);
  const router = useRouter();

  useEffect(() => {
    modeRef.current = mode;
  }, [mode]);

  // Load search index once when dialog first opens.
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

  const backToSearch = useCallback(() => {
    abortRef.current?.abort();
    setMode("search");
    setAnswer("");
    setCitations([]);
    setAskStatus("idle");
    setFocused(0);
    setTimeout(() => inputRef.current?.focus(), 20);
  }, []);

  const closeDialog = useCallback(() => {
    abortRef.current?.abort();
    setOpen(false);
  }, []);

  // Keyboard shortcut Cmd+K / Ctrl+K; Esc backs out of answer mode first.
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape") {
        if (modeRef.current === "answer") {
          e.preventDefault();
          backToSearch();
        } else {
          setOpen(false);
        }
      }
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [backToSearch]);

  // Reset when dialog opens.
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery("");
      setResults([]);
      setFocused(0);
      setMode("search");
      setAnswer("");
      setCitations([]);
      setAskStatus("idle");
    } else {
      abortRef.current?.abort();
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

  const runAsk = useCallback(async (q: string) => {
    const trimmed = q.trim();
    if (!trimmed) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setMode("answer");
    setQuestion(trimmed);
    setAnswer("");
    setCitations([]);
    setAskStatus("loading");

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
        signal: controller.signal,
      });

      if (res.status === 503) return setAskStatus("unconfigured");
      if (res.status === 429) return setAskStatus("ratelimited");
      if (!res.ok || !res.body) return setAskStatus("error");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";
      setAskStatus("streaming");

      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        let nl: number;
        while ((nl = buf.indexOf("\n")) >= 0) {
          const raw = buf.slice(0, nl).trim();
          buf = buf.slice(nl + 1);
          if (!raw) continue;
          let msg: {
            type: string;
            text?: string;
            citations?: Citation[];
          };
          try {
            msg = JSON.parse(raw);
          } catch {
            continue;
          }
          if (msg.type === "citations" && msg.citations) {
            setCitations(msg.citations);
          } else if (msg.type === "delta" && msg.text) {
            setAnswer((a) => a + msg.text);
          } else if (msg.type === "done") {
            setAskStatus("done");
          }
        }
      }
      setAskStatus((s) => (s === "streaming" ? "done" : s));
    } catch (err) {
      if ((err as Error)?.name === "AbortError") return;
      setAskStatus("error");
    }
  }, []);

  // Combined navigable list for arrow-key handling in search mode.
  const displayResults =
    results.length > 0
      ? results
      : query.trim() && docs.length > 0
        ? []
        : docs.slice(0, 6);

  const navItems: NavItem[] = query.trim()
    ? [{ kind: "ask" }, ...displayResults.map((doc) => ({ kind: "result" as const, doc }))]
    : displayResults.map((doc) => ({ kind: "result" as const, doc }));

  const activate = (item: NavItem) => {
    if (item.kind === "ask") {
      runAsk(query);
    } else {
      closeDialog();
      router.push(item.doc.href);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setFocused((v) => Math.min(v + 1, navItems.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocused((v) => Math.max(v - 1, 0));
    } else if (e.key === "Enter" && navItems[focused]) {
      e.preventDefault();
      activate(navItems[focused]);
    }
  };

  const navigate = (href: string) => {
    closeDialog();
    router.push(href);
  };

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
          onClick={(e) => e.target === e.currentTarget && closeDialog()}
          role="dialog"
          aria-modal="true"
          aria-label="Search"
        >
          <div className="search-dialog">
            {mode === "search" ? (
              <>
                <div className="search-input-wrap">
                  <Search size={18} color="var(--color-muted)" />
                  <input
                    ref={inputRef}
                    className="search-input"
                    placeholder="Search or ask a question..."
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
                      style={{
                        background: "none",
                        border: "none",
                        cursor: "pointer",
                        color: "var(--color-muted)",
                        display: "flex",
                      }}
                    >
                      <X size={16} />
                    </button>
                  )}
                </div>

                <div className="search-results" role="listbox">
                  {query.trim() && (
                    <button
                      className={`search-result ask-row${
                        focused === 0 ? " search-result--focused" : ""
                      }`}
                      onClick={() => runAsk(query)}
                      onMouseEnter={() => setFocused(0)}
                      role="option"
                      aria-selected={focused === 0}
                    >
                      <span className="ask-row-icon">
                        <Sparkles size={16} />
                      </span>
                      <span className="ask-row-label">
                        Ask OcuTrap AI:{" "}
                        <span className="ask-row-query">
                          &ldquo;{query.trim()}&rdquo;
                        </span>
                      </span>
                      <CornerDownLeft
                        size={14}
                        className="ask-row-enter"
                        aria-hidden="true"
                      />
                    </button>
                  )}

                  {displayResults.length === 0 && query.trim() ? (
                    <div className="search-empty">
                      No pages match &ldquo;{query}&rdquo; — try Ask OcuTrap AI above.
                    </div>
                  ) : displayResults.length === 0 ? (
                    <div className="search-empty">
                      Start typing to search…
                    </div>
                  ) : (
                    <>
                      {!query.trim() && (
                        <div
                          style={{
                            padding: "0.375rem 1.125rem 0.125rem",
                            fontSize: "0.6875rem",
                            fontWeight: 700,
                            textTransform: "uppercase",
                            letterSpacing: "0.06em",
                            color: "var(--color-muted)",
                          }}
                        >
                          Recent pages
                        </div>
                      )}
                      {displayResults.map((doc, i) => {
                        const navIndex = query.trim() ? i + 1 : i;
                        return (
                          <button
                            key={doc.href}
                            className={`search-result${
                              navIndex === focused
                                ? " search-result--focused"
                                : ""
                            }`}
                            onClick={() => navigate(doc.href)}
                            onMouseEnter={() => setFocused(navIndex)}
                            role="option"
                            aria-selected={navIndex === focused}
                          >
                            {doc.section && (
                              <div className="search-result-section">
                                {doc.section}
                              </div>
                            )}
                            <div className="search-result-title">
                              {doc.title}
                            </div>
                            {doc.excerpt && (
                              <div className="search-result-excerpt">
                                {doc.excerpt}
                              </div>
                            )}
                          </button>
                        );
                      })}
                    </>
                  )}
                </div>

                <div className="search-footer">
                  <span className="search-shortcut">
                    <kbd>↑↓</kbd> navigate
                  </span>
                  <span className="search-shortcut">
                    <kbd>↵</kbd> open / ask
                  </span>
                  <span className="search-shortcut">
                    <kbd>Esc</kbd> close
                  </span>
                </div>
              </>
            ) : (
              <>
                <div className="ask-header">
                  <span className="ask-header-icon">
                    <Sparkles size={16} />
                  </span>
                  <span className="ask-header-question">{question}</span>
                  <button
                    className="ask-back"
                    onClick={backToSearch}
                    aria-label="Back to search"
                  >
                    <X size={16} />
                  </button>
                </div>

                <div className="ask-body">
                  {askStatus === "unconfigured" ? (
                    <div className="ask-notice">
                      AI answers aren&rsquo;t available right now. You can still
                      use search, or browse the documentation directly.
                    </div>
                  ) : askStatus === "ratelimited" ? (
                    <div className="ask-notice">
                      You&rsquo;ve asked a lot of questions in a short time.
                      Please wait a moment and try again.
                    </div>
                  ) : askStatus === "error" ? (
                    <div className="ask-notice">
                      Something went wrong generating an answer. Please try
                      again.
                    </div>
                  ) : (
                    <>
                      {askStatus === "loading" && !answer && (
                        <div className="ask-loading">
                          <span className="ask-dot" />
                          <span className="ask-dot" />
                          <span className="ask-dot" />
                          <span className="ask-loading-text">
                            Searching the documentation…
                          </span>
                        </div>
                      )}

                      {answer && (
                        <div className="ask-answer">
                          {answer}
                          {askStatus === "streaming" && (
                            <span className="ask-caret" />
                          )}
                        </div>
                      )}

                      {citations.length > 0 &&
                        (askStatus === "done" || askStatus === "streaming") && (
                          <div className="ask-sources">
                            <div className="ask-sources-title">Sources</div>
                            {citations.map((c) => (
                              <button
                                key={c.href}
                                className="ask-source"
                                onClick={() => navigate(c.href)}
                              >
                                {c.title}
                              </button>
                            ))}
                          </div>
                        )}
                    </>
                  )}
                </div>

                <div className="search-footer">
                  <span className="ask-disclaimer">
                    AI-generated from OcuTrap docs — verify important steps.
                  </span>
                  <span className="search-shortcut">
                    <kbd>Esc</kbd> back
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}
