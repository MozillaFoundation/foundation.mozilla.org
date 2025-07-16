// frontend/legacy/lint-js.js (Re-written frontend/redesign/lint-js.js to CommonJS)

const path = require("path");
const { ESLint } = require("eslint");

const rootPath = path.resolve(__dirname, "../../");
const eslintConfigPath = path.join(
  rootPath,
  "frontend/legacy/eslint.config.js"
);

(async function () {
  const eslint = new ESLint({
    overrideConfigFile: eslintConfigPath,
    ignore: false,
    cwd: rootPath,
    fix: process.argv.includes("--fix"),
  });

  const results = await eslint.lintFiles([
    "foundation_cms/legacy_apps/static/js/**/*.js",
    "foundation_cms/legacy_apps/static/js/**/*.jsx",
    "foundation_cms/legacy_apps/wagtailcustomization/**/*.js",
    "frontend/legacy/**/*.js",
  ]);

  await ESLint.outputFixes(results);

  const formatter = await eslint.loadFormatter("stylish");
  console.log(formatter.format(results));

  if (results.some((r) => r.errorCount > 0)) {
    process.exit(1);
  }
})();
