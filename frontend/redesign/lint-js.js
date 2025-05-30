// We use this file because ESLint's CLI does not allow linting files
// outside the current working directory (e.g., from ./frontend to ../foundation_cms).
// By using the ESLint Node API, we can bypass that limitation.

import path from "path";
import { fileURLToPath } from "url";
import { ESLint } from "eslint";

// Get the current directory of this script (i.e., /frontend)
const __dirname = path.dirname(fileURLToPath(import.meta.url));
// These paths need to be in absolute format
const rootPath = path.resolve(__dirname, "../../");
const eslintConfigPath = path.join(rootPath, "frontend/eslint.config.js");

// Wrap in async IIFE to use await at top level in environments that don't support top-level await
(async () => {
  // Create an instance of ESLint using our flat config file in /frontend
  const eslint = new ESLint({
    overrideConfigFile: eslintConfigPath,
    // By default, ESLint ignores files outside the current working directory
    // and respects .eslintignore or default rules (like ignoring node_modules).
    // Setting ignore: false disables that behavior, allowing us to lint files
    // outside /frontend (e.g., in ../foundation_cms) via the Node API.
    ignore: false,
    cwd: rootPath,
    fix: process.argv.includes("--fix"),
  });

  const results = await eslint.lintFiles([
    "foundation_cms/static/js/**/*.js",
    "frontend/**/*.js",
  ]);

  // Write fixes to disk if any
  await ESLint.outputFixes(results);

  // Format the results using ESLint's default formatter
  const formatter = await eslint.loadFormatter("stylish");
  const resultText = formatter.format(results);

  console.log(resultText);

  // Exit with error code 1 if any errors were found
  const hasErrors = results.some((r) => r.errorCount > 0);
  if (hasErrors) process.exit(1);
})();
