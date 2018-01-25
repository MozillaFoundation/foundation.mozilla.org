import React from 'react';
import ReactGA from 'react-ga';
import classNames from 'classnames';
import basketSignup from '../../basket-signup.js';

export default class Petition extends React.Component {
  constructor(props) {
    super(props);
    // Default props defined at end of file

    this.submitDataToApi = this.submitDataToApi.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.formSubmissionSuccessful = this.formSubmissionSuccessful.bind(this);
    this.formSubmissionFailure = this.formSubmissionFailure.bind(this);

    this.state = {
      signupSuccess: false,
      signupFailed: false,
      userSubmitted: false
    };

    // there may be up to four checkboxes per petition
    this.checkbox1 = this.props.checkbox1;
    this.checkbox2 = this.props.checkbox2;
  }

  submitDataToApi() {
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

  submitForm(event) {
    this.setState({userSubmitted: true});

    event.preventDefault();

    let basketSignupPromise = new Promise((resolve, reject) => {
      if(this.refs.email.value && this.refs.privacy.checked && this.refs.newsletterSignup.checked){
        basketSignup({
          email: this.refs.email.value,
          privacy: this.refs.privacy.checked,
          newsletter: this.props.newsletter
        }, resolve, reject);
      } else {
        reject();
      }
    });

    Promise.all([this.submitDataToApi, basketSignupPromise])
      .then(this.formSubmissionSuccessful)
      .catch(this.formSubmissionFailure);

    ReactGA.event({
      category: `signup`,
      action: `form submit tap`,
      label: `Signup form submitted`
    });
  }

  onInputFocus() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`
    });
  }

  formSubmissionSuccessful() {
    this.setState({signupSuccess: true});
  }

  formSubmissionFailure(e) {
    console.error(e);
    if(e instanceof Error) {
      this.setState({signupFailed: true});
    }
  }

  render() {
    let inputGroupClass = classNames({
      'has-danger': !this.state.signupSuccess && this.state.userSubmitted && !this.refs.email.value || this.state.signupFailed
    });

    let privacyClass = classNames({
      'form-check': true,
      'has-danger': !this.state.signupSuccess && this.state.userSubmitted && !this.refs.privacy.checked
    });

    let signupState = classNames({
      'row': true,
      'signup-success': this.state.signupSuccess && this.state.userSubmitted,
      'signup-fail': !this.state.signupSuccess && this.state.userSubmitted
    });

    let checkboxes = [];
    let generateCheckbox = (s, ref) => <label key={s}><input type="checkbox" ref={ref} /> <span dangerouslySetInnerHTML={{__html: s}}/></label>;

    if(this.checkbox1) {
      checkboxes.push(generateCheckbox(this.checkbox1, "checkbox1"));
    }
    if(this.checkbox2) {
      checkboxes.push(generateCheckbox(this.checkbox2, "checkbox2"));
    }

    return (
      <div className={signupState}>
        <div className="col">
          <div className="row">
            <div className="col-12 petition-content">
              {!this.state.signupSuccess ?
                <p className="body-black" dangerouslySetInnerHTML={{__html:this.props.ctaDescription}}></p>
                : <p>{this.props.thankYouMessage}</p>
              }
            </div>
            { !this.state.signupSuccess &&
            <div className="col petition-form">
              <form onSubmit={this.submitForm}>
                <div className={inputGroupClass}>
                  <div className="mb-2">
                    <input type="text" className="form-control" placeholder="Given Name(s)" ref="givenNames" onFocus={this.onInputFocus}/>
                    {this.state.userSubmitted && !this.refs.givenNames.value && <small className="form-check form-control-feedback">Please enter your given name(s)</small>}
                    <input type="text" className="form-control" placeholder="Surname" ref="surname" onFocus={this.onInputFocus}/>
                    {this.state.userSubmitted && !this.refs.surname.value && <small className="form-check form-control-feedback">Please enter your surname</small>}
                    <input type="email" className="form-control" placeholder="EMAIL ADDRESS" ref="email" onFocus={this.onInputFocus}/>
                    {this.state.userSubmitted && !this.refs.email.value && <small className="form-check form-control-feedback">Please enter your email</small>}
                  </div>
                  {this.state.signupFailed && <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small>}
                </div>
                { checkboxes.length > 0 ? (<div>{checkboxes}</div>) : null }
                <div className={privacyClass}>
                  <label className="form-check-label mb-4">
                    <input type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="newsletterSignup" />
                    <span className="small-gray form-text">Yes, I want to receive email updates about Mozilla’s campaigns.</span>
                  </label>
                  <label className="form-check-label mb-4">
                    <input type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
                    <span className="small-gray form-text">I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>
                    {this.state.userSubmitted && !this.refs.privacy.checked && <small className="has-danger">Please check this box if you want to proceed</small>}
                  </label>
                  <div>
                    <button className="btn btn-normal petition-btn">Sign Up</button>
                  </div>
                </div>
              </form>
            </div>
            }
          </div>
        </div>
      </div>
    );
  }
}

Petition.defaultProps = {
  ctaDescription: `Sign the petition to do a thing`,
  ctaHeader: `Sign the Petition!`,
  thankYouMessage: `You're a great human being.`,
  newsletter: `mozilla-leadership-network`
};
