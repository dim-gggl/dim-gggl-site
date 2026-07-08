import { useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import SectionHeading from "../components/SectionHeading";
import ProjectCard from "../components/ProjectCard";
import Loader from "../components/Loader";
import Lightbox from "../components/Lightbox";
import CtaBanner from "../components/CtaBanner";
import ProseText from "../components/ProseText";
import NotFound from "./NotFound";
import {
  CheckIcon,
  ChevronIcon,
  DocIcon,
  ExternalIcon,
  GitHubIcon,
} from "../components/icons";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { stagger, staggerItem } from "../lib/motion";

function HeroLink({ href, children, primary = false }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-semibold transition-all duration-300 ${
        primary
          ? "bg-accent text-bg hover:bg-accent-bright"
          : "border border-line text-ink hover:border-accent hover:text-accent"
      }`}
    >
      {children}
    </a>
  );
}

export default function ProjectDetail() {
  const { slug } = useParams();
  const [searchParams] = useSearchParams();
  const { t } = useLanguage();
  const { data: project, error } = useFetch(`/projects/${slug}/`, {
    from: searchParams.get("from") ?? "",
  });
  const [lightbox, setLightbox] = useState(null);

  if (error?.status === 404) return <NotFound />;

  if (!project) {
    return (
      <PageShell title="dim-gggl">
        <Loader />
      </PageShell>
    );
  }

  const accent = project.primary_color || "#a3e635";

  return (
    <PageShell title={`${project.title} - dim-gggl`}>
      {/* Hero */}
      <section
        className="relative overflow-hidden border-b border-line"
        style={{
          background: `radial-gradient(ellipse 75% 65% at 50% -10%, ${accent}1f, transparent 70%)`,
        }}
      >
        <div className="mx-auto max-w-5xl px-5 pb-16 pt-14 md:pt-20">
          {project.origin_context && (
            <motion.div
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-8"
            >
              <Link
                to={project.origin_context.url}
                className="inline-flex items-center gap-1.5 font-mono text-xs font-semibold text-accent transition-opacity hover:opacity-75"
              >
                <ChevronIcon direction="left" className="h-3.5 w-3.5" />
                {project.origin_context.label}
              </Link>
            </motion.div>
          )}

          <Reveal>
            {project.category && (
              <p className="mb-4 font-mono text-xs uppercase tracking-[0.35em] text-ink-dim">
                {project.category.name}
              </p>
            )}
            {project.logo && (
              <img
                src={project.logo}
                alt={`${project.title} logo`}
                className="mb-6 h-20 w-20 object-contain"
              />
            )}
            <h1
              className="font-display text-5xl font-semibold tracking-tight md:text-7xl"
              style={{ color: accent }}
            >
              {project.title}
            </h1>
            {project.tagline && (
              <p className="mt-5 max-w-2xl text-xl leading-relaxed text-ink-dim md:text-2xl">
                {project.tagline}
              </p>
            )}
          </Reveal>

          <motion.div
            variants={stagger}
            initial="hidden"
            animate="visible"
            className="mt-8 flex flex-wrap gap-2"
          >
            {project.technologies.map((tech) => (
              <motion.span
                key={tech.slug}
                variants={staggerItem}
                className="rounded-full border border-line bg-surface/70 px-3.5 py-1.5 font-mono text-xs text-ink-dim backdrop-blur-sm"
              >
                {tech.name}
              </motion.span>
            ))}
          </motion.div>

          <Reveal delay={0.2} className="mt-9 flex flex-wrap gap-3">
            {project.github_url && (
              <HeroLink href={project.github_url} primary>
                <GitHubIcon className="h-4 w-4" />
                {t("project.github")}
              </HeroLink>
            )}
            {project.demo_url && (
              <HeroLink href={project.demo_url}>
                <ExternalIcon className="h-4 w-4" />
                {t("project.demo")}
              </HeroLink>
            )}
            {project.title === "Aura" && (
              <HeroLink href="https://aura-app.org/">
                <ExternalIcon className="h-4 w-4" />
                {t("project.website")}
              </HeroLink>
            )}
            {project.documentation_url && (
              <HeroLink href={project.documentation_url}>
                <DocIcon className="h-4 w-4" />
                {t("project.documentation")}
              </HeroLink>
            )}
          </Reveal>
        </div>
      </section>

      {/* About */}
      {project.description && (
        <section className="mx-auto max-w-3xl px-5 py-16">
          <SectionHeading title={t("project.about")} />
          <Reveal delay={0.1}>
            <ProseText text={project.description} className="mt-6 text-lg" />
          </Reveal>
        </section>
      )}

      {/* Gallery */}
      {project.gallery.length > 0 && (
        <section className="mx-auto max-w-6xl px-5 py-12">
          <SectionHeading
            title={`${project.title} — ${t("project.screenshots")}`}
          />
          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-60px" }}
            className="mt-8 grid gap-5 md:grid-cols-2"
          >
            {project.gallery.map((image, index) => (
              <motion.button
                key={image.url}
                type="button"
                variants={staggerItem}
                onClick={() => setLightbox(image.url)}
                className="group cursor-zoom-in overflow-hidden rounded-2xl border border-line bg-surface transition-colors duration-300 hover:border-accent/60"
              >
                <img
                  src={image.url}
                  alt={
                    image.caption ||
                    `${project.title} — ${t("project.screenshots")} ${index + 1}`
                  }
                  loading="lazy"
                  className="h-auto w-full transition-transform duration-700 ease-out group-hover:scale-[1.02]"
                />
                {image.caption && (
                  <p className="border-t border-line px-4 py-3 text-left text-sm text-ink-dim">
                    {image.caption}
                  </p>
                )}
              </motion.button>
            ))}
          </motion.div>
        </section>
      )}

      {/* Features */}
      {project.features.length > 0 && (
        <section className="mx-auto max-w-4xl px-5 py-12">
          <SectionHeading title={t("project.features_title")} />
          <motion.ul
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-60px" }}
            className="mt-8 space-y-3"
          >
            {project.features.map((feature) => (
              <motion.li
                key={feature}
                variants={staggerItem}
                className="flex gap-4 rounded-2xl border border-line bg-surface p-5"
              >
                <span
                  className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
                  style={{ backgroundColor: `${accent}22`, color: accent }}
                >
                  <CheckIcon className="h-3.5 w-3.5" />
                </span>
                <ProseText text={feature} className="!whitespace-normal text-[15px]" />
              </motion.li>
            ))}
          </motion.ul>
        </section>
      )}

      {/* Challenges & learnings */}
      {(project.challenges || project.learnings) && (
        <section className="mx-auto max-w-6xl px-5 py-12">
          <div className="grid gap-5 md:grid-cols-2">
            {project.challenges && (
              <Reveal className="rounded-2xl border border-line bg-surface p-7">
                <h3 className="font-display text-xl font-semibold text-ink">
                  {t("project.challenges")}
                </h3>
                <ProseText text={project.challenges} className="mt-4 text-[15px]" />
              </Reveal>
            )}
            {project.learnings && (
              <Reveal delay={0.1} className="rounded-2xl border border-line bg-surface p-7">
                <h3 className="font-display text-xl font-semibold text-ink">
                  {t("project.learnings")}
                </h3>
                <ProseText text={project.learnings} className="mt-4 text-[15px]" />
              </Reveal>
            )}
          </div>
        </section>
      )}

      {/* Stack */}
      <section className="mx-auto max-w-5xl px-5 py-12">
        <SectionHeading title={t("project.stack")} />
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4"
        >
          {project.technologies.map((tech) => (
            <motion.div
              key={tech.slug}
              variants={staggerItem}
              className="rounded-2xl border border-line bg-surface p-5 text-center transition-colors duration-300 hover:border-accent/50"
            >
              <p className="font-display font-semibold text-ink">{tech.name}</p>
              <p className="mt-1 font-mono text-[11px] text-ink-mute">
                {tech.category_label}
              </p>
              <div className="mt-3 flex justify-center gap-1">
                {[1, 2, 3, 4, 5].map((level) => (
                  <span
                    key={level}
                    className="h-1.5 w-1.5 rounded-full"
                    style={{
                      backgroundColor:
                        level <= tech.proficiency ? accent : "var(--color-raised)",
                    }}
                  />
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Similar */}
      {project.similar.length > 0 && (
        <section className="mx-auto max-w-6xl px-5 py-12">
          <SectionHeading title={t("project.related")} />
          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-60px" }}
            className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
          >
            {project.similar.map((similar) => (
              <ProjectCard key={similar.slug} project={similar} />
            ))}
          </motion.div>
        </section>
      )}

      {/* Prev / next */}
      <section className="border-t border-line">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-6 px-5 py-10">
          {project.previous ? (
            <Link
              to={`/projects/${project.previous.slug}/`}
              className="group flex items-center gap-3 text-ink-dim transition-colors duration-300 hover:text-ink"
            >
              <ChevronIcon
                direction="left"
                className="h-5 w-5 transition-transform duration-300 group-hover:-translate-x-1"
              />
              <span className="text-left">
                <span className="block font-mono text-[11px] text-ink-mute">
                  {t("project.previous_label")}
                </span>
                <span className="font-display font-semibold">
                  {project.previous.title}
                </span>
              </span>
            </Link>
          ) : (
            <span />
          )}
          {project.next ? (
            <Link
              to={`/projects/${project.next.slug}/`}
              className="group flex items-center gap-3 text-right text-ink-dim transition-colors duration-300 hover:text-ink"
            >
              <span>
                <span className="block font-mono text-[11px] text-ink-mute">
                  {t("project.next_label")}
                </span>
                <span className="font-display font-semibold">
                  {project.next.title}
                </span>
              </span>
              <ChevronIcon className="h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
            </Link>
          ) : (
            <span />
          )}
        </div>
      </section>

      <CtaBanner
        title={t("project.cta_title")}
        body={t("project.cta_body")}
        contactLabel={t("project.cta_contact")}
        secondaryLabel={t("project.cta_projects")}
        secondaryHref="/projects/"
      />

      <Lightbox
        src={lightbox}
        alt={project.title}
        onClose={() => setLightbox(null)}
        closeLabel={t("ai.lightbox_close")}
      />
    </PageShell>
  );
}
