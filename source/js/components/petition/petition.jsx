import React from "react";
import { ReactGA } from "../../common";
import classNames from "classnames";
import DonationModal from "./donation-modal.jsx";
import FloatingLabelInput from "./floating-label-input.jsx";
import FloatingLabelTextarea from "./floating-label-textarea.jsx";
import CountrySelect from "./country-select.jsx";
import { getText, getCurrentLanguage } from "./locales";
import copyToClipboard from "../../copy-to-clipboard";
const SALESFORCE_COMMENT_LIMIT = 500;
const CHECKBOX_LABEL_CLASS = `body-small`;

export default class Petition extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();

    // There may be up to four checkboxes per petition, but
    // the first two are hardcoded in the render() pipeline.
    this.checkbox1 = this.props.checkbox1;
    this.checkbox2 = this.props.checkbox2;

    // Do we have modal data?
    this.modals = false;
    if (this.props.modals) {
      this.modals = this.props.modals;
      try {
        this.modals = JSON.parse(this.modals);
      } catch (e) {
        this.modals = false;
        console.error(`Could not parse modal data from petition markup.`);
      }
    }
  }

  // helper function for initial component state
  getInitialState() {
    // Values that match the various use cases described in render():
    //
    //  1. all false
    //  2. all false, click "submit" on the page
    //  3. all filled in, click "submit" on the page
    //  4. true, true, false, true
    //  5. true, false, true, true
    //
    return {
      apiSubmitted: false,
      apiSuccess: false,
      apiFailed: false,
      userTriedSubmitting: false,
      showDonationModal: false
    };
  }

  // helper function to set up GA input events
  onInputFocus() {
    ReactGA.event({
      category: `petition`,
      action: `form focus`,
      label: `Petition form input focused`
    });
  }

  // helper function for auto-generating checkboxes off of the passed props.
  generateCheckboxes(disabled) {
    return [`checkbox1`, `checkbox2`]
      .map(name => {
        let label = this[name];

        if (!label) {
          return null;
        }
        return (
          <div key={name}>
            <label className="form-check-label">
              <input
                className="form-check-input"
                disabled={disabled}
                type="checkbox"
                ref={name}
              />
              <div
                className={CHECKBOX_LABEL_CLASS}
                dangerouslySetInnerHTML={{ __html: label }}
              />
            </label>
          </div>
        );
      })
      .filter(v => v);
  }

  // state update function
  apiSubmissionSuccessful() {
    let update = {
      apiSuccess: true
    };

    if (this.props.modals && this.props.modals.length > 0) {
      update.showDonationModal = true;
    }

    this.setState(update);
  }

  // state update function
  apiSubmissionFailure(e) {
    if (e && e instanceof Error) {
      this.setState({ apiFailed: true });
    }
  }

  // state check function
  apiIsDone() {
    return (
      this.state.apiSubmitted && (this.state.apiSuccess || this.state.apiFailed)
    );
  }

  shareButtonClicked(event, shareProgressButtonId) {
    ReactGA.event({
      category: `petition`,
      action: `share tap`,
      label: `${document.title} - share tap`
    });

    if (shareProgressButtonId) {
      let shareProgressButton = document.querySelector(
        `#${shareProgressButtonId} a`
      );

      if (shareProgressButton) {
        shareProgressButton.click();
      }
    } else {
      copyToClipboard(event.target, window.location.href);
    }
  }

  /**
   * Submit the user's data to the API server.
   *
   * @returns {promise} the result the XHR post attempt.
   */
  submitDataToApi() {
    this.setState({ apiSubmitted: true });

    return new Promise((resolve, reject) => {
      let givenNames = this.givenNames.element.value;
      let surname = this.surname.element.value;
      let country = this.country && this.country.element.value;
      let postalCode = this.postalCode && this.postalCode.element.value;
      let comment = this.comment && this.comment.element.value;
      let newsletterSignup = false;
      let lang = getCurrentLanguage();

      // These should not be possible due to the fact that we validate
      // their content prior to submission. TODO: remove these rejections?
      if (!givenNames || !surname) {
        return reject(new Error(`missing name/surname`));
      }

      if (this.props.requiresCountryCode === `True` && !country) {
        return reject(new Error(`missing country`));
      }

      if (this.props.requiresPostalCode === `True` && !postalCode) {
        return reject(new Error(`missing postal code`));
      }

      if (this.props.commentRequirements === `required` && !comment) {
        return reject(new Error(`missing required comment`));
      }

      if (comment && comment.length >= SALESFORCE_COMMENT_LIMIT) {
        return reject(new Error(`comment too long`));
      }

      if (this.refs.newsletterSignup) {
        newsletterSignup = !!this.refs.newsletterSignup.checked;
      }

      let payload = {
        givenNames,
        surname,
        email: this.email.element.value,
        checkbox1: this.props.checkbox1 ? !!this.refs.checkbox1.checked : null,
        checkbox2: this.props.checkbox2 ? !!this.refs.checkbox2.checked : null,
        newsletterSignup,
        country,
        lang,
        postalCode,
        comment,
        source: window.location.toString()
      };

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
   * kick off the form processing when the user hits "submit".
   * @param {event} event the form submission event generated by the browser
   * @returns {void}
   */
  processFormData(event) {
    this.setState({ userTriedSubmitting: true });
    event.preventDefault();

    // validate data here. Do not continue unless we're cool.
    let hasName = this.givenNames.element.value && this.surname.element.value;
    let email = this.email.element.value;

    email = email && this.validatesAsEmail(email);

    let consent = this.refs.privacy.checked;
    let country = true;
    let postalCode = true;
    let comment = true;

    if (this.props.requiresCountryCode === `True`) {
      country = !!this.country.element.value;
    }

    if (this.props.requiresPostalCode === `True`) {
      postalCode = !!this.postalCode.element.value;
    }

    let commentValue = this.comment
      ? this.comment.element && this.comment.element.value
      : ``;

    if (this.props.commentRequirements === `required`) {
      comment = !!commentValue;
    }

    if (comment && commentValue.length >= SALESFORCE_COMMENT_LIMIT) {
      comment = false;
    }

    if (hasName && email && consent && country && postalCode && comment) {
      this.submitDataToApi()
        .then(() => {
          this.apiSubmissionSuccessful();
        })
        .catch(e => this.apiSubmissionFailure(e));
    }

    ReactGA.event({
      category: `petition`,
      action: `form submit tap`,
      label: `Petition form submitted`
    });
  }

  /**
   * Performs very simple validation for emails.
   * @param {string} input the string that should be validated as an email address
   * @returns {boolean} true if the input is a legal-enough email address, else false
   */
  validatesAsEmail(input) {
    if (!input) {
      return false;
    }
    return input.match(/[^@]+@[^.@]+(\.[^.@]+)+$/) !== null;
  }

  userElectedToDonate() {
    this.setState({ showDonationModal: false });
  }

  userElectedToShare() {
    this.setState({ showDonationModal: false });
  }

  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  /**
   * master render entry point - this will branch out
   * to different render functions depending on the
   * state of the user's data and xhr call results.
   *
   * @returns {jsx} the main render output.
   */
  render() {
    // There are six possible render paths:
    //
    //  1. Waiting for user to fill in data and hit submit
    //  2. user clicked submit but with incomplete data
    //  3. user clicked submit, data was accepted, we're waiting for things to happen
    //  4. API post attempted, and succeeded
    //  5. API post attempted, and failed
    //
    // These paths effect:
    //
    //  1. normal render path for user input UI
    //  2. normal render path for faulty user input UI
    //  3. normal render with disabled fields
    //  4. thank the user and let them share the call-out
    //  5. notify that something went wrong and ask them to try again later

    let signingIsDone = this.apiIsDone();
    let success = signingIsDone && this.state.apiSuccess;

    let signupState = classNames({
      row: true,
      "sign-success": success,
      "sign-failure": signingIsDone && this.state.apiFailed
    });

    let unrecoverableError =
      this.state.apiSubmitted && !this.state.apiSuccess && this.state.apiFailed;

    let petitionContent, formContent;

    if (success) {
      petitionContent = this.renderThankYou();
    } else if (unrecoverableError) {
      petitionContent = this.renderUnrecoverableError();
    } else {
      petitionContent = this.renderStandardHeading();
      formContent = !unrecoverableError && this.renderSubmissionForm();
    }

    return (
      <div className={signupState}>
        <div className="col">
          <div className="row">
            <div className="col-12 petition-content">{petitionContent}</div>
            {formContent}
          </div>
        </div>
        {this.state.showDonationModal ? this.renderDonationModal() : null}
      </div>
    );
  }

  /**
   * This renders a donation modal on the page as full-page-overlay,
   * provided the petition HTML specifies that as a thing that should happen.
   * @returns {JSX} the donation modal component to render
   */
  renderDonationModal() {
    // This is where can do client-side A/B testing
    let modals = this.modals;

    if (modals.length === 0) {
      return null;
    }

    let modal = modals[0];

    return (
      <DonationModal
        slug={this.props.ctaSlug}
        name={modal.name}
        heading={modal.header}
        bodyText={modal.body}
        donateText={modal.donate_text}
        shareText={modal.dismiss_text}
        onDonate={() => this.userElectedToDonate()}
        onShare={() => this.userElectedToShare()}
        onClose={() => this.setState({ showDonationModal: false })}
      />
    );
  }

  /**
   * @returns {jsx} What users see when their petition sign up succeeded.
   */
  renderThankYou() {
    if (this.props.shareLink) {
      return (
        <div>
          <p>{this.props.thankYou}</p>
          <a href={this.props.shareLink} className="btn btn-info">
            {this.props.shareText}
          </a>
        </div>
      );
    } else {
      return (
        <div>
          <p>{this.props.thankYou}</p>
          <div className="share-button-group rectangle stacked">
            <div className="subgroup">
              <button
                className="btn btn-secondary btn-share facebook-share"
                onClick={e => this.shareButtonClicked(e, `share-progress-fb`)}
              >
                Facebook
              </button>
              <button
                className="btn btn-secondary btn-share twitter-share"
                onClick={e => this.shareButtonClicked(e, `share-progress-tw`)}
              >
                Twitter
              </button>
            </div>
            <div className="subgroup">
              <button
                className="btn btn-secondary btn-share email-share"
                onClick={e => this.shareButtonClicked(e, `share-progress-em`)}
              >
                Email
              </button>
              <button
                className="btn btn-secondary btn-share link-share"
                onClick={e => this.shareButtonClicked(e)}
                data-success-text="Copied"
              >
                Copy
              </button>
            </div>
          </div>
        </div>
      );
    }
  }

  /**
   * @returns {jsx} What users see when an unrecoverable error occurs.
   */
  renderUnrecoverableError() {
    return (
      <div>
        <p>
          Something went wrong while trying to sign the petition. Please try
          again later.
        </p>
      </div>
    );
  }

  /**
   * @returns {jsx} What users see when they initially open the page, above the actual petition form.
   */
  renderStandardHeading() {
    return (
      <div>
        <h5 className="h5-heading">{this.props.ctaHeader}</h5>
        {this.renderCtaDescription()}
      </div>
    );
  }

  /**
   * @returns {jsx} Petition cta description if one exists.
   */
  renderCtaDescription() {
    if (this.props.ctaDescription) {
      return (
        <div dangerouslySetInnerHTML={{ __html: this.props.ctaDescription }} />
      );
    }
    return null;
  }

  /**
   * Render the submission form, either interactive, with fields
   * marked as not valid yet, or with fields disabled if the
   * user submitted the form data for processing.
   *
   * @returns {jsx} the petition form
   */
  renderSubmissionForm() {
    let disableFields =
      this.state.userTriedSubmitting && this.state.apiSubmitted
        ? `disabled`
        : null;

    let givenGroupClass = classNames({
      "has-danger":
        this.state.userTriedSubmitting && !this.givenNames.element.value
    });

    let surGroupClass = classNames({
      "has-danger":
        this.state.userTriedSubmitting && !this.surname.element.value
    });

    let emailGroupClass = classNames({
      "has-danger":
        this.state.userTriedSubmitting &&
        (!this.email.element.value ||
          !this.validatesAsEmail(this.email.element.value))
    });

    let countryGroupClass = classNames({
      "has-danger":
        this.props.requiresCountryCode === `True` &&
        this.state.userTriedSubmitting &&
        !this.country.element.value
    });

    let postalCodeGroupClass = classNames({
      "has-danger":
        this.props.requiresPostalCode === `True` &&
        this.state.userTriedSubmitting &&
        !this.postalCode.element.value
    });

    let commentGroupClass = classNames({
      "has-danger":
        (this.props.commentRequirements === `required` &&
          this.state.userTriedSubmitting &&
          !this.comment.element.value) ||
        (this.state.userTriedSubmitting &&
          this.comment &&
          this.comment.element.value &&
          this.comment.element.value.length >= SALESFORCE_COMMENT_LIMIT)
    });

    let privacyClass = classNames(`my-3`, {
      "form-check": true,
      "has-danger": this.state.userTriedSubmitting && !this.refs.privacy.checked
    });

    let errorMessageClass = `body-small form-control-feedback`;

    let checkboxes = this.generateCheckboxes(disableFields);

    return (
      <div className="col petition-form" id="petition-form">
        <form onSubmit={e => this.processFormData(e)} noValidate={true}>
          <div className="mb-3">
            <div className={givenGroupClass}>
              <FloatingLabelInput
                className="mb-1 w-100"
                ref={element => {
                  this.givenNames = element;
                }}
                id="givenNames"
                type="text"
                label={getText(`First name`)}
                disabled={disableFields}
                onFocus={this.onInputFocus}
              />
              {this.state.userTriedSubmitting &&
                !this.givenNames.element.value && (
                  <p className={errorMessageClass}>
                    {getText(`Please enter your given name(s)`)}
                  </p>
                )}
            </div>
            <div className={surGroupClass}>
              <FloatingLabelInput
                className="mb-1 w-100"
                ref={element => {
                  this.surname = element;
                }}
                id="surname"
                type="text"
                label={getText(`Last name`)}
                disabled={disableFields}
                onFocus={this.onInputFocus}
              />
              {this.state.userTriedSubmitting &&
                !this.surname.element.value && (
                  <p className={errorMessageClass}>
                    {getText(`Please enter your surname`)}
                  </p>
                )}
            </div>
            <div className={emailGroupClass}>
              <FloatingLabelInput
                className="mb-1 w-100"
                ref={element => {
                  this.email = element;
                }}
                id="emailInput"
                type="email"
                label={getText(`Email address`)}
                disabled={disableFields}
                onFocus={this.onInputFocus}
              />
              {this.state.userTriedSubmitting &&
                (!this.email.element.value ||
                  !this.validatesAsEmail(this.email.element.value)) && (
                  <p className={errorMessageClass}>
                    {getText(`Please enter your email`)}
                  </p>
                )}
            </div>
            <div className={countryGroupClass}>
              <CountrySelect
                className="form-control-lg mb-1 w-100"
                ref={element => {
                  this.country = element;
                }}
                label={getText(`Your country`)}
                disabled={disableFields}
                onFocus={this.onInputFocus}
              />
              {this.props.requiresCountryCode === `True` &&
                this.state.userTriedSubmitting &&
                !this.country.element.value && (
                  <p className={errorMessageClass}>
                    {getText(`Please enter your country`)}
                  </p>
                )}
            </div>

            {this.props.requiresPostalCode === `False` ? null : (
              <div className={postalCodeGroupClass}>
                <FloatingLabelInput
                  className="mb-1 w-100"
                  ref={element => {
                    this.postalCode = element;
                  }}
                  id="postalCodeInput"
                  type="text"
                  label={getText(`Postal code`)}
                  disabled={disableFields}
                  onFocus={this.onInputFocus}
                />
                {this.state.userTriedSubmitting &&
                  !this.postalCode.element.value && (
                    <p className={errorMessageClass}>
                      {getText(`Please enter your postal code`)}
                    </p>
                  )}
              </div>
            )}
            {this.props.commentRequirements === `none` ? null : (
              <div className={commentGroupClass}>
                <FloatingLabelTextarea
                  className="mb-1 w-100"
                  ref={element => {
                    this.comment = element;
                  }}
                  id="commentInput"
                  type="text"
                  label={getText(`Comment`)}
                  disabled={disableFields}
                  onFocus={this.onInputFocus}
                />
                {this.props.commentRequirements === `required` &&
                  this.state.userTriedSubmitting &&
                  !this.comment.element.value && (
                    <p className={errorMessageClass}>
                      Please include a comment
                    </p>
                  )}
                {this.state.userTriedSubmitting &&
                  this.comment &&
                  this.comment.element.value &&
                  this.comment.element.value.length >=
                    SALESFORCE_COMMENT_LIMIT && (
                    <p className={errorMessageClass}>
                      Comments cannot be longer than {SALESFORCE_COMMENT_LIMIT}{" "}
                      characters
                    </p>
                  )}
              </div>
            )}
          </div>
          <div className={privacyClass}>
            <div className="my-2">
              <label className="form-check-label">
                <input
                  disabled={disableFields}
                  type="checkbox"
                  className="form-check-input"
                  id="PrivacyCheckbox"
                  ref="privacy"
                />
                <div className={CHECKBOX_LABEL_CLASS}>
                  {getText(
                    `I'm okay with Mozilla handling my info as explained in this Privacy Notice`
                  )}
                </div>
                {this.state.userTriedSubmitting &&
                  !this.refs.privacy.checked && (
                    <p className={errorMessageClass}>
                      {getText(`Please check this box if you want to proceed`)}
                    </p>
                  )}
              </label>
            </div>
            {this.props.subscribed ? null : (
              <div className="my-2">
                <label className="form-check-label">
                  <input
                    disabled={disableFields}
                    type="checkbox"
                    className="form-check-input"
                    id="NewsletterSignup"
                    ref="newsletterSignup"
                  />
                  <div className={CHECKBOX_LABEL_CLASS}>
                    {getText(
                      `Yes, I want to receive email updates about Mozilla's campaigns.`
                    )}
                  </div>
                </label>
              </div>
            )}
            {checkboxes.length > 0 ? <div>{checkboxes}</div> : null}
          </div>
          <div className="my-3">
            <button
              disabled={disableFields}
              className="col-12 btn btn-primary petition-btn"
            >
              {getText(`Add my name`)}
            </button>
          </div>
        </form>
      </div>
    );
  }
}

Petition.defaultProps = {
  ctaDescription: <p>{getText(`Add my name`)}</p>,
  ctaHeader: ``,
  newsletter: `mozilla-foundation`
};
