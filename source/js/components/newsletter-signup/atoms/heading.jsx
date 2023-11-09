import React from "react";
import PropTypes from "prop-types";

const Heading = ({ level = 2, children }) => {
  const TagName = `h${level}`;
  return <TagName className="tw-h1-heading">{children}</TagName>;
};

Heading.propTypes = {
  level: PropTypes.number,
  children: PropTypes.node.isRequired,
};

export default Heading;
