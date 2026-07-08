import { Fragment } from "react";

/**
 * Render project long text: preserves line breaks and converts
 * `backtick` snippets and **bold** markers into styled elements
 * (mirrors the old render_project_text template filter).
 */
export default function ProseText({ text, className = "" }) {
  if (!text) return null;

  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g);

  return (
    <div className={`project-prose ${className}`}>
      {parts.map((part, index) => {
        if (part.startsWith("`") && part.endsWith("`")) {
          return <code key={index}>{part.slice(1, -1)}</code>;
        }
        if (part.startsWith("**") && part.endsWith("**")) {
          return <strong key={index}>{part.slice(2, -2)}</strong>;
        }
        return <Fragment key={index}>{part}</Fragment>;
      })}
    </div>
  );
}
