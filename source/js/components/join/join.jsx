import React from 'react';
import ReactGA from 'react-ga';
import classNames from 'classnames';
import basketSignup from '../../basket-signup.js';

export default class JoinUs extends React.Component {
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
      'row py-5': true,
      'signup-success': this.state.signupSuccess && this.state.userSubmitted,
      'signup-fail': !this.state.signupSuccess && this.state.userSubmitted
    });

    return (
      <div className={ `container ${signupState}` }>
        <div className="col join-main-content">
          <div className="row">
            <div className="col-12 col-md-6 d-flex justify-content-center flex-column join-content">
              <div className="mb-5 join-page-title">
                <h2 className="h1-white">{!this.state.signupSuccess ? `${this.props.ctaHeader}` : `Thanks!`}</h2>
              </div>
              <div className="join-heading">
                { this.state.signupSuccess && <h3 className="h3-black">Thanks!</h3> }
              </div>
              {!this.state.signupSuccess ?
                <p className="lead-black" dangerouslySetInnerHTML={{__html:this.props.ctaDescription}}></p>
                : <p dangerouslySetInnerHTML={{__html:this.props.thankYouMessage}}></p>
              }
            </div>
            { !this.state.signupSuccess &&
            <div className="col-12 col-md-6 join-form">
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
                    <span className="form-text">I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>
                    {this.state.userSubmitted && !this.refs.privacy.checked && <small className="has-danger">Please check this box if you want to proceed</small>}
                  </label>
                  <div>
                    <button className="btn btn-normal join-btn">Sign Up</button>
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

JoinUs.defaultProps = {
  ctaDescription: `Sign up for opportunities and news related to a healthy internet.`,
  ctaHeader: `Get Connected`,
  thankYouMessage: `Please check your inbox to confirm your subscription.<br/><br/>If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. Please check your inbox or your spam filter for an email from us.`,
  newsletter: `mozilla-foundation`
};
