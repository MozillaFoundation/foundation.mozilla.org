import bindHeaderDonateButtonHanlder from "./header-donate-button.js"
import bindFooterDonateButtonHandler from "./footer-donate-button.js";

/**
 * Bind event handlers
 */
export const bindCommonEventHandlers = () => {
  bindHeaderDonateButtonHanlder();
  bindFooterDonateButtonHandler();
};
