import React from "react";
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

export default InputEmailField;
