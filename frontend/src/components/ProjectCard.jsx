import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { staggerItem } from "../lib/motion";
import { ArrowIcon } from "./icons";

/**
 * Modern project card: quiet surface, per-project accent tint on hover,
 * card artwork floating over a soft gradient.
 */
export default function ProjectCard({ project, origin }) {
  const href = origin
    ? `${project.url}?from=${origin}`
    : project.url;
  const image = project.card_image || project.featured_image;
  const accent = project.primary_color || "#a3e635";

  return (
    <motion.article
      variants={staggerItem}
      layout
      className="group relative"
      style={{ "--card-accent": accent }}
    >
      <Link
        to={href}
        className="block overflow-hidden rounded-2xl border border-line bg-surface transition-all duration-500 hover:-translate-y-1.5 hover:border-(--card-accent) hover:shadow-[0_24px_60px_-24px_rgba(0,0,0,0.9)]"
      >
        <div
          className="relative flex aspect-[16/10] items-center justify-center overflow-hidden"
          style={{
            background: `radial-gradient(ellipse 90% 90% at 50% 110%, ${accent}14, transparent 65%)`,
          }}
        >
          {image ? (
            <img
              src={image}
              alt={project.title}
              loading="lazy"
              className="max-h-[70%] max-w-[70%] object-contain drop-shadow-2xl transition-transform duration-700 ease-out group-hover:scale-105"
            />
          ) : (
            <span
              className="font-display text-4xl font-semibold opacity-40"
              style={{ color: accent }}
            >
              {project.title.slice(0, 2)}
            </span>
          )}
          {project.category && (
            <span className="absolute left-4 top-4 rounded-full border border-line bg-bg/70 px-3 py-1 font-mono text-[11px] text-ink-dim backdrop-blur-sm">
              {project.category.name}
            </span>
          )}
        </div>

        <div className="flex flex-col gap-3 border-t border-line p-5">
          <div className="flex items-center justify-between gap-3">
            <h3 className="font-display text-lg font-semibold tracking-tight text-ink transition-colors duration-300 group-hover:text-(--card-accent)">
              {project.title}
            </h3>
            <ArrowIcon className="h-4 w-4 shrink-0 -translate-x-1 text-ink-mute opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:text-(--card-accent) group-hover:opacity-100" />
          </div>
          {project.tagline && (
            <p className="line-clamp-2 text-sm leading-relaxed text-ink-dim">
              {project.tagline}
            </p>
          )}
          <div className="mt-1 flex flex-wrap gap-1.5">
            {project.technologies.slice(0, 4).map((tech) => (
              <span
                key={tech.slug}
                className="rounded-md border border-line bg-raised px-2 py-0.5 font-mono text-[11px] text-ink-dim"
              >
                {tech.name}
              </span>
            ))}
            {project.technologies.length > 4 && (
              <span className="rounded-md px-2 py-0.5 font-mono text-[11px] text-ink-mute">
                +{project.technologies.length - 4}
              </span>
            )}
          </div>
        </div>
      </Link>
    </motion.article>
  );
}
