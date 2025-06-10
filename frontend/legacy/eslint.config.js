const eslintPluginPrettier = require("eslint-plugin-prettier");
const eslintPluginPrettierRecommended = require("eslint-plugin-prettier/recommended");
const eslintPluginReact = require("eslint-plugin-react");
const jsxA11y = require("eslint-plugin-jsx-a11y");

module.exports = [
  {
    files: ["**/*.js", "**/*.jsx"],
    plugins: {
      prettier: eslintPluginPrettier,
      react: eslintPluginReact,
      "jsx-a11y": jsxA11y,
    },
    languageOptions: {
      globals: {
        es6: "writable",
      },
      parserOptions: {
        sourceType: "module",
        ecmaVersion: 2022,
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    rules: {
      "prettier/prettier": [
        "error",
        {
          trailingComma: "es5",
          endOfLine: "auto",
        },
      ],
      "react/jsx-uses-vars": "error",
    },
  },
  eslintPluginPrettierRecommended,
];
