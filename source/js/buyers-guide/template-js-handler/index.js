import mobileNavStickinessHandler from "./mobile-nav-stickiness-handler";
import productCommentGaEventHandler from "./product-page-comment-handler";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  mobileNavStickinessHandler();
  productCommentGaEventHandler();
};
