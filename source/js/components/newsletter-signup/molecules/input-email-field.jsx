import React from "react";
import PropTypes from "prop-types";
import Label from "../atoms/label.jsx";
import InputEmail from "../atoms/input-email.jsx";

const InputEmailField = ({
  id,
  label,
  name,
  value,
  placeholder,
  onFocus,
  onInput,
  onChange,
  required,
}) => {
  return (
    <div>
      <Label htmlFor={id}>{label}</Label>
      <InputEmail
        id={id}
        name={name}
        value={value}
        placeholder={placeholder}
        onFocus={onFocus}
        onInput={onInput}
        onChange={onChange}
        required={required}
      />
    </div>
  );
};

InputEmailField.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  name: PropTypes.string,
  value: PropTypes.string,
  placeholder: PropTypes.string,
  onFocus: PropTypes.func.isRequired,
  onInput: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
};

InputEmailField.defaultProps = {};

export default InputEmailField;
