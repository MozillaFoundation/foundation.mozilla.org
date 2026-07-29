import path from "path";
import { fileURLToPath } from "url";
import { defineConfig } from "vitest/config";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Coverage matches file paths relative to `root`, so `root` must span both
// this config and the JS source under foundation_cms for coverage to work.
const repoRoot = path.resolve(__dirname, "../..");

export default defineConfig({
  root: repoRoot,
  test: {
    environment: "jsdom",
    include: ["foundation_cms/static/js/**/*.test.js"],
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      reportsDirectory: path.join(__dirname, "coverage"),
      include: ["foundation_cms/static/js/**/*.js"],
      exclude: ["foundation_cms/static/js/**/*.test.js"],
    },
  },
});
