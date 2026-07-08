import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { useLanguage } from "../lib/LanguageContext";
import { EASE } from "../lib/motion";

/**
 * Terminal window that types the historical intro sequence line by line.
 * Reuses the original intro copy from the translation catalog.
 */
export default function Terminal() {
  const { t } = useLanguage();
  const lines = useMemo(
    () =>
      [1, 2, 3, 4, 5, 6, 7].map((index) => t(`intro.line_${index}`)),
    [t]
  );
  const [visibleCount, setVisibleCount] = useState(0);

  useEffect(() => {
    setVisibleCount(0);
    const timer = setInterval(() => {
      setVisibleCount((count) => {
        if (count >= lines.length) {
          clearInterval(timer);
          return count;
        }
        return count + 1;
      });
    }, 380);
    return () => clearInterval(timer);
  }, [lines]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 24, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.8, delay: 0.5, ease: EASE }}
      className="w-full overflow-hidden rounded-2xl border border-line bg-surface/80 shadow-[0_32px_80px_-32px_rgba(0,0,0,0.9)] backdrop-blur"
    >
      <div className="flex items-center gap-2 border-b border-line px-4 py-3">
        <span className="h-2.5 w-2.5 rounded-full bg-[#ff5f57]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[#febc2e]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[#28c840]" />
        <span className="ml-3 font-mono text-xs text-ink-mute">
          dim-gggl — zsh
        </span>
      </div>
      <div className="min-h-44 px-5 py-4 font-mono text-[13px] leading-7 text-ink-dim">
        {lines.slice(0, visibleCount).map((line, index) => (
          <motion.p
            key={index}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.25 }}
            className={
              index >= 4 ? "font-semibold text-accent" : undefined
            }
          >
            {line || " "}
          </motion.p>
        ))}
        <p>
          <span className="text-accent">➜</span>
          <span className="cursor-blink ml-2 inline-block h-3.5 w-2 translate-y-0.5 bg-accent" />
        </p>
      </div>
    </motion.div>
  );
}
