import { useState } from "react";
import { motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import SectionHeading from "../components/SectionHeading";
import ProjectCard from "../components/ProjectCard";
import Loader from "../components/Loader";
import Lightbox from "../components/Lightbox";
import { ExternalIcon } from "../components/icons";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { stagger } from "../lib/motion";

function PromptBlock({ label, text }) {
  const [open, setOpen] = useState(false);
  if (!text) return null;
  return (
    <div className="rounded-xl border border-line bg-raised">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center justify-between px-4 py-3 text-left"
        aria-expanded={open}
      >
        <span className="font-mono text-xs uppercase tracking-[0.25em] text-accent">
          {label}
        </span>
        <motion.span
          animate={{ rotate: open ? 45 : 0 }}
          className="font-mono text-lg leading-none text-ink-dim"
        >
          +
        </motion.span>
      </button>
      <motion.div
        initial={false}
        animate={{ height: open ? "auto" : 0, opacity: open ? 1 : 0 }}
        transition={{ duration: 0.4 }}
        className="overflow-hidden"
      >
        <pre className="max-h-96 overflow-y-auto whitespace-pre-wrap px-4 pb-4 font-mono text-xs leading-6 text-ink-dim">
          {text.trim()}
        </pre>
      </motion.div>
    </div>
  );
}

export default function Ai() {
  const { t } = useLanguage();
  const { data } = useFetch("/ai/");
  const [lightbox, setLightbox] = useState(null);

  if (!data) {
    return (
      <PageShell title={t("meta.ai_title")}>
        <Loader />
      </PageShell>
    );
  }

  const { prompting, vibe_engineering: vibe } = data;

  return (
    <PageShell title={t("meta.ai_title")}>
      <section className="hero-glow mx-auto max-w-6xl px-5 pb-10 pt-16 md:pt-20">
        <Reveal>
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.35em] text-accent">
            {prompting.intro.title}
          </p>
          <h1 className="font-display text-5xl font-semibold tracking-tight text-ink md:text-7xl">
            {t("nav.ai")}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink-dim">
            {prompting.intro.body}
          </p>
        </Reveal>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-10">
        <div className="grid gap-5 lg:grid-cols-2">
          <Reveal className="flex flex-col gap-5 rounded-2xl border border-line bg-surface p-6">
            <h2 className="font-display text-2xl font-semibold text-ink">
              {prompting.music.title}
            </h2>
            <iframe
              src={prompting.music.spotify_embed_url}
              width="100%"
              height="352"
              frameBorder="0"
              allowFullScreen
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
              className="rounded-xl"
              title="Spotify embed"
            />
            <p className="text-sm leading-relaxed text-ink-dim">
              {prompting.music.spotify_caption}
            </p>
            <a
              href={prompting.music.spotify_external_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex w-fit items-center gap-2 rounded-full border border-line px-5 py-2.5 text-sm font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
            >
              {t("ai.spotify_open")}
              <ExternalIcon className="h-3.5 w-3.5" />
            </a>
            <div className="space-y-3">
              <p className="font-mono text-xs uppercase tracking-[0.25em] text-ink-mute">
                {prompting.music.track_title}
              </p>
              <PromptBlock label="Style prompt" text={prompting.music.style_prompt} />
              <PromptBlock label="Lyrics prompt" text={prompting.music.lyrics_prompt} />
            </div>
          </Reveal>

          <div className="flex flex-col gap-5">
            <Reveal delay={0.1} className="rounded-2xl border border-line bg-surface p-6">
              <h2 className="font-display text-2xl font-semibold text-ink">
                {prompting.video.title}
              </h2>
              <p className="mt-4 leading-relaxed text-ink-dim">
                {prompting.video.body}
              </p>
              <a
                href={prompting.video.sora_url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-5 inline-flex items-center gap-2 rounded-full border border-line px-5 py-2.5 text-sm font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
              >
                {prompting.video.cta_label}
                <ExternalIcon className="h-3.5 w-3.5" />
              </a>
            </Reveal>

            <Reveal delay={0.2} className="rounded-2xl border border-line bg-surface p-6">
              <h2 className="font-display text-2xl font-semibold text-ink">
                {prompting.jailbreak.title}
              </h2>
              <p className="mt-4 whitespace-pre-line leading-relaxed text-ink-dim">
                {prompting.jailbreak.body}
              </p>
              {prompting.jailbreak.screenshot && (
                <button
                  type="button"
                  onClick={() => setLightbox(prompting.jailbreak.screenshot)}
                  className="mt-5 block w-full cursor-zoom-in overflow-hidden rounded-xl border border-line transition-colors duration-300 hover:border-accent"
                >
                  <img
                    src={prompting.jailbreak.screenshot}
                    alt={prompting.jailbreak.image_alt}
                    loading="lazy"
                    className="w-full"
                  />
                </button>
              )}
            </Reveal>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-14">
        <SectionHeading eyebrow="Gemini 3 Pro" title={vibe.title} />
        <Reveal delay={0.1}>
          <p className="mt-4 max-w-2xl text-ink-dim">{vibe.body}</p>
        </Reveal>
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="mt-8 grid gap-5 sm:grid-cols-2"
        >
          {vibe.projects.map((project) => (
            <ProjectCard key={project.slug} project={project} origin="ai" />
          ))}
        </motion.div>
      </section>

      <Lightbox
        src={lightbox}
        alt={prompting.jailbreak.image_alt}
        onClose={() => setLightbox(null)}
        closeLabel={t("ai.lightbox_close")}
      />
    </PageShell>
  );
}
