import React from "react";

const Heading = ({ level = 2, children }) => {
  const TagName = `h${level}`;
  return <TagName>{children}</TagName>;
};

export default Heading;
