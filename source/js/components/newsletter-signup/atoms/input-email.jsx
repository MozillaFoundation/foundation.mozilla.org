import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

// [TODO] probably worth moving this into Tailwind config?
const BASE_CLASSES = `
  tw-form-control
  has-error:tw-border
  has-error:tw-border-solid
  has-error:tw-border-[#c01]
  dark:has-error:tw-border-2
  dark:has-error:tw-border-red-40
  tw-border-1
  tw-border-black
  placeholder:tw-text-gray-40
  focus:tw-border-blue-40
  focus:tw-shadow-none
  focus-visible:tw-drop-shadow-none
`;

const InputEmail = ({ ariaLabel, outerMarginClasses, ...otherProps }) => {
  // [TODO]
  // Ideally styling for this "atom" component should be pre-defined in a Tailwind config file.
  // Because our design system still needs to be finalized,
  // we are using hardcoded Tailwind classes directly here for now.
  let classes = classNames(BASE_CLASSES, outerMarginClasses);

  return (
    <input
      type="email"
      className={classes}
      {...otherProps}
      {...(ariaLabel ? { "aria-label": ariaLabel } : {})}
    />
  );
};

InputEmail.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string,
  value: PropTypes.string,
  placeholder: PropTypes.string,
  onFocus: PropTypes.func.isRequired,
  onInput: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
  ariaLabel: PropTypes.string,
};

export default InputEmail;
