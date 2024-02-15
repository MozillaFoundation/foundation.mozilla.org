const plugin = require("tailwindcss/plugin");

module.exports = [
  plugin(function ({ addComponents, theme }) {
    const newComponents = {
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

    addComponents(newComponents);
  }),
];
