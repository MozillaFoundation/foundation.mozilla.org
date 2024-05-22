const plugin = require("tailwindcss/plugin");

function shared(theme) {
  const media = (breakpoint) => `@media (min-width: ${breakpoint})`;

  return {
    ".nav-mobile-dropdown": {
      "&[data-should-wayfinding-be-actzive='true']": {
        borderInlineStartWidth: theme("borderWidth.4"),
        borderColor: theme("colors.gray.60"),
        "[data-accordion-button]": {
          "&[aria-expanded='true']": {
            span: {
              borderInlineStartWidth: 0,
              borderColor: theme("colors.gray.60"),
              borderBottomWidth: theme("borderWidth.4"),
            },
          },
          "&:hover": {
            span: {
              textDecorationLine: "none",
            },
          },
        },
      },
      "[data-accordion-button]": {
        border: "none",
        "&:focus": {
          background: theme("colors.blue.03"),
        },
        "&:hover": {
          background: theme("colors.blue.03"),
          span: {
            textDecorationLine: "underline",
          },
        },
      },
    },
    ".nav-desktop-dropdown": {
      "[data-accordion-button]": {
        span: {
          borderLeftWidth: 0,
          borderRightWidth: 0,
          borderTopWidth: 0,
          borderBottomWidth: 0,
          paddingTop: 0,
          paddingBottom: 0,
        },
        [media(theme("screens.xlarge"))]: {
          border: "none",
          span: {
            borderBottomWidth: theme("borderWidth.6"),
            borderBottomColor: "transparent",
            color: "black",
            "[data-should-wayfinding-be-active='true']&": {
              borderBottomColor: "black",
            },
            "[data-should-wayfinding-be-active='true'].highlighted&": {
              borderBottomColor: "black !important",
              color: "black !important",
            },
            "[data-should-wayfinding-be-active].grayed-out&": {
              color: `${theme("colors.gray.40")} !important`,
            },
            "[data-should-wayfinding-be-active='true'].grayed-out&": {
              borderBottomColor: `${theme("colors.gray.40")} !important`,
            },
          },
          "&[aria-expanded='true']": {
            span: {
              borderBottomColor: "black",
              color: "black",
            },
          },
        },
      },
    },
    ".nav-accordion-content-inner": {
      display: "flex",
      flexDirection: "column",
      background: "white",
      gap: `${theme("gap.22")} ${theme("gap.16")}`,
      marginLeft: `-${theme("margin.8")}`,
      marginRight: `-${theme("margin.8")}`,
      paddingTop: "1.5rem",
      paddingBottom: `${1.5 + 1}rem`,
      paddingLeft: theme("padding.8"),
      paddingRight: theme("padding.8"),
      "&.has-featured-column": {
        paddingBottom: "1.5rem",
      },
      [media(theme("screens.xlarge"))]: {
        display: "grid",
        gap: `${theme("gap.0")} ${theme("gap.8")}`,
        marginLeft: 0,
        marginRight: 0,
        padding: 0,
        borderLeftWidth: "2.5rem",
        borderRightWidth: "2.5rem",
        borderLeftColor: theme("colors.white"),
        borderRightColor: theme("colors.white"),
        "&.has-featured-column": {
          paddingBottom: 0,
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
        padding: `${theme("padding.12")} ${theme("padding.8")}`,
        [media(theme("screens.xlarge"))]: {
          marginTop: 0,
          marginBottom: 0,
          padding: `${theme("padding.22")} ${theme("padding.8")}`,
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
