import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";

const ButtonQuit = ({
  children,
  buttonStyle = "primary",
  widthClasses = `tw-w-full`,
  handleQuitButtonClick,
}) => {
  // [TODO]
  // Ideally styling for this "atom" component should be pre-defined in a Tailwind config file.
  // Because our design system still needs to be finalized,
  // we are using hardcoded Tailwind classes directly here for now.
  let classes = classNames(
    `tw-btn tw-btn-${buttonStyle} btn-dismiss`,
    widthClasses
  );

  return (
    <button type="button" className={classes} onClick={handleQuitButtonClick}>
      {children}
    </button>
  );
};

ButtonQuit.propTypes = {
  children: PropTypes.node.isRequired,
  buttonStyle: PropTypes.oneOf(["primary", "secondary"]),
  widthClasses: PropTypes.string,
  handleQuitButtonClick: PropTypes.func.isRequired,
};

export default ButtonQuit;
