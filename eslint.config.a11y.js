const jsxA11y = require("eslint-plugin-jsx-a11y");
const jsxA11yRecommended = require("eslint-plugin-jsx-a11y/recommended");

module.exports = [
  {
    plugins: {
      "jsx-a11y": jsxA11y,
    },
  },
  jsxA11yRecommended,
];
