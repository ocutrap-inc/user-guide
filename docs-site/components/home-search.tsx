"use client";

import { Search, ArrowRight } from "lucide-react";

export default function HomeSearch() {
  return (
    <button className="home-search" onClick={() => document.dispatchEvent(new Event("docs:open-search"))}>
      <Search size={20} aria-hidden="true" />
      <span>Search documentation</span>
      <ArrowRight size={18} aria-hidden="true" />
    </button>
  );
}
