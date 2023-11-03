import React, { Component } from "react";
import copyToClipboard from "../../../copy-to-clipboard";

class ProductQuizShareButtons extends Component {
  constructor(props) {
    super(props);
    this.shareButtonClasses =
      "tw-btn tw-bg-white tw-h-22 tw-w-22 tw-border-black hover:tw-bg-black hover:tw-text-white active:tw-bg-black active:tw-text-white focus:tw-bg-black focus:tw-text-white btn-share after:tw-hidden";
  }

  renderFacebookButton(child) {
    return (
      <button
        className={`${this.shareButtonClasses} facebook-share`}
        onClick={(e) => this.shareButtonClicked(e, "share-progress-fb")}
      >
        {child}
      </button>
    );
  }

  renderTwitterButton(child) {
    return (
      <button
        className={`${this.shareButtonClasses} twitter-share`}
        onClick={(e) => this.shareButtonClicked(e, "share-progress-tw")}
      >
        {child}
      </button>
    );
  }

  renderEmailButton(child) {
    return (
      <button
        className={`${this.shareButtonClasses} email-share`}
        onClick={(e) => this.shareButtonClicked(e, "share-progress-em")}
      >
        {child}
      </button>
    );
  }

  renderCopyLinkButton(child) {
    return (
      <button
        className={`${this.shareButtonClasses} link-share`}
        onClick={(e) => this.shareButtonClicked(e)}
      >
        {child}
      </button>
    );
  }

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
    const mobileShareButtons = (
      <div className="circle share-button-group tw-justify-center tw-flex medium:tw-hidden">
        <div className="subgroup">
          {this.renderFacebookButton(
            <span className="sr-only">Share on Facebook</span>
          )}
          {this.renderTwitterButton(
            <span className="sr-only">Share on Twitter</span>
          )}
        </div>
        <div className="subgroup tw-mr-0">
          {this.renderEmailButton(
            <span className="sr-only">Share by Email</span>
          )}
          {this.renderCopyLinkButton(
            <span className="sr-only">Copy to clipboard</span>
          )}
        </div>
      </div>
    );

    const desktopShareButtons = (
      <div className="rectangle share-button-group tw-hidden medium:tw-flex">
        <div className="subgroup">
          {this.renderFacebookButton(<span>Facebook</span>)}
          {this.renderTwitterButton(<span>Twitter</span>)}
        </div>
        <div className="subgroup">
          {this.renderEmailButton(<span>Email</span>)}
          {this.renderCopyLinkButton(<span>Copy</span>)}
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
