import mobileNavStickinessHandler from "./mobile-nav-stickiness-handler";
import commentoSubmissionGaEventHandler from "./comment-submission-ga";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  mobileNavStickinessHandler();
  commentoSubmissionGaEventHandler();
};
