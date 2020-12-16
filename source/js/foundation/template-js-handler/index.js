import stickyCtaHandler from "./window/sticky-cta";
import stickyShareButtonGroupHandler from "./window/sticky-share-button-group";

import articleFootLinkHandler from "./article-footnote-link.js";
import homepageHandler from "./homepage";
import internetHealthSeeMoreHandler from "./internet-health-see-more.js";
import loadMoreEntriesHandler from "./load-more-entries.js";
import participatePageDonateHandler from "./participate-page-donate.js";
import pulseProfileCardHandler from "./pulse-profile-card.js";
import pulseProfileListFilterHandler from "./pulse-profile-list-filter.js";

/**
 * Bind global event handlers
 */
export const bindWindowEventHandlers = () => {
  // global handlers for "window"
  stickyCtaHandler();
  stickyShareButtonGroupHandler();
};

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  articleFootLinkHandler();
  homepageHandler();
  internetHealthSeeMoreHandler();
  loadMoreEntriesHandler();
  participatePageDonateHandler();
  pulseProfileCardHandler();
  pulseProfileListFilterHandler();
};
