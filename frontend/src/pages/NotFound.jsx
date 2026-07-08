import { Link } from "react-router-dom";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import { useLanguage } from "../lib/LanguageContext";

export default function NotFound() {
  const { t } = useLanguage();

  return (
    <PageShell title="404 - dim-gggl">
      <section className="mx-auto flex max-w-6xl flex-col items-center px-5 py-32 text-center">
        <Reveal>
          <p className="font-mono text-8xl font-bold text-accent">404</p>
          <h1 className="mt-6 font-display text-2xl font-semibold text-ink">
            {t("projects.empty_title")}
          </h1>
          <Link
            to="/"
            className="mt-8 inline-block rounded-full bg-accent px-7 py-3 font-semibold text-bg transition-colors duration-300 hover:bg-accent-bright"
          >
            {t("nav.home")}
          </Link>
        </Reveal>
      </section>
    </PageShell>
  );
}
