import React from 'react';
import ReactGA from 'react-ga';
import classNames from 'classnames';
import basketSignup from '../../basket-signup.js';

export default class Petition extends React.Component {
  constructor(props) {
    super(props);
    // Default props defined at end of file

    this.submitForm = this.submitForm.bind(this);
    this.formSubmissionSuccessful = this.formSubmissionSuccessful.bind(this);
    this.formSubmissionFailure = this.formSubmissionFailure.bind(this);

    this.state = {
      signupSuccess: false,
      signupFailed: false,
      userSubmitted: false
    };
  }

  submitForm(event) {
    this.setState({userSubmitted: true});

    event.preventDefault();

    if(this.refs.email.value && this.refs.privacy.checked){
      basketSignup({
        email: this.refs.email.value,
        privacy: this.refs.privacy.checked,
        newsletter: this.props.newsletter
      }, this.formSubmissionSuccessful, this.formSubmissionFailure);
    }

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
    this.setState({signupFailed: true});
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

    return (
      <div className={signupState}>
        <div className="col">
          <div className="row">
            <div className="col-12 join-content">
              {!this.state.signupSuccess ?
                <p className="body-black" dangerouslySetInnerHTML={{__html:this.props.ctaDescription}}></p>
                : <p>{this.props.thankYouMessage}</p>
              }
            </div>
            { !this.state.signupSuccess &&
            <div className="col join-form">
              <form onSubmit={this.submitForm}>
                <div className={inputGroupClass}>
                  <div className="mb-2">
                    <input type="email" className="form-control" placeholder="EMAIL ADDRESS" ref="email" onFocus={this.onInputFocus}/>
                  </div>
                  {this.state.userSubmitted && !this.refs.email.value && <small className="form-check form-control-feedback">Please enter your email</small>}
                  {this.state.signupFailed && <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small>}
                </div>
                <div className={privacyClass}>
                  <label className="form-check-label mb-4">
                    <input type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
                    <span className="small-gray form-text">I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>
                    {this.state.userSubmitted && !this.refs.privacy.checked && <small className="has-danger">Please check this box if you want to proceed</small>}
                  </label>
                  <div>
                    <button className="btn btn-normal join-btn">Take Action</button>
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
