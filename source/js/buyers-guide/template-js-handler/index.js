import mobileNavStickinessHandler from "./mobile-nav-stickiness-handler";
import mobileSearchBar from "./mobile-search-bar";
import desktopSearchBar from "./desktop-search-bar";
import diveDeeperListExpansionHandler from "./product-page-dive-deeper-list";
import categoryDropdown from "./pni-category-dropdown";
import productCommentGaEventHandler from "./product-page-comment-handler";
import parallaxBackground from "./parallax-background";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  parallaxBackground();
  mobileNavStickinessHandler();
  mobileSearchBar();
  desktopSearchBar();
  diveDeeperListExpansionHandler();
  categoryDropdown();
  productCommentGaEventHandler();
};
