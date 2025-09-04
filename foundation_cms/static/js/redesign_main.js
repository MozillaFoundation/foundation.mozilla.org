import $ from "jquery";
import "foundation-sites";
import { initImpactNumberStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";
import { initAllHorizontalAccordions } from "./blocks/hero_accordion.js";
import injectNewsletterSignups from "./components/newsletter_signup/newsletter_signup.js";
import { initPortraitCardSetCarousels } from "./blocks/portrait_card_carousel.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./components/primary_nav";
import { initDonateBanner } from "./components/donate_banner.js";
import { initSpotlightCardCarousels } from "./blocks/spotlight_card_carousel.js";
import { initPillarCardLinks } from "./blocks/pillar_card_set.js";
import { initTabbedContent } from "./blocks/tabbed_content_container.js";
import initShareContainer from "./components/share_container.js"

let foundationSiteURL = window.location.origin;

$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
initDonateBanner();
initImpactNumberStatAnimationsOnScroll();
initAllHorizontalAccordions();
injectNewsletterSignups(foundationSiteURL);
initPortraitCardSetCarousels();
initWordmarkVisibilityOnScroll();
initSpotlightCardCarousels();
initPillarCardLinks();
initTabbedContent();
initShareContainer();
