"use client";

import { Printer } from "lucide-react";

export default function PrintButton() {
  return (
    <button
      className="print-btn"
      onClick={() => window.print()}
      aria-label="Print page"
      title="Print / Save as PDF"
    >
      <Printer size={14} />
      <span>Print</span>
    </button>
  );
}
