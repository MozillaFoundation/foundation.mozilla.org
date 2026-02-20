// Using CommonJS (.cjs) to avoid the need for --config-type=module (only in Stylelint v16+).
// We're on Stylelint v17 with stylelint-scss v7 for the latest features and Node 20+ support.

module.exports = {
  customSyntax: "postcss-scss",
  extends: [
    "stylelint-config-standard-scss",
  ],
  ignoreFiles: [
    "../../foundation_cms/static/scss/settings/customized-settings.scss",
    "../../foundation_cms/static/scss/settings/foundation-framework-defaults.scss",
  ],
  rules: {
    "block-no-empty": true,
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
    // Disable deprecated rule
    "scss/at-import-no-partial-leading-underscore": null,
    // Disallow relative image paths
    "declaration-property-value-disallowed-list": [
      {
        "/^background(-image)?$/": [
          "/\\.\\.\\//",
          "/^\\.\\//",
        ],
        "/^content$/": [
          "/\\.\\.\\//",
          "/^\\.\\//",
        ],
      },
      {
        message: "Use absolute paths (starting with /) for images instead of relative paths",
      }
    ],
    "no-descending-specificity": null,
  },
};
