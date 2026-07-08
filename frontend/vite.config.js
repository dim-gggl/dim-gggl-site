import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// The build is consumed by Django: assets land in static/frontend/ with
// stable names, referenced from core/templates/core/spa.html via
// {% static %} (WhiteNoise adds content hashes at collectstatic time).
export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: "/static/frontend/",
  build: {
    outDir: "../static/frontend",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/main.jsx",
      output: {
        entryFileNames: "assets/app.js",
        chunkFileNames: "assets/[name].js",
        assetFileNames: "assets/app[extname]",
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/media": "http://127.0.0.1:8000",
      "/static/images": "http://127.0.0.1:8000",
      "/static/favicon": "http://127.0.0.1:8000",
    },
  },
});
