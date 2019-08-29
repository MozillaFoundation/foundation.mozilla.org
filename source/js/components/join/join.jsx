import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import classNames from "classnames";
import basketSignup from "../../basket-signup.js";

export default class JoinUs extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  reset() {
    if (!this.state.apiSuccess) {
      this.email.value = "";
      this.privacy.checked = false;
    }
    this.setState(this.getInitialState());
  }

  getInitialState() {
    return {
      apiSubmitted: false,
      apiSuccess: false,
      apiFailed: false,
      userTriedSubmitting: false
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
      apiSuccess: true
    });
  }

  // state update function
  apiSubmissionFailure(e) {
    if (e && e instanceof Error) {
      this.setState({
        apiFailed: true
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
      return false;
    }
    return input.match(/[^@]+@[^.@]+(\.[^.@]+)+$/) !== null;
  }

  /**
   * Submit the user's data to the API server.
   */
  submitDataToApi() {
    this.setState({ apiSubmitted: true });

    return new Promise((resolve, reject) => {
      let payload = {
        email: this.email.value,
        /* Strip query params in source url for newsletter signups: https://github.com/mozilla/foundation.mozilla.org/issues/2994#issuecomment-516997473 */
        source: window.location.href.split(`?`)[0]
      };

      if (this.givenNames) {
        payload.givenNames = this.givenNames.value;
      }
      if (this.surname) {
        payload.surname = this.surname.value;
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

    if (email && this.validatesAsEmail(email) && consent) {
      this.submitDataToApi()
        .then(() => {
          this.apiSubmissionSuccessful();
        })
        .catch(e => this.apiSubmissionFailure(e));
    }

    ReactGA.event({
      category: `signup`,
      action: `form submit tap`,
      label: `Signup submitted from ${
        this.props.formPosition ? this.props.formPosition : document.title
      }`
    });
  }

  /**
   * GA event when users interact with the signup form.
   */
  onInputFocus() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`
    });
  }

  /**
   * Render the signup CTA.
   */
  render() {
    let signupState = classNames({
      "signup-success": this.state.apiSuccess && this.state.apiSubmitted,
      "signup-fail": !this.state.apiFailed && this.state.apiSubmitted
    });

    let layoutClass =
      this.props.layout === `2-column` ? `col-12 col-md-6` : `col-12`;

    return (
      <div className={`row ${signupState}`}>
        <div className={layoutClass}>{this.renderFormHeading()}</div>
        <div className={layoutClass}>{this.renderFormContent()}</div>
      </div>
    );
  }

  /**
   * Render the CTA heading.
   */
  renderFormHeading() {
    return (
      <div>
        <h5 className="h5-heading">
          {!this.state.apiSuccess ? `${this.props.ctaHeader}` : `Thanks!`}
        </h5>
        {!this.state.apiSuccess ? (
          <p
            dangerouslySetInnerHTML={{
              __html: this.props.ctaDescription
            }}
          />
        ) : (
          <p
            dangerouslySetInnerHTML={{
              __html: this.props.thankYouMessage
            }}
          />
        )}
      </div>
    );
  }

  /**
   * Render the email field in signup CTA.
   */
  renderEmailField() {
    let wrapperClasses = classNames(``, {
      "has-danger":
        (!this.state.apiSuccess &&
          this.state.userTriedSubmitting &&
          !this.validatesAsEmail(this.email.value)) ||
        this.state.signupFailed
    });

    let classes = classNames(``, {
      "position-relative": wrapperClasses != ``
    });

    return (
      <div className={wrapperClasses}>
        <div className={classes}>
          <input
            type="email"
            className="form-control align-items"
            placeholder="Enter email address"
            ref={el => (this.email = el)}
            onFocus={evt => this.onInputFocus(evt)}
          />
          {this.state.userTriedSubmitting &&
            !this.state.apiSubmitted &&
            !this.validatesAsEmail(this.email.value) && (
              <div className="glyph-container">
                <span className="form-error-glyph" />
              </div>
            )}
        </div>
        {this.state.userTriedSubmitting &&
          (this.email.value == "" || this.email.value == null) && (
            <p className="body-small form-check form-control-feedback has-danger">
              This is a required section.
            </p>
          )}
        {this.state.userTriedSubmitting &&
          !this.state.apiSubmitted &&
          !this.validatesAsEmail(this.email.value) &&
          (!this.email.value == "" || !this.email.value == null) && (
            <p className="body-small form-check form-control-feedback has-danger">
              Please enter a valid email address.
            </p>
          )}
        {this.state.signupFailed && (
          <small className="form-check form-control-feedback has-danger">
            Something went wrong. Please check your email address and try again
          </small>
        )}
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
          <input
            type="text"
            className="form-control"
            placeholder="First name"
            ref={el => (this.givenNames = el)}
            onFocus={evt => this.onInputFocus(evt)}
          />
        </div>
        <div className="mb-2">
          <input
            type="text"
            className="form-control"
            placeholder="Last name"
            ref={el => (this.surname = el)}
            onFocus={evt => this.onInputFocus(evt)}
          />
        </div>
      </div>
    );
  }
  /**
   * Render the privacy field in signup CTA.
   */
  renderPrivacyField() {
    let classes = classNames(`my-3`, {
      "form-check": true,
      "has-danger":
        !this.state.apiSuccess &&
        this.state.userTriedSubmitting &&
        !this.privacy.checked
    });

    return (
      <div className={classes}>
        <div className="d-flex align-items-start">
          <div className="mb-0 form-check d-flex align-items-start">
            <input
              type="checkbox"
              className="form-check-input ml-0"
              id="PrivacyCheckbox"
              ref={el => (this.privacy = el)}
              required
            />
            <label className="form-check-label">
              <p className="d-inline-block body-small my-0">
                I'm okay with Mozilla handling my info as explained in this{" "}
                <a href="https://www.mozilla.org/privacy/websites/">
                  Privacy Notice
                </a>
              </p>
            </label>
          </div>
          {this.state.userTriedSubmitting &&
            !this.state.apiSubmitted &&
            !this.privacy.checked && (
              <span class="form-error-glyph d-flex mt-1 mt-lg-0" />
            )}
        </div>
        {this.state.userTriedSubmitting &&
          !this.state.apiSubmitted &&
          !this.privacy.checked && (
            <p className="body-small form-check form-control-feedback mt-0 mb-3">
              Please check this box if you want to proceed.
            </p>
          )}
      </div>
    );
  }

  /**
   * Render the submit button in signup CTA.
   */
  renderSubmitButton() {
    return <button className="btn btn-primary w-100">Sign up</button>;
  }

  /**
   * Render the actual CTA form, with an email
   * field and a consent checkbox.
   */
  renderFormContent() {
    if (this.state.apiSuccess) return null;

    let formClass = `d-flex flex-column`;
    let fieldsWrapperClass = `w-100`;
    let submitWrapperClass = `w-100`;

    if (this.props.buttonPosition === `side`) {
      formClass = `${formClass} flex-md-row`;
      fieldsWrapperClass = ``;
      submitWrapperClass = `ml-md-3`;
    }

    return (
      <form
        noValidate
        onSubmit={evt => this.processFormData(evt)}
        className={formClass}
      >
        <div className={`fields-wrapper ${fieldsWrapperClass}`}>
          {/* the data attribute is passed as a String from Python, so we need this check structured this way */}
          {this.props.askName === "True" && this.renderNameFields()}
          {this.renderEmailField()}
          {this.renderPrivacyField()}
        </div>
        <div className={submitWrapperClass}>{this.renderSubmitButton()}</div>
      </form>
    );
  }
}

JoinUs.defaultProps = {
  ctaHeader: `Protect the internet as a global public resource`,
  ctaDescription: `Join our email list to take action and stay updated!`,
  thankYouMessage: `If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. <strong>Please check your inbox or your spam filter for an email from us.</strong>`,
  newsletter: `mozilla-foundation`,
  askName: false
};
