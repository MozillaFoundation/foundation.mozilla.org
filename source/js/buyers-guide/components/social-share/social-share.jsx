import React from "react";
import ReactGA from "../../../react-ga-proxy";
import copyToClipboard from "../../copy-to-clipboard.js";

const SocialShareLink = props => {
  let classes = `social-icon`;
  let srLabel = ``;
  let link = `PrivacyNotIncluded.org`;
  let shareText = `I think this ${
    props.productName
  } is ${props.creepType.toUpperCase()}. What do you think? Check out the Creep-O-Meter over on @mozilla’s ${link} buyer’s guide.`;
  let shareEvent = {
    category: `product`,
    action: `share tap`,
    label: `share vote `,
    transport: `beacon`
  };

  if (props.type === `facebook`) {
    classes += ` social-button-fb`;
    srLabel = `Facebook`;
    shareEvent.label += `to facebook`;
    link = `https://www.facebook.com/sharer/sharer.php?u=https://${link}`;
  }

  if (props.type === `twitter`) {
    classes += ` social-button-twitter`;
    srLabel = `Twitter`;
    shareEvent.label += `to twitter`;
    link = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
      shareText
    )}`;
  }

  if (props.type === `email`) {
    classes += ` social-button-email`;
    srLabel = `Email`;
    shareEvent.label += `via email`;
    link = `mailto:?&body=${encodeURIComponent(shareText)}`;
  }

  if (props.type === `link`) {
    classes += ` social-button-link`;
    srLabel = `Link`;
    shareEvent.label += `using a link`;
    link = `#`;
  }

  let trackShareAction = () => {
    ReactGA.event(shareEvent);
  };

  // We actually need slightly different behaviour
  // for the "copy link" functionality:
  if (props.type === `link`) {
    let _trackShareAction = trackShareAction;

    trackShareAction = evt => {
      evt.preventDefault();
      copyToClipboard(evt.target, window.location.href);
      evt.target.innerHTML = evt.target.innerHTML.replace(srLabel, `Copied`);
      _trackShareAction();
    };
  }

  return (
    <a
      target="_blank"
      className="pni-s-link"
      href={link}
      onClick={trackShareAction}
    >
      <span className={classes} /> {srLabel}
    </a>
  );
};

const SocialShare = props => {
  return (
    <div class="social pni-share-buttons d-flex justify-content-center flex-wrap flex-md-nowrap mt-3">
      <SocialShareLink type="facebook" {...props} />
      <SocialShareLink type="twitter" {...props} />
      <SocialShareLink type="email" {...props} />
      <SocialShareLink type="link" {...props} />
    </div>
  );
};

export default SocialShare;
