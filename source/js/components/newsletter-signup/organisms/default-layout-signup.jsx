import React, { Component } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import Heading from "../atoms/heading.jsx";
import Description from "../atoms/description.jsx";
import InputText from "../atoms/input-text.jsx";
import Select from "../atoms/select.jsx";
import InputCheckboxWithLabel from "../molecules/input-checkbox-with-label.jsx";
import ButtonSubmit from "../atoms/button-submit.jsx";
import ButtonQuit from "../atoms/button-quit.jsx";
import APIErrorMessage from "../atoms/api-error-message.jsx";
import withSubmissionLogic from "./with-submission-logic.jsx";
import utility from "../../../utility.js";
import { ReactGA } from "../../../common";
import { getCurrentLanguage } from "../../petition/locales";
import { COUNTRY_OPTIONS } from "../data/country-options.js";
import { LANGUAGE_OPTIONS } from "../data/language-options.js";
import { FORM_STYLE } from "./form-specific-style.js";

const FIELD_MARGIN_CLASSES = `tw-mb-4`;
const FIELD_ID_PREFIX = `default-layout-newsletter`;

class DefaultSignupForm extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
    this.ids = this.generateFieldIds([
      "firstName",
      "lastName",
      "email",
      "country",
      "language",
      "privacy",
    ]);
    this.style = FORM_STYLE[props.formStyle];
    this.buttonText = props.buttonText || gettext("Sign up");
  }

  getInitialState() {
    return {
      formData: {
        firstName: "",
        lastName: "",
        email: "",
        country: "",
        language: getCurrentLanguage(),
        privacy: "",
      },
      showCountryField:
        this.props.showCountryFieldByDefault?.toLowerCase() === "true",
      showLanguageField:
        this.props.showLanguageFieldByDefault?.toLowerCase() === "true",
      showQuitButton: this.props.showQuitButton?.toLowerCase() === "true",
      submitButtonDisabled: this.props.disableSubmitButtonByDefault,
    };
  }

  // reset state to initial values
  reset() {
    this.setState(this.getInitialState());
  }

  // generate unique IDs for form fields
  generateFieldIds(fieldNames = []) {
    return fieldNames.reduce((obj, field) => {
      obj[field] = utility.generateUniqueId(`${FIELD_ID_PREFIX}-${field}`);
      return obj;
    }, {});
  }

  updateFormFieldValue(name, value) {
    this.setState((prevState) => ({
      formData: {
        ...prevState.formData,
        [name]: value,
      },
    }));
  }

  getFormFieldValue(name) {
    return this.state.formData[name];
  }

  // Toggle the submit button disabled state if the button is disabled by default
  toggleSubmitButton(setToDisabled) {
    if (this.props.disableSubmitButtonByDefault) {
      this.setState({
        submitButtonDisabled: setToDisabled,
      });
    }
  }

  handleInputFocus() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`,
    });
  }

  handleFirstNameChange(event) {
    this.updateFormFieldValue(event.target.name, event.target.value);
  }

  handleLastNameChange(event) {
    this.updateFormFieldValue(event.target.name, event.target.value);
  }

  handleEmailFocusAndInput() {
    this.handleInputFocus();

    this.setState({ showCountryField: true, showLanguageField: true });
  }

  handleEmailChange(event) {
    this.updateFormFieldValue(event.target.name, event.target.value);
    this.toggleSubmitButton(event.target.value === "");
  }

  handleCountryChange(event) {
    this.updateFormFieldValue(event.target.name, event.target.value);
  }

  handleLanguageChange(event) {
    this.updateFormFieldValue(event.target.name, event.target.value);
  }

  handlePrivacyChange(event) {
    this.updateFormFieldValue(
      event.target.name,
      event.target.checked.toString()
    );
  }

  renderHeader() {
    if (!this.props.ctaHeader) return null;

    return (
      <Heading
        level={this.style.headingLevel}
        classes={this.style.headingClass}
      >
        {this.props.ctaHeader}
      </Heading>
    );
  }

  renderDescription() {
    if (!this.props.ctaDescription) return null;

    return (
      <Description
        content={this.props.ctaDescription}
        classes={this.style.descriptionClass}
      />
    );
  }

  renderAPIErrorMessage() {
    if (!this.props.apiError) return null;

    return <APIErrorMessage apiErrorMessage={this.props.apiError} />;
  }

  renderFirstNameField() {
    const name = "firstName";

    return (
      <InputText
        id={this.ids[name]}
        name={name}
        ariaLabel={gettext("First name")}
        value={this.getFormFieldValue(name)}
        placeholder={gettext("First name")}
        onFocus={() => this.handleInputFocus()}
        onChange={(event) => this.handleFirstNameChange(event)}
        required={false}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
        errorMessage={this.props.errors[name]}
        fieldStyle={this.style.fieldStyle}
      />
    );
  }

  renderLastNameField() {
    const name = "lastName";

    return (
      <InputText
        id={this.ids[name]}
        name={name}
        ariaLabel={gettext("Last name")}
        value={this.getFormFieldValue(name)}
        placeholder={gettext("Last name")}
        onFocus={() => this.handleInputFocus()}
        onChange={(event) => this.handleLastNameChange(event)}
        required={false}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
        errorMessage={this.props.errors[name]}
        fieldStyle={this.style.fieldStyle}
      />
    );
  }

  renderEmailField() {
    const name = "email";

    return (
      <InputText
        id={this.ids[name]}
        type="email"
        name={name}
        ariaLabel={gettext("Email address")}
        value={this.getFormFieldValue(name)}
        placeholder={gettext("Please enter your email")}
        onFocus={() => this.handleEmailFocusAndInput()}
        onInput={() => this.handleEmailFocusAndInput()}
        onChange={(event) => this.handleEmailChange(event)}
        required={true}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
        errorMessage={this.props.errors[name]}
        fieldStyle={this.style.fieldStyle}
      />
    );
  }

  renderCountryField() {
    const name = "country";

    return (
      <Select
        id={this.ids[name]}
        name={name}
        value={this.getFormFieldValue(name)}
        options={COUNTRY_OPTIONS}
        onChange={(event) => this.handleCountryChange(event)}
        required={false}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
        fieldStyle={this.style.fieldStyle}
      />
    );
  }

  renderLanguageField() {
    const name = "language";

    return (
      <Select
        id={this.ids[name]}
        name={name}
        value={this.getFormFieldValue(name)}
        options={LANGUAGE_OPTIONS}
        onChange={(event) => this.handleLanguageChange(event)}
        required={false}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
        fieldStyle={this.style.fieldStyle}
      />
    );
  }

  renderPrivacyCheckbox() {
    const name = "privacy";
    const privacy_text =
      "I'm okay with Mozilla handling my info as explained in this <a href='https://www.mozilla.org/privacy/websites/'>Privacy Notice</a>.";

    const label = (
      <span>
        {pgettext(
          `Pre-link text of: ${privacy_text}`,
          "I'm okay with Mozilla handling my info as explained in this "
        )}
        <a target="_blank" href="https://www.mozilla.org/privacy/websites/">
          {pgettext(`Link text of: ${privacy_text}`, "Privacy Notice")}
        </a>
        {pgettext(`Post-link text of: ${privacy_text}`, ".")}
      </span>
    );

    return (
      <InputCheckboxWithLabel
        id={this.ids[name]}
        name={name}
        label={label}
        value={this.getFormFieldValue(name)}
        checked={this.getFormFieldValue(name) === "true"}
        onChange={(event) => this.handlePrivacyChange(event)}
        required={true}
        errorMessage={this.props.errors[name]}
      />
    );
  }

  renderButtons() {
    let wrapperClasses = classNames({
      "tw-flex-shrink-0 tw-mt-8 medium:tw-mt-0":
        this.style.buttonPosition !== "bottom",
      "tw-mt-24 medium:tw-mt-12 tw-text-right":
        this.style.buttonPosition === "bottom",
    });

    let submitButton = (
      <ButtonSubmit
        buttonStyle={this.style.buttonStyle}
        widthClasses={this.style.buttonWidthClasses}
        disabled={this.state.submitButtonDisabled}
      >
        {this.buttonText}
      </ButtonSubmit>
    );

    let buttons = submitButton;

    if (this.state.showQuitButton) {
      buttons = (
        <div className="tw-flex tw-gap-x-4">
          {submitButton}
          <ButtonQuit
            widthClasses={this.style.buttonWidthClasses}
            handleQuitButtonClick={this.props.handleQuitButtonClick}
          >
            {gettext("No thanks")}
          </ButtonQuit>
        </div>
      );
    }

    return <div className={wrapperClasses}>{buttons}</div>;
  }

  renderForm() {
    if (this.props.hideForm) return null;

    let containerClasses = classNames({
      "d-flex flex-column flex-lg-row medium:tw-gap-8":
        this.style.buttonPosition !== "bottom",
    });

    return (
      <form
        noValidate={this.props.noBrowserValidation}
        onSubmit={(event) => this.props.onSubmit(event, this.state.formData)}
      >
        <div className={containerClasses}>
          <div className="tw-flex-grow">
            <fieldset className={FIELD_MARGIN_CLASSES}>
              {this.props.askName === "True" && this.renderFirstNameField()}
              {this.props.askName === "True" && this.renderLastNameField()}
              {this.renderEmailField()}
              {this.state.showCountryField && this.renderCountryField()}
              {this.state.showLanguageField && this.renderLanguageField()}
            </fieldset>
            <fieldset>{this.renderPrivacyCheckbox()}</fieldset>
          </div>
          {this.renderButtons()}
        </div>
      </form>
    );
  }

  render() {
    return (
      <div
        className={this.style.innerWrapperClass}
        data-submission-status={this.props.apiSubmissionStatus}
      >
        <div className={this.style.introContainerClass}>
          {this.renderAPIErrorMessage()}
          {this.renderHeader()}
          {this.renderDescription()}
        </div>
        <div className={this.style.formContainerClass}>{this.renderForm()}</div>
      </div>
    );
  }
}

DefaultSignupForm.propTypes = {
  ctaHeader: PropTypes.string,
  ctaDescription: PropTypes.oneOfType([PropTypes.string, PropTypes.node])
    .isRequired,
  errors: PropTypes.shape({
    fieldName: PropTypes.string,
    errorMessage: PropTypes.string,
  }),
  onSubmit: PropTypes.func.isRequired,
  noBrowserValidation: PropTypes.bool,
  hideForm: PropTypes.bool,
  showCountryFieldByDefault: PropTypes.string,
  showLanguageFieldByDefault: PropTypes.string,
  showQuitButton: PropTypes.string,
};

/**
 * This renders a signup form which includes the following fields
 *   - email input field, (required)
 *   - country dropdown, (optional, field is hidden until email field is focused)
 *   - language dropdown, (optional, field is hidden until email field is focused)
 *   - privacy agreement checkbox (required)
 */
export default withSubmissionLogic(DefaultSignupForm);
