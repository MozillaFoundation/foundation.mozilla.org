import Plane from "./plane.js";
import ctaButtonHandler from "./cta-button.js";

/**
 * Bind event handlers to Dear Internet page specific elements
 */
export const bindEventHandlers = () => {
  new Plane();
  ctaButtonHandler();
};
