import $ from "jquery";
import "foundation-sites";
import { initImpactNumberStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";
import injectNewsletterSignups from "./components/newsletter-signup/newsletter_signup.js";

let networkSiteURL = window.location.origin;


$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initImpactNumberStatAnimationsOnScroll();

injectNewsletterSignups(networkSiteURL);