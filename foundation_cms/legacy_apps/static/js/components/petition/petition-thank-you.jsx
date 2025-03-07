import { Component } from "react";
import DonationModal from "./donation-modal.jsx";
import copyToClipboard from "../../copy-to-clipboard";

/**
 * Thank you screen for FormAssembly petitions
 * This is a simplified version of the original Petition component
 */
class PetitionThankYou extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();

    // Do we have modal data?
    this.modals = false;
    if (this.props.modals) {
      this.modals = this.props.modals;
      try {
        this.modals = JSON.parse(this.modals);
      } catch (e) {
        this.modals = false;
        console.error(`Could not parse modal data from petition markup.`);
      }
    }
  }

  getInitialState() {
    return {
      showDonationModal: true,
    };
  }

  // [FA TODO] set up GA event tracking for form submissions
  setAnalytics() {
    // window.dataLayer = window.dataLayer || [];
    // window.dataLayer.push({
    //   event: "form_submission",
    //   form_name: this.props.ctaName,
    //   form_location: this.props.formLocation,
    //   form_type: "petition-form",
    //   form_id: this.props.petitionId,
    // });
  }

  shareButtonClicked(event, shareProgressButtonId) {
    // ReactGA.event({
    //   category: `petition`,
    //   action: `share tap`,
    //   label: `${document.title} - share tap`,
    // });

    if (shareProgressButtonId) {
      let shareProgressButton = document.querySelector(
        `#${shareProgressButtonId} a`
      );

      if (shareProgressButton) {
        shareProgressButton.click();
      }
    } else {
      // copying current page URL (without query param or hash) to clipboard
      copyToClipboard(
        event.target,
        window.location.href.split("?")[0].split("#")[0]
      );
    }
  }

  userElectedToDonate() {
    this.setState({ showDonationModal: false });
  }

  userElectedToShare() {
    this.setState({ showDonationModal: false });
  }

  /**
   * @returns {jsx} the main render output.
   */
  render() {
    return (
      <div className="">
        <div className="col">
          <div className="row">
            <div className="col-12 petition-content">
              {this.renderThankYou()}
            </div>
          </div>
        </div>
        {this.state.showDonationModal ? this.renderDonationModal() : null}
      </div>
    );
  }

  /**
   * This renders a donation modal on the page as full-page-overlay,
   * provided the petition HTML specifies that as a thing that should happen.
   * @returns {JSX} the donation modal component to render
   */
  renderDonationModal() {
    // This is where can do client-side A/B testing
    let modals = this.modals;

    if (modals.length === 0) {
      return null;
    }

    let modal = modals[0];

    return (
      <DonationModal
        slug={this.props.ctaSlug}
        campaignId={this.props.campaignId}
        name={modal.name}
        heading={modal.header}
        bodyText={modal.body}
        donateText={modal.donate_text}
        donateUrl={modal.donate_url}
        shareText={modal.dismiss_text}
        onDonate={() => this.userElectedToDonate()}
        onShare={() => this.userElectedToShare()}
        onClose={() => this.setState({ showDonationModal: false })}
      />
    );
  }

  /**
   * @returns {jsx} What users see when their petition sign up succeeded.
   */
  renderThankYou() {
    if (this.props.shareLink) {
      return (
        <div>
          <p>{this.props.thankYou}</p>
          <a href={this.props.shareLink} className="tw-btn btn-info">
            {this.props.shareText}
          </a>
        </div>
      );
    } else {
      let facebookBtn = this.props.spFacebook && (
        <button
          className="tw-btn tw-btn-secondary btn-share after:tw-hidden facebook-share"
          onClick={(e) => this.shareButtonClicked(e, `share-progress-fb`)}
        >
          Facebook
        </button>
      );
      let twitterBtn = this.props.spTwitter && (
        <button
          className="tw-btn tw-btn-secondary btn-share after:tw-hidden twitter-share"
          onClick={(e) => this.shareButtonClicked(e, `share-progress-tw`)}
        >
          Twitter
        </button>
      );
      let emailBtn = this.props.spEmail && (
        <button
          className="tw-btn tw-btn-secondary btn-share after:tw-hidden email-share"
          onClick={(e) => this.shareButtonClicked(e, `share-progress-em`)}
        >
          Email
        </button>
      );
      let linkBtn = (
        <button
          className="tw-btn tw-btn-secondary btn-share after:tw-hidden link-share"
          onClick={(e) => this.shareButtonClicked(e)}
          data-success-text="Copied"
        >
          Copy
        </button>
      );

      return (
        <div>
          <p>{this.props.thankYou}</p>
          <div className="share-button-group rectangle stacked">
            <div className="subgroup">
              {facebookBtn}
              {twitterBtn}
            </div>
            <div className="subgroup">
              {emailBtn}
              {linkBtn}
            </div>
          </div>
        </div>
      );
    }
  }
}

export default PetitionThankYou;
