import React from "react";
import PropTypes from "prop-types";

const Label = ({ htmlFor, children, classes }) => {
  return (
    <label htmlFor={htmlFor} className={classes}>
      {children}
    </label>
  );
};

Label.propTypes = {
  htmlFor: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  classes: PropTypes.string,
};

export default Label;
