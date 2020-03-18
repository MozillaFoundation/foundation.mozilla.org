import React from "react";
import classNames from "classnames";
import copyToClipboard from "../../copy-to-clipboard";

export default class ShareButtonGroup extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      linkCopied: false
    };
  }

  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  renderFacebookButton() {
    let label =
      this.props.version === `mini` ? (
        <span className="sr-only">Share on Facebook</span>
      ) : (
        `Facebook`
      );

    let link = this.props.link || ``;

    return (
      <a
        className="btn btn-secondary btn-share facebook-share"
        href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
          link
        )}`}
      >
        {label}
      </a>
    );
  }

  renderTwitterButton() {
    let shareText = this.props.shareText
      ? encodeURIComponent(this.props.shareText)
      : ``;
    let link = this.props.link ? ` ${encodeURIComponent(this.props.link)}` : ``;
    let label =
      this.props.version === `mini` ? (
        <span className="sr-only">Share on Twitter</span>
      ) : (
        `Twitter`
      );

    return (
      <a
        className="btn btn-secondary btn-share twitter-share"
        href={`https://twitter.com/intent/tweet?text=${shareText}${link}`}
      >
        {label}
      </a>
    );
  }

  renderEmailButton() {
    let shareText = this.props.shareText
      ? encodeURIComponent(this.props.shareText)
      : ``;
    let link = this.props.link ? ` ${encodeURIComponent(this.props.link)}` : ``;
    let label =
      this.props.version === `mini` ? (
        <span className="sr-only">Share by email</span>
      ) : (
        `Email`
      );

    return (
      <a
        className="btn btn-secondary btn-share email-share"
        href={`mailto:?&body=${shareText}${link}`}
      >
        {label}
      </a>
    );
  }

  handleLinkButtonClick(event) {
    event.preventDefault();

    copyToClipboard(event.target, window.location.href);
    this.setState({
      linkCopied: true
    });
  }

  renderLinkButton() {
    let tooltip = this.state.linkCopied
      ? `Copied`
      : `Copy page URL to clipboard`;
    let label = this.state.linkCopied ? `Copied` : `Copy`;
    label =
      this.props.version === `mini` ? (
        <span className="sr-only">{label} page link</span>
      ) : (
        label
      );

    let classes = classNames(`btn btn-secondary btn-share link-share`, {
      copied: this.state.linkCopied
    });

    return (
      <button
        className={classes}
        onClick={event => this.handleLinkButtonClick(event)}
        title={tooltip}
      >
        {label}
      </button>
    );
  }

  renderRectangleButtons() {
    let classes = classNames(`share-button-group rectangle`, {
      stacked: this.props.layout === `stacked`
    });

    return (
      <div className={classes}>
        <div className="subgroup">
          {this.renderFacebookButton()}
          {this.renderTwitterButton()}
        </div>
        <div className="subgroup">
          {this.renderEmailButton()}
          {this.renderLinkButton()}
        </div>
      </div>
    );
  }

  renderCircleButtons() {
    let classes = classNames(`share-button-group circle`, {
      stacked: this.props.layout === `stacked`
    });

    return (
      <div className={classes}>
        {this.renderFacebookButton()}
        {this.renderTwitterButton()}
        {this.renderEmailButton()}
        {this.renderLinkButton()}
      </div>
    );
  }

  render() {
    return (
      <React.Fragment>
        {this.props.version === `mini`
          ? this.renderCircleButtons()
          : this.renderRectangleButtons()}
      </React.Fragment>
    );
  }
}
