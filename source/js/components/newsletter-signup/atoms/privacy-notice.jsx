import React from "react";
import PropTypes from "prop-types";

const PrivacyNotice = ({ content, classes }) => {
  if (typeof content === "string") {
    return (
      <span
        dangerouslySetInnerHTML={{
          __html: content,
        }}
        className={classes}
      />
    );
  }

  return <span className={classes}>{content}</span>;
};

PrivacyNotice.propTypes = {
  content: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  classes: PropTypes.string,
};

export default PrivacyNotice;
