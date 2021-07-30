const colors = require("tailwindcss/colors");
const plugin = require("tailwindcss/plugin");

module.exports = {
  purge: ["./source/js/**/*.{js,jsx}", "./network-api/networkapi/**/*.html"],
  mode: "jit",
  darkMode: "class", // use tw-dark
  important: true,
  corePlugins: {
    // overriding TW default container
    container: false,
  },
  plugins: [
    plugin(function ({ addUtilities }) {
      // Adding Column Count to Tailwind CSS
      const newUtilities = {
        ".col-count-1": {
          columnCount: 1,
        },
        ".col-count-2": {
          columnCount: 2,
        },
        ".col-count-3": {
          columnCount: 3,
        },
      };
      addUtilities(newUtilities);
    }),
    plugin(function ({ addComponents }) {
      addComponents([
        {
          "@media (min-width: 576px)": {
            ".container": {
              maxWidth: "540px",
            },
          },
        },
        {
          "@media (min-width: 768px)": {
            ".container": {
              maxWidth: "720px",
            },
          },
        },
        {
          "@media (min-width: 992px)": {
            ".container": {
              maxWidth: "960px",
            },
          },
        },
        {
          "@media (min-width: 1200px)": {
            ".container": {
              maxWidth: "1140px",
            },
          },
        },
        {
          ".container": {
            width: "100%",
            paddingRight: "1rem",
            paddingLeft: "1rem",
            marginRight: "auto",
            marginLeft: "auto",
          },
        },
        {
          ".row": {
            display: "flex",
            flexWrap: "wrap",
            marginRight: "-1rem",
            marginLeft: "-1rem",
          },
        },
      ]);
    }),
  ],
  theme: {
    extend: {
      fontWeight: {
        inherit: "inherit",
      },
      screens: {
        print: { raw: "print" },
      },
    },
    // Renaming breakpoints temporary until we remove bootstrap usage
    screens: {
      small: "576px",
      medium: "768px",
      large: "992px",
      xlarge: "1200px",
    },
    fontFamily: {
      sans: ["Nunito Sans", "Helvetica", "Arial", "sans-serif"],
      zilla: ["Zilla Slab", "sans-serif"],
    },
    colors: {
      transparent: "transparent",
      current: "currentColor",
      inherit: "inherit",
      black: colors.black,
      white: colors.white,
      gray: {
        "05": "#f2f2f2",
        20: "#cccccc",
        40: "#999999",
        60: "#666666",
        80: "#333333",
      },
      red: {
        DEFAULT: "#ff4f5e",
        light: "#ffe6e8",
        dark: "#cc0011",
      },
      blue: {
        DEFAULT: "#595cf3",
        dark: "#0d10bf",
        light: "#b7b9fa",
        lightest: "#e7e7fc",
      },
      pni: {
        lilac: "#d3d5fc",
        blue: "#1808f2",
        "blue-purple": "#4a17d4",
        purple: "#7f28b7",
        "purple-pink": "#b0379b",
        pink: "#e4487d",
        yellow: "#fbd545",
      },
      pulse: {
        pink: "#ff506f",
        purple: "#a66efd",
      },
      festival: {
        blue: "#0e11bf",
        purple: "#8f14fb",
      },
      "dear-internet": {
        lilac: "#d3d5fc",
        pink: "#fff0f1",
      },
      "youtube-regrets": {
        red: "#ea0b12",
        "red-lighter": "#fd6976",
        "red-light": "#ffdcdc",
        "red-dark": "#d73027",
        "gray-dark": "#696969",
        purple: "#353552",
      },
    },
  },
  variants: {
    extend: {},
  },
  prefix: "tw-",
};
