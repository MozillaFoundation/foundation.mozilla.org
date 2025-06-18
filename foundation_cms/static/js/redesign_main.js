import $ from "jquery";
import "foundation-sites";
import { initImpactNumberStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";
import injectNewsletterSignups from "./components/newsletter-signup/newsletter_signup.js";

let foundationSiteURL = window.location.origin;
import { initPortraitCardSetCarousels } from "./blocks/portrait_card_carousel.js";
import { initVideoBlocks } from "./blocks/video_block.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./components/primary_nav";

$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
initImpactNumberStatAnimationsOnScroll();

injectNewsletterSignups(foundationSiteURL);
initPortraitCardSetCarousels();
initVideoBlocks();
initWordmarkVisibilityOnScroll();
