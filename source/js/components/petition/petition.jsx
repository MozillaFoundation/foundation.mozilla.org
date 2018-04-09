import React from 'react';
import ReactGA from 'react-ga';
import classNames from 'classnames';
import basketSignup from '../../basket-signup.js';

export default class Petition extends React.Component {
  constructor(props) {
    super(props);
    // Default props defined at end of file

    // TODO: this needs a better solution, because explicitly binding
    //       ten+ functions is kind of silly. The code should already
    //       guarantee the correct `this` will be used.
    this.submitDataToApi = this.submitDataToApi.bind(this);
    this.signUpToBasket = this.signUpToBasket.bind(this);
    this.processFormData = this.processFormData.bind(this);

    this.apiSubmissionSuccessful = this.apiSubmissionSuccessful.bind(this);
    this.apiSubmissionFailure = this.apiSubmissionFailure.bind(this);
    this.basketSubmissionSuccessful = this.basketSubmissionSuccessful.bind(this);
    this.basketSubmissionFailure = this.basketSubmissionFailure.bind(this);

    this.apiIsDone = this.apiIsDone.bind(this);
    this.basketIsDone = this.basketIsDone.bind(this);
    this.submissionsAreDone = this.submissionsAreDone.bind(this);

    this.twButtonClicked = this.twButtonClicked.bind(this);
    this.fbButtonClicked = this.fbButtonClicked.bind(this);
    this.emButtonClicked = this.emButtonClicked.bind(this);

    this.state = this.getInitialState();

    // There may be up to four checkboxes per petition, but
    // the first two are hardcoded in the render() pipeline.
    this.checkbox1 = this.props.checkbox1;
    this.checkbox2 = this.props.checkbox2;
  }

