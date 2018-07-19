import React from 'react';
import classNames from 'classnames';

class DonationModal extends React.Component {

  render() {
    return (
      <div className="modal-underlay">
        <div className="modal show" role="dialog">
          <div className="modal-dialog modal-lg" role="document">
            {this.getModalContent()}
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
          <button className="close" data-dismiss="modal" aria-label="Close" onClick={this.props.onClose}>
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
