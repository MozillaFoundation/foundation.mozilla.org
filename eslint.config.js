const eslintPluginPrettier = require("eslint-plugin-prettier");
const eslintPluginPrettierRecommended = require("eslint-plugin-prettier/recommended");
const eslintPluginReact = require("eslint-plugin-react");

module.exports = [
  {
    plugins: {
      prettier: eslintPluginPrettier,
      react: eslintPluginReact,
    },
    languageOptions: {
      globals: {
        es6: "writable",
      },
      parserOptions: {
        sourceType: "module",
        ecmaVersion: 2020,
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
