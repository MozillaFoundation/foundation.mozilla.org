import React from "react";
import PropTypes from "prop-types";

const InputCheckbox = (props) => {
  // [TODO]
  // Ideally styling for this "atom" component should be pre-defined in a Tailwind config file.
  // Because our design system still needs to be finalized,
  // we are using hardcoded Tailwind classes directly here for now.
  return <input type="checkbox" className="form-check-input" {...props} />;
};

InputCheckbox.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  checked: PropTypes.bool,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
};

export default InputCheckbox;
