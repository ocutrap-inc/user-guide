"use client";

import { useEffect } from "react";
import { fetchStatus } from "@/lib/status";

// Progressive-enhancement hydrator for the Statuspage bookmark card
// (SW-331 / spec SITE-08). The markdown transform emits the card with a
// `data-status-url` attribute and a hidden `.bookmark-card__status` pill
// placeholder. On mount we fetch the live status and, only on success, fill
// the pill text, tag it with the indicator (drives the dot color in CSS), and
// reveal it. If the fetch fails — or JS never runs — the pill stays hidden and
// the card is byte-for-byte what it was before this feature.
export default function StatusPill() {
  useEffect(() => {
    const cards = document.querySelectorAll<HTMLAnchorElement>(
      ".bookmark-card[data-status-url]"
    );
    if (cards.length === 0) return;

    let cancelled = false;

    cards.forEach((card) => {
      const url = card.getAttribute("data-status-url");
      const pill = card.querySelector<HTMLElement>(".bookmark-card__status");
      const text = card.querySelector<HTMLElement>(
        ".bookmark-card__status-text"
      );
      if (!url || !pill || !text) return;

      fetchStatus(url).then((status) => {
        if (cancelled || !status) return;
        text.textContent = status.description;
        pill.dataset.indicator = status.indicator;
        pill.hidden = false;
      });
    });

    return () => {
      cancelled = true;
    };
  }, []);

  return null;
}
