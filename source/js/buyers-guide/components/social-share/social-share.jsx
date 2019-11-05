import React from "react";
import ReactGA from "../../../react-ga-proxy";
import copyToClipboard from "../../../../js/copy-to-clipboard.js";

const SocialShareLink = props => {
  let classes = ``;
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
    classes += `facebook-share`;
    srLabel = `Facebook`;
    shareEvent.label += `to facebook`;
    link = `https://www.facebook.com/sharer/sharer.php?u=https://${link}`;
  }

  if (props.type === `twitter`) {
    classes += `twitter-share`;
    srLabel = `Twitter`;
    shareEvent.label += `to twitter`;
    link = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
      shareText
    )}`;
  }

  if (props.type === `email`) {
    classes += `email-share`;
    srLabel = `Email`;
    shareEvent.label += `via email`;
    link = `mailto:?&body=${encodeURIComponent(shareText)}`;
  }

  if (props.type === `link`) {
    classes += `link-share`;
    srLabel = `Copy`;
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
      evt.target.classList.add("copied");
      _trackShareAction();
    };
  }

  return (
    <a
      target="_blank"
      className={`btn btn-secondary btn-share ${classes}`}
      href={link}
      onClick={trackShareAction}
    >
      {srLabel}
    </a>
  );
};

const SocialShare = props => {
  return (
    <div className="row">
      <div className="col-xl-10 m-auto px-2 px-sm-3">
        <div className="share-button-group rectangle flex-lg-nowrap">
          <div className="subgroup">
            <SocialShareLink type="facebook" {...props} />
            <SocialShareLink type="twitter" {...props} />
          </div>
          <div className="subgroup">
            <SocialShareLink type="email" {...props} />
            <SocialShareLink type="link" {...props} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SocialShare;
