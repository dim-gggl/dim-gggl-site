import { useEffect } from "react";
import { motion } from "framer-motion";
import { pageTransition } from "../lib/motion";

/**
 * Wraps every routed page: consistent enter/exit transition,
 * top padding under the fixed navbar, and document title.
 */
export default function PageShell({ title, children, className = "" }) {
  useEffect(() => {
    if (title) document.title = title;
  }, [title]);

  return (
    <motion.main
      variants={pageTransition}
      initial="initial"
      animate="animate"
      exit="exit"
      className={`pt-16 ${className}`}
    >
      {children}
    </motion.main>
  );
}
