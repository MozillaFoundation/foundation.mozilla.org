import React from "react";
import PropTypes from "prop-types";
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

SelectField.propTypes = {
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
};

SelectField.defaultProps = {};

export default SelectField;
