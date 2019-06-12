import React from "react";
import ReactDOM from "react-dom";
import ReactGA from "../react-ga-proxy.js";

const DISMISSED_CHECK_KEY = "fundraising-banner";
const MILLISECONDS = 1000;
const DAY = 24 * 3600 * MILLISECONDS;
const localStorage = typeof window === "undefined" ? {} : window.localStorage;

class DonateModal extends React.Component {
  constructor(props) {
    super(props);

    const INITIAL_DELAY_IN_MILLISECONDS = parseInt(this.props.delay) || 10 * MILLISECONDS; // 10 seconds, in ms
    const DISMISSAL_DELAY_IN_DAYS = parseInt(this.props.hideFor) || 7; // one week, in days

    // Don't treat the modal as dismissed if:
    // 1. the user never dismissed it before, or
    // 2. it's been longer than a week since they dismissed
    let dismissed = false;
    let lastLoad = localStorage[DISMISSED_CHECK_KEY];
    if (lastLoad) {
      var diff = (Date.now() - parseInt(lastLoad, 10)) / DAY;
      if (diff < DISMISSAL_DELAY_IN_DAYS) {
        dismissed = true;
      }
    }

    this.state = {
      delay: INITIAL_DELAY_IN_MILLISECONDS,
      visible: false,
      dismissed
    };
  }

  componentDidMount() {
    if (!this.state.dismissed) {
      // show modal after delay. If delay is a negative value, show modal immediately
      this.runTimer = setTimeout(
        () => this.setState({ visible: true }),
        this.state.delay
      );
    }
  }

  handleBtnClick() {
    if (this.props.ga) {
      ReactGA.event(this.props.ga);
    }

    this.dismiss();
  }

  dismiss() {
    clearInterval(this.runTimer);
    localStorage[DISMISSED_CHECK_KEY] = Date.now();
    this.setState({ dismissed: true });
  }

  render() {
    if (this.state.dismissed) {
      return null;
    }

    let title = this.props.title,
      subheading = this.props.subheading,
      cta = this.props.cta,
      utm = this.props.utm;

    return (
      <div className={`donate-modal ${this.state.visible ? `show` : ``}`}>
        <button className="close" onClick={() => this.dismiss()}>
          <span class="sr-only">Close donate modal</span>
        </button>
        <div className="container">
          <div className="row align-items-center text-center text-md-left">
            <div className="col-md-6">
              <h1 className="h2-heading">{title}</h1>
              <p>{subheading} </p>
            </div>
            <div className="col-md-4 offset-md-2">
              <h2 className="h5-heading">{cta.title}</h2>
              <div>
                <a
                  className="d-block d-md-inline-block text-center btn btn-donate ml-0"
                  onClick={evt => this.handleBtnClick(evt)}
                  href={`https://donate.mozilla.org/?utm_source=foundation.mozilla.org&utm_medium=${
                    utm.medium
                  }&utm_campaign=${utm.campaign}&utm_content=${utm.content}`}
                  target="_blank"
                >
                  {cta.text}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// Export a manual injection function.

export default function injectDonateModal(element, props = {}) {
  ReactDOM.render(<DonateModal {...props} />, element);
}
