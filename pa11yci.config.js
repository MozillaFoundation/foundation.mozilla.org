// const BASE_URL = "https://foundation.mozilla.org";
const BASE_URL = "http://localhost:8000";

module.exports = {
  defaults: {
    concurrency: 4,
    standard: "WCAG2AA",
    runners: ["axe", "htmlcs"],
    reporters: [
      "cli",
      ["pa11y-ci-reporter-html", { destination: "./pa11y-reports" }],
    ],
  },
  urls: [
    BASE_URL,
    BASE_URL + "/blog",
    BASE_URL + "/campaigns",
    BASE_URL + "/about",
  ],
};
