"use client";

import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { useRouter } from "next/navigation";
import { Search, X, Sparkles, CornerDownLeft } from "lucide-react";
import { createSearchEngine, searchDocuments } from "@/lib/search";
import { useNativeDialog } from "./use-native-dialog";
import type { SearchDoc } from "@/lib/docs";
import { renderAnswerMarkdown } from "@/lib/answer-markdown";
import { capture } from "@/lib/analytics";

// Grounded-refusal ("declined") heuristic for docs_ask. The ask endpoint always
// streams citations for the chunks it retrieved, so citations alone don't prove
// the model actually answered. We treat an ask as "declined" when either no
// chunks were retrieved (zero citations) OR the answer text matches the
// documented refusal phrasing the system prompt instructs the model to use
// ("...don't have that information in the OcuTrap documentation..."). Anything
// else with body text counts as "answered".
function isDeclinedAnswer(answer: string, citations: Citation[]): boolean {
  if (citations.length === 0) return true;
  const a = answer.toLowerCase();
  return (
    /don'?t have (that|this|the)?\s*information/.test(a) ||
    /couldn'?t find/.test(a) ||
    /(isn'?t|is not|aren'?t|not) (covered|available|included|documented)/.test(a) ||
    (/contact (ocutrap )?support/.test(a) && /documentation/.test(a))
  );
}

type Citation = { title: string; href: string };
type AskStatus =
  | "idle"
  | "loading"
  | "streaming"
  | "done"
  | "error"
  | "ratelimited"
  | "unconfigured"
  | "offline";

// A row in the keyboard-navigable list: the "Ask AI" action or a search hit.
type NavItem = { kind: "ask" } | { kind: "result"; doc: SearchDoc };

