import React from "react";
import { getText } from "../../petition/locales";
import PropTypes from "prop-types";

const PrivacyNotice = ({ content, classes }) => {
  //[TODO] Investigate removing the legacy richtext template which renders an empty rich-text div wrapper
  // Jira TP1-601 / Github Issue #12285 https://github.com/MozillaFoundation/foundation.mozilla.org/issues/12285
  if (!content || content == "<div class='rich-text'></div>") {
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
