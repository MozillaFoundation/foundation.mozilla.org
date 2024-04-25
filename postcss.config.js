let commonPlugins = [
  require("postcss-import"),
  require("tailwindcss"),
  require("autoprefixer"),
  require("postcss-custom-properties")({
    importFrom: [
      {
        customProperties: {
          "--asset-domain": process.env.ASSET_DOMAIN,
          "--font-sans-300": `url("${process.env.FONT_SANS_300 || ""}")`,
          "--font-sans-400": `url("${process.env.FONT_SANS_400 || ""}")`,
          "--font-sans-700": `url("${process.env.FONT_SANS_700 || ""}")`,
          "--font-semi-slab-300": `url("${process.env.FONT_SEMI_SLAB_300 || ""}")`,
          "--font-semi-slab-400": `url("${process.env.FONT_SEMI_SLAB_400 || ""}")`,
          "--font-semi-slab-600": `url("${process.env.FONT_SEMI_SLAB_600 || ""}")`,
          "--font-semi-slab-700": `url("${process.env.FONT_SEMI_SLAB_700 || ""}")`,
        },
      },
    ],
    preserve: false,
  }),
];

let prodPlugins = [
  require("cssnano")({
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
      ? commonPlugins.concat(prodPlugins)
      : commonPlugins,
};
