import { motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import SectionHeading from "../components/SectionHeading";
import Loader from "../components/Loader";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { stagger, staggerItem } from "../lib/motion";

function TechChips({ title, techs }) {
  return (
    <div>
      <h3 className="mb-4 font-display text-lg font-semibold text-ink-dim">
        {title}
      </h3>
      <motion.div
        variants={stagger}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-40px" }}
        className="flex flex-wrap gap-2"
      >
        {techs.map((tech) => (
          <motion.span
            key={tech.slug}
            variants={staggerItem}
            className="rounded-full border border-line bg-surface px-4 py-1.5 font-mono text-sm text-ink-dim transition-colors duration-300 hover:border-accent hover:text-accent"
          >
            {tech.name}
          </motion.span>
        ))}
      </motion.div>
    </div>
  );
}

export default function Skills() {
  const { t } = useLanguage();
  const { data } = useFetch("/about/");

  if (!data) {
    return (
      <PageShell title={t("meta.skills_title")}>
        <Loader />
      </PageShell>
    );
  }

  const backend = data.skills.backend;
  const dataTools = [
    ...data.skills.database,
    ...data.skills.tools,
    ...data.skills.frontend,
  ];
  const marqueeItems = [...backend, ...dataTools];

  return (
    <PageShell title={t("meta.skills_title")}>
      <section className="hero-glow mx-auto max-w-6xl px-5 pb-10 pt-16 md:pt-20">
        <Reveal>
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.35em] text-accent">
            {t("skills.stack_title")}
          </p>
          <h1 className="font-display text-5xl font-semibold tracking-tight text-ink md:text-7xl">
            {t("skills.title")}
          </h1>
        </Reveal>
      </section>

      {/* Marquee ribbon */}
      <div className="overflow-hidden border-y border-line py-4">
        <div className="marquee-track flex w-max gap-8">
          {[...marqueeItems, ...marqueeItems].map((tech, index) => (
            <span
              key={`${tech.slug}-${index}`}
              className="font-mono text-sm text-ink-mute"
            >
              {tech.name} <span className="ml-6 text-accent">·</span>
            </span>
          ))}
        </div>
      </div>

      <section className="mx-auto max-w-6xl space-y-12 px-5 py-16">
        <SectionHeading title={t("skills.stack_title")} />
        <TechChips title={t("skills.backend")} techs={backend} />
        <TechChips title={t("skills.data_tools")} techs={dataTools} />
      </section>
    </PageShell>
  );
}
