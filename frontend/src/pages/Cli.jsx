import { motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import ProjectCard from "../components/ProjectCard";
import Loader from "../components/Loader";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { stagger } from "../lib/motion";

export default function Cli() {
  const { t } = useLanguage();
  const { data } = useFetch("/cli/");

  if (!data) {
    return (
      <PageShell title={t("meta.cli_title")}>
        <Loader />
      </PageShell>
    );
  }

  return (
    <PageShell title={t("meta.cli_title")}>
      <section className="hero-glow mx-auto max-w-6xl px-5 pb-10 pt-16 md:pt-20">
        <Reveal>
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.35em] text-accent">
            <span className="text-ink-mute">$</span> {data.intro.title.toLowerCase()} --list
          </p>
          <h1 className="font-display text-5xl font-semibold tracking-tight text-ink md:text-7xl">
            {data.intro.title}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink-dim">
            {data.intro.body}
          </p>
        </Reveal>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-10">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="grid gap-5 sm:grid-cols-2"
        >
          {data.projects.map((project) => (
            <ProjectCard key={project.slug} project={project} origin="cli" />
          ))}
        </motion.div>
      </section>
    </PageShell>
  );
}
