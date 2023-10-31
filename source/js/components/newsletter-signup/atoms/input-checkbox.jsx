import React from "react";

const InputCheckbox = ({ id, name, checked, onChange, required }) => {
  return (
    <input
      type="checkbox"
      id={id}
      name={name}
      checked={checked}
      onChange={onChange}
      required={required}
      className="form-check-input"
    />
  );
};

export default InputCheckbox;
