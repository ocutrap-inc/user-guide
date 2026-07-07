"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { Menu, X, FileDown, FileText, Printer } from "lucide-react";
import type { NavSection, NavItem } from "@/lib/docs";

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

  const depthClass =
    depth === 0
      ? "nav-item"
      : depth === 1
        ? "nav-item nav-item--child"
        : "nav-item nav-item--grandchild";

  return (
    <li>
      <Link
        href={item.href}
        className={`${depthClass}${isActive ? " nav-item--active" : ""}`}
        aria-current={isActive ? "page" : undefined}
      >
        {item.title}
      </Link>
      {hasChildren && (
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
        <Link href="/" className="sidebar-logo">
          <span className="sidebar-logo-icon">
            <Image
              src="/gitbook-assets/OcuTrap_icon_favpng.png"
              alt="OcuTrap"
              width={28}
              height={28}
            />
          </span>
          OcuTrap Knowledge Base
        </Link>

        <ul style={{ listStyle: "none", margin: 0, padding: "0 0 2rem" }}>
          {/* PDF downloads + print-friendly manual (nav-level shortcut) */}
          <li>
            <div className="nav-section-title">PDF Downloads</div>
            <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
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
              <li>
                <Link
                  href="/manual"
                  className={`nav-item nav-item--pdf${pathname === "/manual" ? " nav-item--active" : ""}`}
                >
                  <Printer size={14} />
                  Print-friendly Manual
                </Link>
              </li>
            </ul>
          </li>
          <li><div className="nav-separator" /></li>

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
              </ul>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
}
