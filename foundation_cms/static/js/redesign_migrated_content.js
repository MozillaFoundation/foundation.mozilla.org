import injectNewsletterSignups from "./components/newsletter-signup/newsletter_signup.js";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./components/primary_nav";

let foundationSiteURL = window.location.origin;

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initPrimaryNav();
injectNewsletterSignups(foundationSiteURL);
initWordmarkVisibilityOnScroll();
