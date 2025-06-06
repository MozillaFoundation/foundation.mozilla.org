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
    // Allow kebab-case or BEM (block__element--modifier) class names:
    "selector-class-pattern": [
      // 1) block: lowercase + optional -words
      // 2) optional __element: lowercase + optional -words
      // 3) optional --modifier: lowercase + optional -words
      "^[a-z0-9]+(?:-[a-z0-9]+)*(?:__[a-z0-9]+(?:-[a-z0-9]+)*)?(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?$",
      {
        message:
          "Class selectors must be kebab-case (e.g. foo-bar) or BEM (e.g. foo-bar__element--modifier).",
      },
    ],
  },
};
