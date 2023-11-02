import React, { Component } from "react";
import PropTypes from "prop-types";
import Description from "../atoms/description.jsx";
import InputEmail from "../atoms/input-email.jsx";
import Select from "../atoms/select.jsx";
import InputCheckboxField from "../molecules/input-checkbox-field.jsx";
import ButtonSubmit from "../atoms/button-submit.jsx";
import utility from "../../../utility.js";
import { getText } from "../../petition/locales";
import { getCurrentLanguage } from "../../petition/locales";
import { COUNTRY_OPTIONS } from "../data/country-options.js";
import { LANGUAGE_OPTIONS } from "../data/language-options.js";

const FIELD_MARGIN_CLASSES = `tw-mb-4`;
const FIELD_ID_PREFIX = `blog-body-newsletter`;

class BlogBodySignForm extends Component {
  constructor(props) {
    super(props);

    this.state = this.getInitialState();
    this.ids = this.generateFieldIds([
      "email",
      "country",
      "language",
      "privacy",
    ]);
  }

  getInitialState() {
    return {
      emailValue: "",
      countryValue: "",
      languageValue: getCurrentLanguage(),
      privacyValue: false,
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

  handleSubmit(event) {
    event.preventDefault();
    console.log(`this.state: ${this.state}`);
  }

  showAllFields() {
    this.setState({ showAllFields: true });
  }

  handleEmailChange(event) {
    this.setState({ emailValue: event.target.value });
  }

  handleCountryChange(event) {
    this.setState({ countryValue: event.target.value });
  }

  handleLanguageChange(event) {
    this.setState({ languageValue: event.target.value });
  }

  handlePrivacyChange(event) {
    this.setState({ privacyValue: event.target.checked });
  }

  renderDescription() {
    const description = this.props.ctaHeader ? (
      <>
        <strong>{this.props.ctaHeader}</strong> // {this.props.ctaDescription}
      </>
    ) : (
      this.props.ctaDescription
    );

    return <Description>{description}</Description>;
  }

  renderEmailField() {
    return (
      <InputEmail
        id={this.ids.email}
        label={getText(`Email address`)}
        value={this.state.emailValue}
        placeholder={getText(`Please enter your email`)}
        onFocus={() => this.showAllFields()}
        onInput={() => this.showAllFields()}
        onChange={(event) => this.handleEmailChange(event)}
        required={true}
        outerMarginClasses={FIELD_MARGIN_CLASSES}
      />
    );
  }

  renderAdditionalFields() {
    return (
      <>
        <Select
          id={this.ids.country}
          name="country"
          value={this.state.countryValue}
          options={COUNTRY_OPTIONS}
          onChange={(event) => this.handleCountryChange(event)}
          required={false}
          outerMarginClasses={FIELD_MARGIN_CLASSES}
        />
        <Select
          id={this.ids.language}
          name="language"
          value={this.state.languageValue}
          options={LANGUAGE_OPTIONS}
          onChange={(event) => this.handleLanguageChange(event)}
          required={false}
          outerMarginClasses={FIELD_MARGIN_CLASSES}
        />
      </>
    );
  }

  renderPrivacyCheckbox() {
    return (
      <InputCheckboxField
        id={this.ids.privacy}
        label={getText(
          `I'm okay with Mozilla handling my info as explained in this Privacy Notice`
        )}
        checked={this.state.privacyValue}
        onChange={(event) => this.handlePrivacyChange(event)}
        required={true}
      />
    );
  }

  render() {
    return (
      <form
        onSubmit={(event) => this.handleSubmit(event)}
        className="tw-relative tw-border tw-px-8 tw-pt-14 tw-pb-12 medium:tw-p-16 before:tw-absolute before:tw-top-0 before:tw-left-1/2 before:-tw-translate-x-1/2 before:-tw-translate-y-1/2 before:tw-content-[''] before:tw-inline-block before:tw-w-[72px] before:tw-h-14 before:tw-bg-[url('../_images/glyphs/letter.svg')] before:tw-bg-white before:tw-bg-no-repeat before:tw-bg-center before:tw-bg-[length:24px_auto]"
      >
        {this.renderDescription()}
        <div className="d-flex flex-column flex-md-row medium:tw-gap-8">
          <div className="tw-flex-grow">
            <fieldset className={FIELD_MARGIN_CLASSES}>
              {this.renderEmailField()}
              {this.state.showAllFields && this.renderAdditionalFields()}
            </fieldset>
            <fieldset>{this.renderPrivacyCheckbox()}</fieldset>
          </div>
          <div className="tw-mt-8 medium:tw-mt-0">
            <ButtonSubmit widthClasses="tw-w-full">Join Now</ButtonSubmit>
          </div>
        </div>
      </form>
    );
  }
}

BlogBodySignForm.propTypes = {
  somePropName: PropTypes.string,
};

BlogBodySignForm.defaultProps = {
  somePropName: "",
};

export default BlogBodySignForm;
