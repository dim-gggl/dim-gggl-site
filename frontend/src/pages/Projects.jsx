import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import PageShell from "../components/PageShell";
import Reveal from "../components/Reveal";
import ProjectCard from "../components/ProjectCard";
import Loader from "../components/Loader";
import CtaBanner from "../components/CtaBanner";
import { useFetch } from "../lib/useFetch";
import { useLanguage } from "../lib/LanguageContext";
import { EASE, stagger } from "../lib/motion";

const SELECT_CLASSES =
  "rounded-xl border border-line bg-surface px-4 py-2.5 text-sm text-ink outline-none transition-colors duration-300 focus:border-accent";

export default function Projects() {
  const { t, person } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();

  const query = searchParams.get("q") ?? "";
  const category = searchParams.get("category") ?? "";
  const sort = searchParams.get("sort") ?? "order";
  const page = searchParams.get("page") ?? "1";
  const techs = useMemo(() => searchParams.getAll("tech"), [searchParams]);

  const [searchInput, setSearchInput] = useState(query);
  const [techsOpen, setTechsOpen] = useState(techs.length > 0);

  const updateParams = (updates, { resetPage = true } = {}) => {
    const next = new URLSearchParams(searchParams);
    for (const [key, value] of Object.entries(updates)) {
      next.delete(key);
      if (Array.isArray(value)) {
        value.forEach((item) => next.append(key, item));
      } else if (value) {
        next.set(key, value);
      }
    }
    if (resetPage) next.delete("page");
    setSearchParams(next, { replace: true });
  };

  // Debounce free-text search into the URL.
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== query) updateParams({ q: searchInput });
    }, 350);
    return () => clearTimeout(timer);
  }, [searchInput]); // eslint-disable-line react-hooks/exhaustive-deps

  const { data } = useFetch("/projects/", {
    q: query,
    category,
    sort: sort === "order" ? "" : sort,
    tech: techs,
    page: page === "1" ? "" : page,
  });

  const toggleTech = (slug) => {
    const next = techs.includes(slug)
      ? techs.filter((item) => item !== slug)
      : [...techs, slug];
    updateParams({ tech: next });
  };

  const hasFilters = Boolean(query || category || techs.length);
  const resultsLabel = data
    ? data.filtered_count !== data.total
      ? t(
          data.filtered_count === 1
            ? "projects.results_filtered_single"
            : "projects.results_filtered_plural",
          { count: data.filtered_count, total: data.total }
        )
      : t(
          data.total === 1
            ? "projects.results_all_single"
            : "projects.results_all_plural",
          { count: data.total }
        )
    : "";

  return (
    <PageShell title={t("meta.projects_title")}>
      <section className="hero-glow mx-auto max-w-6xl px-5 pb-8 pt-16 md:pt-20">
        <Reveal>
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.35em] text-accent">
            {t("nav.projects")}
          </p>
          <h1 className="font-display text-5xl font-semibold tracking-tight text-ink md:text-7xl">
            {t("projects.hero_title")}
          </h1>
        </Reveal>
      </section>

      <section className="sticky top-16 z-40 border-y border-line bg-bg/85 backdrop-blur-xl">
        <div className="mx-auto max-w-6xl space-y-3 px-5 py-4">
          <div className="flex flex-col gap-3 md:flex-row md:items-center">
            <input
              type="search"
              value={searchInput}
              onChange={(event) => setSearchInput(event.target.value)}
              placeholder={t("projects.search_placeholder")}
              className={`${SELECT_CLASSES} flex-1`}
              aria-label={t("projects.search_placeholder")}
            />
            <select
              value={category}
              onChange={(event) => updateParams({ category: event.target.value })}
              className={SELECT_CLASSES}
              aria-label={t("projects.all_categories")}
            >
              <option value="">{t("projects.all_categories")}</option>
              {data?.categories.map((item) => (
                <option key={item.slug} value={item.slug}>
                  {item.name} ({item.count})
                </option>
              ))}
            </select>
            <select
              value={sort}
              onChange={(event) => updateParams({ sort: event.target.value })}
              className={SELECT_CLASSES}
              aria-label={t("projects.sort_default")}
            >
              <option value="order">{t("projects.sort_default")}</option>
              <option value="recent">{t("projects.sort_recent")}</option>
              <option value="title">{t("projects.sort_title")}</option>
            </select>
            <button
              type="button"
              onClick={() => setTechsOpen((value) => !value)}
              aria-expanded={techsOpen}
              className={`${SELECT_CLASSES} text-left md:w-auto ${
                techs.length ? "border-accent text-accent" : "text-ink-dim"
              }`}
            >
              {t("projects.technologies", {
                count: data?.technologies.length ?? 0,
              })}
              {techs.length > 0 &&
                ` · ${t(
                  techs.length === 1
                    ? "projects.selected_count"
                    : "projects.selected_count_plural",
                  { count: techs.length }
                )}`}
            </button>
          </div>

          <AnimatePresence initial={false}>
            {techsOpen && data && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.35, ease: EASE }}
                className="overflow-hidden"
              >
                <p className="mb-2 text-xs text-ink-mute">
                  {t("projects.technology_hint")}
                </p>
                <div className="flex flex-wrap gap-2 pb-1">
                  {data.technologies.map((tech) => {
                    const active = techs.includes(tech.slug);
                    return (
                      <button
                        key={tech.slug}
                        type="button"
                        onClick={() => toggleTech(tech.slug)}
                        aria-pressed={active}
                        className={`rounded-full border px-3 py-1.5 font-mono text-xs transition-all duration-300 ${
                          active
                            ? "border-accent bg-accent font-semibold text-bg"
                            : "border-line text-ink-dim hover:border-accent/60 hover:text-ink"
                        }`}
                      >
                        {tech.name}
                        <span className="ml-1 opacity-60">({tech.count})</span>
                      </button>
                    );
                  })}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="font-mono text-xs text-ink-mute">{resultsLabel}</p>
            {hasFilters && (
              <button
                type="button"
                onClick={() => {
                  setSearchInput("");
                  setSearchParams({}, { replace: true });
                }}
                className="rounded-full border border-line px-3 py-1 font-mono text-xs text-ink-dim transition-colors duration-300 hover:border-accent hover:text-accent"
              >
                {t("projects.reset")}
              </button>
            )}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-12">
        {!data ? (
          <Loader />
        ) : data.results.length ? (
          <>
            <motion.div
              variants={stagger}
              initial="hidden"
              animate="visible"
              className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3"
            >
              <AnimatePresence mode="popLayout">
                {data.results.map((project) => (
                  <ProjectCard key={project.slug} project={project} />
                ))}
              </AnimatePresence>
            </motion.div>

            {data.num_pages > 1 && (
              <div className="mt-12 flex items-center justify-center gap-4">
                {data.page > 1 && (
                  <button
                    type="button"
                    onClick={() =>
                      updateParams(
                        { page: String(data.page - 1) },
                        { resetPage: false }
                      )
                    }
                    className="rounded-full border border-line px-6 py-2.5 text-sm font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
                  >
                    {t("projects.previous")}
                  </button>
                )}
                <span className="font-mono text-xs text-ink-mute">
                  {t("projects.page", {
                    current: data.page,
                    total: data.num_pages,
                  })}
                </span>
                {data.page < data.num_pages && (
                  <button
                    type="button"
                    onClick={() =>
                      updateParams(
                        { page: String(data.page + 1) },
                        { resetPage: false }
                      )
                    }
                    className="rounded-full border border-line px-6 py-2.5 text-sm font-semibold text-ink transition-colors duration-300 hover:border-accent hover:text-accent"
                  >
                    {t("projects.next")}
                  </button>
                )}
              </div>
            )}
          </>
        ) : (
          <Reveal className="py-16 text-center">
            <h2 className="font-display text-2xl font-semibold text-ink">
              {t("projects.empty_title")}
            </h2>
            <p className="mt-2 text-ink-dim">{t("projects.empty_body")}</p>
            <button
              type="button"
              onClick={() => {
                setSearchInput("");
                setSearchParams({}, { replace: true });
              }}
              className="mt-6 rounded-full bg-accent px-6 py-3 font-semibold text-bg transition-colors duration-300 hover:bg-accent-bright"
            >
              {t("projects.empty_cta")}
            </button>
          </Reveal>
        )}
      </section>

      <CtaBanner
        title={t("projects.cta_title")}
        body={t("projects.cta_body")}
        contactLabel={t("projects.cta_contact")}
        secondaryLabel={t("projects.cta_github")}
        secondaryHref={person.github}
        secondaryExternal
      />
    </PageShell>
  );
}
