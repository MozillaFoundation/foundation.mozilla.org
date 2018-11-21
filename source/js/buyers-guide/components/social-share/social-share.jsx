import React from 'react';
import ReactGA from '../../react-ga-proxy';

const SocialShareLink = (props) => {
  let classes = `social-button`;
  let srLabel = ``;
  let link = `privacynotincluded.org`;
  let shareText = `I think ${props.productName} is ${props.creepType.toUpperCase()}. What do you think? Check out the Creep-O-Meter over on @mozilla’s ${link} holiday buyer’s guide.`;
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

  let trackShareAction = () => {
    ReactGA.event(shareEvent);
  };

  return <a target="_blank" className={classes} href={link} onClick={trackShareAction}><span class="sr-only">{srLabel}</span></a>;
};

const SocialShare = (props) => {
  return (
    <div class="social d-flex justify-content-center mt-3">
      <SocialShareLink type="facebook" {...props} />
      <SocialShareLink type="twitter" {...props} />
      <SocialShareLink type="email" {...props} />
    </div>
  );
};

export default SocialShare;
