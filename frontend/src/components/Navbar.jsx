import { useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { useLanguage } from "../lib/LanguageContext";
import { EASE } from "../lib/motion";

function useNavItems() {
  const { t } = useLanguage();
  return [
    { to: "/", label: t("nav.home"), end: true },
    { to: "/ai/", label: t("nav.ai") },
    { to: "/cli/", label: t("nav.cli") },
    { to: "/django/", label: t("nav.django") },
    { to: "/projects/", label: t("nav.projects") },
    { to: "/about/", label: t("nav.about") },
  ];
}

function DesktopLink({ item, active }) {
  return (
    <NavLink
      to={item.to}
      end={item.end}
      className={`relative px-3 py-2 text-sm font-medium transition-colors duration-300 ${
        active ? "text-ink" : "text-ink-dim hover:text-ink"
      }`}
    >
      {item.label}
      {active && (
        <motion.span
          layoutId="nav-underline"
          className="absolute inset-x-3 -bottom-px h-px bg-accent"
          transition={{ duration: 0.4, ease: EASE }}
        />
      )}
    </NavLink>
  );
}

export default function Navbar() {
  const { t, lang, toggleLang } = useLanguage();
  const items = useNavItems();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const isActive = (item) =>
    item.end
      ? location.pathname === item.to
      : location.pathname.startsWith(item.to);

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-line bg-bg/75 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <Link
          to="/"
          className="group flex items-baseline gap-0.5 font-mono text-base font-semibold tracking-tight text-ink"
          aria-label="dim-gggl — home"
        >
          <span className="text-accent">~/</span>
          <span>dim-gggl</span>
          <span className="cursor-blink ml-1 inline-block h-4 w-2 translate-y-0.5 bg-accent" />
        </Link>

        <nav className="hidden items-center md:flex" aria-label="Primary">
          {items.map((item) => (
            <DesktopLink key={item.to} item={item} active={isActive(item)} />
          ))}
          <button
            type="button"
            onClick={toggleLang}
            aria-label={
              lang === "fr" ? t("nav.switch_to_english") : t("nav.switch_to_french")
            }
            className="ml-4 rounded-full border border-line px-3 py-1 font-mono text-xs font-semibold uppercase text-ink-dim transition-colors duration-300 hover:border-accent hover:text-accent"
          >
            {lang === "fr" ? "EN" : "FR"}
          </button>
        </nav>

        <button
          type="button"
          className="flex h-10 w-10 flex-col items-center justify-center gap-1.5 md:hidden"
          onClick={() => setOpen((value) => !value)}
          aria-label={t("nav.menu")}
          aria-expanded={open}
        >
          <motion.span
            animate={open ? { rotate: 45, y: 4 } : { rotate: 0, y: 0 }}
            className="block h-px w-6 bg-ink"
          />
          <motion.span
            animate={open ? { rotate: -45, y: -3 } : { rotate: 0, y: 0 }}
            className="block h-px w-6 bg-ink"
          />
        </button>
      </div>

      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.35, ease: EASE }}
            className="overflow-hidden border-t border-line bg-bg/95 backdrop-blur-xl md:hidden"
            aria-label="Mobile"
          >
            <div className="flex flex-col px-5 py-4">
              {items.map((item, index) => (
                <motion.div
                  key={item.to}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.05 * index, duration: 0.3, ease: EASE }}
                >
                  <NavLink
                    to={item.to}
                    end={item.end}
                    onClick={() => setOpen(false)}
                    className={`block py-3 font-display text-lg ${
                      isActive(item) ? "text-accent" : "text-ink-dim"
                    }`}
                  >
                    {item.label}
                  </NavLink>
                </motion.div>
              ))}
              <button
                type="button"
                onClick={() => {
                  toggleLang();
                  setOpen(false);
                }}
                className="mt-3 w-fit rounded-full border border-line px-4 py-1.5 font-mono text-xs font-semibold uppercase text-ink-dim"
              >
                {lang === "fr" ? "EN" : "FR"}
              </button>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
