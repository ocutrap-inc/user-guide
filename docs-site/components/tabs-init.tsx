"use client";

import { useEffect } from "react";

// Hydrates interactive tab behaviour for markdown-rendered tab groups
export default function TabsInit() {
  useEffect(() => {
    const containers = document.querySelectorAll<HTMLElement>(".tabs-container");
    containers.forEach((container) => {
      const buttons = container.querySelectorAll<HTMLButtonElement>(".tab-btn");
      const panels = container.querySelectorAll<HTMLElement>(".tab-panel");

      buttons.forEach((btn, i) => {
        btn.addEventListener("click", () => {
          buttons.forEach((b) => b.classList.remove("tab-btn--active"));
          panels.forEach((p) => p.classList.add("tab-panel--hidden"));
          btn.classList.add("tab-btn--active");
          panels[i]?.classList.remove("tab-panel--hidden");
        });
      });
    });
  }, []);

  return null;
}
