import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import SectionHeading from "../components/SectionHeading";
import Loader from "../components/Loader";
import Stat from "../components/Stat";
import CtaBanner from "../components/CtaBanner";
import { ArrowIcon } from "../components/icons";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { EASE, stagger, staggerItem } from "../lib/motion";

function SkillGroup({ title, skills, delay = 0 }) {
  return (
    <Reveal delay={delay} className="rounded-2xl border border-line bg-surface p-7">
      <h3 className="mb-6 font-display text-xl font-semibold text-ink">{title}</h3>
      <div className="space-y-4">
        {skills.map((tech) => (
          <div key={tech.slug}>
            <div className="mb-1.5 flex items-center justify-between">
              <span className="text-sm font-medium text-ink-dim">{tech.name}</span>
              <span className="font-mono text-[11px] text-ink-mute">
                {tech.proficiency}/5
              </span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-raised">
              <motion.div
                initial={{ width: 0 }}
                whileInView={{ width: `${tech.proficiency * 20}%` }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 1.1, ease: EASE }}
                className="h-full rounded-full"
                style={{
                  background: `linear-gradient(to right, ${tech.color_from}, ${tech.color_to})`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </Reveal>
  );
}

function TimelineItem({ period, title, org, body, highlight = false, index }) {
  return (
    <motion.li
      initial={{ opacity: 0, x: -32 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.7, delay: index * 0.12, ease: EASE }}
      className="relative pl-10"
    >
      <span
        className={`absolute left-0 top-1.5 flex h-4 w-4 items-center justify-center rounded-full border ${
          highlight ? "border-accent bg-accent/20" : "border-line bg-surface"
        }`}
      >
        <span
          className={`h-1.5 w-1.5 rounded-full ${highlight ? "bg-accent" : "bg-ink-mute"}`}
        />
      </span>
      <p
        className={`inline-block rounded-full px-3 py-1 font-mono text-[11px] font-semibold ${
          highlight ? "bg-accent text-bg" : "bg-raised text-ink-dim"
        }`}
      >
        {period}
      </p>
      <h3 className="mt-3 font-display text-xl font-semibold text-ink">{title}</h3>
      <p className="mt-1 font-mono text-xs text-ink-mute">{org}</p>
      <p className="mt-3 max-w-xl leading-relaxed text-ink-dim">{body}</p>
    </motion.li>
  );
}

export default function About() {
  const { t, person } = useLanguage();
  const { data } = useFetch("/about/");

  if (!data) {
    return (
      <PageShell title={t("meta.about_title")}>
        <Loader />
      </PageShell>
    );
  }

  const qualities = ["creativity", "adaptability", "team", "results"];

  return (
    <PageShell title={t("meta.about_title")}>
      {/* Hero */}
      <section className="hero-glow relative overflow-hidden">
        <div className="mx-auto grid max-w-6xl items-center gap-12 px-5 pb-16 pt-16 md:pt-24 lg:grid-cols-[1.1fr_1fr]">
          <div>
            <motion.img
              initial={{ opacity: 0, scale: 0.94 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, ease: EASE }}
              src="/static/images/profile-photo.png"
              alt={person.name}
              className="mb-8 h-44 w-36 rounded-3xl border border-line object-cover shadow-2xl"
            />
            <Reveal>
              <h1 className="font-display text-5xl font-semibold tracking-tight text-ink md:text-6xl">
                Dimitri <span className="text-accent">Gaggioli</span>
              </h1>
              <p className="mt-4 text-xl text-ink-dim">{person.title}</p>
            </Reveal>
            <Reveal delay={0.15} className="mt-6 flex flex-wrap gap-2">
              {[t("hero.tagline_1"), t("hero.tagline_2"), t("hero.tagline_3")].map(
                (tag) => (
                  <span
                    key={tag}
                    className="rounded-full border border-accent/40 bg-accent-soft px-4 py-1.5 font-mono text-sm text-accent"
                  >
                    {tag}
                  </span>
                )
              )}
            </Reveal>
            <Reveal delay={0.25} className="mt-8">
              <a
                href={`mailto:${person.contact_email}`}
                className="group inline-flex items-center gap-2 rounded-full bg-accent px-7 py-3 font-semibold text-bg transition-colors duration-300 hover:bg-accent-bright"
              >
                {t("about.cta_contact")}
                <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
              </a>
            </Reveal>
          </div>

          <motion.div
            variants={stagger}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-2 gap-4"
          >
            <Stat value={data.stats.projects} label={t("about.stats_projects")} />
            <Stat
              value={data.stats.years_experience}
              label={t("about.stats_years")}
            />
            <Stat
              value={data.stats.technologies}
              label={t("about.stats_technologies")}
            />
            <Stat value={100} suffix="%" label={t("about.stats_passion")} />
          </motion.div>
        </div>
      </section>

      {/* Who am I */}
      <section className="mx-auto max-w-3xl px-5 py-16">
        <SectionHeading title={t("about.who_title")} />
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="mt-8 space-y-5 text-lg leading-relaxed text-ink-dim"
        >
          {["p1", "p2", "p3", "p4"].map((key) => (
            <motion.p key={key} variants={staggerItem}>
              {t(`about.${key}`)}
            </motion.p>
          ))}
        </motion.div>
      </section>

      {/* Timeline */}
      <section className="border-y border-line bg-surface/40">
        <div className="mx-auto max-w-4xl px-5 py-16">
          <SectionHeading title={t("about.timeline_title")} />
          <ul className="relative mt-10 space-y-12">
            <span
              aria-hidden="true"
              className="absolute bottom-2 left-[7px] top-2 w-px bg-line"
            />
            <TimelineItem
              index={0}
              highlight
              period="2024 - 2025"
              title={t("about.timeline_1_title")}
              org="OpenClassrooms"
              body={t("about.timeline_1_body")}
            />
            <TimelineItem
              index={1}
              period="2012"
              title={t("about.timeline_2_title")}
              org="Paris X Nanterre"
              body={t("about.timeline_2_body")}
            />
            <TimelineItem
              index={2}
              period="2010 - 2024"
              title={t("about.timeline_3_title")}
              org="La Clef Revival & independent venues"
              body={t("about.timeline_3_body")}
            />
          </ul>
        </div>
      </section>

      {/* Detailed skills */}
      <section className="mx-auto max-w-6xl px-5 py-16">
        <SectionHeading title={t("about.skills_title")} />
        <div className="mt-8 grid gap-5 md:grid-cols-2">
          <SkillGroup title={t("about.skills_backend")} skills={data.skills.backend} />
          <SkillGroup
            title={t("about.skills_frontend")}
            skills={data.skills.frontend}
            delay={0.08}
          />
          <SkillGroup
            title={t("about.skills_databases")}
            skills={data.skills.database}
            delay={0.16}
          />
          <SkillGroup
            title={t("about.skills_tools")}
            skills={data.skills.tools}
            delay={0.24}
          />
        </div>
      </section>

      {/* Interests */}
      <section className="mx-auto max-w-6xl px-5 py-10">
        <SectionHeading title={t("about.interests_title")} />
        <div className="mt-8 grid gap-5 md:grid-cols-2">
          {["poetry", "cinema"].map((interest, index) => (
            <Reveal
              key={interest}
              delay={index * 0.1}
              className="group rounded-2xl border border-line bg-surface p-8 transition-colors duration-500 hover:border-accent/60"
            >
              <h3 className="font-display text-2xl font-semibold text-ink transition-colors duration-300 group-hover:text-accent">
                {t(`about.interest_${interest}_title`)}
              </h3>
              <p className="mt-4 leading-relaxed text-ink-dim">
                {t(`about.interest_${interest}_body`)}
              </p>
              <p className="mt-4 text-sm text-ink-mute">
                {t(`about.interest_${interest}_note`)}
              </p>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Qualities */}
      <section className="mx-auto max-w-5xl px-5 py-16">
        <SectionHeading title={t("about.qualities_title")} />
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="mt-8 grid gap-4 md:grid-cols-2"
        >
          {qualities.map((quality) => (
            <motion.div
              key={quality}
              variants={staggerItem}
              className="rounded-2xl border border-line bg-surface p-6"
            >
              <h3 className="font-display text-lg font-semibold text-ink">
                {t(`about.quality_${quality}_title`)}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-ink-dim">
                {t(`about.quality_${quality}_body`)}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      <CtaBanner
        title={t("about.cta_title")}
        body={t("about.cta_body")}
        contactLabel={t("about.cta_contact")}
        secondaryLabel={t("about.cta_projects")}
        secondaryHref="/projects/"
      />
    </PageShell>
  );
}
