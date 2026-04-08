import { NextResponse } from "next/server";
import { buildSearchIndex } from "@/lib/docs";

// Cache the search index for the lifetime of the server instance
let cachedIndex: ReturnType<typeof buildSearchIndex> | null = null;

export async function GET() {
  try {
    if (!cachedIndex) {
      cachedIndex = buildSearchIndex();
      console.log(`[search] Built index with ${cachedIndex.length} docs`);
    }
    return NextResponse.json(cachedIndex, {
      headers: {
        "Cache-Control": "public, s-maxage=3600, stale-while-revalidate=86400",
      },
    });
  } catch (err) {
    console.error("[search] Failed to build search index:", err);
    return NextResponse.json({ error: "Search unavailable" }, { status: 500 });
  }
}
