import bindDataWrapperIframeHandler from "./datawrapper-embed.js";
import bindHeaderDonateButtonHandler from "./header-donate-button.js";
import bindFooterDonateButtonHandler from "./footer-donate-button.js";
import stickyCtaHandler from "./sticky-cta";

/**
 * Bind event handlers
 */
export const bindCommonEventHandlers = () => {
  bindDataWrapperIframeHandler();
  bindHeaderDonateButtonHandler();
  bindFooterDonateButtonHandler();
  stickyCtaHandler();
};
