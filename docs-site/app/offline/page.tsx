import Link from "next/link";
import type { Metadata } from "next";

// Offline fallback page (SITE-11 / SW-334). The service worker precaches this
// route and serves it when a navigation misses both the cache and the network,
// so a field customer with no coverage still lands on a useful screen instead
// of the browser's dinosaur.
export const metadata: Metadata = {
  title: "Offline",
  description: "You are offline — saved OcuTrap docs are still available.",
  robots: { index: false, follow: false },
};

export default function OfflinePage() {
  return (
    <div className="page-content">
      <article className="doc-body">
        <header className="page-header">
          <div className="page-eyebrow">Offline</div>
          <h1 className="page-title">You&rsquo;re offline</h1>
          <p className="page-subtitle">
            This page wasn&rsquo;t saved for offline reading. Pages you&rsquo;ve
            visited and the core setup, operation, and troubleshooting guides
            are still available from the menu.
          </p>
        </header>
        <p>
          The AI ask needs a connection and will resume once you&rsquo;re back
          online. Full-text search still works on saved docs.
        </p>
        <p>
          <Link href="/">← Back to the Knowledge Base home</Link>
        </p>
      </article>
    </div>
  );
}
