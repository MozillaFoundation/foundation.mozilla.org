import React from "react";
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
        name={id}
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

export default InputCheckboxField;
