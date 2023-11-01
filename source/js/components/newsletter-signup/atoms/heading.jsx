import React from "react";
import PropTypes from "prop-types";

const Heading = ({ level = 2, children }) => {
  const TagName = `h${level}`;
  return <TagName>{children}</TagName>;
};

Heading.propTypes = {
  level: PropTypes.number,
  children: PropTypes.node.isRequired,
};

Heading.defaultProps = {};

export default Heading;
