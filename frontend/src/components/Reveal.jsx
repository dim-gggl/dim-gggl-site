import { motion } from "framer-motion";
import { EASE } from "../lib/motion";

/**
 * Scroll-reveal wrapper: fades and lifts its children into view once.
 */
export default function Reveal({
  children,
  delay = 0,
  y = 28,
  className,
  ...rest
}) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.7, delay, ease: EASE }}
      {...rest}
    >
      {children}
    </motion.div>
  );
}
