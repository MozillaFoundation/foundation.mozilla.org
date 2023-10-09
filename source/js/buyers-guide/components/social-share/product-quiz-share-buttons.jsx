import React, { Component } from "react";
import copyToClipboard from "../../../copy-to-clipboard";

const tabletBreakpoint = 768;

class ProductQuizShareButtons extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isMobileOrTablet: window.innerWidth < tabletBreakpoint,
    };
    this.handleResize = this.handleResize.bind(this);
  }

  componentDidMount() {
    window.addEventListener("resize", this.handleResize);
  }

  handleResize(){
    this.setState({
      isMobileOrTablet: window.innerWidth < tabletBreakpoint,
    });
  };

  shareButtonClicked(event, shareProgressButtonId) {
    if (shareProgressButtonId) {
      let shareProgressButton = document.querySelector(
        `#${shareProgressButtonId} a`
      );

      if (shareProgressButton) {
        shareProgressButton.click();
      }
    } else {
      const linkButton = event.target;

      linkButton.classList.add("copied");
      linkButton.title = window.gettext("Copied");
      const spanElements = linkButton.querySelectorAll("span");

      // Iterate through each <span> element and update its inner text
      spanElements.forEach((span) => {
        span.innerText = window.gettext("Copied");
      });
      copyToClipboard(event.target, window.location.href);
    }
  }

  render() {
    const { isMobileOrTablet } = this.state;
    const shareButtonClasses = `tw-btn tw-bg-white tw-border-black hover:tw-bg-black hover:tw-text-white btn-share after:tw-hidden`;

    let facebookBtn = (
      <button
        className={`${shareButtonClasses} facebook-share`}
        onClick={(e) => this.shareButtonClicked(e, `share-progress-fb`)}
      >
        {isMobileOrTablet ? (
          <span className="sr-only">Share on Facebook</span>
        ) : (
          <span>Facebook</span>
        )}
      </button>
    );

    let twitterBtn = (
      <button
        className={`${shareButtonClasses} twitter-share`}
        onClick={(e) => this.shareButtonClicked(e, `share-progress-tw`)}
      >
        {isMobileOrTablet ? (
          <span className="sr-only">Share on Twitter</span>
        ) : (
          <span>Twitter</span>
        )}
      </button>
    );

    let emailBtn = (
      <button
        className={`${shareButtonClasses} email-share`}
        onClick={(e) => this.shareButtonClicked(e, `share-progress-em`)}
      >
        {isMobileOrTablet ? (
          <span className="sr-only">Share by Email</span>
        ) : (
          <span>Email</span>
        )}
      </button>
    );

    let linkBtn = (
      <button
        className={`${shareButtonClasses} link-share`}
        onClick={(e) => this.shareButtonClicked(e)}
      >
        <span className="sr-only medium:tw-hidden">Copy to clipboard</span>
        <span className="tw-hidden medium:tw-block">Copy</span>
      </button>
    );

    return (
      <div
        className={`${
          isMobileOrTablet ? "circle" : "rectangle"
        } share-button-group tw-justify-center`}
      >
        <div className="subgroup">
          {facebookBtn}
          {twitterBtn}
        </div>
        <div className="subgroup">
          {emailBtn}
          {linkBtn}
        </div>
      </div>
    );
  }
}

export default ProductQuizShareButtons;
