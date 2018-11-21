import React from 'react';
import ReactDOM from 'react-dom';
import ReactGA from 'react-ga';
import DNT from './dnt.js';

const KEY_STATE = `donate modal state`;
const KEY_TIMER = `donate modal timer`;
const DELAY = 10000; // in ms
const TIMER_INCREMENT = 1000; // in ms

class DonateModal extends React.Component {
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
    if (this.props.ga && DNT.allowTracking) {
      ReactGA.event(this.props.ga);
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
              <h1 className="h3-heading">{ this.props.title }</h1>
              <p className="normal">{ this.props.subheading } </p>
            </div>
            <div className="col-md-4 offset-md-2">
              <h2 className="h5-heading">{ this.props.cta.title }</h2>
              <div>{ this.props.cta.body }</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default function injectDonateModal(element, props={}) {
  ReactDOM.render(<DonateModal {...props} />, element);
}
