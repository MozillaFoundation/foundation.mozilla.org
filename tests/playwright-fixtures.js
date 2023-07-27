const { playwrightTest } = require("@axe-core/watcher");
const PLAYWRIGHT_CONFIG = require("../playwright.config.js");

module.exports = playwrightTest({
  axe: {
    apiKey: "535ab4de-5290-4325-9274-6be0dc8fa4ef",
  },
  headless: false,
});
