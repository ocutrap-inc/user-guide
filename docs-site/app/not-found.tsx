import Link from "next/link";

export default function NotFound() {
  return (
    <div className="page-content" style={{ justifyContent: "center" }}>
      <div className="doc-body" style={{ textAlign: "center", paddingTop: "4rem" }}>
        <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>📄</div>
        <h1 style={{ fontSize: "1.5rem", fontWeight: 700, color: "var(--color-heading)", marginBottom: "0.75rem" }}>
          Page not found
        </h1>
        <p style={{ color: "var(--color-muted)", marginBottom: "1.5rem" }}>
          The page you're looking for doesn't exist or may have moved.
        </p>
        <Link
          href="/"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "0.375rem",
            padding: "0.625rem 1.25rem",
            background: "var(--color-brand)",
            color: "#fff",
            borderRadius: "6px",
            textDecoration: "none",
            fontWeight: 500,
            fontSize: "0.875rem",
          }}
        >
          Back to home
        </Link>
      </div>
    </div>
  );
}
