import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [
    vue(),
  ],
  root: resolve("./src"),
  base: "/static/",
  server: {
    host: "localhost",
    port: 5183,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    alias: {
      "@": resolve("src"),
    },
    extensions: [".js", ".jsx", ".ts", ".tsx", ".vue", ".json"],
  },
  optimizeDeps: {
    include: ["vue"],
  },
  build: {
    outDir: resolve("../djing/dist"),
    assetsDir: resolve("./src/assets"),
    manifest: "manifest.json",
    emptyOutDir: true,
    target: "es2015",
    rollupOptions: {
      input: ["./src/index.ts", "./src/index.css", "./src/components.ts"],
      output: {
        entryFileNames: "djing/js/[name].js",
        chunkFileNames: "djing/js/[name].js",
        assetFileNames: "djing/[ext]/[name].[ext]",
        compact: true,
        manualChunks: {
          vue: ["vue"],
        },
      },
    },
  },
});
