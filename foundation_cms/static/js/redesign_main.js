import $ from "jquery";
import "foundation-sites";
import { initImpactNumberStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";
import { initAllHorizontalAccordions } from "./blocks/hero_accordion.js";
import { initAllAccordionBlocks } from "./blocks/accordion_block.js";
import { initImageCarousels } from "./blocks/image_carousel_block.js";
import injectNewsletterSignups from "./components/newsletter_signup/newsletter_signup.js";
import injectNewsletterUnsubscribes from "./components/newsletter_unsubscribe.js";
import { initPortraitCardSetCarousels } from "./blocks/portrait_card_carousel.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
  initSearchToggle,
} from "./components/primary_nav/index.js";
import { initDonateBanner } from "./components/donate_banner.js";
import { initDonateLightbox } from "./components/donate_lightbox.js";
import { initSpotlightCardCarousels } from "./blocks/spotlight_card_carousel.js";
import { initPillarCardLinks } from "./blocks/pillar_card_set.js";
import { initProjectBlocks } from "./blocks/project_block.js";
import { initTabbedContent } from "./blocks/tabbed_content_container.js";
import initBackToTopButton from "./components/back_to_top.js";
import { initCopyToClipboardButtons } from "./components/copy_to_clipboard.js";
import { initCsrfForms } from "./utils/csrf.js";

let foundationSiteURL = window.location.origin;

$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
initDonateBanner();
initDonateLightbox();
initImpactNumberStatAnimationsOnScroll();
initAllHorizontalAccordions();
initAllAccordionBlocks();
injectNewsletterSignups(foundationSiteURL);
injectNewsletterUnsubscribes(foundationSiteURL);
initImageCarousels();
initPortraitCardSetCarousels();
initWordmarkVisibilityOnScroll();
initSpotlightCardCarousels();
initPillarCardLinks();
initProjectBlocks();
initTabbedContent();
initBackToTopButton();
initSearchToggle();
initCopyToClipboardButtons();
initCsrfForms();
