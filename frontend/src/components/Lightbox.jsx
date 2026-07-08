import { useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { EASE } from "../lib/motion";

export default function Lightbox({ src, alt, onClose, closeLabel }) {
  useEffect(() => {
    if (!src) return;
    const onKey = (event) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [src, onClose]);

  return (
    <AnimatePresence>
      {src && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
          className="fixed inset-0 z-[70] flex flex-col bg-bg/95 backdrop-blur-md"
          onClick={onClose}
        >
          <div className="flex justify-end p-4">
            <button
              type="button"
              onClick={onClose}
              className="rounded-full border border-line bg-surface px-4 py-1.5 font-mono text-xs text-ink-dim transition-colors hover:border-accent hover:text-accent"
            >
              {closeLabel}
            </button>
          </div>
          <div
            className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-4 pb-10 sm:px-8"
            onClick={(event) => event.stopPropagation()}
          >
            <motion.img
              initial={{ opacity: 0, y: 24, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.4, ease: EASE }}
              src={src}
              alt={alt}
              className="mx-auto block h-auto w-full max-w-4xl select-none rounded-2xl border border-line"
              draggable={false}
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
