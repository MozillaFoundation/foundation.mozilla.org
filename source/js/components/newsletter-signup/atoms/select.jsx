import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";

const BASE_CLASSES = `
  tw-form-control
  tw-w-full
  tw-border-1
  dark:tw-border-white
  focus:tw-border-blue-40
  focus:tw-shadow-none
`;

const Select = ({ options, outerMarginClasses, fieldStyle, ...otherProps }) => {
  let classes = classNames(BASE_CLASSES, outerMarginClasses, {
    "tw-border-black": fieldStyle === "outlined",
  });

  return (
    <select {...otherProps} className={classes}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

Select.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
    })
  ).isRequired,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
  outerMarginClasses: PropTypes.string,
  fieldStyle: PropTypes.oneOf(["outlined", "filled"]),
};

export default Select;
