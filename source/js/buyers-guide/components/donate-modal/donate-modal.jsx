import React from 'react';
import ReactGA from 'react-ga';
import DNT from '../../dnt.js';


export default class DonateModal extends React.Component {
  constructor(props) {
    super(props);
    let dismissed = !!sessionStorage.getItem(`dismissed`) || false;

    this.state = {
      delay: this.props.delay || 100,
      visible: false,
      dismissed
    };
  }

  componentDidMount() {
    if (this.state.dismissed) {
      this.props.onDismiss();
    }
    setTimeout(() => this.setState({ visible: true }), this.state.delay);
  }

  dismiss() {
    console.log(`close button clicked`);
    // sessionStorage.setItem(`dismissed`, `dismissed`);
    // this.setState({
    //   dismissed: true
    // });
  }

  trackDonation() {
    if (DNT.allowTracking) {
      ReactGA.event({
        category: `site`,
        action: `donate tap`,
        label: `donate popup`
      });
    }
  }

  render() {
    if (this.state.dismissed) {
      return null;
    }

    return (
      <div className={`donate-modal ${this.state.visible ? `show` : ``}`}>
        <button className="close" onClick={() => this.dismiss()}>
          <span class="sr-only">Close donate modal</span>
        </button>
        <div className="container">
          <div className="row align-items-center text-center text-md-left">
            <div className="col-md-6">
              <h1 className="h3-heading">We made this guide with support from people like you</h1>
              <p>Our supporters told us they are uncertain about how to be safer online. We listened. This guide is a result.</p>
            </div>
            <div className="col-md-4 offset-md-2">
              <h2 className="h5-heading">Help us keep this work going</h2>
              <div>
                <a className="d-block d-md-inline-block text-center btn btn-donate ml-0" target="_blank" onClick={evt => this.trackDonation(evt)} href="https://donate.mozilla.org?utm_source=pni">Support Mozilla</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
