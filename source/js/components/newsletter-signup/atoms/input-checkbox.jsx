import React from "react";
import PropTypes from "prop-types";

const InputCheckbox = (props) => {
  return <input type="checkbox" className="form-check-input" {...props} />;
};

InputCheckbox.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string,
  checked: PropTypes.bool,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
};

InputCheckbox.defaultProps = {};

export default InputCheckbox;
