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
        lineHeight: "1.25rem",
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
        position: "relative",
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
        ".chevron": {
          position: "absolute",
          right: 0,
          width: "20px",
          height: "20px",
          backgroundRepeat: "no-repeat",
          backgroundPosition: `right 0 top 50%`,
          backgroundImage: 'url("../_images/glyphs/down-chevron.svg")',
          backgroundSize: `cover`,
          transition: "transform 0.15s",
        },
        "&[aria-expanded='true'] .chevron": {
          transform: "rotate(180deg)",
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