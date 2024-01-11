import React from "react";
import PropTypes from "prop-types";

const Heading = ({ level = 3, classes = "", children }) => {
  const TagName = `h${level}`;
  return <TagName className={classes}>{children}</TagName>;
};

Heading.propTypes = {
  level: PropTypes.number,
  classes: PropTypes.string,
  children: PropTypes.node.isRequired,
};

export default Heading;
