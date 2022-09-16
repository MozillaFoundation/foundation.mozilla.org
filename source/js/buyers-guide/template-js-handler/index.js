import mobileNavStickinessHandler from "./mobile-nav-stickiness-handler";
import mobileSearchBar from "./mobile-search-bar";
import diveDeeperListExpansionHandler from "./dive-deeper";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  mobileNavStickinessHandler();
  mobileSearchBar();
  diveDeeperListExpansionHandler();
};
