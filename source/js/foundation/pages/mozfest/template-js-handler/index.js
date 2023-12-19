import homepageBannerHandler from "./home-banner.js";
import primaryButtonHandler from "./primary-button.js";
import footerSocialButtonHandler from "./footer-social-button.js";
import videoHandler from "./video.js";

/**
 * Bind event handlers to MozFest specific elements
 */
export const bindEventHandlers = () => {
  footerSocialButtonHandler();
  homepageBannerHandler();
  primaryButtonHandler();
  videoHandler();
};
