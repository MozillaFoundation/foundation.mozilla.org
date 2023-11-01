import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";

const ButtonSubmit = ({ children, widthClasses }) => {
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

ButtonSubmit.defaultProps = {};

export default ButtonSubmit;
