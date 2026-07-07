// Live OcuTrap system-status client (SW-331 / spec SITE-08).
//
// Fetches the public Statuspage summary JSON and caches it in sessionStorage
// for ~5 minutes so a browsing session makes at most one request per tab.
// CORS is open on the endpoint (access-control-allow-origin: *, verified
// 2026-07-07), so the fetch runs directly from the browser — no proxy route.
//
// Every consumer is a client component that calls these functions inside a
// useEffect, so the browser-only APIs (fetch, sessionStorage) never run during
// SSR. All failure modes resolve to `null` for graceful degradation.

export type StatusIndicator = "none" | "minor" | "major" | "critical";

export type StatusResult = {
  indicator: StatusIndicator;
  description: string;
};

// Default summary endpoint (host mirrors the bookmark card on the home page).
export const STATUS_JSON_URL =
  "https://ocutrap.statuspage.io/api/v2/status.json";

const CACHE_KEY = "ocutrap:statuspage-status";
const TTL_MS = 5 * 60 * 1000; // ~5 minutes

const VALID: readonly StatusIndicator[] = ["none", "minor", "major", "critical"];

function isValidIndicator(v: unknown): v is StatusIndicator {
  return typeof v === "string" && (VALID as readonly string[]).includes(v);
}

// Human-readable fallback label per indicator, used only when the API omits a
// description. The API normally supplies its own (e.g. "All Systems Operational").
export function indicatorLabel(indicator: StatusIndicator): string {
  switch (indicator) {
    case "none":
      return "All Systems Operational";
    case "minor":
      return "Partially Degraded Service";
    case "major":
      return "Partial System Outage";
    case "critical":
      return "Major System Outage";
  }
}

function readCache(url: string): StatusResult | null {
  try {
    const raw = sessionStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as {
      at?: number;
      url?: string;
      data?: StatusResult;
    };
    if (
      parsed.url === url &&
      typeof parsed.at === "number" &&
      Date.now() - parsed.at < TTL_MS &&
      parsed.data &&
      isValidIndicator(parsed.data.indicator)
    ) {
      return parsed.data;
    }
  } catch {
    // Malformed cache / storage unavailable — ignore and re-fetch.
  }
  return null;
}

function writeCache(url: string, data: StatusResult): void {
  try {
    sessionStorage.setItem(
      CACHE_KEY,
      JSON.stringify({ at: Date.now(), url, data })
    );
  } catch {
    // Storage full / disabled — non-fatal.
  }
}

// Fetch (or return the cached) system status. Resolves to `null` on any
// network error, non-2xx response, or unrecognized payload so callers can fall
// back to their plain, JS-off appearance.
export async function fetchStatus(
  url: string = STATUS_JSON_URL
): Promise<StatusResult | null> {
  const cached = readCache(url);
  if (cached) return cached;

  try {
    const res = await fetch(url, {
      headers: { Accept: "application/json" },
      // Let the browser/CDN cache too; sessionStorage is the primary guard.
      cache: "no-store",
    });
    if (!res.ok) return null;
    const json = (await res.json()) as {
      status?: { indicator?: unknown; description?: unknown };
    };
    const indicator = json?.status?.indicator;
    if (!isValidIndicator(indicator)) return null;
    const description =
      typeof json?.status?.description === "string" &&
      json.status.description.trim()
        ? json.status.description.trim()
        : indicatorLabel(indicator);
    const data: StatusResult = { indicator, description };
    writeCache(url, data);
    return data;
  } catch {
    return null;
  }
}
