/* eslint-disable prettier/prettier */
const colors = require("tailwindcss/colors");
const plugin = require("tailwindcss/plugin");
const componentPlugins = require("./tailwind-plugins/components");
const buttonPlugins = require("./tailwind-plugins/button");
const typePlugins = require("./tailwind-plugins/type");
const glyphPlugins = require("./tailwind-plugins/glyph");

module.exports = {
  content: ["./source/js/**/*.{js,jsx}", "./network-api/networkapi/**/*.html"],
  darkMode: "class", // use tw-dark
  important: true,
  corePlugins: {
    // overriding TW default container
    container: false,
    // eventually we have to extract what bootstrap base/reset styles we need
    preflight: false,
  },
  plugins: [
    plugin(function ({ addUtilities }) {
      // Adding Column Count to Tailwind CSS
      const newUtilities = {
        ".hash": {
          content: '"#"',
        },
        ".no-scrollbar::-webkit-scrollbar": {
          display: "none",
        },
        ".no-scrollbar": {
          "-ms-overflow-style": "none" /* IE and Edge */,
          "scrollbar-width": "none" /* Firefox */,
        },
      };
      addUtilities(newUtilities);
    }),
    plugin(function ({ addBase, addVariant }) {
      const newBase = {
        "*,::before,::after": {
          borderWidth: 0,
          borderStyle: "solid",
        },
        "img,svg,video,canvas,audio,iframe,embed,object": {
          display: "block",
          verticalAlign: "middle",
        },
      };
      addVariant("summary-open", ["details[open] > summary > &"]);
      addVariant("details-open", ["details[open] > &"]);
      addBase(newBase);
    }),
    ...componentPlugins,
    ...buttonPlugins,
    ...typePlugins,
    ...glyphPlugins,
    require("@tailwindcss/forms")({ strategy: "class" }),
    require("@tailwindcss/line-clamp"),
    require('@tailwindcss/aspect-ratio'),
  ],
  theme: {
    extend: {
      fontWeight: {
        inherit: "inherit",
      },
      cursor: {
        grabbing: "grabbing",
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
    // Remove after removing SASS/Bootstrap
    screens: {
      small: "576px",
      medium: "768px",
      large: "992px",
      xlarge: "1200px",
    },
    fontFamily: {
      sans: ["Nunito Sans", "Helvetica", "Arial", "sans-serif"],
      zilla: ["Zilla Slab", "sans-serif"],
      changa: ["Changa", "sans-serif"],
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
        "05": "#ffe6e8",
        10: "#ffb4ba",
        20: "#ff818c",
        40: "#ff4f5e",
        60: "#e62434",
        80: "#cc0011",
        100: "#9a000e",
      },
      blue: {
        "05": "#e7e7fc",
        10: "#d3d5fc",
        20: "#b7b9fa",
        40: "#595cf3",
        60: "#3032d9",
        80: "#0d10bf",
        100: "#0003a6",
      },
      cyan: {
        "05": "#e6ffff",
        10: "#acffff",
        20: "#73ffff",
        40: "#00ffff",
        60: "#00c9c9",
        80: "#009494",
        100: "#005e5e",
      },
      green: {
        "05": "#d8fff0",
        10: "#acffe0",
        20: "#80ffce",
        40: "#54ffbd",
        60: "#2cc98e",
        80: "#109462",
        100: "#005e3a",
      },
      yellow: {
        "05": "#fffcd9",
        10: "#fff9ab",
        20: "#fff67d",
        40: "#fff44f",
        60: "#e5d92f",
        80: "#ccbf15",
        100: "#b2a600",
      },
      purple: {
        "05": "#ecd8fe",
        10: "#deb8fe",
        20: "#cd97fd",
        40: "#8f14fb",
        60: "#760bd4",
        80: "#5e05ac",
        100: "#470085",
      },
      pink: {
        "05": "#ffe5f1",
        10: "#ffbedc",
        20: "#ff98c6",
        40: "#ff298a",
        60: "#cc1165",
        80: "#9a0146",
        100: "#66012f",
      },
      pni: {
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
          100: "#2e05ff",
        },
        purple: {
          100: "#fa00ff",
        },
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
  // TODO remove after removing SASS/Bootstrap
  prefix: "tw-",
};
