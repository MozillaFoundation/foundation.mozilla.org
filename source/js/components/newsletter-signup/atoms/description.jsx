import React from "react";
import PropTypes from "prop-types";

const Description = ({ content }) => {
  if (typeof content === "string") {
    return (
      <div
        dangerouslySetInnerHTML={{
          __html: content,
        }}
      />
    );
  }

  return <div>{content}</div>;
};

Description.propTypes = {
  content: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
};

export default Description;
