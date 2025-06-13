// Using CommonJS (.cjs) to avoid the need for --config-type=module (only in Stylelint v16+).
// We're on Stylelint v15 for compatibility with stylelint-scss, since v5.3.x breaks on Node 20.
// This avoids runtime issues and works better with Yarn v1, CI, and cross-platform setups.

module.exports = {
  customSyntax: "postcss-scss",
  extends: "stylelint-config-standard-scss",
  ignoreFiles: [
    "../../foundation_cms/static/scss/settings/customized-settings.scss",
    "../../foundation_cms/static/scss/settings/foundation-framework-defaults.scss",
  ],
  rules: {
    "block-no-empty": true,
    "selector-class-pattern": [
      "^[a-z0-9]+(?:-[a-z0-9]+)*(?:__(?:[a-z0-9]+(?:-[a-z0-9]+)*))?(?:--(?:[a-z0-9]+(?:-[a-z0-9]+)*))?$",
      {
        message:
          "Expected class selector to be kebab-case or BEM (block__element--modifier)",
      },
    ],
  },
};
