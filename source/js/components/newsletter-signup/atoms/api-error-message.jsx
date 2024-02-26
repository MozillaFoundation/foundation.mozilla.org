import React from "react";

const APIErrorMessage = ({ apiErrorMessage }) => {
  return (
        <div className="tw-flex tw-bg-red-100 tw-px-8 tw-pt-8 tw-mb-5" role="alert">
            <p>{ apiErrorMessage }</p>
        </div>
    );
};

export default APIErrorMessage;
