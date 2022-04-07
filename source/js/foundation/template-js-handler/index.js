import stickyCtaHandler from "./window/sticky-cta";
import shareButtonGroupHandler from "./share-button-group.js";
import stickyShareButtonGroupHandler from "./window/sticky-share-button-group";
import articleFootLinkHandler from "./article-footnote-link.js";
import audioBlockHandler from "./audio-player-handler";
import homepageHandler from "./homepage";
import loadMoreEntriesHandler from "./load-more-entries.js";
import loopingVideoHandler from "./looping-video-handler.js";
import participatePageDonateHandler from "./participate-page-donate.js";
import publicationSummaryBar from "./publication-summary-bar.js";
import continuousScrollingBox from "./continuous-scrolling-box.js";
import pulseProfileCardHandler from "./pulse-profile-card.js";
import pulseProfileListFilterHandler from "./pulse-profile-list-filter.js";
import articleHeroVideoHandler from "./article-hero-video-handler.js";
import blogHeroVideoHandler from "./blog-hero-video-handler.js";
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
  articleHeroVideoHandler();
  audioBlockHandler();
  homepageHandler();
  loadMoreEntriesHandler();
  loopingVideoHandler();
  participatePageDonateHandler();
  publicationSummaryBar();
  pulseProfileCardHandler();
  pulseProfileListFilterHandler();
  shareButtonGroupHandler();
  blogHeroVideoHandler();
  continuousScrollingBox();
};
