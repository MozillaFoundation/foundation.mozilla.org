import React from "react";
import classNames from "classnames";

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
  console.log(classes);

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

export default Select;
