const plugin = require("tailwindcss/plugin");

function shared(theme) {
  const media = (breakpoint) => `@media (min-width: ${breakpoint})`;

  return {
    ".nav-accordion-content-inner": {
      display: "flex",
      flexDirection: "column",
      background: "white",
      gap: theme("gap.8"),
      [media(theme("screens.xlarge"))]: {
        display: "grid",
        gap: `${theme("gap.0")} ${theme("gap.8")}`,
        borderLeftWidth: "40px",
        borderRightWidth: "40px",
        borderLeftColor: theme("colors.white"),
        borderRightColor: theme("colors.white"),
        "&.has-featured-column": {
          borderRightColor: theme("colors.gray.02"),
        },
      },
    },
    ".nav-dropdown-column": {
      display: "flex",
      flexDirection: "column",
      alignItems: "start",
      flex: "1",
      [media(theme("screens.xlarge"))]: {
        marginTop: theme("margin.22"),
        marginBottom: theme("margin.22"),
      },
      "&.featured-column": {
        padding: `${theme("padding.8")} ${theme("padding.12")}`,
        [media(theme("screens.xlarge"))]: {
          marginTop: 0,
          marginBottom: 0,
          paddingTop: theme("padding.22"),
          paddingBottom: theme("padding.22"),
        },
      },
    },
  };
}

module.exports = [
  plugin(function ({ addComponents, theme }) {
    addComponents([shared(theme)]);
  }),
];
