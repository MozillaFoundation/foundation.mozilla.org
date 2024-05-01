import React from "react";
import PropTypes from "prop-types";

const PrivacyNotice = ({ content }) => {
  if (typeof content === "string") {
    return (
      <span
        dangerouslySetInnerHTML={{
          __html: content,
        }}
        className="[&_p]:tw-body-small"
      />
    );
  }

  return <span className="[&_p]:tw-body-small">{content}</span>;
};

PrivacyNotice.propTypes = {
  content: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
};

export default PrivacyNotice;
