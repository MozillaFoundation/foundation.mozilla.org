import React from "react";
import PropTypes from "prop-types";
import Label from "../atoms/label.jsx";
import InputCheckbox from "../atoms/input-checkbox.jsx";

const InputCheckboxField = ({
  id,
  label,
  checked,
  onChange,
  required,
  outerMarginClasses,
}) => {
  return (
    <div
      className={`tw-flex tw-items-start tw-relative tw-pl-10 ${outerMarginClasses}`}
    >
      <InputCheckbox
        id={id}
        checked={checked}
        onChange={onChange}
        required={required}
      />
      <Label
        htmlFor={id}
        classes="form-check-label tw-body-small tw-text-black"
      >
        {label}
      </Label>
    </div>
  );
};

InputCheckboxField.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  checked: PropTypes.bool,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
  outerMarginClasses: PropTypes.string,
};

InputCheckboxField.defaultProps = {};

export default InputCheckboxField;
