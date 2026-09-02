"use client";

// Interactive LED diagnostic wizard (SITE-10 / SW-333).
//
// Two taps: pick the LED color → pick the blink pattern → get the diagnosis
// and linked fix pages. Data comes entirely from the `matrix` prop, which the
// page route parses from the ```led-diagnostics block in the LED guide
// markdown (single source — see lib/led-diagnostics.ts). This component holds
// zero content of its own; editing the markdown changes it on next build.
//
// Progressive enhancement: server render + first client paint + JS-off all
// show the plain fallback table (rendered from the same matrix). After mount
// the interactive wizard appears and CSS hides the table ("wizard hydrates on
// top"); print restores the table. Mobile-first, one-thumb, both themes.

import { useEffect, useState } from "react";
import { ArrowLeft, RotateCcw } from "lucide-react";
import { capture } from "@/lib/analytics";
import {
  type LedMatrix,
  colorLabelOf,
  colorsInOrder,
  entriesFor,
  ledMatrixToHtmlTable,
  patternLabel,
  patternsForColor,
} from "@/lib/led-diagnostics";

// Presentation-only swatch styling per color id (the *content* — meanings and
// links — lives in the markdown). Unknown colors fall back to a neutral chip.
const SWATCH: Record<string, { css: string; dark?: boolean }> = {
  blue: { css: "#2f6fdb" },
  green: { css: "#2fa84f" },
  cyan: { css: "#28c3c9" },
  yellow: { css: "#e8c020" },
  magenta: { css: "#c850b0" },
  white: { css: "#f4f4f2" },
  red: { css: "#d5433a" },
  "no-light": { css: "transparent", dark: true },
};

function swatchStyle(color: string): React.CSSProperties {
  const s = SWATCH[color];
  if (!s) return { background: "var(--color-border)" };
  if (color === "no-light") {
    return {
      background:
        "repeating-linear-gradient(45deg, var(--color-border) 0 6px, transparent 6px 12px)",
    };
  }
  return { background: s.css };
}

export default function LedWizard({ matrix }: { matrix: LedMatrix }) {
  const [mounted, setMounted] = useState(false);
  const [color, setColor] = useState<string | null>(null);
  const [pattern, setPattern] = useState<string | null>(null);

  useEffect(() => setMounted(true), []);

  // Emit the SITE-07 analytics event once a full color+pattern result is
  // shown. Keyed on the pair so re-selecting a different combo re-fires.
  useEffect(() => {
    if (color && pattern) {
      capture("docs_led_wizard", { color, pattern });
    }
  }, [color, pattern]);

  const colors = colorsInOrder(matrix);
  const patterns = color ? patternsForColor(matrix, color) : [];
  const results = color && pattern ? entriesFor(matrix, color, pattern) : [];

  const reset = () => {
    setColor(null);
    setPattern(null);
  };

  const step = !color ? 1 : !pattern ? 2 : 3;

  return (
    <div className={`led-wizard${mounted ? " led-wizard--ready" : ""}`}>
      {/* Interactive UI — only rendered after mount so the server markup and
          first client paint match the fallback (no hydration mismatch). */}
      {mounted && (
        <section
          className="led-wizard__interactive"
          aria-label="Interactive LED diagnostic"
        >
          <ol className="led-wizard__steps" aria-hidden="true">
            <li className={step >= 1 ? "is-active" : ""}>1. Color</li>
            <li className={step >= 2 ? "is-active" : ""}>2. Pattern</li>
            <li className={step >= 3 ? "is-active" : ""}>3. Diagnosis</li>
          </ol>

          {/* Step 1 — color */}
          {step === 1 && (
            <div className="led-wizard__panel">
              <h3 className="led-wizard__q">What color is the light?</h3>
              <p className="led-wizard__hint">
                Watch the trap for a few seconds. On battery the light flashes
                briefly every ~10 seconds. That brief flash is the color to
                pick. If you see nothing at all, choose “No light”.
              </p>
              <div className="led-wizard__swatches" role="list">
                {colors.map((c) => {
                  const label = colorLabelOf({
                    color: c,
                    pattern: "",
                    meaning: "",
                  });
                  return (
                    <button
                      key={c}
                      type="button"
                      role="listitem"
                      className="led-swatch"
                      onClick={() => {
                        setColor(c);
                        setPattern(null);
                      }}
                      aria-label={`Light color: ${label}`}
                    >
                      <span
                        className={`led-swatch__chip led-swatch__chip--${c}`}
                        style={swatchStyle(c)}
                        aria-hidden="true"
                      />
                      <span className="led-swatch__label">{label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Step 2 — pattern */}
          {step === 2 && color && (
            <div className="led-wizard__panel">
              <button
                type="button"
                className="led-wizard__back"
                onClick={() => setColor(null)}
              >
                <ArrowLeft size={15} aria-hidden="true" /> Color
              </button>
              <h3 className="led-wizard__q">
                How is the{" "}
                <span
                  className="led-wizard__q-chip"
                  style={swatchStyle(color)}
                  aria-hidden="true"
                />
                <span className="led-wizard__q-color">
                  {colorLabelOf({ color, pattern: "", meaning: "" })}
                </span>{" "}
                light behaving?
              </h3>
              <div className="led-wizard__patterns">
                {patterns.map((p) => (
                  <button
                    key={p}
                    type="button"
                    className="led-pattern-btn"
                    onClick={() => setPattern(p)}
                  >
                    {patternLabel(p)}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 3 — result */}
          {step === 3 && color && pattern && (
            <div className="led-wizard__panel">
              <button
                type="button"
                className="led-wizard__back"
                onClick={() => setPattern(null)}
              >
                <ArrowLeft size={15} aria-hidden="true" /> Pattern
              </button>
              <div className="led-wizard__result-head">
                <span
                  className="led-wizard__result-chip"
                  style={swatchStyle(color)}
                  aria-hidden="true"
                />
                <span>
                  {colorLabelOf({ color, pattern, meaning: "" })} ·{" "}
                  {patternLabel(pattern)}
                </span>
              </div>

              {results.length === 0 ? (
                <div className="led-result-card">
                  <p className="led-result-card__meaning">
                    That color and pattern combination isn’t a documented
                    state. Double-check the color, or see the full table below.
                  </p>
                </div>
              ) : (
                results.map((entry, i) => (
                  <div className="led-result-card" key={i}>
                    {results.length > 1 && (
                      <div className="led-result-card__alt">
                        Possibility {i + 1} of {results.length}
                      </div>
                    )}
                    <p className="led-result-card__meaning">
                      {entry.meaning}
                      {entry.context ? (
                        <span className="led-result-card__context">
                          {" "}
                          ({entry.context})
                        </span>
                      ) : null}
                    </p>
                    {entry.action && (
                      <p className="led-result-card__action">
                        <strong>What to do:</strong> {entry.action}
                      </p>
                    )}
                    {entry.links && entry.links.length > 0 && (
                      <div className="led-result-card__links">
                        {entry.links.map((l) => (
                          <a
                            key={l.href}
                            href={l.href}
                            className="led-result-card__link"
                          >
                            {l.label} →
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}

              <button
                type="button"
                className="led-wizard__restart"
                onClick={reset}
              >
                <RotateCcw size={15} aria-hidden="true" /> Start over
              </button>
            </div>
          )}
        </section>
      )}

      {/* Plain fallback — server-rendered, JS-off, and print. Same matrix,
          same markup as the markdown pipeline's injected table. */}
      <div
        className="led-wizard__fallback"
        dangerouslySetInnerHTML={{ __html: ledMatrixToHtmlTable(matrix) }}
      />
    </div>
  );
}
