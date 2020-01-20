import React from "react";
import { ReactGA } from "../../common";
import ReactDOM from "react-dom";
import classNames from "classnames";
import CountrySelect from "../petition/country-select.jsx";
import { getCurrentLanguage } from "../petition/locales";
import LanguageSelect from "./language-select.jsx";
import { Localized } from "../localized.js";
import utility from "../../utility";

export default class JoinUs extends React.Component {
  constructor(props) {
    super(props);
    this.id = {
      userEmail: utility.generateUniqueId(`join-user-email`),
      privacyCheckbox: utility.generateUniqueId(`join-privacy-checkbox`),
    };
    this.state = this.getInitialState(props);
  }

  reset() {
    if (!this.state.apiSuccess) {
      this.email.value = "";
      this.privacy.checked = false;
    }
    this.setState(this.getInitialState(this.props));
  }

  getInitialState(props) {
    return {
      apiSubmitted: false,
      apiSuccess: false,
      apiFailed: false,
      userTriedSubmitting: false,
      lang: getCurrentLanguage(),
      hideLocaleFields: [
        `header`,
        `body`,
        `footer`,
        `youtube-regrets-reporter`,
      ].includes(props.formPosition),
    };
  }

  /**
   * Ensure that the parent component is informed
   * about this component being mounted (primarily
   * used in the context of automated testing)
   */
  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  componentDidUpdate(prevProps, prevState) {
    let navWrapper = document.querySelector("#nav-newsletter-form-wrapper");

    // when user has successfully signed up for newsletter from the newsletter section on the nav,
    // update the dismiss button so it reads "Back to menu" instead of "No thanks"
    if (
      navWrapper &&
      navWrapper.contains(ReactDOM.findDOMNode(this)) &&
      navWrapper.querySelector(".form-dismiss") &&
      this.state.apiSuccess
    ) {
      navWrapper.querySelector(".form-dismiss").textContent = "Back to menu";
    }
  }

  // state update function
  apiSubmissionSuccessful() {
    this.setState({
      apiSuccess: true,
    });
  }

  // state update function
  apiSubmissionFailure(e) {
    if (e && e instanceof Error) {
      this.setState({
        apiFailed: true,
      });
    }
  }

  // state check function
  apiIsDone() {
    return (
      this.state.apiSubmitted && (this.state.apiSuccess || this.state.apiFailed)
    );
  }

  /**
   * Performs very simple validation for emails.
   * @param {string} input the string that should be validated as an email address
   * @returns {boolean} true if the input is a legal-enough email address, else false
   */
  validatesAsEmail(input) {
    if (!input) {
      return {
        valid: false,
        errorMessage: (
          <Localized stringId="form-field-required">{`This is a required section.`}</Localized>
        ),
      };
    }

    let valid = input.match(/[^@]+@[^.@]+(\.[^.@]+)+$/) !== null;

    if (!valid) {
      return {
        valid: false,
        errorMessage: (
          <Localized stringId="form-email-invalid">{`Please enter a valid email address.`}</Localized>
        ),
      };
    }

    return {
      valid: true,
    };
  }

  /**
   * Submit the user's data to the API server.
   */
  submitDataToApi() {
    this.setState({ apiSubmitted: true });

    return new Promise((resolve, reject) => {
      let payload = {
        email: this.email.value,
        /* keeping query params in source url for newsletter signups: https://github.com/mozilla/foundation.mozilla.org/issues/4102#issuecomment-590973606 */
        source: window.location.href,
      };

      if (this.givenNames) {
        payload.givenNames = this.givenNames.value;
      }
      if (this.surname) {
        payload.surname = this.surname.value;
      }

      if (this.country && this.country.element.value) {
        payload.country = this.country.element.value;
      }

      if (this.state.lang) {
        payload.lang = this.state.lang;
      }

      let xhr = new XMLHttpRequest();

      xhr.onreadystatechange = () => {
        if (xhr.readyState !== XMLHttpRequest.DONE) {
          return;
        }

        if (xhr.status !== 201) {
          reject(new Error(xhr.responseText));
        }

        resolve();
      };

      xhr.open(`POST`, this.props.apiUrl, true);
      xhr.setRequestHeader(`Content-Type`, `application/json`);
      xhr.setRequestHeader(`X-Requested-With`, `XMLHttpRequest`);
      xhr.setRequestHeader(`X-CSRFToken`, this.props.csrfToken);
      xhr.timeout = 5000;
      xhr.ontimeout = () => reject(new Error(`xhr timed out`));

      xhr.send(JSON.stringify(payload));
    });
  }

