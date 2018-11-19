import React from 'react';
import ReactGA from 'react-ga';
import DNT from '../../dnt.js';

const KEY_STATE = `donate modal state`;
const KEY_TIMER = `donate modal timer`;
const DELAY = 10000; // in ms
const TIMER_INCREMENT = 1000; // in ms

export default class DonateModal extends React.Component {
  constructor(props) {
    super(props);

    let dismissed = !!sessionStorage.getItem(KEY_STATE) || false;
    let prevTimer = this.getPrevTimer();

    this.state = {
      delay: DELAY - prevTimer,
      visible: false,
      dismissed
    };
    this.timer = prevTimer;
    this.runTimer;
  }

  getPrevTimer() {
    let prevTimer = parseInt(sessionStorage.getItem(KEY_TIMER), 10);

    if (isNaN(prevTimer)) {
      prevTimer = 0;
    }

    return prevTimer;
  }

  componentDidMount() {
    if (!this.state.dismissed) {
      this.startTimer();

      // show modal after delay. If delay is a negative value, show modal immediately
      setTimeout(() => this.setState({ visible: true }), Math.max(this.state.delay, 0));
    }
  }

  startTimer() {
    this.runTimer = setInterval(() => {
      this.timer += TIMER_INCREMENT;

      sessionStorage.setItem(KEY_TIMER, this.timer);
    }, TIMER_INCREMENT);
  }

  handleBtnClick() {
    if (DNT.allowTracking) {
      let url = window.location.pathname.replace(/\w\w(-\W\W)?\/privacynotincluded\//,``);

      ReactGA.event({
        category: `buyersguide`,
        action: `donate tap`,
        label: `donate popup on ${url}`
      });
    }

    this.dismiss();
  }

  dismiss() {
    sessionStorage.setItem(KEY_STATE, `dismissed`);
    sessionStorage.removeItem(KEY_TIMER);

    this.setState({
      dismissed: true
    }, () => {
      clearInterval(this.runTimer);
    });
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
              <p className="normal">Our supporters told us they are uncertain about how to be safer online. We listened. This guide is a result.</p>
            </div>
            <div className="col-md-4 offset-md-2">
              <h2 className="h5-heading">Help us keep this work going</h2>
              <div>
                <a className="d-block d-md-inline-block text-center btn btn-donate ml-0" target="_blank" onClick={evt => this.handleBtnClick(evt)} href="https://donate.mozilla.org/?utm_source=foundation.mozilla.org&utm_medium=buyersguide&utm_campaign=buyersguide2018&utm_content=popupbutton">Support Mozilla</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
