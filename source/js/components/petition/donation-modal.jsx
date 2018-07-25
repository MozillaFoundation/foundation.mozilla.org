import React from 'react';
import classNames from 'classnames';

/**
 * Supported event handlers:
 *
 *   - onClose
 *   - onShare
 *   - onDonate
 *
 * Supported plain props:
 *
 *   - ctn, the campaign tracing number
 *   - dmi, the donate modal id
 *   - heading, the modal header
 *   - bodyText, the main text
 *   - donateText, the "donate" button label
 *   - shareText, the "no donate, just share" button label
 */
class DonationModal extends React.Component {

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
  }

  componentWillUnmount() {
    // Make sure to put the dom node back where it belongs
    // before unmounting, so that React doesn't get too confused.
    this.domLocation.appendChild(this.fragment);
  }

  render() {
    return (
      <div ref={e => (this.domLocation = e)}>
        <div className="modal-underlay" ref={e => (this.fragment = e)}>
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
      let query = [
        `ctn=${this.props.ctn}`,
        `dmi=${this.props.dmi}`
      ].join(`&`);

      this.donateURL = `https://donate.mozilla.org/en-US/?${query}`;
    }
    return (
      <div className="modal-content" tabIndex="0">
        <div className="modal-header text-right">
          <button className="close" data-dismiss="modal" aria-label="Close" onClick={e => this.props.onClose(e)}>
            <span aria-hidden="true">&times;</span>
          </button>
        </div>

        <div className="modal-body">
          <h3 className={ classNames(`h3-heading`, `text-center`) }>
            { this.props.heading }
          </h3>
          <p className={ classNames(`body-large`, `text-center`) }>
            {this.props.bodyText}
          </p>
        </div>

        <div className="text-center">
          <a className="btn btn-normal" href={this.donateURL} target="_blank" onClick={e => this.userElectedToDonate(e)}>
            {this.props.donateText}
          </a>
        </div>

        <div className="text-center">
          <button className="text dismiss" data-dismiss="modal" onClick={e => this.userElectedToShare(e)}>
            {this.props.shareText}
          </button>
        </div>
      </div>
    );
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
