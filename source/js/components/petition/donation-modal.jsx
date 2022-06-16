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
 *   - name, the donate modal id
 *   - heading, the modal header
 *   - bodyText, the main text
 *   - donateText, the "donate" button label
 *   - shareText, the "no donate, just share" button label
 */
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
        <div className="modal-underlay" ref={(e) => (this.fragment = e)}>
          <div className="modal show" role="dialog">
            <div className="modal-dialog modal-lg" role="document">
              {this.getModalContent()}
            </div>
          </div>
        </div>
      </div>
    );
  }

  getModalContent() {
    if (!this.donateURL) {
      let base = `https://donate.mozilla.org/?`,
        query = [
          `utm_source=foundation.mozilla.org`,
          `utm_medium=petitionmodal`,
          `utm_campaign=${this.props.slug}`,
          `utm_content=${this.props.name}`,
        ].join(`&`);

      this.donateURL = `${base}${query}`;
    }
    return (
      <div className="modal-content" role="dialog">
        <button
          ref={(e) => (this.closeButton = e)}
          className="close"
          data-dismiss="modal"
          aria-label="Close"
          tabIndex="0"
        >
          <span aria-hidden="true">&times;</span>
        </button>

        <div className="modal-body">
          <h3 className={classNames(`tw-h2-heading`, `text-center`)}>
            {this.props.heading}
          </h3>
          <p className={classNames(`tw-body-large`, `text-center`)}>
            {this.props.bodyText}
          </p>
        </div>

        <div className="text-center">
          <a
            ref={(e) => (this.userElectedToDonateLink = e)}
            className="tw-btn-primary"
            href={this.donateURL}
            target="_blank"
            tabIndex="0"
          >
            {this.props.donateText}
          </a>
        </div>

        <div className="text-center">
          <button
            ref={(e) => (this.userElectedToShareLink = e)}
            className="text dismiss"
            data-dismiss="modal"
            tabIndex="0"
          >
            {this.props.shareText}
          </button>
        </div>
      </div>
    );
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
