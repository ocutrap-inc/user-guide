"use client";

import { useEffect, useState } from "react";

// Client-side PWA plumbing (SITE-11 / SW-334):
//  1. Registers the build-id-keyed service worker (public/sw.js, generated at
//     build time). updateViaCache:"none" so the SW script itself is always
//     revalidated — a new deploy's SW installs promptly instead of being pinned
//     by the HTTP cache.
//  2. Renders a slim "Offline — showing saved docs" banner while the browser
//     reports no connection, so a customer in a low-coverage field knows they
//     are reading cached content.
export default function PWA() {
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    // Reflect the current connection state and keep it in sync.
    const update = () => setOffline(!navigator.onLine);
    update();
    window.addEventListener("online", update);
    window.addEventListener("offline", update);

    // Register the service worker (production build only — the generated
    // public/sw.js exists after prebuild/predev).
    if ("serviceWorker" in navigator) {
      const register = () => {
        navigator.serviceWorker
          .register("/sw.js", { scope: "/", updateViaCache: "none" })
          .catch(() => {
            /* SW is a progressive enhancement; ignore registration failures. */
          });
      };
      if (document.readyState === "complete") register();
      else window.addEventListener("load", register);
    }

    return () => {
      window.removeEventListener("online", update);
      window.removeEventListener("offline", update);
    };
  }, []);

  if (!offline) return null;

  return (
    <div className="offline-banner" role="status" aria-live="polite">
      <span className="offline-banner__dot" aria-hidden="true" />
      Offline — showing saved docs
    </div>
  );
}
