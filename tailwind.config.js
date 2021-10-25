/* eslint-disable prettier/prettier */
const colors = require("tailwindcss/colors");
const plugin = require("tailwindcss/plugin");
const componentPlugins = require("./tailwind.components");

module.exports = {
  purge: ["./source/js/**/*.{js,jsx}", "./network-api/networkapi/**/*.html"],
  mode: "jit",
  darkMode: "class", // use tw-dark
  important: true,
  corePlugins: {
    // overriding TW default container
    container: false
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
        ".hash": {
          content: "\"#\"",
        }
      };
      addUtilities(newUtilities);
    }),
    ...componentPlugins,
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
    // Overriding default spacing
    spacing: {
      0: "0",
      px: "1px",
      1: "0.25rem",
      2: "0.5rem",
      3: "0.75rem",
      4: "1rem",
      5: "1.5rem",
      6: "2rem",
      7: "3rem",
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
      table: "#dee2e6",
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
        blue: {
          DEFAULT: "#0e11bf",
          100: "#4C56EC",
        },
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
