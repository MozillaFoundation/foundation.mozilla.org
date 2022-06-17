const plugin = require("tailwindcss/plugin");

// TODO refactor with theme references after removing SASS/Bootstrap
// https://tailwindcss.com/docs/theme#referencing-other-values

const btnDefault = {
  fontFamily: "Nunito Sans",
  display: "inline-block",
  fontWeight: "700",
  lineHeight: "1.22",
  textAlign: "center",
  whiteSpace: "normal",
  verticalAlign: "middle",
  userSelect: "none",
  border: "1px solid transparent",
  padding: "0.5rem 1rem",
  fontSize: "18px",
  borderRadius: "0",
  transition:
    "color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out",
  color: "#000000",
  backgroundColor: "transparent",
  "&:focus, &:hover": {
    textDecoration: "none",
    color: "#000000",
  },
  "&:hover": {
    cursor: "pointer",
  },
  "&:focus, &.focus": {
    outline: "0",
    boxShadow: "0 0 0 0.2rem rgb(0 123 255 / 25%)",
  },
  "&.disabled, &:disabled, &[disabled]": {
    opacity: "0.3",
    cursor: "not-allowed",
    pointerEvents: "none",
  },
  "&:active, &.active": {
    backgroundImage: "none",
  },
  "&:not(:disabled):not(.disabled)": {
    cursor: "pointer",
  },
};

module.exports = [
  plugin(function ({ addComponents }) {
    addComponents([
      {
        ".btn": { ...btnDefault },
        ".btn-primary": {
          ...btnDefault,
          border: "2px solid #595cf3",
          color: "#ffffff",
          backgroundColor: "#595cf3",
          borderColor: "transparent",
          "&:focus, &:hover": {
            color: "#ffffff",
            backgroundColor: "#0d10bf",
            borderColor: "transparent",
            textDecoration: "none",
          },
          "&:not(:disabled):not(.disabled):active, &:not(:disabled):not(.disabled).active":
            {
              color: "#ffffff",
              backgroundColor: "#b7b9fa",
              borderColor: "transparent",
            },
          "&:focus, &.focus": {
            outline: "0",
            boxShadow: "0 0 0 0.2rem rgb(38 143 255 / 50%)",
          },
          ".dark &": {
            "&:focus, &:hover": {
              color: "#000000",
              backgroundColor: "#b7b9fa",
              borderColor: "transparent",
            },
            "&:not(:disabled):not(.disabled):active, &:not(:disabled):not(.disabled).active":
              {
                color: "#000000",
                backgroundColor: "#0d10bf",
              },
          },
        },
        ".btn-secondary": {
          ...btnDefault,
          border: "2px solid #000000",
          color: "#000000",
          backgroundColor: "transparent",
          "&:focus, &:hover": {
            color: "#ffffff",
            backgroundColor: "#000000",
            borderColor: "transparent",
            textDecoration: "none",
          },
          "&:not(:disabled):not(.disabled):active, &:not(:disabled):not(.disabled).active":
            {
              color: "#ffffff",
              backgroundColor: "#595cf3",
              borderColor: "transparent",
            },
          "&:focus, &.focus": {
            boxShadow: "0 0 0 0.2rem rgb(130 138 145 / 50%)",
          },
          '&[href*="//"]:not([href*="foundation.mozilla.org"]):not([href*="donate.mozilla.org"])':
            {
              display: "inline-flex",
              alignItems: "center",
              "&::after": {
                filter: "brightness(0)",
                content: '" "',
                display: "block",
                width: "16px",
                height: "14px",
                background: "url(../_images/glyphs/external.svg) no-repeat",
                marginLeft: "8px",
                position: "relative",
                bottom: "1px",
                transition: "filter 0.2s ease-in-out",
              },
              "&:focus, &:hover": {
                "&::after": { filter: "brightness(1)" },
              },
            },
          ".dark &": {
            color: "#ffffff",
            backgroundColor: "transparent",
            borderColor: "#ffffff",
            fontWeight: "700",
            "&:focus, &:hover": {
              color: "#000000",
              backgroundColor: "#ffffff",
              borderColor: "transparent",
              textDecoration: "none",
            },
            "&:not(:disabled):not(.disabled):active, &:not(:disabled):not(.disabled).active":
              {
                color: "#000000",
                backgroundColor: "#595cf3",
                borderColor: "transparent",
              },
            '&[href*="//"]:not([href*="foundation.mozilla.org"]):not([href*="donate.mozilla.org"])':
              {
                "&::after": {
                  filter: "brightness(1)",
                },
                "&:focus, &:hover": {
                  "&::after": { filter: "brightness(0)" },
                },
              },
          },
        },
        ".btn-pop": {
          ...btnDefault,
          color: "#000000",
          backgroundColor: "transparent",
          border: "2px solid #000000",
          boxShadow: "4px 4px #000000",
          position: "relative",
          top: "-2px",
          transition: "all 0.08s ease",
          "&:not(:disabled):not(.disabled):active, &:not(:disabled):not(.disabled).active":
            {
              color: "#ffffff",
              backgroundColor: "#000000",
              borderColor: "transparent",
              transform: "translate(4px, 4px)",
              boxShadow: "none",
            },
          "&:focus, &:hover": {
            transform: "translate(4px, 4px)",
            boxShadow: "none",
            color: "#000000",
            backgroundColor: "transparent",
            borderColor: "#000000",
          },
          ".dark &": {
            color: "#ffffff",
            backgroundColor: "transparent",
            borderColor: "#ffffff",
            boxShadow: "4px 4px #ffffff",
            fontWeight: "700",
            "&:not(:disabled):not(.disabled):active, &:not(:disabled):not(.disabled).active":
              {
                color: "#000",
                backgroundColor: "#fff",
                borderColor: "transparent",
                transform: "translate(4px, 4px)",
                boxShadow: "none",
              },
            "&:focus, &:hover": {
              transform: "translate(4px, 4px)",
              boxShadow: "none",
              color: "#fff",
              backgroundColor: "transparent",
              borderColor: "#fff",
              textDecoration: "none",
            },
          },
        },
      },
    ]);
  }),
];
