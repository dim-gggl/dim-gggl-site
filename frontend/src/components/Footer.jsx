import { useLanguage } from "../lib/LanguageContext";
import { GitHubIcon, LinkedInIcon, MailIcon, PinIcon } from "./icons";
import Reveal from "./Reveal";

function SocialLink({ href, label, children, external = true }) {
  return (
    <a
      href={href}
      aria-label={label}
      {...(external
        ? { target: "_blank", rel: "noopener noreferrer" }
        : {})}
      className="group flex items-center gap-2 text-sm text-ink-dim transition-colors duration-300 hover:text-accent"
    >
      <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-line bg-surface transition-colors duration-300 group-hover:border-accent/60">
        {children}
      </span>
      <span className="font-mono text-xs">{label}</span>
    </a>
  );
}

export default function Footer() {
  const { t, person } = useLanguage();
  const year = new Date().getFullYear();

  return (
    <footer className="mt-28 border-t border-line">
      <div className="mx-auto max-w-6xl px-5 py-14">
        <Reveal className="flex flex-col items-start justify-between gap-10 md:flex-row md:items-center">
          <div>
            <p className="font-mono text-sm text-accent">
              {"// "}
              {person.baseline}
            </p>
            <a
              href={`mailto:${person.contact_email}`}
              className="mt-3 block font-display text-2xl font-semibold tracking-tight text-ink transition-colors duration-300 hover:text-accent md:text-3xl"
            >
              {person.contact_email}
            </a>
          </div>

          <div className="flex flex-wrap items-center gap-6">
            <SocialLink href={person.github} label="GitHub">
              <GitHubIcon className="h-4.5 w-4.5" />
            </SocialLink>
            <SocialLink href={person.linkedin} label="LinkedIn">
              <LinkedInIcon className="h-4.5 w-4.5" />
            </SocialLink>
            <SocialLink
              href={`mailto:${person.contact_email}`}
              label="Email"
              external={false}
            >
              <MailIcon className="h-4.5 w-4.5" />
            </SocialLink>
          </div>
        </Reveal>

        <div className="mt-12 flex flex-col items-start justify-between gap-3 border-t border-line pt-6 font-mono text-xs text-ink-mute md:flex-row md:items-center">
          <p className="flex items-center gap-2">
            <span className="text-accent">$</span>
            <span>
              © {year} {person.name}
            </span>
            <span className="hidden text-line-strong md:inline">|</span>
            <span className="hidden md:inline">{t("footer.rights")}</span>
          </p>
          <p className="flex items-center gap-2">
            <PinIcon className="h-3.5 w-3.5 text-accent" />
            {t("footer.location")}
          </p>
          <p className="flex items-center gap-1.5">
            <span>{t("footer.built_with")}</span>
            <span className="animate-pulse text-accent">❤</span>
            <span>& Django</span>
          </p>
        </div>
      </div>
    </footer>
  );
}
