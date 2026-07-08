import { motion } from "framer-motion";

export default function Loader() {
  return (
    <div className="flex min-h-[40vh] items-center justify-center" role="status">
      <motion.span
        className="h-2.5 w-2.5 rounded-full bg-accent"
        animate={{ opacity: [1, 0.25, 1], scale: [1, 0.75, 1] }}
        transition={{ duration: 1.2, repeat: Infinity, ease: "easeInOut" }}
      />
    </div>
  );
}
