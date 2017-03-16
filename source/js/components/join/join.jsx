import React from 'react';
import classNames from 'classnames';
import basketSignup from '../../basket-signup.js';

export default class JoinUs extends React.Component {
  constructor(props) {
    super(props);

    this.show = this.show.bind(this);
    this.hide = this.hide.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.formSubmissionSuccessful = this.formSubmissionSuccessful.bind(this);
    this.formSubmissionFailure = this.formSubmissionFailure.bind(this);

    this.state = {
      isHidden: typeof this.props.isHidden === `boolean` ? this.props.isHidden : true,
      signupSuccess: false,
      signupFailed: false,
      userSubmitted: false
    };
  }

  show () {
    this.setState({
      isHidden: false
    });
  }

  hide () {
    this.setState({
      isHidden: true
    });
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

    return (
      <div hidden={this.state.isHidden} className="row">
        <div className="col-12">
          <div className="row d-flex justify-content-end">
            <button className="close-button" onClick={this.hide}>X</button>
          </div>
        </div>
        <div className="col-12 hidden-md-up text-center mb-2 mt-4">
          <img width="33%" src={`/_images/burst${this.state.signupSuccess ? `2` : `1`}.svg`}/>
        </div>
        <div className="col-12 my-3">
          <h1 className="h1-white">{!this.state.signupSuccess ? `Stay Connected` : `Thank You`}</h1>
        </div>
        <div className="col-md-6 mb-3">
          {!this.state.signupSuccess ?
          <div className="py-md-4">
            <p className="body-black">Sign up for opportunities and news related to a healthy internet.</p>
            <form onSubmit={this.submitForm}>
              <div className={inputGroupClass}>
                <div className="mb-2">
                  <input type="email" className="form-control" placeholder="EMAIL ADDRESS" ref="email"/>
                </div>
                {this.state.userSubmitted && !this.refs.email.value ? <small className="form-check form-control-feedback">Please enter your email</small> : null }
                {this.state.signupFailed? <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small> : null }
              </div>
              <div className={privacyClass}>
                <label className="form-check-label mb-3">
                  <input type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
                  <span className="small-gray form-text">I'm okay with Mozilla handling my info as explained in this <a href="#TODO">Privacy Notice</a></span>
                  {this.state.userSubmitted && !this.refs.privacy.checked ? <small className="has-danger">Please check this box if you want to proceed</small> : null }
                </label>
                <div>
                  <button className="btn btn-normal">Sign Up</button>
                </div>
              </div>
            </form>
          </div>
          :
          <p className="py-md-5">Thanks for joining. The Internet already feels a bit more vibrant (^_^). We will e-mail you soon to confirm.</p>
          }
        </div>
        <div className="col-md-6 mb-5 text-center hidden-sm-down">
          <img src={`/_images/burst${this.state.signupSuccess ? `2` : `1`}.svg`}/>
        </div>
      </div>
    );
  }
}
