import mobileNavStickinessHandler from "./mobile-nav-stickiness-handler";
import mobileSearchBar from "./mobile-search-bar";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  mobileNavStickinessHandler();
  mobileSearchBar();
};
