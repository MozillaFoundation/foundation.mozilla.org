const plugin = require("tailwindcss/plugin");

// Add Bootstrap .form-control stylings to Tailwind
// Stylings converted based on https://github.com/twbs/bootstrap/blob/v4.6.0/scss/_forms.scss

const SELECT = {
  backgroundSize: "24px",
  paddingX: "12px",
  paddingRight: "48px", // paddingX * 2 + backgroundSize
};

/**
 * Stylings for .form-control (converted from Bootstrap 4.6 with our custom SCSS)
 * @param {*} theme Tailwind theme config
 * @returns {object} Stylings
 */
function formControl(theme) {
  return {
    display: "block",
    width: "100%",
    height: "calc( 2.5rem + 2px)", // 42px if 1rem = 16px
    padding: "0 0.75rem", // 12px if 1rem = 16px
    fontFamily: theme("fontFamily.sans"),
    fontSize: "1.125rem", // 18px if 1rem = 16px
    fontWeight: theme("fontWeight.normal"),
    lineHeight: "1.5",
    color: theme("colors.black"),
    backgroundColor: theme("colors.white"),
    backgroundClip: "padding-box",
    border: `1px solid ${theme("colors.gray.20")}`,
    borderRadius: 0,
    transition:
      "border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out",
    // Unstyle the caret on `<select>`s in IE10+.
    "&::-ms-expand": {
      backgroundColor: "transparent",
      border: 0,
    },
    // Remove select outline from select box in FF
    "&:-moz-focusring": {
      color: "transparent",
      textShadow: "0 0 0 $input-color",
    },
    // Customize the `:focus` state to imitate native WebKit styles.
    "&:focus": {
      color: "#495057",
      backgroundColor: theme("colors.white"),
      borderColor: "#80bdff",
      outline: "0",
      boxShadow: "0 0 0 0.2rem rgba(0, 123, 255, 0.25)",
    },
    "&::placeholder": {
      color: theme("colors.gray.40"),
      // Override Firefox's unusual default opacity; see https://github.com/twbs/bootstrap/pull/11526.
      opacity: 1,
    },
    // Disabled and read-only inputs
    //
    // HTML5 says that controls under a fieldset > legend:first-child won't be
    // disabled if the fieldset is disabled. Due to implementation difficulty, we
    // don't honor that edge case; we style them as disabled anyway.
    "&:disabled, &[readonly]": {
      backgroundColor: "#e9ecef",
      // iOS fix for unreadable disabled content; see https://github.com/twbs/bootstrap/issues/11655.
      opacity: 1,
    },
    "textarea&": {
      height: "auto",
    },
  };
}

/**
 * Stylings for select.form-control (converted from Bootstrap 4.6 with our custom SCSS)
 * @param {*} theme Tailwind theme config
 * @returns {object} Stylings
 */
function selectFormControl(theme) {
  return {
    appearance: "none",
    backgroundRepeat: "no-repeat",
    backgroundPosition: `right ${SELECT.paddingX} top 50%`,
    backgroundImage: 'url("../_images/glyphs/down-chevron.svg")',
    backgroundSize: `${SELECT.backgroundSize} ${SELECT.backgroundSize}`,
    border: `1px solid ${theme("colors.gray.20")}`,
    borderRadius: "0",
    color: theme("colors.black"),
    padding: `5px ${SELECT.paddingRight} 5px ${SELECT.paddingX}`,
    ".dark &": {
      backgroundImage: "url(../_images/glyphs/down-chevron-dark-theme.svg)",
      backgroundColor: "transparent",
      border: `1px solid ${theme("colors.white")}`,
      color: theme("colors.white"),
      option: {
        color: theme("colors.black"),
      },
      "&:focus": {
        color: theme("colors.white"),
        backgroundColor: "transparent",
        borderColor: theme("colors.white"),
      },
    },
    "&:focus::-ms-value": {
      // Suppress the nested default white text on blue background highlight given to
      // the selected option text when the (still closed) <select> receives focus
      // in IE and (under certain conditions) Edge, as it looks bad and cannot be made to
      // match the appearance of the native widget.
      // See https://github.com/twbs/bootstrap/issues/19398.
      color: "#495057",
      backgroundColor: theme("colors.white"),
    },
  };
}

/**
 * Stylings for select.form-control-lg (converted from Bootstrap 4.6 with our custom SCSS)
 * @param {*} theme Tailwind theme config
 * @returns {object} Stylings
 */
function selectFormLgControl(theme) {
  return {
    ...selectFormControl(theme),
    height: "auto",
    padding: `${SELECT.paddingX} ${SELECT.paddingRight} ${SELECT.paddingX} ${SELECT.paddingX}`,
    fontSize: "1.25rem",
    lineHeight: "1.25",
  };
}

module.exports = [
  plugin(function ({ addComponents, theme }) {
    addComponents([
      {
        ".form-control": {
          ...formControl(theme),
        },
        "select.form-control": {
          ...selectFormControl(theme),
        },
        "select.form-control-lg": {
          ...selectFormLgControl(theme),
        },
        "input[type='date'].form-control, input[type='time'].form-control, input[type='datetime-local'].form-control, input[type='month'].form-control":
          {
            appearance: "none",
          },
      },
    ]);
  }),
];
