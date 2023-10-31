import React from "react";
import classNames from "classnames";

const ButtonSubmit = ({ children, widthClasses }) => {
  let classes = classNames(`tw-btn tw-btn-primary`, widthClasses);

  return (
    <button type="submit" className={classes}>
      {children}
    </button>
  );
};

export default ButtonSubmit;
