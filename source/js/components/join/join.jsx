import React from 'react';
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
        privacy: this.refs.privacy.checked
      }, this.formSubmissionSuccessful, this.formSubmissionFailure);
    }
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
      'py-3': true,
      'signup-success': this.state.signupSuccess && this.state.userSubmitted,
      'signup-fail': !this.state.signupSuccess && this.state.userSubmitted
    });

    return (
      <div className={signupState}>
        <div className="col text-center mb-2 join-graphic">
          <img src={`/_images/burst${this.state.signupSuccess ? `2` : `1`}.svg`}/>
        </div>
        <div className="col">
          <div className="row">
            <div className="col-12 join-content">
              <div className="my-3 join-page-title">
                <h2 className="h1-white">{!this.state.signupSuccess ? `${this.props.ctaHeader}` : `Thank You`}</h2>
              </div>
              <div className="join-heading">
                <h2 className="h3-black">{!this.state.signupSuccess ? `${this.props.ctaHeader}` : `Thank You`}</h2>
              </div>
              {!this.state.signupSuccess ?
                <p className="body-black" dangerouslySetInnerHTML={{__html:this.props.ctaDescription}}></p>
                : <p>{this.props.thankYouMessage}</p>
              }
            </div>
          { !this.state.signupSuccess ?
          <div className="col join-form">
            <form onSubmit={this.submitForm}>
              <div className={inputGroupClass}>
                <div className="mb-2">
                  <input type="email" className="form-control" placeholder="EMAIL ADDRESS" ref="email"/>
                </div>
                {this.state.userSubmitted && !this.refs.email.value ? <small className="form-check form-control-feedback">Please enter your email</small> : null }
                {this.state.signupFailed? <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small> : null }
              </div>
              <div className={privacyClass}>
                <label className="form-check-label mb-2">
                  <input type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
                  <span className="small-gray form-text">I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>
                  {this.state.userSubmitted && !this.refs.privacy.checked ? <small className="has-danger">Please check this box if you want to proceed</small> : null }
                </label>
                <div>
                  <button className="btn btn-normal join-btn">Sign Up</button>
                </div>
              </div>
            </form>
          </div>
          :
          null
          }
        </div>
        </div>
      </div>
    );
  }
}

JoinUs.defaultProps = {
  ctaDescription: `Sign up for opportunities and news related to a healthy internet.`,
  ctaHeader: `Stay Connected`,
  thankYouMessage: `Thanks for joining. The Internet already feels a bit more vibrant (^_^). We will e-mail you soon to confirm.`
};

