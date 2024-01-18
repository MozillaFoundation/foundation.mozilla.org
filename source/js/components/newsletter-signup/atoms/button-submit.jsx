import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";

const ButtonSubmit = ({
  disabled = false,
  children,
  buttonStyle = "primary",
  widthClasses = `tw-w-full`,
}) => {
  // [TODO]
  // Ideally styling for this "atom" component should be pre-defined in a Tailwind config file.
  // Because our design system still needs to be finalized,
  // we are using hardcoded Tailwind classes directly here for now.
  let classes = classNames(`tw-btn tw-btn-${buttonStyle}`, widthClasses);

  return (
    <button type="submit" className={classes} disabled={disabled}>
      {children}
    </button>
  );
};

ButtonSubmit.propTypes = {
  children: PropTypes.node.isRequired,
  buttonStyle: PropTypes.oneOf(["primary", "secondary"]),
  widthClasses: PropTypes.string,
};

export default ButtonSubmit;
