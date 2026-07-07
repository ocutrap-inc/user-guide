"use client";

import { useEffect, useState } from "react";
import { fetchStatus, type StatusResult } from "@/lib/status";

// Slim live-incident banner for the high-traffic troubleshooting pages
// (SW-331 / spec SITE-08). Renders nothing unless OcuTrap systems are actually
// degraded (indicator !== "none"), so healthy days stay noise-free. When a
// real incident is live it surfaces the Statuspage description and a link,
// tinted amber (minor/major) or red (critical) via `data-indicator` in CSS.
// Fetch failure or JS-off → renders nothing (graceful).
export default function StatusBanner() {
  const [status, setStatus] = useState<StatusResult | null>(null);

  useEffect(() => {
    let active = true;
    fetchStatus().then((s) => {
      if (active && s && s.indicator !== "none") setStatus(s);
    });
    return () => {
      active = false;
    };
  }, []);

  if (!status) return null;

  return (
    <div className="status-banner" data-indicator={status.indicator} role="status">
      <span className="status-banner__dot" aria-hidden="true" />
      <span className="status-banner__text">
        OcuTrap systems: {status.description} —{" "}
        <a
          href="https://ocutrap.statuspage.io/"
          target="_blank"
          rel="noopener noreferrer"
        >
          check status page
        </a>
      </span>
    </div>
  );
}
