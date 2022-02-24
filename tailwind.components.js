const plugin = require("tailwindcss/plugin");

const formControlStylings = {
  appearance: "none",
  backgroundImage: 'url("../_images/glyphs/down-chevron.svg")',
  backgroundRepeat: "no-repeat",
  backgroundPosition: "right 12px top 50%",
  backgroundSize: "24px 24px",
  borderRadius: "0",
  border: "1px solid #cccccc",
  padding: "5px 48px 5px 12px",
  color: "#000000",
  display: "block",
  width: "100%",
  height: "calc(1.5em + .75rem + 2px)",
  fontSize: "1rem",
  fontWeight: "400",
  lineHeight: "1.25",
  backgroundColor: "#ffffff",
  backgroundClip: "padding-box",
  transition:
    "border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out",
  "&:focus": {
    color: "#495057",
    backgroundColor: "#fff",
    borderColor: "#80bdff",
    outline: "0",
    boxShadow: "0 0 0 0.2rem rgba(0, 123, 255, 0.25)",
  },
};
module.exports = [
  plugin(function ({ addComponents }) {
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
      // Add bootstrap form control to tailwind
      {
        "select.form-control": {
          ...formControlStylings,
          "&-lg": {
            ...formControlStylings,
            height: "auto",
            padding: "12px 48px 12px 12px",
            fontSize: "1.25rem",
            lineHeight: "1.25",
          },
        },
      },
    ]);
  }),
];
