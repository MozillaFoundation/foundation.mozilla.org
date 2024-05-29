import React from "react";
import PropTypes from "prop-types";

const PrivacyNotice = ({ content, classes }) => {
  //[TODO] Investigate removing the legacy richtext template which renders an empty rich-text div wrapper
  // Jira TP1-601 / Github Issue #12285 https://github.com/MozillaFoundation/foundation.mozilla.org/issues/12285
  if (
    !this.props.ctaPrivacyNotice ||
    this.props.ctaPrivacyNotice == "<div class='rich-text'></div>"
  )
    return null;

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
