import { ImageResponse } from "next/og";
import fs from "fs";
import path from "path";

// Reads the raccoon mark from the filesystem → needs the Node.js runtime.
export const runtime = "nodejs";

// Load the raccoon mark once at module init and inline it as a data URI so the
// ImageResponse renderer (which can't fetch same-origin assets at build time)
// always has the image available.
const RACCOON_DATA_URI = (() => {
  try {
    const buf = fs.readFileSync(
      path.join(process.cwd(), "public", "ocutrap-mark.png")
    );
    return `data:image/png;base64,${buf.toString("base64")}`;
  } catch {
    return "";
  }
})();

const BRAND_BLUE = "#0050ff";
const FOOTER = "OcuTrap Knowledge Base";

// Dynamic 1200×630 social card: brand-blue background, raccoon mark in a white
// chip, the page title in large white type, and a footer line (SITE-01).
export async function GET(req: Request): Promise<ImageResponse> {
  const { searchParams } = new URL(req.url);
  const rawTitle = searchParams.get("title") || FOOTER;
  const title = rawTitle.slice(0, 120);
  const section = (searchParams.get("section") || "").slice(0, 60);
  const isHome = !searchParams.get("title") || title === FOOTER;

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: BRAND_BLUE,
          backgroundImage: `linear-gradient(135deg, ${BRAND_BLUE} 0%, #003ad1 100%)`,
          padding: "72px 80px",
          fontFamily: "sans-serif",
        }}
      >
        {/* Top: raccoon chip + brand wordmark */}
        <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: 104,
              height: 104,
              borderRadius: 24,
              background: "#ffffff",
              boxShadow: "0 8px 24px rgba(0,0,0,0.18)",
            }}
          >
            {RACCOON_DATA_URI ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={RACCOON_DATA_URI}
                width={78}
                height={78}
                alt="OcuTrap"
                style={{ objectFit: "contain" }}
              />
            ) : null}
          </div>
          <div
            style={{
              color: "#ffffff",
              fontSize: 40,
              fontWeight: 700,
              letterSpacing: "-0.02em",
            }}
          >
            OcuTrap
          </div>
        </div>

        {/* Middle: optional section eyebrow + page title */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {section && !isHome ? (
            <div
              style={{
                color: "rgba(255,255,255,0.82)",
                fontSize: 26,
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              {section}
            </div>
          ) : null}
          <div
            style={{
              color: "#ffffff",
              fontSize: title.length > 48 ? 68 : 84,
              fontWeight: 800,
              lineHeight: 1.05,
              letterSpacing: "-0.03em",
              maxWidth: 1000,
            }}
          >
            {title}
          </div>
        </div>

        {/* Footer line */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            color: "rgba(255,255,255,0.9)",
            fontSize: 30,
            fontWeight: 600,
          }}
        >
          {FOOTER}
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
