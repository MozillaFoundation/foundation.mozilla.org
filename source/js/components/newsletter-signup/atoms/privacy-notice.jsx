import React from "react";
import { getText } from "../../petition/locales";
import PropTypes from "prop-types";

const PrivacyNotice = ({ content, classes }) => {
  if (!content) {
    content = getText(
      `I'm okay with Mozilla handling my info as explained in this Privacy Notice`
    );
  }
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
