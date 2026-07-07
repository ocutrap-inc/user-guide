"use client";

import { Printer } from "lucide-react";

// `variant`:
//  - "full" (default): labeled button, used on the /manual screen header.
//  - "icon": compact icon-only button, used inline on article pages.
export default function PrintButton({
  variant = "full",
  label = "Print",
}: {
  variant?: "full" | "icon";
  label?: string;
}) {
  return (
    <button
      className={variant === "icon" ? "print-btn print-btn--icon" : "print-btn"}
      onClick={() => window.print()}
      aria-label="Print this page"
      title="Print / Save as PDF"
    >
      <Printer size={variant === "icon" ? 16 : 14} />
      {variant !== "icon" && <span>{label}</span>}
    </button>
  );
}
