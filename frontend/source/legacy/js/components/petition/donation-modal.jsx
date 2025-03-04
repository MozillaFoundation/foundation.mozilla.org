import { Component } from "react";
import classNames from "classnames";

/**
 * Supported event handlers:
 *
 *   - onClose
 *   - onShare
 *   - onDonate
 *
 * Supported plain props:
 *
 *   - slug, the petition slug on foundation.mozilla.org
 *   - campaignId, the petition's salesforce campaign ID.
 *   - name, the donate modal id
 *   - heading, the modal header
 *   - bodyText, the main text
 *   - donateText, the "donate" button label
 *   - donateUrl, the URL the button should link to
 *   - shareText, the "no donate, just share" button label
 */

const MODAL_OVERLAY_CLASS = "tw-fixed tw-inset-0 tw-bg-white/90 tw-z-[1050]";
const MODAL_CLASS =
  "tw-block tw-overflow-scroll [@media(min-width:50rem)]:tw-top-40";
const MODAL_CONTENT_CLASS =
  "tw-border-2 tw-border-black tw-bg-white tw-rounded-none tw-shadow-[4px_4px_0_0_black] tw-px-16 tw-pb-16";
const MODAL_BODY_CLASS = "tw-mt-0 tw-pt-8";
const CLOSE_BUTTON_CLASS =
  "tw-absolute tw-border-none tw-bg-transparent tw-right-0 tw-text-center tw-font-normal tw-text-[2.5rem] tw-leading-none tw-text-black [text-shadow:_0_1px_0_white] tw-py-4 tw-px-8";
const SKIP_DONATE_BUTTON_CLASS =
  "tw-border-none tw-bg-inherit tw-font-sans tw-text-gray-40 tw-underline tw-mt-8";

class DonationModal extends Component {
  componentDidMount() {
    // Thanks to Safari's poor support of the "sticky"
    // CSS position property, we need to relocate the DOM
    // node so that we get the full-viewport effect.
    let body = document.body,
      c1 = body.children[0],
      n = this.fragment;

    if (!c1) {
      body.appendChild(n);
    } else {
      body.insertBefore(n, c1);
    }

    // For some reason appendChild and inserBefore cause event handler binding problems.
    // We cannot use the typical <SomeReactNode onClick=...> to bind event handlers as
    // it will just attach a noop function to it.
    // We have to rely on DOM API instead.
    this.closeButton.addEventListener(`click`, () => {
      this.userElectedCloseModal();
    });

    this.userElectedToDonateLink.addEventListener(`click`, () => {
      this.userElectedToDonate();
    });

    this.userElectedToShareLink.addEventListener(`click`, () => {
      this.userElectedToShare();
    });
  }

  componentWillUnmount() {
    // Make sure to put the dom node back where it belongs
    // before unmounting, so that React doesn't get too confused.
    this.domLocation.appendChild(this.fragment);
  }

  render() {
    return (
      <div ref={(e) => (this.domLocation = e)}>
        <div className={MODAL_OVERLAY_CLASS} ref={(e) => (this.fragment = e)}>
          <div className={classNames(`modal`, MODAL_CLASS)} role="dialog">
            <div className="modal-dialog modal-lg" role="document">
              {this.getModalContent()}
            </div>
          </div>
        </div>
      </div>
    );
  }

  getModalContent() {
    this.donateButtonUrl = this.generateDonateButtonUrl();

    return (
      <div
        className={classNames(`modal-content`, MODAL_CONTENT_CLASS)}
        role="dialog"
      >
        <button
          ref={(e) => (this.closeButton = e)}
          className={CLOSE_BUTTON_CLASS}
          data-dismiss="modal"
          aria-label="Close"
          tabIndex="0"
        >
          <span aria-hidden="true">&times;</span>
        </button>

        <div className={classNames(`modal-body`, MODAL_BODY_CLASS)}>
          <h3 className={classNames(`tw-h2-heading`, `tw-text-center`)}>
            {this.props.heading}
          </h3>
          <div
            className={classNames(
              `tw-rich-text-wrapper`,
              `tw-body-large`,
              `tw-text-center`
            )}
            dangerouslySetInnerHTML={{
              __html: this.props.bodyText,
            }}
          />
        </div>

        <div className="tw-text-center">
          <a
            ref={(e) => (this.userElectedToDonateLink = e)}
            className="tw-btn-primary"
            href={this.donateButtonUrl}
            tabIndex="0"
          >
            {this.props.donateText}
          </a>
        </div>

        <div className="tw-text-center">
          <button
            ref={(e) => (this.userElectedToShareLink = e)}
            className={SKIP_DONATE_BUTTON_CLASS}
            data-dismiss="modal"
            tabIndex="0"
          >
            {this.props.shareText}
          </button>
        </div>
      </div>
    );
  }

  generateDonateButtonUrl() {
    const url = new URL(this.props.donateUrl, window.location.href);

    // Appending campaign ID as URL param for tracking purposes
    const params = new URLSearchParams(url.search);
    params.append("c_id", this.props.campaignId);
    url.search = params.toString();

    const current = new URL(window.location.href);
    const baseUrl = current.origin + current.pathname;

    return url.toString().replace(baseUrl, "");
  }

  userElectedCloseModal() {
    this.props.onClose();
  }

  userElectedToDonate() {
    // Inform the owning component that the user opted to donate
    this.props.onDonate();
  }

  userElectedToShare() {
    // Inform the owning component that the user opted to just
    // share the fact that they did a thing, without donating.
    this.props.onShare();
  }
}

export default DonationModal;
