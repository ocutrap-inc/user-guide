import parse from "html-react-parser";

// Renders server-generated markdown HTML as React elements (no XSS risk —
// content comes from the controlled OcuTrap KB repository processed by rehype).
export default function DocContent({ html }: { html: string }) {
  return <div className="prose">{parse(html)}</div>;
}
