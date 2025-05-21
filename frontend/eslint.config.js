/** @type {import("eslint/use-at-your-own-risk").FlatConfig[]} */
export default [
  {
    files: ["**/*.js"],
    languageOptions: {
      globals: {
        es6: "writable",
      },
      parserOptions: {
        sourceType: "module",
        ecmaVersion: 2020,
      },
    }
  },
];
