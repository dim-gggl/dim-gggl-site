import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Terminal from "../components/Terminal";
import Reveal from "../components/Reveal";
import SectionHeading from "../components/SectionHeading";
import ProjectCard from "../components/ProjectCard";
import Loader from "../components/Loader";
import { ArrowIcon } from "../components/icons";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { EASE, stagger, staggerItem } from "../lib/motion";

function Tagline() {
  const { t } = useLanguage();
  const words = [t("hero.tagline_1"), t("hero.tagline_2"), t("hero.tagline_3")];
  return (
    <motion.div
      variants={stagger}
      initial="hidden"
      animate="visible"
      className="flex flex-wrap items-center gap-x-3 gap-y-1"
      aria-label={words.join(" ")}
    >
      {words.map((word, index) => (
        <motion.span
          key={word}
          variants={staggerItem}
          className={`font-display text-5xl font-semibold tracking-tight sm:text-7xl lg:text-8xl ${
            index === 2 ? "text-accent" : "text-ink"
          }`}
        >
          {word}
        </motion.span>
      ))}
    </motion.div>
  );
}

function Hero() {
  const { t, person } = useLanguage();

  return (
    <section className="hero-glow relative overflow-hidden">
      <div className="mx-auto grid max-w-6xl items-center gap-14 px-5 pb-20 pt-16 md:pt-24 lg:grid-cols-[1.15fr_1fr]">
        <div>
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: EASE }}
            className="mb-8 inline-flex items-center gap-2 rounded-full border border-line bg-surface px-4 py-1.5"
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-60" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-accent" />
            </span>
            <span className="font-mono text-xs text-ink-dim">
              {t("about.cta_body")}
            </span>
          </motion.div>

          <Tagline />

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.35, ease: EASE }}
            className="mt-8 max-w-xl text-lg leading-relaxed text-ink-dim"
          >
            {t("hero.description", { location: person.location })}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5, ease: EASE }}
            className="mt-9 flex flex-wrap items-center gap-3"
          >
            <Link
              to="/projects/"
              className="group inline-flex items-center gap-2 rounded-full bg-accent px-7 py-3 font-semibold text-bg transition-colors duration-300 hover:bg-accent-bright"
            >
              {t("hero.cta_projects")}
              <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
            </Link>
            <a
              href={`mailto:${person.contact_email}`}
              className="inline-flex items-center rounded-full border border-line px-7 py-3 font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
            >
              {t("hero.cta_contact")}
            </a>
          </motion.div>
        </div>

        <div className="relative">
          <motion.div
            initial={{ opacity: 0, scale: 0.94 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.3, ease: EASE }}
            className="absolute -top-10 right-2 z-10 hidden lg:block"
          >
            <img
              src="/static/images/profile-photo.png"
              alt={person.name}
              className="h-28 w-24 rounded-2xl border border-line object-cover shadow-2xl grayscale transition-all duration-500 hover:grayscale-0"
            />
          </motion.div>
          <Terminal />
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 1.2 }}
            className="mt-4 text-right font-mono text-xs text-ink-mute"
          >
            {person.name} — {person.title}
          </motion.p>
        </div>
      </div>
    </section>
  );
}

function SummaryTiles({ stats }) {
  const { t } = useLanguage();
  const tiles = [
    {
      to: "/projects/",
      title: t("summary.projects"),
      body: t("summary.projects_count", { count: stats.projects ?? 0 }),
    },
    {
      to: "/skills/",
      title: t("summary.skills"),
      body: t("summary.skills_count", { count: stats.technologies ?? 0 }),
    },
    {
      to: "/about/",
      title: t("summary.about"),
      body: t("summary.about_description"),
    },
  ];

  return (
    <section className="mx-auto max-w-6xl px-5 py-14" aria-label={t("summary.title")}>
      <SectionHeading title={t("summary.title")} />
      <motion.div
        variants={stagger}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        className="mt-8 grid gap-4 sm:grid-cols-3"
      >
        {tiles.map((tile) => (
          <motion.div key={tile.to} variants={staggerItem}>
            <Link
              to={tile.to}
              className="group flex h-full flex-col justify-between rounded-2xl border border-line bg-surface p-6 transition-all duration-500 hover:-translate-y-1 hover:border-accent/60"
            >
              <div className="flex items-center justify-between">
                <h3 className="font-display text-xl font-semibold text-ink transition-colors duration-300 group-hover:text-accent">
                  {tile.title}
                </h3>
                <ArrowIcon className="h-4 w-4 -translate-x-1 text-ink-mute opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:text-accent group-hover:opacity-100" />
              </div>
              <p className="mt-4 text-sm text-ink-dim">{tile.body}</p>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}

function IntroBlock({ intro }) {
  const { t } = useLanguage();
  return (
    <section className="mx-auto max-w-6xl px-5 py-14">
      <Reveal className="max-w-3xl">
        <p className="mb-3 font-mono text-xs uppercase tracking-[0.35em] text-accent">
          {t("home.label")}
        </p>
        <h2 className="font-display text-4xl font-semibold tracking-tight text-ink md:text-6xl">
          {intro.title}
        </h2>
        <p className="mt-6 text-lg leading-relaxed text-ink-dim">{intro.body}</p>
      </Reveal>
    </section>
  );
}

function NavigationHub({ sections }) {
  return (
    <section className="mx-auto max-w-6xl px-5 py-10">
      <motion.div
        variants={stagger}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        className="grid gap-4 md:grid-cols-2 xl:grid-cols-3"
      >
        {sections.map((section) => (
          <motion.div key={section.url} variants={staggerItem}>
            <Link
              to={section.url}
              className="group block h-full rounded-2xl border border-line bg-surface p-7 transition-all duration-500 hover:-translate-y-1 hover:border-accent/60"
            >
              <p className="font-mono text-xs uppercase tracking-[0.35em] text-accent">
                {section.eyebrow}
              </p>
              <div className="mt-5 flex items-center justify-between">
                <h3 className="font-display text-2xl font-semibold text-ink transition-colors duration-300 group-hover:text-accent">
                  {section.title}
                </h3>
                <ArrowIcon className="h-5 w-5 -translate-x-1 text-ink-mute opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:text-accent group-hover:opacity-100" />
              </div>
              <p className="mt-3 text-sm leading-relaxed text-ink-dim">
                {section.description}
              </p>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}

export default function Home() {
  const { t, stats } = useLanguage();
  const { data } = useFetch("/home/");

  return (
    <PageShell title={t("meta.home_title")}>
      <Hero />
      {!data ? (
        <Loader />
      ) : (
        <>
          <SummaryTiles stats={stats} />

          <section className="mx-auto max-w-6xl px-5 py-14">
            <SectionHeading title={t("featured.title")} />
            {data.featured.length ? (
              <motion.div
                variants={stagger}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-60px" }}
                className="mt-8 grid gap-5 sm:grid-cols-2"
              >
                {data.featured.map((project) => (
                  <ProjectCard key={project.slug} project={project} />
                ))}
              </motion.div>
            ) : (
              <p className="mt-8 text-ink-dim">{t("featured.empty")}</p>
            )}
          </section>

          <IntroBlock intro={data.intro} />
          <NavigationHub sections={data.navigation} />

          <section className="mx-auto max-w-6xl px-5 pb-10 pt-4">
            <Reveal>
              <Link
                to="/projects/"
                className="group inline-flex items-center gap-2 rounded-full border border-line px-6 py-3 font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
              >
                {t("home.archive")}
                <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
              </Link>
            </Reveal>
          </section>
        </>
      )}
    </PageShell>
  );
}
