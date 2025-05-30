import postcssImport from "postcss-import";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import cssnano from "cssnano";

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

export default {
  plugins:
    process.env.NODE_ENV === "production"
      ? [...commonPlugins, ...prodPlugins]
      : commonPlugins,
};
