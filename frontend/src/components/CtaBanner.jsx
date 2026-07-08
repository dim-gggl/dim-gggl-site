import Reveal from "./Reveal";
import { useLanguage } from "../lib/LanguageContext";
import { ArrowIcon } from "./icons";
import { Link } from "react-router-dom";

/**
 * Closing call-to-action panel shared by several pages.
 * `secondary` is either an internal route or an external URL.
 */
export default function CtaBanner({
  title,
  body,
  contactLabel,
  secondaryLabel,
  secondaryHref,
  secondaryExternal = false,
}) {
  const { person } = useLanguage();

  return (
    <section className="mx-auto max-w-6xl px-5 py-20">
      <Reveal className="relative overflow-hidden rounded-3xl border border-line bg-surface p-10 text-center md:p-16">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 70% 90% at 50% 120%, rgba(163,230,53,0.10), transparent 65%)",
          }}
        />
        <h2 className="relative font-display text-3xl font-semibold tracking-tight text-ink md:text-4xl">
          {title}
        </h2>
        <p className="relative mx-auto mt-4 max-w-xl text-ink-dim">{body}</p>
        <div className="relative mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <a
            href={`mailto:${person.contact_email}`}
            className="group inline-flex items-center gap-2 rounded-full bg-accent px-7 py-3 font-semibold text-bg transition-colors duration-300 hover:bg-accent-bright"
          >
            {contactLabel}
            <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
          </a>
          {secondaryLabel &&
            (secondaryExternal ? (
              <a
                href={secondaryHref}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full border border-line px-7 py-3 font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
              >
                {secondaryLabel}
              </a>
            ) : (
              <Link
                to={secondaryHref}
                className="inline-flex items-center gap-2 rounded-full border border-line px-7 py-3 font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
              >
                {secondaryLabel}
              </Link>
            ))}
        </div>
      </Reveal>
    </section>
  );
}
