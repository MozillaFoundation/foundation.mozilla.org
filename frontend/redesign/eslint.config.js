/** @type {import("eslint/use-at-your-own-risk").FlatConfig[]} */
export default [
  {
    ignores: ["**/coverage/**"],
  },
  {
    files: ["**/*.js"],
    languageOptions: {
      globals: {
        es6: "writable",
      },
      parserOptions: {
        sourceType: "module",
        ecmaVersion: 2022,
      },
    },
  },
];
