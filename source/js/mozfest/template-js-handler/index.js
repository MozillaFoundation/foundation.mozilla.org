import homepageBannerHandler from "./home-banner.js";
import primaryButtonHandler from "./primary-button.js";
import footerSocialButtonHandler from "./footer-social-button.js";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  footerSocialButtonHandler();
  homepageBannerHandler();
  primaryButtonHandler();
};
