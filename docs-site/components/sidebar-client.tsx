"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, FileDown, FileText, ChevronRight } from "lucide-react";
import { useNativeDialog } from "./use-native-dialog";
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
  const dialogRef = useRef<HTMLDialogElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  useNativeDialog(open, dialogRef, closeRef);

  // Close sidebar on navigation
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  useEffect(() => {
    const desktop = window.matchMedia("(min-width: 901px)");
    const closeOnDesktop = () => { if (desktop.matches) setOpen(false); };
    desktop.addEventListener("change", closeOnDesktop);
    return () => desktop.removeEventListener("change", closeOnDesktop);
  }, []);

  const navigation = (
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
  );

  return (
    <>
      <button className="hamburger" onClick={() => setOpen(true)}
        aria-label="Open menu" aria-expanded={open} aria-controls="mobile-navigation">
        <Menu size={20} />
      </button>
      <nav className="sidebar sidebar--desktop" aria-label="Documentation navigation">{navigation}</nav>
      <dialog id="mobile-navigation" ref={dialogRef} className="mobile-nav-dialog"
        aria-label="Documentation menu" onCancel={() => setOpen(false)} onClose={() => setOpen(false)}
        onClick={(e) => { if (e.target === e.currentTarget) setOpen(false); }}>
        <div className="mobile-nav-panel">
          <div className="mobile-nav-header">
            <Link href="/" onClick={() => setOpen(false)}>OcuTrap Knowledge Base</Link>
            <button ref={closeRef} className="dialog-close" onClick={() => setOpen(false)} aria-label="Close menu"><X size={20} /></button>
          </div>
          <nav aria-label="Documentation navigation" onClick={(e) => {
            if ((e.target as HTMLElement).closest("a")) setOpen(false);
          }}>{navigation}</nav>
        </div>
      </dialog>
    </>
  );
}