export default function SearchDialog() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(0);
  const [docs, setDocs] = useState<SearchDoc[]>([]);
  const [indexStatus, setIndexStatus] = useState<"idle" | "loading" | "ready" | "error">("idle");
  const [retry, setRetry] = useState(0);
  const fuse = useMemo(() => createSearchEngine(docs), [docs]);
  const results = useMemo(() => searchDocuments(fuse, query), [fuse, query]);
  const dialogRef = useRef<HTMLDialogElement>(null);

  // Answer ("ask AI") mode state.
  const [mode, setMode] = useState<"search" | "answer">("search");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [askStatus, setAskStatus] = useState<AskStatus>("idle");

  const inputRef = useRef<HTMLInputElement>(null);
  const backRef = useRef<HTMLButtonElement>(null);
  useNativeDialog(open, dialogRef, inputRef);
  const abortRef = useRef<AbortController | null>(null);
  const resultsRef = useRef(results);
  const router = useRouter();

  useEffect(() => {
    if (!open) return;
    // A mode switch removes the clicked option; focus after the browser has
    // finished that click's default focus handling.
    const frame = requestAnimationFrame(() => {
      (mode === "search" ? inputRef.current : backRef.current)?.focus();
    });
    return () => cancelAnimationFrame(frame);
  }, [open, mode]);

  // Keep the latest results readable from the debounced analytics timer
  // without retriggering it on every keystroke.
  resultsRef.current = results;

  // docs_search: fire once ~800ms after the query settles (not per keystroke),
  // and only for non-empty queries. resultCount is what search surfaced;
  // zeroResults flags a likely content gap.
  useEffect(() => {
    const q = query.trim();
    if (!q) return;
    const t = setTimeout(() => {
      const count = resultsRef.current.length;
      capture("docs_search", {
        query: q,
        resultCount: count,
        zeroResults: count === 0,
      });
    }, 800);
    return () => clearTimeout(t);
  }, [query]);

  // Recompute results when the index arrives, even if the query was typed first.
  useEffect(() => {
    if (!open || docs.length > 0) return;
    const controller = new AbortController();
    setIndexStatus("loading");
    fetch("/api/search", { signal: controller.signal })
      .then((r) => {
        if (!r.ok) throw new Error("Search index unavailable");
        return r.json();
      })
      .then((data: SearchDoc[]) => {
        if (!Array.isArray(data)) throw new Error("Invalid search index");
        setDocs(data);
        setIndexStatus("ready");
      })
      .catch((error) => {
        if (error.name !== "AbortError") setIndexStatus("error");
      });
    return () => controller.abort();
  }, [open, docs.length, retry]);

  const backToSearch = useCallback(() => {
    abortRef.current?.abort();
    setMode("search");
    setAnswer("");
    setCitations([]);
    setAskStatus("idle");
    setFocused(0);
  }, []);

  const closeDialog = useCallback(() => {
    abortRef.current?.abort();
    setOpen(false);
  }, []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        if (document.querySelector("dialog:modal:not(.search-overlay)")) return;
        e.preventDefault();
        setOpen((v) => !v);
      }
    };
    const openSearch = () => setOpen(true);
    document.addEventListener("keydown", handler);
    document.addEventListener("docs:open-search", openSearch);
    return () => {
      document.removeEventListener("keydown", handler);
      document.removeEventListener("docs:open-search", openSearch);
    };
  }, []);

  // Reset when dialog opens.
  useEffect(() => {
    if (open) {
      setQuery("");
      setFocused(0);
      setMode("search");
      setAnswer("");
      setCitations([]);
      setAskStatus("idle");
    } else {
      abortRef.current?.abort();
    }
  }, [open]);

  const handleSearch = (q: string) => {
    setQuery(q);
    setFocused(0);
  };

  const runAsk = useCallback(async (q: string) => {
    const trimmed = q.trim();
    if (!trimmed) return;
    // AI ask needs a live connection (the /api/* routes are network-only in the
    // offline SW). Short-circuit with a friendly notice instead of a failed
    // fetch when the browser reports no connection (SITE-11).
    if (typeof navigator !== "undefined" && !navigator.onLine) {
      setMode("answer");
      setQuestion(trimmed);
      setAnswer("");
      setCitations([]);
      setAskStatus("offline");
      return;
    }
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setMode("answer");
    setQuestion(trimmed);
    setAnswer("");
    setCitations([]);
    setAskStatus("loading");

    // Local accumulators so we can classify the outcome for docs_ask without
    // racing React state updates.
    let localAnswer = "";
    let localCitations: Citation[] = [];

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
        signal: controller.signal,
      });

      if (res.status === 503) {
        // AI not configured in this environment (e.g. local without a key).
        capture("docs_ask", { question: trimmed, outcome: "error" });
        return setAskStatus("unconfigured");
      }
      if (res.status === 429) {
        capture("docs_ask", { question: trimmed, outcome: "rate_limited" });
        return setAskStatus("ratelimited");
      }
      if (!res.ok || !res.body) {
        capture("docs_ask", { question: trimmed, outcome: "error" });
        return setAskStatus("error");
      }

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
            localCitations = msg.citations;
            setCitations(msg.citations);
          } else if (msg.type === "delta" && msg.text) {
            localAnswer += msg.text;
            setAnswer((a) => a + msg.text);
          } else if (msg.type === "done") {
            setAskStatus("done");
          }
        }
      }
      setAskStatus((s) => (s === "streaming" ? "done" : s));

      const declined = isDeclinedAnswer(localAnswer, localCitations);
      capture("docs_ask", {
        question: trimmed,
        outcome: declined ? "declined" : "answered",
        ...(declined
          ? {}
          : { citedPages: localCitations.map((c) => c.href) }),
      });
    } catch (err) {
      if ((err as Error)?.name === "AbortError") return;
      capture("docs_ask", { question: trimmed, outcome: "error" });
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
    ? [...displayResults.map((doc) => ({ kind: "result" as const, doc })), { kind: "ask" }]
    : displayResults.map((doc) => ({ kind: "result" as const, doc }));

  useEffect(() => {
    dialogRef.current?.querySelector(`[data-result-index="${focused}"]`)?.scrollIntoView({ block: "nearest" });
  }, [focused]);

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
      setFocused((v) => Math.max(0, Math.min(v + 1, navItems.length - 1)));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocused((v) => Math.max(v - 1, 0));
    } else if (e.key === "Enter" && indexStatus !== "loading" && navItems[focused]) {
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
      {/* Desktop: full search input. Mobile: collapses to an icon button. */}
      <button
        className="search-trigger search-trigger--full"
        onClick={() => setOpen(true)}
        aria-label="Search documentation"
      >
        <Search size={14} />
        <span>Search docs...</span>
        <span className="search-kbd">⌘K</span>
      </button>
      <button
        className="search-trigger--icon"
        onClick={() => setOpen(true)}
        aria-label="Search documentation"
      >
        <Search size={18} />
      </button>

        <dialog
          ref={dialogRef}
          className="search-overlay"
          onCancel={(e) => {
            e.preventDefault();
            if (mode === "answer") backToSearch();
            else closeDialog();
          }}
          onClose={closeDialog}
          onClick={(e) => e.target === e.currentTarget && closeDialog()}
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
                    placeholder="Search documentation..."
                    aria-label="Search documentation"
                    role="combobox"
                    aria-autocomplete="list"
                    aria-expanded={open && mode === "search"}
                    aria-controls="docs-search-results"
                    aria-activedescendant={navItems[focused] ? `docs-search-option-${focused}` : undefined}
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
                      className="search-clear"
                    >
                      <X size={16} />
                    </button>
                  )}
                  <button className="dialog-close" onClick={closeDialog} aria-label="Close search">Close</button>
                </div>

                <div className="search-results" id="docs-search-results" role="listbox" aria-label="Search results" aria-busy={indexStatus === "loading"}>
                  {indexStatus === "loading" ? (
                    <div className="search-empty" role="status">Loading documentation…</div>
                  ) : indexStatus === "error" ? (
                    <div className="search-empty" role="status">
                      Search could not load. Check your connection and <button className="search-retry" onClick={() => setRetry((v) => v + 1)}>try again</button>.
                    </div>
                  ) : displayResults.length === 0 && query.trim() ? (
                    <div className="search-empty">
                      No pages match &ldquo;{query}&rdquo; — try a shorter search or ask OcuTrap AI below.
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
                          Browse pages
                        </div>
                      )}
                      {displayResults.map((doc, i) => {
                        const navIndex = i;
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
                            id={`docs-search-option-${navIndex}`}
                            data-result-index={navIndex}
                            tabIndex={-1}
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
                  {query.trim() && (
                    <button
                      className={`search-result ask-row${
                        focused === displayResults.length ? " search-result--focused" : ""
                      }`}
                      onClick={() => runAsk(query)}
                      onMouseEnter={() => setFocused(displayResults.length)}
                      id={`docs-search-option-${displayResults.length}`}
                      data-result-index={displayResults.length}
                      tabIndex={-1}
                      role="option"
                      aria-selected={focused === displayResults.length}
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
                    ref={backRef}
                    className="ask-back"
                    onClick={backToSearch}
                    aria-label="Back to search"
                  >
                    Back
                  </button>
                  <button className="dialog-close" onClick={closeDialog} aria-label="Close search">Close</button>
                </div>

                <div className="ask-body">
                  {askStatus === "offline" ? (
                    <div className="ask-notice">
                      AI ask needs a connection. You&rsquo;re offline right now —
                      full-text search still works on your saved docs, or
                      reconnect to ask the AI.
                    </div>
                  ) : askStatus === "unconfigured" ? (
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
                        <div
                          className="ask-answer"
                          dangerouslySetInnerHTML={{
                            __html: renderAnswerMarkdown(
                              answer,
                              askStatus === "streaming"
                            ),
                          }}
                        />
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
        </dialog>
    </>
  );
}
