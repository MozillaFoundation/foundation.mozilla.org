import React from "react";
import PropTypes from "prop-types";

const Description = ({ content, classes }) => {
  if (typeof content === "string") {
    return (
      <div
        dangerouslySetInnerHTML={{
          __html: content,
        }}
        className={classes}
      />
    );
  }

  return <div className={classes}>{content}</div>;
};

Description.propTypes = {
  content: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  classes: PropTypes.string,
};

export default Description;
