import Reveal from "./Reveal";

export default function SectionHeading({ eyebrow, title, className = "" }) {
  return (
    <Reveal className={className}>
      {eyebrow && (
        <p className="mb-3 font-mono text-xs uppercase tracking-[0.35em] text-accent">
          {eyebrow}
        </p>
      )}
      <h2 className="font-display text-3xl font-semibold tracking-tight text-ink md:text-4xl">
        {title}
      </h2>
    </Reveal>
  );
}
