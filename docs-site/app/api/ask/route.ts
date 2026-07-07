import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { retrieve, buildSystemPrompt, answerLines } from "@/lib/ask";

// Reads the KB from the filesystem via lib/docs → needs the Node.js runtime.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Model is env-overridable; defaults to Haiku 4.5 (flat-cost, fast).
const MODEL = process.env.ANSWER_MODEL || "claude-haiku-4-5-20251001";
const MAX_QUESTION_LENGTH = 500;
const TOP_K = 6;
const MAX_TOKENS = 1024;

// Per-IP sliding-window rate limit.
// NOTE: this in-memory Map is per-instance. On Vercel (multiple serverless
// instances) the effective limit is per-instance, not global — acceptable for
// v1 abuse control; a shared store (KV/Redis) would be needed for a hard cap.
const RATE_LIMIT = 10; // requests
const RATE_WINDOW_MS = 60_000; // per minute
const hits = new Map<string, number[]>();

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const recent = (hits.get(ip) ?? []).filter((t) => now - t < RATE_WINDOW_MS);
  recent.push(now);
  hits.set(ip, recent);
  // Opportunistic cleanup so the Map doesn't grow unbounded.
  if (hits.size > 5000) {
    for (const [k, v] of hits) {
      if (v.every((t) => now - t >= RATE_WINDOW_MS)) hits.delete(k);
    }
  }
  return recent.length > RATE_LIMIT;
}

function clientIp(req: NextRequest): string {
  const fwd = req.headers.get("x-forwarded-for");
  if (fwd) return fwd.split(",")[0].trim();
  return req.headers.get("x-real-ip") ?? "unknown";
}

// Adapt the Anthropic message stream to a bare async iterable of text deltas.
async function* textDeltas(
  stream: AsyncIterable<Anthropic.MessageStreamEvent>
): AsyncGenerator<string> {
  for await (const event of stream) {
    if (
      event.type === "content_block_delta" &&
      event.delta.type === "text_delta"
    ) {
      yield event.delta.text;
    }
  }
}

export async function POST(req: NextRequest) {
  // 503 — feature not configured (no API key in this environment).
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "AI search is not configured." },
      { status: 503 }
    );
  }

  // 400 — invalid / too long.
  let question: unknown;
  try {
    const body = await req.json();
    question = body?.question;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }
  if (typeof question !== "string" || question.trim().length === 0) {
    return NextResponse.json(
      { error: "A non-empty 'question' string is required." },
      { status: 400 }
    );
  }
  question = question.trim();
  if ((question as string).length > MAX_QUESTION_LENGTH) {
    return NextResponse.json(
      { error: `Question too long (max ${MAX_QUESTION_LENGTH} characters).` },
      { status: 400 }
    );
  }

  // 429 — rate limited.
  if (rateLimited(clientIp(req))) {
    return NextResponse.json(
      { error: "Too many requests. Please wait a moment and try again." },
      { status: 429, headers: { "Retry-After": "60" } }
    );
  }

  const q = question as string;
  const chunks = retrieve(q, TOP_K);

  const anthropic = new Anthropic({ apiKey });
  // Single-turn only: KB in the system block, the question alone in the user turn.
  const stream = anthropic.messages.stream({
    model: MODEL,
    max_tokens: MAX_TOKENS,
    system: buildSystemPrompt(chunks),
    messages: [{ role: "user", content: q }],
  });

  const encoder = new TextEncoder();
  const body = new ReadableStream<Uint8Array>({
    async start(controller) {
      try {
        for await (const line of answerLines(chunks, textDeltas(stream))) {
          controller.enqueue(encoder.encode(JSON.stringify(line) + "\n"));
        }
      } catch {
        controller.enqueue(
          encoder.encode(JSON.stringify({ type: "done" }) + "\n")
        );
      } finally {
        controller.close();
      }
    },
    cancel() {
      stream.abort();
    },
  });

  return new Response(body, {
    headers: {
      "Content-Type": "application/x-ndjson; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}
