"use client";

// Per-page "Was this helpful?" 👍👎 widget (SITE-07 / SW-330).
// Emits a `docs_feedback` event {path, vote} and remembers the vote in
// localStorage so a returning visitor sees the thanks state instead of the
// buttons (one vote per page). Hidden in print (see globals.css §SITE-07).

import { useEffect, useState } from "react";
import { ThumbsUp, ThumbsDown } from "lucide-react";
import { capture } from "@/lib/analytics";

type Vote = "up" | "down";

const storageKey = (path: string) => `docs_feedback:${path}`;

export default function Feedback({ path }: { path: string }) {
  const [voted, setVoted] = useState<Vote | null>(null);
  const [ready, setReady] = useState(false);

  // Read any prior vote after mount (localStorage is client-only) so the
  // server-rendered markup and first client paint agree.
  useEffect(() => {
    try {
      const prior = localStorage.getItem(storageKey(path));
      if (prior === "up" || prior === "down") setVoted(prior);
    } catch {
      /* ignore storage errors (private mode, etc.) */
    }
    setReady(true);
  }, [path]);

  const vote = (v: Vote) => {
    if (voted) return; // one vote per page
    setVoted(v);
    try {
      localStorage.setItem(storageKey(path), v);
    } catch {
      /* ignore */
    }
    capture("docs_feedback", { path, vote: v });
  };

  // Avoid a flash of the buttons before we know whether they already voted.
  if (!ready) return <div className="doc-feedback" aria-hidden="true" />;

  return (
    <div className="doc-feedback" role="group" aria-label="Page feedback">
      {voted ? (
        <p className="doc-feedback-thanks">
          Thanks for your feedback!
        </p>
      ) : (
        <>
          <span className="doc-feedback-label">Was this helpful?</span>
          <div className="doc-feedback-buttons">
            <button
              type="button"
              className="doc-feedback-btn"
              onClick={() => vote("up")}
              aria-label="Yes, this page was helpful"
            >
              <ThumbsUp size={16} aria-hidden="true" />
              <span>Yes</span>
            </button>
            <button
              type="button"
              className="doc-feedback-btn"
              onClick={() => vote("down")}
              aria-label="No, this page was not helpful"
            >
              <ThumbsDown size={16} aria-hidden="true" />
              <span>No</span>
            </button>
          </div>
        </>
      )}
    </div>
  );
}
