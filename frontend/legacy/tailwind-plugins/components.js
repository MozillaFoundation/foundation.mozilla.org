const plugin = require("tailwindcss/plugin");

// TODO refactor with theme references after removing SASS/Bootstrap
// https://tailwindcss.com/docs/theme#referencing-other-values

module.exports = [
  plugin(function ({ addComponents, theme }) {
    // Using Same breakpoints for containers as bootstrap
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
      // Adding rows to Tailwind CSS
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
];
