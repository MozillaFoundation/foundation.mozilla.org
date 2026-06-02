import injectNewsletterSignups from "./components/newsletter_signup/newsletter_signup.js";
import injectNewsletterUnsubscribes from "./components/newsletter_unsubscribe.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
  initSearchToggle,
} from "./components/primary_nav/index.js";
import { initDonateBanner } from "./components/donate_banner.js";
import { initDonateLightbox } from "./components/donate_lightbox.js";
let foundationSiteURL = window.location.origin;

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
initDonateBanner();
initDonateLightbox();
injectNewsletterSignups(foundationSiteURL);
injectNewsletterUnsubscribes(foundationSiteURL);
initWordmarkVisibilityOnScroll();
initSearchToggle();
