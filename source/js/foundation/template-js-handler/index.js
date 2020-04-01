import internetHealthSeeMoreHanlder from "./internet-health-see-more.js";
import loadMoreEntriesHandler from "./load-more-entries.js";
import participatePageDonateHandler from "./participate-page-donate.js";
import pulseProfileCardHandler from "./pulse-profile-card.js";
import pulseProfileListFilterHandler from "./pulse-profile-list-filter.js";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  internetHealthSeeMoreHanlder();
  loadMoreEntriesHandler();
  participatePageDonateHandler();
  pulseProfileCardHandler();
  pulseProfileListFilterHandler();
};
