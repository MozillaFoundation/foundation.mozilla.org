import $ from "jquery";
import "foundation-sites";
import { initImpactNumberStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";
import { initAllHorizontalAccordions } from "./blocks/hero_accordion.js";
import injectNewsletterSignups from "./components/newsletter-signup/newsletter_signup.js";
import { initPortraitCardSetCarousels } from "./blocks/portrait_card_carousel.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./components/primary_nav";
import { initSpotlightCardCarousels } from "./blocks/spotlight_card_carousel.js";

let foundationSiteURL = window.location.origin;

$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
initImpactNumberStatAnimationsOnScroll();
initAllHorizontalAccordions();
injectNewsletterSignups(foundationSiteURL);
initPortraitCardSetCarousels();
initWordmarkVisibilityOnScroll();
initSpotlightCardCarousels();
