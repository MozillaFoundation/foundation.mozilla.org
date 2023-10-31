import React from "react";
import Label from "../atoms/label.jsx";
import Select from "../atoms/select";

const SelectField = ({ id, name, value, options, onChange, required }) => {
  return (
    <div>
      <Label htmlFor={id}>{label}</Label>
      <Select
        id={id}
        name={name}
        value={value}
        options={options}
        onChange={onChange}
        required={required}
      />
    </div>
  );
};

export default SelectField;
