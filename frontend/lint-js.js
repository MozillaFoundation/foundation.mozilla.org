// We use this file because ESLint's CLI does not allow linting files
// outside the current working directory (e.g., from ./frontend to ../foundation_cms).
// By using the ESLint Node API, we can bypass that limitation.

import path from "path";
import { fileURLToPath } from "url";
import { ESLint } from "eslint";

// Get the current directory of this script (i.e., /frontend)
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Absolute path to foundation_cms
const foundationCmsPath = path.resolve(__dirname, "../foundation_cms");

// Absolute path to the ESLint config in /frontend
const configPath = path.resolve(__dirname, "./eslint.config.js");

// Create an instance of ESLint using our flat config file in /frontend
const eslint = new ESLint({
  overrideConfigFile: configPath, // this needs to be an absolute path
  ignore: false, // By default, ESLint ignores files outside the current working directory
                 // and respects .eslintignore or default rules (like ignoring node_modules).
                 // Setting ignore: false disables that behavior, allowing us to lint files
                 // outside /frontend (e.g., in ../foundation_cms) via the Node API.
  cwd: foundationCmsPath // this needs to be an absolute path

});

const results = await eslint.lintFiles([
   "static/js/**/*.js",                 // all JS files in foundation_cms/static/js/
]);


// Format the results using ESLint's default formatter
const formatter = await eslint.loadFormatter("stylish");
const resultText = formatter.format(results);

console.log(resultText);

// Exit with error code 1 if any errors were found
const hasErrors = results.some(r => r.errorCount > 0);
if (hasErrors) process.exit(1);
