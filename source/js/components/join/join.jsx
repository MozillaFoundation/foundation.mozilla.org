import React from 'react';
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
    event.preventDefault();
    basketSignup({
      lang: `en-US`,
      email: `failure@example.com`,
      country: `United States`
    }, this.formSubmissionSuccessful, this.formSubmissionFailure);
  }

  formSubmissionSuccessful(e) {
    console.log(`success!`);
    console.log(e);
  }
  formSubmissionFailure(e) {
    console.log(`fail`);
    console.log(e);
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
          <form onSubmit={this.submitForm}>
            <input placeholder="Email Address"/>
            <button className="btn btn-normal">Join Us</button>
            <label>
              <input type="checkbox"/><span className="small-gray">&nbsp;I'm okay with Mozilla handling my info as explained in this <a href="#TODO">Privacy Notice</a></span>
            </label>
          </form>
        </div>
      </div>
    );
  }
}
