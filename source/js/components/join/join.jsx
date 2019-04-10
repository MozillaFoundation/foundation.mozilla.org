import React from "react";
import ReactGA from "react-ga";
import classNames from "classnames";
import basketSignup from "../../basket-signup.js";

export default class JoinUs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
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
   * Submit the user's data to the API server.
   */
  submitDataToApi() {
    this.setState({ apiSubmitted: true });

    return new Promise((resolve, reject) => {
      let payload = {
        email: this.email.value,
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

    if (email && consent) {
      this.submitDataToApi()
        .then(() => {
          this.apiSubmissionSuccessful();
        })
        .catch(e => this.apiSubmissionFailure(e));
    }

    ReactGA.event({
      category: `signup`,
      action: `form submit tap`,
      label: `Signup submitted`
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

  createClasslist(classes = ``) {
    if (this.props.theme === `dark-theme`) {
      classes = ` ${classes} dark-theme`;
    }

    return classes;
  }

  /**
   * Render the signup CTA.
   */
  render() {
    let signupState = classNames({
      "signup-success": this.state.apiSuccess && this.state.apiSubmitted,
      "signup-fail": !this.state.apiFailed && this.state.apiSubmitted
    });

    return (
      <div className={this.createClasslist(`container px-0 ${signupState}`)}>
        <div className="row">
          {this.renderFormHeading()}
          {this.renderFormContent()}
        </div>
      </div>
    );
  }

  /**
   * Render the CTA heading.
   */
  renderFormHeading() {
    return (
      <div className="col-12">
        <h5 className={this.createClasslist(`h5-heading`)}>
          {!this.state.apiSuccess ? `${this.props.ctaHeader}` : `Thanks!`}
        </h5>
        {!this.state.apiSuccess ? (
          <p
            className={this.createClasslist()}
            dangerouslySetInnerHTML={{
              __html: this.props.ctaDescription
            }}
          />
        ) : (
          <p
            className={this.createClasslist()}
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
    let classes = classNames(`mb-2`, {
      "has-danger":
        (!this.state.apiSuccess &&
          this.state.userTriedSubmitting &&
          !this.email.value) ||
        this.state.signupFailed
    });

    return (
      <div className={classes}>
        <input
          type="email"
          className="form-control"
          placeholder="Enter email address"
          ref={el => (this.email = el)}
          onFocus={evt => this.onInputFocus(evt)}
        />
        {this.state.userTriedSubmitting &&
          !this.state.apiSubmitted &&
          !this.email.value && (
            <p className="body-small form-check form-control-feedback">
              Please enter your email
            </p>
          )}
        {this.state.signupFailed && (
          <small className="form-check form-control-feedback">
            Something went wrong. Please check your email address and try again
          </small>
        )}
      </div>
    );
  }

  /**
   * Render the privacy field in signup CTA.
   */
  renderPrivacyField() {
    let classes = classNames(`mb-2`, {
      "form-check": true,
      "has-danger":
        !this.state.apiSuccess &&
        this.state.userTriedSubmitting &&
        !this.privacy.checked
    });

    return (
      <div className={classes}>
        <label className="form-check-label">
          <input
            type="checkbox"
            className="form-check-input"
            id="PrivacyCheckbox"
            ref={el => (this.privacy = el)}
          />
          <p className={this.createClasslist(`d-inline-block body-small mb-0`)}>
            I'm okay with Mozilla handling my info as explained in this{" "}
            <a
              href="https://www.mozilla.org/privacy/websites/"
              className={this.createClasslist()}
            >
              Privacy Notice
            </a>
          </p>
          {this.state.userTriedSubmitting &&
            !this.state.apiSubmitted &&
            !this.privacy.checked && (
              <p className="body-small form-check form-control-feedback">
                Please check this box if you want to proceed
              </p>
            )}
        </label>
      </div>
    );
  }

  /**
   * Render the submit button in signup CTA.
   */
  renderSubmitButton() {
    return (
      <button
        className={this.createClasslist(`btn btn-primary join-btn w-100`)}
      >
        Sign up
      </button>
    );
  }

  /**
   * Render the actual CTA form, with an email
   * field and a consent checkbox.
   */
  renderFormContent() {
    if (this.state.apiSuccess) return null;

    let fieldsWrapperClass =
      this.props.layout === `side-button` ? `col-md-9` : `col-md-12`;
    let submitWrapperClass =
      this.props.layout === `side-button` ? `col-md-3 pl-md-0` : `col-md-12`;

    return (
      <div className="col-12">
        <form onSubmit={evt => this.processFormData(evt)} className="row">
          <div className={fieldsWrapperClass}>
            {this.renderEmailField()}
            {this.renderPrivacyField()}
          </div>
          <div className={submitWrapperClass}>{this.renderSubmitButton()}</div>
        </form>
      </div>
    );
  }
}

JoinUs.defaultProps = {
  ctaHeader: `Want to get smarter about your online life?`,
  ctaDescription: `Sign up for our Mozilla newsletter!`,
  thankYouMessage: `If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. <strong>Please check your inbox or your spam filter for an email from us.</strong>`,
  newsletter: `mozilla-foundation`
};
