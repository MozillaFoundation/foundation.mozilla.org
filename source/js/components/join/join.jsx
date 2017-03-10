import React from 'react';
import classNames from 'classNames';
import basketSignup from '../../basket-signup.js';

export default class JoinUs extends React.Component {
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

  constructor(props) {
    super(props);

    this.show = this.show.bind(this);
    this.hide = this.hide.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.formSubmissionSuccessful = this.formSubmissionSuccessful.bind(this);
    this.formSubmissionFailure = this.formSubmissionFailure.bind(this);

    this.state = {
      isHidden: typeof this.props.isHidden === `boolean` ? this.props.isHidden : true
    };
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
      <div hidden={this.state.isHidden} className="row p-4">
        <div className="col-12">
          <div className="row d-flex justify-content-end">
            <button className="close-button" onClick={this.hide}>X</button>
          </div>
        </div>
        <div className="col-6">
          <h3 className="h3-cta-black">Join Our Ranks</h3>
          <p className="body-black">Access to bright minds, passionate community, and invaluable resources.</p>
        </div>
        <div className="col-6">
          {!this.state.signupSuccess ?
          <form onSubmit={this.submitForm}>
            <div className={inputGroupClass}>
              <div className="input-group">
                <input type="email" className="form-control" placeholder="Email Address" ref="email"/>
                <span className="input-group-btn">
                  <button className="btn btn-normal">Join Us</button>
                </span>
              </div>
              {this.state.userSubmitted && !this.refs.email.value ? <small className="form-check form-control-feedback">Please enter your email</small> : null }
              {this.state.signupFailed? <small className="form-check form-control-feedback">Something went wrong. Please check your email address and try again</small> : null }
            </div>
            <div className={privacyClass}>
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="PrivacyCheckbox" ref="privacy" />
                <span className="small-gray form-text">&nbsp;I'm okay with Mozilla handling my info as explained in this <a href="#TODO">Privacy Notice</a></span>
                {this.state.userSubmitted && !this.refs.privacy.checked ? <small className="has-danger">Please check this box if you want to proceed</small> : null }
              </label>
            </div>
          </form>
          : `Thank you!`}
        </div>
      </div>
    );
  }
}
