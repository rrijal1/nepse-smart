import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [vue(), tailwindcss()],
    resolve: {
      alias: {
        "@": new URL("./src", import.meta.url).pathname,
      },
    },
    server: {
      port: 3000,
      proxy: {
        "/api": {
          target: env.VITE_API_BASE_URL || "http://backend:8000",
          changeOrigin: true,
          rewrite: (path) => path,
        },
        "/ws": {
          target: env.VITE_API_BASE_URL || "http://backend:8000",
          changeOrigin: true,
          ws: true,
        },
      },
    },
  };
});
