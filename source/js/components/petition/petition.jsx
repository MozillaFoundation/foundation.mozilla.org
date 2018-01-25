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

    this.state = this.getInitialState();

    // There may be up to four checkboxes per petition, but
    // the first two are hardcoded in the render() pipeline.
    this.checkbox1 = this.props.checkbox1;
    this.checkbox2 = this.props.checkbox2;
  }

  // helper function for initial component state
  getInitialState() {
    return {
      apiSubmitted: true,
      apiSuccess: true,
      apiFailed: false,
      basketSubmitted: true,
      basketSuccess: false,
      basketFailed: true,
      userTriedSubmitting: false
    }
  }

  // helper function to set up GA input events
  onInputFocus() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`
    });
  }

  // helper function for auto-generating checkboxes off of the passed props.
  generateCheckboxes(disabled) {
    return ['checkbox1', 'checkbox2'].map(name => {
      let label = this[name];
      if (!label) return null;
      return (
        <div key={name}>
          <label>
            <input disabled={disabled} type="checkbox" ref={name} /> <span dangerouslySetInnerHTML={{__html: label}}/>
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
    return this.state.apiSubmitted && (this.state.apiSuccess || this.state.apiFailed);
  }

  // state check function
  submissionsAreDone() {
    return this.apiIsDone() && this.basketIsDone();
  }

  /**
   * submit the user's data to the API server.
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
        checkbox_1: this.props.checkbox1 ? !!(this.refs.checkbox1.checked) : null,
        checkbox_2: this.props.checkbox2 ? !!(this.refs.checkbox2.checked) : null,
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

      xhr.open("POST", this.props.apiUrl, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.setRequestHeader("X-Requested-With","XMLHttpRequest");
      xhr.timeout = 5000;
      xhr.ontimeout = reject;

      xhr.send(JSON.stringify(payload));
    });
  }

  /**
   * sign the user up for the mozilla newsletter.
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
            .catch(this.basketSubmissionFailure)
        })
        .catch(this.apiSubmissionFailure)
    }

    ReactGA.event({
      category: `signup`,
      action: `form submit tap`,
      label: `Signup form submitted`
    });
  }

  /**
   * master render entry point - this will branch out
   * to different render functions depending on the
   * state of the user's data and xhr call results.
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
      petitionContent = <p>{this.props.thankYouMessage}</p>;
    } else if (unrecoverableError) {
      petitionContent = <p>Something went wrong while trying to sign the petition. Please try again later and we'll get this fixed ASAP</p>;
    } else {
      petitionContent = <p className="body-black" dangerouslySetInnerHTML={{__html:this.props.ctaDescription}}></p>;
      formContent = !unrecoverableError && !this.state.basketSuccess && this.renderSubmissionForm(signingIsDone);
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
   * Render the submission form, either interactive, with fields
   * marked as not valid yet, or with fields disabled if the
   * user submitted the form data for processing.
   */
  renderSubmissionForm(signingIsDone) {
    let disableFields = (this.state.userTriedSubmitting && this.state.apiSubmitted) ? "disabled" : null;

    let inputGroupClass = classNames({
      'has-danger': !signingIsDone && this.state.userTriedSubmitting && !this.refs.email.value
    });

    let privacyClass = classNames({
      'form-check': true,
      'has-danger': !signingIsDone && this.state.userTriedSubmitting && !this.refs.privacy.checked
    });

    let checkboxes = this.generateCheckboxes(disableFields);

    return (
      <div className="col petition-form">
        <form onSubmit={this.processFormData}>
          <div className={inputGroupClass}>
            <div className="mb-2">
              <input disabled={disableFields} type="text" className="form-control" placeholder="Given Name(s)" ref="givenNames" onFocus={this.onInputFocus}/>
              {this.state.userTriedSubmitting && !this.refs.givenNames.value && <small className="form-check form-control-feedback">Please enter your given name(s)</small>}
              <input disabled={disableFields} type="text" className="form-control" placeholder="Surname" ref="surname" onFocus={this.onInputFocus}/>
              {this.state.userTriedSubmitting && !this.refs.surname.value && <small className="form-check form-control-feedback">Please enter your surname</small>}
              <input disabled={disableFields} type="email" className="form-control" placeholder="EMAIL ADDRESS" ref="email" onFocus={this.onInputFocus}/>
              {this.state.userTriedSubmitting && !this.refs.email.value && <small className="form-check form-control-feedback">Please enter your email</small>}
            </div>
            {this.state.basketFailed && <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small>}
          </div>
          { checkboxes.length > 0 ? (<div>{checkboxes}</div>) : null }
          <div className={privacyClass}>
            <label className="form-check-label mb-4">
              <input disabled={disableFields} type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="newsletterSignup" />
              <span className="small-gray form-text">Yes, I want to receive email updates about Mozilla’s campaigns.</span>
            </label>
            <label className="form-check-label mb-4">
              <input disabled={disableFields} type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
              <span className="small-gray form-text">I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>
              {this.state.userTriedSubmitting && !this.refs.privacy.checked && <small className="has-danger">Please check this box if you want to proceed</small>}
            </label>
            <div>
              <button disabled={disableFields} className="btn btn-normal petition-btn">Sign Up</button>
            </div>
          </div>
        </form>
      </div>
    )
  }
}

Petition.defaultProps = {
  ctaDescription: `Sign the petition to do a thing`,
  ctaHeader: `Sign the Petition!`,
  thankYouMessage: `You're a great human being.`,
  newsletter: `mozilla-leadership-network`
};
