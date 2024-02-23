const plugin = require("tailwindcss/plugin");

function shared(theme) {
  const media = (breakpoint) => `@media (min-width: ${breakpoint})`;

  return {
    ".overview-heading": {
      fontFamily: theme("fontFamily.zilla"),
      fontStyle: "italic",
      fontSize: "1.375rem",
      lineHeight: "1.75rem",
      fontWeight: theme("fontWeight.medium"),
      marginBottom: theme("margin.10"),
      [media(theme("screens.medium"))]: {
        fontSize: "1.5rem",
        lineHeight: "1.25",
      },
    },
    ".overview-description": {
      fontFamily: theme("fontFamily.sans"),
      fontStyle: "normal",
      fontSize: "1rem",
      fontWeight: theme("fontWeight.normal"),
      lineHeight: "normal",
    },
  };
}

function widePrimaryNavComponents(theme) {
  return {
    ".secondary-nav-link": {
      color: theme("colors.black"),
      fontSize: theme("fontSize.lg"),
      fontWeight: theme("fontWeight.semibold"),
      transition: "transform 0.15s",
      "&:hover": {
        color: theme("colors.blue.80"),
        fontFamily: theme("fontFamily.sans"),
        textDecoration: "underline",
      },
    },
  };
}

function narrowPrimaryNavComponents(theme) {
  return {
    ".narrow-screen-menu-container": {
      ".primary-nav": {
        color: theme("colors.black"),
        fontFamily: theme("fontFamily.sans"),
        fontSize: theme("fontSize.lg"),
        fontStyle: theme("fontStyle.normal"),
        fontWeight: theme("fontWeight.bold"),
        lineHeight: theme("lineHeight.none"),
        textTransform: theme("textTransform.captilize"),
        "&:hover, &:focus, &:focus-visible, &:focus-within, &:active": {
          textDecoration: "none",
        },
      },
    },
  };
}

module.exports = [
  plugin(function ({ addComponents, theme }) {
    addComponents([
      shared(theme),
      widePrimaryNavComponents(theme),
      narrowPrimaryNavComponents(theme),
    ]);
  }),
];
