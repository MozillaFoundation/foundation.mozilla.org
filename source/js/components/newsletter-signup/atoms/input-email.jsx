import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

// [TODO] probably worth moving this into Tailwind config?
// [TODO]
// Ideally styling for this "atom" component should be pre-defined in a Tailwind config file.
// Because our design system still needs to be finalized,
// we are using hardcoded Tailwind classes directly here for now.
const FIELD_CLASSES = `
  tw-form-control
  has-error:tw-border
  has-error:tw-border-solid
  has-error:tw-border-[#c01]
  dark:has-error:tw-border-2
  dark:has-error:tw-border-red-40
  tw-border-1
  dark:tw-border-white
  focus:tw-border-blue-40
  focus:tw-shadow-none
  focus-visible:tw-drop-shadow-none
  tw-pr-18
`;

const InputEmail = ({
  ariaLabel,
  outerMarginClasses = "",
  errorMessage,
  fieldStyle,
  ...otherProps
}) => {
  let inputField = (
    <input
      type="email"
      className={classNames(FIELD_CLASSES, {
        "tw-border-black": fieldStyle === "outlined",
      })}
      {...otherProps}
      {...(ariaLabel ? { "aria-label": ariaLabel } : {})}
    />
  );
  let errorNotice = null;

  if (errorMessage) {
    inputField = (
      <div className="tw-relative">
        {inputField}
        <div className="tw-absolute tw-top-0 tw-bottom-0 tw-right-0 tw-flex tw-items-center tw-justify-end">
          <span className="tw-form-error-glyph" />
        </div>
      </div>
    );

    errorNotice = (
      <>
        <p className="error-message tw-body-small tw-mt-4 tw-text-[#c01] dark:tw-text-red-40">
          {errorMessage}
        </p>
      </>
    );
  }

  return (
    <div
      className={classNames(outerMarginClasses, {
        "tw-has-error": errorMessage,
      })}
    >
      {inputField}
      {errorNotice}
    </div>
  );
};

InputEmail.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  placeholder: PropTypes.string,
  onFocus: PropTypes.func.isRequired,
  onInput: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  required: PropTypes.bool,
  ariaLabel: PropTypes.string,
  errorMessage: PropTypes.string,
  fieldStyle: PropTypes.oneOf(["outlined", "filled"]),
};

export default InputEmail;
