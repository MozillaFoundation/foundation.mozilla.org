import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

// FIXME: probably worth moving this into Tailwind config?
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

let InputEmail = ({
  id,
  name,
  value,
  placeholder,
  onFocus,
  onInput,
  onChange,
  required,
  label,
  outerMarginClasses,
}) => {
  let classes = classNames(BASE_CLASSES, outerMarginClasses);

  // FIXME: should i just do ...props here?
  return (
    <input
      type="email"
      id={id}
      name={name}
      value={value}
      placeholder={placeholder}
      onFocus={onFocus}
      onInput={onInput}
      onChange={onChange}
      required={required}
      className={classes}
      aria-label={label}
    />
  );
};

InputEmail.propTypes = {
  id: PropTypes.string,
};

InputEmail.defaultProps = {};

export default InputEmail;