  /**
   * Process the form data, to make sure there is a valid
   * email address, and the consent checkbox has been checked,
   * before proceding with a data post to the API server.
   */
  processFormData(event) {
    this.setState({ userTriedSubmitting: true });
    event.preventDefault();

    // validate data here. Do not continue unless we're cool.
    let email = this.email.value;
    let consent = this.privacy.checked;

    if (email && this.validatesAsEmail(email).valid && consent) {
      this.submitDataToApi()
        .then(() => {
          this.apiSubmissionSuccessful();
        })
        .catch((e) => this.apiSubmissionFailure(e));
    }

    ReactGA.event({
      category: `signup`,
      action: `form submit tap`,
      label: `Signup submitted from ${
        this.props.formPosition ? this.props.formPosition : document.title
      }`,
    });
  }

  /**
   * On focus, we want to do two things:
   * 1.Fire a GA event when users interact with the signup form
   * 2.Reveal localization fields for header and footer signup forms
   */
  onInputFocus() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`,
    });

    if (this.state.hideLocaleFields) {
      this.setState({
        hideLocaleFields: false,
      });
    }
  }

  /**
   * Render the signup CTA.
   */
  render() {
    if (this.state.apiSuccess && this.state.apiSubmitted && this.isFlowForm()) {
      this.props.handleSignUp(true);
    }

    let signupState = classNames({
      "signup-success": this.state.apiSuccess && this.state.apiSubmitted,
      "signup-fail": !this.state.apiFailed && this.state.apiSubmitted,
    });

    let layoutClasses = classNames(`col-12`, {
      "col-md-6": this.props.layout === `2-column` && !this.state.apiSuccess,
      "col-sm-12 col-md-8":
        this.props.layout === `2-column` && this.state.apiSuccess,
      "col-md-11 m-auto": this.isFlowForm(),
    });

    return (
      <div className={`row ${signupState}`}>
        <div className={layoutClasses}>{this.renderFormHeading()}</div>
        <div className={layoutClasses}>{this.renderFormContent()}</div>
      </div>
    );
  }

  isFlowForm() {
    return this.props.formPosition === "flow";
  }

  /**
   * Render the CTA heading.
   */
  renderFlowHeading() {
    return [
      <h2 className="text-center">{this.props.flowHeading}</h2>,
      <p className="text-center">{this.props.flowText}</p>,
    ];
  }

  /**
   * Render the CTA heading.
   */
  renderSnippetHeading() {
    let header = (
      <Localized stringId="cta-header">{`Protect the internet as a global public resource`}</Localized>
    );
    let description = (
      <Localized
        stringId="cta-description"
        elems={{ strong: <strong></strong> }}
      >
        <p>{`Join our <strong>Mozilla News</strong> email list to take action and stay updated!`}</p>
      </Localized>
    );
    let doubleOptIn = (
      <div>
        <Localized
          stringId="cta-double-opt-in"
          elems={{ strong: <strong></strong> }}
        >
          <p>
            {`If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. <strong>Please check your inbox or your spam filter for an email from us.</strong>`}
          </p>
        </Localized>
        <Localized
          stringId="cta-manage-subscriptions"
          elems={{
            preferencesLink: (
              <a
                href="https://www.mozilla.org/newsletter/recovery/"
                target="_blank"
              >
                ``
              </a>
            ),
          }}
        >
          <p>
            {`If you have already confirmed your opt-in to receive Mozilla-related emails, you can now <preferencesLink>manage your subscriptions</preferencesLink> and update your email preferences.`}
          </p>
        </Localized>
      </div>
    );

    if (!this.state.apiSuccess) {
      if (this.props.ctaHeader) {
        header = this.props.ctaHeader;
      }
      if (this.props.ctaDescription) {
        description = (
          <div
            dangerouslySetInnerHTML={{
              __html: this.props.ctaDescription,
            }}
          />
        );
      }
    } else {
      header = <Localized stringId="thanks">{`Thanks!`}</Localized>;
      description = doubleOptIn;
    }

    return (
      <React.Fragment>
        <p className="h5-heading">{header}</p>
        {description}
      </React.Fragment>
    );
  }

  /**
   * Render the CTA heading.
   */
  renderFormHeading() {
    if (this.isFlowForm()) {
      return this.renderFlowHeading();
    }
    return this.renderSnippetHeading();
  }

  /**
   * Render the email field in signup CTA.
   */
  renderEmailField() {
    // During the first render, we bind the email field to this.email
    // using ref={el => (this.email = el)}
    // This means this.email is undefined until the second render.
    // To avoid TypeError we have do the following conditional assignment.
    let emailValidation = this.email
      ? this.validatesAsEmail(this.email.value)
      : false;

    let wrapperClasses = classNames({
      "has-danger":
        (!this.state.apiSuccess &&
          this.state.userTriedSubmitting &&
          !emailValidation.valid) ||
        this.state.signupFailed,
    });

    let classes = classNames(`mb-2`, {
      "position-relative": wrapperClasses !== ``,
    });

    let errorWrapperClasses = classNames("glyph-container", {
      "d-none": this.isFlowForm(),
    });

    return (
      <div className={wrapperClasses}>
        <div className={classes}>
          {this.isFlowForm() && (
            <label className="font-weight-bold" htmlFor={this.id.userEmail}>
              <Localized stringId="email-label">{`Email`}</Localized>
            </label>
          )}
          <Localized
            stringId="email-input"
            attrs={{ placeholder: true, "aria-label": !this.isFlowForm() }}
          >
            <input
              name="userEmail"
              type="email"
              className="form-control"
              placeholder="Please enter your email"
              ref={(el) => (this.email = el)}
              onFocus={(evt) => this.onInputFocus(evt)}
              aria-label={!this.isFlowForm() ? "Email" : ""}
              id={this.id.userEmail}
            />
          </Localized>
          {this.state.userTriedSubmitting && !emailValidation.valid && (
            <div className={errorWrapperClasses}>
              <span className="form-error-glyph" />
            </div>
          )}
        </div>
        {this.state.userTriedSubmitting && !emailValidation.valid && (
          <p className="body-small form-control-feedback">
            {emailValidation.errorMessage}
          </p>
        )}
        {this.state.signupFailed && (
          <small className="form-control-feedback">
            <Localized stringId="form-error">{`Something went wrong. Please check your email address and try again`}</Localized>
          </small>
        )}
      </div>
    );
  }

  /**
   * Render localization fields
   */

  setLang(lang) {
    this.setState({ lang });
  }

  renderLocaleFields() {
    return (
      <div hidden={this.state.hideLocaleFields}>
        <div className="mb-2">
          <Localized stringId="country" attrs={{ label: true }}>
            <CountrySelect
              ref={(element) => {
                this.country = element;
              }}
              label="Your country"
              className="w-100"
              formPosition={this.props.formPosition}
            />
          </Localized>
        </div>
        <div>
          <LanguageSelect
            className="w-100"
            handleLangChange={(e) => this.setLang(e)}
            selectedLang={this.state.lang}
            formPosition={this.props.formPosition}
          />
        </div>
      </div>
    );
  }

  /**
   * Render fields asking for user name
   */
  renderNameFields() {
    return (
      <div>
        <div className="mb-2">
          <Localized stringId="first-name" attrs={{ placeholder: true }}>
            <input
              type="text"
              className="form-control"
              placeholder="First name"
              ref={(el) => (this.givenNames = el)}
              onFocus={(evt) => this.onInputFocus(evt)}
            />
          </Localized>
        </div>
        <div className="mb-2">
          <Localized stringId="last-name" attrs={{ placeholder: true }}>
            <input
              type="text"
              className="form-control"
              placeholder="Last name"
              ref={(el) => (this.surname = el)}
              onFocus={(evt) => this.onInputFocus(evt)}
            />
          </Localized>
        </div>
      </div>
    );
  }
  /**
   * Render the privacy field in signup CTA.
   */
  renderPrivacyField() {
    let classes = classNames(`my-3 form-check form-group`, {
      "has-danger":
        !this.state.apiSuccess &&
        this.state.userTriedSubmitting &&
        !this.privacy.checked,
    });

    return (
      <div className={classes}>
        <div className="d-flex align-items-start">
          <input
            type="checkbox"
            className="form-check-input"
            id={this.id.privacyCheckbox}
            ref={(el) => (this.privacy = el)}
            required
          />
          <Localized
            stringId="privacy-policy"
            elems={{
              privacyLink: (
                <a href="https://www.mozilla.org/privacy/websites/">``</a>
              ),
            }}
          >
            <label
              className="form-check-label body-small"
              htmlFor={this.id.privacyCheckbox}
            >
              {`I’m okay with Mozilla handling my info as explained in <privacyLink>this Privacy Notice</privacyLink>`}
            </label>
          </Localized>
          {this.state.userTriedSubmitting &&
            !this.state.apiSubmitted &&
            !this.privacy.checked &&
            !this.isFlowForm() && (
              <span className="form-error-glyph privacy-error d-flex" />
            )}
        </div>
        {this.state.userTriedSubmitting && !this.privacy.checked && (
          <p className="body-small form-control-feedback mt-0 mb-3">
            <Localized stringId="form-checkbox">{`Please check this box if you want to proceed.`}</Localized>
          </p>
        )}
      </div>
    );
  }

  /**
   * Render the submit button in signup CTA.
   */
  renderSubmitButton() {
    let classnames = classNames("btn btn-primary", {
      "w-100": !this.isFlowForm(),
      "flex-1 mr-3": this.isFlowForm(),
    });
    return (
      <Localized stringId="sign-up-button">
        <button className={classnames}>{`Sign up`}</button>
      </Localized>
    );
  }

  /**
   * Render the actual CTA form, with an email
   * field and a consent checkbox.
   */
  renderFormContent() {
    if (this.state.apiSuccess) return null;

    let formClass = `d-flex flex-column join-form`;
    let fieldsWrapperClass = `w-100`;
    let buttonsWrapperClass = `w-100`;

    if (this.props.buttonPosition === `side`) {
      formClass = `${formClass} flex-md-row`;
      fieldsWrapperClass = ``;
      buttonsWrapperClass = `ml-md-3`;
    }

    if (this.props.formPosition === `flow`) {
      buttonsWrapperClass = `d-flex`;
    }

    return (
      <form
        noValidate
        onSubmit={(evt) => this.processFormData(evt)}
        className={formClass}
      >
        <div className={`fields-wrapper ${fieldsWrapperClass}`}>
          {/* the data attribute is passed as a String from Python, so we need this check structured this way */}
          {this.props.askName === "True" && this.renderNameFields()}
          {this.renderEmailField()}
          {this.renderLocaleFields()}
          {this.renderPrivacyField()}
        </div>
        <div className={buttonsWrapperClass}>
          {this.renderSubmitButton()}
          {this.isFlowForm() && (
            <Localized stringId="no-thanks-button">
              <button
                className="btn btn-primary btn-dismiss flex-1"
                onClick={() => this.props.handleSignUp(false)}
                type="button"
              >
                {`No Thanks`}
              </button>
            </Localized>
          )}
        </div>
      </form>
    );
  }
}

JoinUs.defaultProps = {
  newsletter: `mozilla-foundation`,
  askName: false,
};
