import $ from "jquery";
import "foundation-sites";
import { initImpactNumberStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";
import { initPortraitCardSetCarousel } from "./blocks/portrait_card_carousel.js";

$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

initImpactNumberStatAnimationsOnScroll();
initPortraitCardSetCarousel();
