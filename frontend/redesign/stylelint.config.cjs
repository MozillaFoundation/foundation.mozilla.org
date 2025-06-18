// Using CommonJS (.cjs) to avoid the need for --config-type=module (only in Stylelint v16+).
// We're on Stylelint v15 for compatibility with stylelint-scss, since v5.3.x breaks on Node 20.
// This avoids runtime issues and works better with Yarn v1, CI, and cross-platform setups.

module.exports = {
  customSyntax: "postcss-scss",
  extends: [
    "stylelint-config-standard-scss",
    // Add "stylelint-config-prettier" last to disable any Stylelint rules that would conflict with Prettier's formatting.
    // This ensures that Prettier handles all code style decisions (e.g., spacing, indentation, line breaks),
    // and Stylelint focuses only on code quality and SCSS best practices — not formatting.
    "stylelint-config-prettier"
  ],
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
    // Disable this rule to avoid conflict with Prettier line breaks
    "scss/dollar-variable-colon-space-after": null,
    "selector-class-pattern": [
      "^[a-z0-9]+(?:-[a-z0-9]+)*(?:__(?:[a-z0-9]+(?:-[a-z0-9]+)*))?(?:--(?:[a-z0-9]+(?:-[a-z0-9]+)*))?$",
      {
        message:
          "Expected class selector to be kebab-case or BEM (block__element--modifier)",
      },
    ],
  },
};
