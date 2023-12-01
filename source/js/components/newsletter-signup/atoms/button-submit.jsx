import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";

const ButtonSubmit = ({ children, widthClasses }) => {
  // [TODO]
  // Ideally styling for this "atom" component should be pre-defined in a Tailwind config file.
  // Because our design system still needs to be finalized,
  // we are using hardcoded Tailwind classes directly here for now.
  let classes = classNames(`tw-btn tw-btn-primary`, widthClasses);

  return (
    <button type="submit" className={classes}>
      {children}
    </button>
  );
};

ButtonSubmit.propTypes = {
  children: PropTypes.node.isRequired,
  widthClasses: PropTypes.string,
};

export default ButtonSubmit;
