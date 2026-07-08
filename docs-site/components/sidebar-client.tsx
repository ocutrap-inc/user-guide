"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, FileDown, FileText, ChevronRight } from "lucide-react";
import type { NavSection, NavItem } from "@/lib/docs";

/* True when the current page is this item or any of its descendants —
   used to auto-expand the trail to the page being read (GitBook behavior). */
function inTrail(item: NavItem, currentPath: string): boolean {
  if (currentPath === item.href) return true;
  return item.children.some((child) => inTrail(child, currentPath));
}

function NavItemLink({
  item,
  currentPath,
  depth = 0,
}: {
  item: NavItem;
  currentPath: string;
  depth?: number;
}) {
  const isActive = currentPath === item.href;
  const hasChildren = item.children.length > 0;
  const active = inTrail(item, currentPath);

  // Subtrees collapse like GitBook: closed by default, open when the current
  // page lives inside them, and freely toggleable via the chevron (the row
  // itself still navigates). Navigating into a collapsed subtree re-opens it.
  const [expanded, setExpanded] = useState(active);
  useEffect(() => {
    if (active) setExpanded(true);
  }, [active]);

  const depthClass =
    depth === 0
      ? "nav-item"
      : depth === 1
        ? "nav-item nav-item--child"
        : "nav-item nav-item--grandchild";

  return (
    <li>
      <span className="nav-row">
        <Link
          href={item.href}
          className={`${depthClass}${isActive ? " nav-item--active" : ""}`}
          aria-current={isActive ? "page" : undefined}
        >
          {item.title}
        </Link>
        {hasChildren && (
          <button
            type="button"
            className={`nav-chevron${expanded ? " nav-chevron--open" : ""}`}
            onClick={() => setExpanded((v) => !v)}
            aria-expanded={expanded}
            aria-label={`${expanded ? "Collapse" : "Expand"} ${item.title}`}
          >
            <ChevronRight size={14} />
          </button>
        )}
      </span>
      {hasChildren && expanded && (
        <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
          {item.children.map((child) => (
            <NavItemLink
              key={child.href}
              item={child}
              currentPath={currentPath}
              depth={depth + 1}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

export default function SidebarClient({
  sections,
}: {
  sections: NavSection[];
}) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  // Close sidebar on navigation
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, []);

  return (
    <>
      {/* Mobile hamburger */}
      <button
        className="hamburger"
        onClick={() => setOpen((v) => !v)}
        aria-label={open ? "Close menu" : "Open menu"}
        aria-expanded={open}
      >
        {open ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Overlay for mobile */}
      {open && (
        <div
          className="sidebar-overlay"
          onClick={() => setOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <nav
        className={`sidebar${open ? " sidebar--open" : ""}`}
        aria-label="Documentation navigation"
      >
        {/* Mobile drawer header (hidden on desktop). Text-only: the old
            low-res raccoon PNG is gone, and the left padding clears the
            fixed close (X) button so the two never overlap. */}
        <Link href="/" className="sidebar-logo">
          OcuTrap Knowledge Base
        </Link>

        <ul style={{ listStyle: "none", margin: 0, padding: "0 0 2rem" }}>
          {sections.map((section, i) => (
            <li key={i}>
              {section.separator && !section.title && (
                <div className="nav-separator" />
              )}
              {section.title && (
                <div className="nav-section-title">{section.title}</div>
              )}
              <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
                {section.items.map((item) => (
                  <NavItemLink
                    key={item.href}
                    item={item}
                    currentPath={pathname}
                  />
                ))}
                {/* PDF downloads live under Appendix and Resources
                    (the /manual route stays reachable by URL, unlinked) */}
                {/appendix/i.test(section.title ?? "") && (
                  <>
                    <li>
                      <a
                        href="/gitbook-assets/OcuTrap_Knowledge_Base.pdf"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="nav-item nav-item--pdf"
                      >
                        <FileDown size={14} />
                        Full Manual (PDF)
                      </a>
                    </li>
                    <li>
                      <a
                        href="/gitbook-assets/R1_Operation_Cheat_Sheet.pdf"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="nav-item nav-item--pdf"
                      >
                        <FileText size={14} />
                        R1 Cheat Sheet (PDF)
                      </a>
                    </li>
                  </>
                )}
              </ul>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
}
