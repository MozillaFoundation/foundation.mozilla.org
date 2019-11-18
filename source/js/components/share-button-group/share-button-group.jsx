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
        <span class="sr-only">{gettext("Share on Facebook")}</span>
      ) : (
        `Facebook`
      );

    let link = this.props.link || ``;

    return (
      <a
        class="btn btn-secondary btn-share facebook-share"
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
        <span class="sr-only">{gettext("Share on Twitter")}</span>
      ) : (
        `Twitter`
      );

    return (
      <a
        class="btn btn-secondary btn-share twitter-share"
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
        <span class="sr-only">{gettext("Share by email")}</span>
      ) : (
        gettext("Email")
      );

    return (
      <a
        class="btn btn-secondary btn-share email-share"
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
      ? gettext("Copied")
      : gettext("Copy page URL to clipboard");
    let label = this.state.linkCopied ? gettext("Copied") : gettext("Copy");
    let labelMini = this.state.linkCopied
      ? gettext("Page link copied")
      : gettext("Copy page link")
    label =
      this.props.version === `mini` ? (
        <span class="sr-only">{labelMini}</span>
      ) : (
        label
      );

    let classes = classNames(`btn btn-secondary btn-share link-share`, {
      copied: this.state.linkCopied
    });

    return (
      <a
        class={classes}
        href="#"
        onClick={event => this.handleLinkButtonClick(event)}
        title={tooltip}
      >
        {label}
      </a>
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
