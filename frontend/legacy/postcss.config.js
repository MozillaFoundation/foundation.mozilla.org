const postcssImport = require("postcss-import");
const tailwindcss = require("tailwindcss");
const autoprefixer = require("autoprefixer");
const cssnano = require("cssnano");

const commonPlugins = [postcssImport, tailwindcss, autoprefixer];

const prodPlugins = [
  cssnano({
    preset: [
      "default",
      {
        discardComments: {
          removeAll: true,
        },
      },
    ],
  }),
];

module.exports = {
  plugins:
    process.env.NODE_ENV === "production"
      ? [...commonPlugins, ...prodPlugins]
      : commonPlugins,
};
