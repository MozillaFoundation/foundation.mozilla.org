import React from "react";
import PropTypes from "prop-types";

const Description = ({ children }) => {
  return <p>{children}</p>;
};

Description.propTypes = {
  children: PropTypes.node.isRequired,
};

export default Description;
