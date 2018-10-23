import React from 'react';

const SocialShareLink = (props) => {
  let classes = `social-button`;
  let srLabel = ``;
  let link = `PrivacyNotINcluded.org`;
  let shareText = `I think ${props.productName} is ${props.creepType.toUpperCase()}. What do you think? Check out the Creep-O-Meter over on @mozilla’s ${link} holiday buyer’s guide.`;

  switch (props.type) {
    case 'facebook':
      classes += " social-button-fb";
      srLabel = `Facebook`;
      link = `https://www.facebook.com/sharer/sharer.php?u=https://${link}`;

      break;
    case 'twitter':
      classes += " social-button-twitter";
      srLabel = `Twitter`;
      link = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`;

      break;
    case 'email':
      classes += " social-button-email";
      srLabel = `Email`;
      link = `mailto:?&body=${encodeURIComponent(shareText)}`;

      break;
  }

  return <a className={classes} href={link}><span class="sr-only">{srLabel}</span></a>;
};

const SocialShare = (props) => {
  return <div class="social d-flex justify-content-center mt-3">
    <SocialShareLink type="facebook" {...props} />
    <SocialShareLink type="twitter" {...props} />
    <SocialShareLink type="email" {...props} />
  </div>
};

export default SocialShare;
