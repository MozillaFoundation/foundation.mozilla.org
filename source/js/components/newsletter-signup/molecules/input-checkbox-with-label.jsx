import React from "react";
import PropTypes from "prop-types";
import Label from "../atoms/label.jsx";
import InputCheckbox from "../atoms/input-checkbox.jsx";

const InputCheckboxField = ({ id, label, errorMessage, ...otherProps }) => {
  return (
    <div className="tw-flex tw-items-start tw-relative tw-pl-10">
      <InputCheckbox id={id} {...otherProps} />
      <div>
        <div className="tw-flex">
          <Label
            htmlFor={id}
            classes="tw-block form-check-label tw-body-small tw-text-black dark:tw-text-gray-40"
          >
            {label}
          </Label>
          {errorMessage && <span className="tw-form-error-glyph tw-ml-2" />}
        </div>
        {errorMessage && (
          <p className="error-message tw-body-small tw-mt-0 tw-text-[#c01] dark:tw-text-red-40">
            {errorMessage}
          </p>
        )}
      </div>
    </div>
  );
};

InputCheckboxField.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  value: PropTypes.string.isRequired,
  checked: PropTypes.bool,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
};

export default InputCheckboxField;
