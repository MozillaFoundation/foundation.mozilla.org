import React from 'react';
import ReactGA from '../../../react-ga-proxy';

const SocialShareLink = (props) => {
  let classes = `social-icon`;
  let srLabel = ``;
  let link = `PrivacyNotIncluded.org`;
  let shareText = `I think this ${props.productName} is ${props.creepType.toUpperCase()}. What do you think? Check out the Creep-O-Meter over on @mozilla’s ${link} buyer’s guide.`;
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
    link = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`;
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
    link = window.location.toString();
  }

  let trackShareAction = () => {
    ReactGA.event(shareEvent);
  };

  return <a target="_blank" className="social-link" href={link} onClick={trackShareAction}><span className={classes}/> {srLabel}</a>;
};

const SocialShare = (props) => {
  return (
    <div class="social social-buttons d-flex justify-content-around flex-wrap flex-md-nowrap mt-3">
       <SocialShareLink type="facebook" {...props} />
       <SocialShareLink type="twitter" {...props} />
       <SocialShareLink type="email" {...props} />
       <SocialShareLink type="link" {...props} />
    </div>
  );
};

export default SocialShare;
