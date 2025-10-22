import injectNewsletterSignups from "./components/newsletter_signup/newsletter_signup.js";
import injectNewsletterUnsubscribes from "./components/newsletter_unsubscribe.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./components/primary_nav";
import { initDonateBanner } from "./components/donate_banner.js";
let foundationSiteURL = window.location.origin;

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
initDonateBanner();
injectNewsletterSignups(foundationSiteURL);
injectNewsletterUnsubscribes(foundationSiteURL);
initWordmarkVisibilityOnScroll();
