import React, { Component } from "react";
import copyToClipboard from "../../../copy-to-clipboard";

class ProductQuizShareButtons extends Component {
  shareButtonClicked(event, shareProgressButtonId) {
    if (shareProgressButtonId) {
      const shareProgressButton = document.querySelector(
        `#${shareProgressButtonId} a`
      );

      if (shareProgressButton) {
        shareProgressButton.click();
      }
    } else {
      // Updating all "copy" buttons (mobile and desktop) to the updated "copied" state.
      const linkButtons = document.querySelectorAll(".link-share");

      linkButtons.forEach((linkButton) => {
        linkButton.classList.add("copied");
        linkButton.title = window.gettext("Copied");
        const spanElement = linkButton.querySelector("span");
        spanElement.innerText = window.gettext("Copied");
      });

      copyToClipboard(event.target, window.location.href);
    }
  }

  render() {
    const shareButtonClasses =
      "tw-btn tw-bg-white tw-h-22 tw-w-22 tw-border-black hover:tw-bg-black hover:tw-text-white btn-share after:tw-hidden";

    const mobileShareButtons = (
      <div className="circle share-button-group tw-justify-center tw-flex medium:tw-hidden">
        <div className="subgroup">
          <button
            className={`${shareButtonClasses} facebook-share`}
            onClick={(e) => this.shareButtonClicked(e, "share-progress-fb")}
          >
            <span className="sr-only">Share on Facebook</span>
          </button>
          <button
            className={`${shareButtonClasses} twitter-share`}
            onClick={(e) => this.shareButtonClicked(e, "share-progress-tw")}
          >
            <span className="sr-only">Share on Twitter</span>
          </button>
        </div>
        <div className="subgroup tw-mr-0">
          <button
            className={`${shareButtonClasses} email-share`}
            onClick={(e) => this.shareButtonClicked(e, "share-progress-em")}
          >
            <span className="sr-only">Share by Email</span>
          </button>
          <button
            className={`${shareButtonClasses} link-share`}
            onClick={(e) => this.shareButtonClicked(e)}
          >
            <span className="sr-only">Copy to clipboard</span>
          </button>
        </div>
      </div>
    );

    const desktopShareButtons = (
      <div className="rectangle share-button-group tw-hidden medium:tw-flex">
        <div className="subgroup">
          <button
            className={`${shareButtonClasses} facebook-share`}
            onClick={(e) => this.shareButtonClicked(e, "share-progress-fb")}
          >
            <span>Facebook</span>
          </button>
          <button
            className={`${shareButtonClasses} twitter-share`}
            onClick={(e) => this.shareButtonClicked(e, "share-progress-tw")}
          >
            <span>Twitter</span>
          </button>
        </div>
        <div className="subgroup">
          <button
            className={`${shareButtonClasses} email-share`}
            onClick={(e) => this.shareButtonClicked(e, "share-progress-em")}
          >
            <span>Email</span>
          </button>
          <button
            className={`${shareButtonClasses} link-share`}
            onClick={(e) => this.shareButtonClicked(e)}
          >
            <span>Copy</span>
          </button>
        </div>
      </div>
    );

    return (
      <div className="share-button-container">
        {mobileShareButtons}
        {desktopShareButtons}
      </div>
    );
  }
}

export default ProductQuizShareButtons;
