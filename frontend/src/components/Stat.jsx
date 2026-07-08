import { useEffect, useRef } from "react";
import {
  animate,
  motion,
  useInView,
  useMotionValue,
  useTransform,
} from "framer-motion";
import { staggerItem } from "../lib/motion";

/**
 * Stat tile whose number counts up when scrolled into view.
 */
export default function Stat({ value, suffix = "+", label }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-40px" });
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest));

  useEffect(() => {
    if (inView) {
      const controls = animate(count, value, { duration: 1.6, ease: "easeOut" });
      return controls.stop;
    }
  }, [inView, value, count]);

  return (
    <motion.div
      ref={ref}
      variants={staggerItem}
      className="rounded-2xl border border-line bg-surface p-6"
    >
      <p className="font-display text-4xl font-semibold tracking-tight text-accent md:text-5xl">
        <motion.span>{rounded}</motion.span>
        {suffix}
      </p>
      <p className="mt-2 text-sm text-ink-dim">{label}</p>
    </motion.div>
  );
}
