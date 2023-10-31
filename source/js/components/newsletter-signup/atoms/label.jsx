import React from "react";

const Label = ({ htmlFor, children, classes }) => {
  return (
    <label htmlFor={htmlFor} className={classes}>
      {children}
    </label>
  );
};

export default Label;