  // helper function for initial component state
  getInitialState() {
    // Values that match the various use cases described in render():
    //
    //  1. all false
    //  2. all false, click "submit" on the page
    //  3. all filled in, click "submit" on the page
    //  4. true, true, false, true, true, false, true
    //  5. true, true, false, true, false, true, true
    //  6. true, false, true, false, false, false, true
    //
    return {
      apiSubmitted: false,
      apiSuccess: false,
      apiFailed: false,
      basketSubmitted: false,
      basketSuccess: false,
      basketFailed: false,
      userTriedSubmitting: false
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
    return [`checkbox1`, `checkbox2`].map(name => {
      let label = this[name];

      if (!label) { return null; }
      return (
        <div key={name}>
          <label className="form-check-label mb-2">
            <input className="form-check-input" disabled={disabled} type="checkbox" ref={name} />
            <span className="h6-heading form-text" dangerouslySetInnerHTML={{__html: label}}/>
          </label>
        </div>
      );
    }).filter(v => v);
  }

  // state update function
  apiSubmissionSuccessful() {
    this.setState({ apiSuccess: true });
  }

  // state update function
  apiSubmissionFailure(e) {
    console.error(e);
    if(e instanceof Error) {
      this.setState({ apiFailed: true });
    }
  }

  // state update function
  basketSubmissionSuccessful() {
    this.setState({ basketSuccess: true });
  }

  // state update function
  basketSubmissionFailure(e) {
    console.error(e);
    if(e instanceof Error) {
      this.setState({ basketFailed: true });
    }
  }

  // state check function
  apiIsDone() {
    return this.state.apiSubmitted && (this.state.apiSuccess || this.state.apiFailed);
  }

  // state check function
  basketIsDone() {
    return this.state.basketSubmitted && (this.state.basketSuccess || this.state.basketFailed);
  }

  // state check function
  submissionsAreDone() {
    return this.apiIsDone() && this.basketIsDone();
  }

  fbButtonClicked() {
    this.shareButtonClicked(`#share-progress-fb`);
  }

  twButtonClicked() {
    this.shareButtonClicked(`#share-progress-tw`);
  }

  emButtonClicked() {
    this.shareButtonClicked(`#share-progress-em`);
  }

  shareButtonClicked(id) {
    ReactGA.event({
      category: `petition`,
      action: `share tap`,
      label: `${document.title} - share tap`
    });

    document.querySelector(id + ` a`).click();
  }

  /**
   * Submit the user's data to the API server.
   *
   * @returns {promise} the result the XHR post attempt.
   */
  submitDataToApi() {
    this.setState({ apiSubmitted: true });

    return new Promise((resolve, reject) => {
      let givenNames = this.refs.givenNames.value;
      let surname = this.refs.surname.value;

      if(!givenNames || !surname) {
        return reject();
      }

      let payload = {
        givenNames,
        surname,
        email: this.refs.email.value,
        checkbox1: this.props.checkbox1 ? !!(this.refs.checkbox1.checked) : null,
        checkbox2: this.props.checkbox2 ? !!(this.refs.checkbox2.checked) : null,
        newsletterSignup: !!(this.refs.newsletterSignup.checked)
      };

      let xhr = new XMLHttpRequest();

      xhr.onreadystatechange = () => {
        if(xhr.readyState !== XMLHttpRequest.DONE) {
          return;
        }

        if(xhr.status !== 201) {
          reject(new Error(xhr.responseText));
        }

        resolve();
      };

      xhr.open(`POST`, this.props.apiUrl, true);
      xhr.setRequestHeader(`Content-Type`, `application/json`);
      xhr.setRequestHeader(`X-Requested-With`,`XMLHttpRequest`);
      xhr.setRequestHeader(`X-CSRFToken`, this.props.csrfToken);
      xhr.timeout = 5000;
      xhr.ontimeout = reject;

      xhr.send(JSON.stringify(payload));
    });
  }

  /**
   * sign the user up for the mozilla newsletter.
   *
   * @returns {promise} the result the XHR post attempt.
   */
  signUpToBasket() {
    this.setState({ basketSubmitted: true });

    return new Promise((resolve, reject) => {
      if(this.refs.email.value && this.refs.privacy.checked){
        if(this.refs.newsletterSignup.checked) {
          basketSignup({
            email: this.refs.email.value,
            privacy: this.refs.privacy.checked,
            newsletter: this.props.newsletter
          }, resolve, reject);
        } else {
          resolve();
        }
      } else {
        reject();
      }
    });
  }

  /**
   * kick off the form processing when the user hits "submit".
   *
   * @returns {void}
   */
  processFormData(event) {
    this.setState({ userTriedSubmitting: true });
    event.preventDefault();

    // validate data here. Do not continue unless we're cool.
    let hasName = this.refs.givenNames.value && this.refs.surname.value;
    let email = this.refs.email.value;
    let consent = this.refs.privacy.checked;

    if (hasName && email && consent) {
      this.submitDataToApi()
        .then(() => {
          this.apiSubmissionSuccessful();
          this.signUpToBasket()
            .then(this.basketSubmissionSuccessful)
            .catch(this.basketSubmissionFailure);
        })
        .catch(this.apiSubmissionFailure);
    }

    ReactGA.event({
      category: `petition`,
      action: `form submit tap`,
      label: `Petition form submitted`
    });
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
    //  4. API post attempted, and succeeded, Basket signup attempted, and succeded
    //  5. API post attempted, and succeeded, Basket signup attempted, and failed
    //  6. API post attempted, and failed, Basket signup not attempted
    //
    // These paths effect:
    //
    //  1. normal render path for user input UI
    //  2. normal render path for faulty user input UI
    //  3. normal render with disabled fields
    //  4. thank the user and let them share the call-out
    //  5. thank the user and let them share the call-out (we ignore basket failure entirely)
    //  6. notify that something went wrong and ask them to try again later

    let signingIsDone = this.submissionsAreDone();
    let success = signingIsDone && this.state.apiSuccess; // we don't actually care about basket succeeding, see (5)

    let signupState = classNames({
      'row': true,
      'sign-success': success,
      'sign-failure': signingIsDone && (this.state.apiFailed || this.state.basketFailed)
    });

    let unrecoverableError = this.state.apiSubmitted && !this.state.apiSuccess && this.state.apiFailed;

    let petitionContent, formContent;

    if (success) {
      petitionContent = this.renderThankYou();
    } else if (unrecoverableError) {
      petitionContent = this.renderUnrecoverableError();
    } else {
      petitionContent = this.renderStandardHeading();
      formContent = !unrecoverableError && !this.state.basketSuccess && this.renderSubmissionForm();
    }

    return (
      <div className={signupState}>
        <div className="col">
          <div className="row">
            <div className="col-12 petition-content">{ petitionContent }</div>
            { formContent }
          </div>
        </div>
      </div>
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
          <a href={this.props.shareLink} className="btn btn-info">{this.props.shareText}</a>
        </div>
      );
    } else {
      return (
        <div>
          <p>{this.props.thankYou}</p>
          <div className="share-btn-container">
            <button className="share-progress-btn share-progress-fb" onClick={this.fbButtonClicked}>
              <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 264 512">
                <path fill="currentColor" d="M76.7 512V283H0v-91h76.7v-71.7C76.7 42.4 124.3 0 193.8 0c33.3 0 61.9 2.5 70.2 3.6V85h-48.2c-37.8 0-45.1 18-45.1 44.3V192H256l-11.7 91h-73.6v229"></path>
              </svg>
              SHARE
            </button>
            <button className="share-progress-btn share-progress-tw" onClick={this.twButtonClicked}>
              <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path fill="currentColor" d="M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z"></path>
              </svg>
              TWEET
            </button>
            <button className="share-progress-btn share-progress-em" onClick={this.emButtonClicked}>
              <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path fill="currentColor" d="M502.3 190.8c3.9-3.1 9.7-.2 9.7 4.7V400c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V195.6c0-5 5.7-7.8 9.7-4.7 22.4 17.4 52.1 39.5 154.1 113.6 21.1 15.4 56.7 47.8 92.2 47.6 35.7.3 72-32.8 92.3-47.6 102-74.1 131.6-96.3 154-113.7zM256 320c23.2.4 56.6-29.2 73.4-41.4 132.7-96.3 142.8-104.7 173.4-128.7 5.8-4.5 9.2-11.5 9.2-18.9v-19c0-26.5-21.5-48-48-48H48C21.5 64 0 85.5 0 112v19c0 7.4 3.4 14.3 9.2 18.9 30.6 23.9 40.7 32.4 173.4 128.7 16.8 12.2 50.2 41.8 73.4 41.4z"></path>
              </svg>
              EMAIL
            </button>
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
        <p>Something went wrong while trying to sign the petition. Please try again later.</p>
      </div>
    );
  }

  /**
   * @returns {jsx} What users see when they initially open the page, above the actual petition form.
   */
  renderStandardHeading() {
    return (
      <div>
        <h2 className="h2-heading">{this.props.ctaHeader}</h2>
        <p dangerouslySetInnerHTML={{__html:this.props.ctaDescription}}></p>
      </div>
    );
  }

  /**
   * Render the submission form, either interactive, with fields
   * marked as not valid yet, or with fields disabled if the
   * user submitted the form data for processing.
   *
   * @returns {jsx} the petition form
   */
  renderSubmissionForm() {
    let disableFields = (this.state.userTriedSubmitting && this.state.apiSubmitted) ? `disabled` : null;

    let inputGroupClass = classNames({
      'has-danger': this.state.userTriedSubmitting && !this.refs.email.value
    });

    let privacyClass = classNames({
      'form-check': true,
      'has-danger': this.state.userTriedSubmitting && !this.refs.privacy.checked
    });

    let checkboxes = this.generateCheckboxes(disableFields);

    return (
      <div className="col petition-form" id="petition-form">
        <form onSubmit={this.processFormData}>
          <div className={inputGroupClass}>
            <div className="mb-2">
              <input disabled={disableFields} type="text" className="form-control mb-1 w-100" placeholder="First name" ref="givenNames" onFocus={this.onInputFocus}/>
              {this.state.userTriedSubmitting && !this.refs.givenNames.value && <small className="form-check form-control-feedback">Please enter your given name(s)</small>}
              <input disabled={disableFields} type="text" className="form-control mb-1 w-100" placeholder="Last name" ref="surname" onFocus={this.onInputFocus}/>
              {this.state.userTriedSubmitting && !this.refs.surname.value && <small className="form-check form-control-feedback">Please enter your surname</small>}
              <input disabled={disableFields} type="email" className="form-control w-100" placeholder="Email address" ref="email" onFocus={this.onInputFocus}/>
              {this.state.userTriedSubmitting && !this.refs.email.value && <small className="form-check form-control-feedback">Please enter your email</small>}
            </div>
            {this.state.basketFailed && <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small>}
          </div>
          <div className={privacyClass}>
            <div>
              <label className="form-check-label mb-2">
                <input disabled={disableFields} type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
                <span className="h6-heading form-text">I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>
                {this.state.userTriedSubmitting && !this.refs.privacy.checked && <small className="has-danger">Please check this box if you want to proceed</small>}
              </label>
            </div>
            <div>
              <label className="form-check-label mb-2">
                <input disabled={disableFields} type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="newsletterSignup" />
                <span className="h6-heading form-text">Yes, I want to receive email updates about Mozilla’s campaigns.</span>
              </label>
            </div>
            { checkboxes.length > 0 ? (<div>{checkboxes}</div>) : null }
            <div>
              <button disabled={disableFields} className="btn btn-normal petition-btn">Add my name</button>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

Petition.defaultProps = {
  ctaDescription: `Add my name`,
  ctaHeader: ``,
  newsletter: `mozilla-foundation`
};
