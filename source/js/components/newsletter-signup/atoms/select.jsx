import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";

const BASE_CLASSES = `
  tw-form-control
  tw-w-full
  tw-border-1
  tw-border-black
  focus:tw-border-blue-40
  focus:tw-shadow-none
`;

const Select = ({
  id,
  name,
  value,
  options,
  onChange,
  required,
  outerMarginClasses,
}) => {
  let classes = classNames(BASE_CLASSES, outerMarginClasses);

  return (
    <select
      id={id}
      // FIXME: is "name" attribute not needed?
      name={name}
      value={value}
      onBlur={onChange}
      onChange={onChange}
      required={required}
      className={classes}
    >
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
  name: PropTypes.string,
  value: PropTypes.string,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
    })
  ).isRequired,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
  outerMarginClasses: PropTypes.string,
};

Select.defaultProps = {};

export default Select;
