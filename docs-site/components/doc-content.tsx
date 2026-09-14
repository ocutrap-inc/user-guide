import parse, { Element, domToReact, type DOMNode, type HTMLReactParserOptions } from "html-react-parser";

const options: HTMLReactParserOptions = {
  replace(node) {
    if (node instanceof Element && node.name === "table") {
      return (
        <div className="table-scroll" role="region" aria-label="Scrollable reference table" tabIndex={0}>
          <table {...node.attribs}>{domToReact(node.children as DOMNode[], options)}</table>
        </div>
      );
    }
  },
};

// Renders server-generated markdown HTML as React elements (no XSS risk —
// content comes from the controlled OcuTrap KB repository processed by rehype).
export default function DocContent({ html }: { html: string }) {
  return <div className="prose">{parse(html, options)}</div>;
}
