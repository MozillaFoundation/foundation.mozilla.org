import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["../../foundation_cms/static/js/**/*.test.js"],
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
    },
  },
});
