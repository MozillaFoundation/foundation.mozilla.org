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
    this.style = FORM_STYLE[props.formPosition];
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
    };
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

  handleEmailChange(event) {
    this.updateFormFieldValue("email", event.target.value);
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

    return <Description content={this.props.ctaDescription} />;
  }

  renderEmailField() {
    const name = "email";
    const outerMarginClasses = classNames({
      [FIELD_MARGIN_CLASSES]: true,
      "tw-has-error": !!this.props.errors[name],
    });

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
        outerMarginClasses={outerMarginClasses}
        errorMessage={this.props.errors[name]}
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
        />
        <Select
          id={this.ids.language}
          name={nameLanguage}
          value={this.getFormFieldValue(nameLanguage)}
          options={LANGUAGE_OPTIONS}
          onChange={(event) => this.handleLanguageChange(event)}
          required={false}
          outerMarginClasses={FIELD_MARGIN_CLASSES}
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

    return (
      <form
        noValidate={this.props.noBrowserValidation}
        onSubmit={(event) => this.props.onSubmit(event, this.state.formData)}
      >
        <div className="d-flex flex-column flex-lg-row medium:tw-gap-8">
          <div className="tw-flex-grow">
            <fieldset className={FIELD_MARGIN_CLASSES}>
              {this.renderEmailField()}
              {this.state.showAllFields && this.renderAdditionalFields()}
            </fieldset>
            <fieldset>{this.renderPrivacyCheckbox()}</fieldset>
          </div>
          <div className="tw-flex-shrink-0 tw-mt-8 medium:tw-mt-0">
            <ButtonSubmit widthClasses="tw-w-full">
              {getText("Sign up")}
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
        {this.renderHeader()}
        {this.renderDescription()}
        {this.renderForm()}
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

export default withSubmissionLogic(DefaultSignupForm);
