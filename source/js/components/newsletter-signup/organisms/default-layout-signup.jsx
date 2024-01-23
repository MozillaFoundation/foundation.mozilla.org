import React, { Component } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import Heading from "../atoms/heading.jsx";
import Description from "../atoms/description.jsx";
import InputEmail from "../atoms/input-email.jsx";
import Select from "../atoms/select.jsx";
import InputCheckboxWithLabel from "../molecules/input-checkbox-with-label.jsx";
import ButtonSubmit from "../atoms/button-submit.jsx";
import withSubmissionLogic from "./with-submission-logic.jsx";
import utility from "../../../utility.js";
import { ReactGA } from "../../../common";
import { getText, getCurrentLanguage } from "../../petition/locales";
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
      "email",
      "country",
      "language",
      "privacy",
    ]);
    this.style = FORM_STYLE[props.formStyle];
    this.buttonText = props.buttonText || getText("Sign up");
  }

  getInitialState() {
    return {
      formData: {
        email: "",
        country: "",
        language: getCurrentLanguage(),
        privacy: "",
      },
      showAllFields: false,
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

  showAllFields() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`,
    });

    this.setState({ showAllFields: true });
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

  handleEmailChange(event) {
    this.updateFormFieldValue("email", event.target.value);
    this.toggleSubmitButton(event.target.value === "");
  }

  handleCountryChange(event) {
    this.updateFormFieldValue("country", event.target.value);
  }

  handleLanguageChange(event) {
    this.updateFormFieldValue("language", event.target.value);
  }

  handlePrivacyChange(event) {
    this.updateFormFieldValue("privacy", event.target.checked.toString());
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

  renderEmailField() {
    const name = "email";

    return (
      <InputEmail
        id={this.ids.email}
        name={name}
        label={getText(`Email address`)}
        value={this.getFormFieldValue(name)}
        placeholder={getText(`Please enter your email`)}
        onFocus={() => this.showAllFields()}
        onInput={() => this.showAllFields()}
        onChange={(event) => this.handleEmailChange(event)}
        required={true}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
        errorMessage={this.props.errors[name]}
        fieldStyle={this.style.fieldStyle}
      />
    );
  }

  renderAdditionalFields() {
    const nameCountry = "country";
    const nameLanguage = "language";

    return (
      <>
        <Select
          id={this.ids.country}
          name={nameCountry}
          value={this.getFormFieldValue(nameCountry)}
          options={COUNTRY_OPTIONS}
          onChange={(event) => this.handleCountryChange(event)}
          required={false}
          outerMarginClasses={FIELD_MARGIN_CLASSES}
          fieldStyle={this.style.fieldStyle}
        />
        <Select
          id={this.ids.language}
          name={nameLanguage}
          value={this.getFormFieldValue(nameLanguage)}
          options={LANGUAGE_OPTIONS}
          onChange={(event) => this.handleLanguageChange(event)}
          required={false}
          outerMarginClasses={FIELD_MARGIN_CLASSES}
          fieldStyle={this.style.fieldStyle}
        />
      </>
    );
  }

  renderPrivacyCheckbox() {
    const name = "privacy";

    return (
      <InputCheckboxWithLabel
        id={this.ids.privacy}
        name={name}
        label={getText(
          `I'm okay with Mozilla handling my info as explained in this Privacy Notice`
        )}
        value={this.getFormFieldValue(name)}
        checked={this.getFormFieldValue(name) === "true"}
        onChange={(event) => this.handlePrivacyChange(event)}
        required={true}
        errorMessage={this.props.errors[name]}
      />
    );
  }

  renderForm() {
    if (this.props.hideForm) return null;

    let containerClasses = classNames({
      "d-flex flex-column flex-lg-row medium:tw-gap-8":
        this.style.buttonPosition !== "bottom",
    });

    let buttonWrapperClasses = classNames({
      "tw-flex-shrink-0 tw-mt-8 medium:tw-mt-0":
        this.style.buttonPosition !== "bottom",
      "tw-mt-24 medium:tw-mt-12 tw-text-right":
        this.style.buttonPosition === "bottom",
    });

    return (
      <form
        noValidate={this.props.noBrowserValidation}
        onSubmit={(event) => this.props.onSubmit(event, this.state.formData)}
      >
        <div className={containerClasses}>
          <div className="tw-flex-grow">
            <fieldset className={FIELD_MARGIN_CLASSES}>
              {this.renderEmailField()}
              {this.state.showAllFields && this.renderAdditionalFields()}
            </fieldset>
            <fieldset>{this.renderPrivacyCheckbox()}</fieldset>
          </div>
          <div className={buttonWrapperClasses}>
            <ButtonSubmit
              buttonStyle={this.style.buttonStyle}
              widthClasses={this.style.buttonWidthClasses}
              disabled={this.state.submitButtonDisabled}
            >
              {this.buttonText}
            </ButtonSubmit>
          </div>
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
};

/**
 * This renders a signup form which includes the following fields
 *   - email input field, (required)
 *   - country dropdown, (optional, field is hidden until email field is focused)
 *   - language dropdown, (optional, field is hidden until email field is focused)
 *   - privacy agreement checkbox (required)
 */
export default withSubmissionLogic(DefaultSignupForm);
