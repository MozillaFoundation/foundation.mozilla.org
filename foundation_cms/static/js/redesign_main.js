import $ from "jquery";
import "foundation-sites";
import { initImpactStatAnimationsOnScroll } from "./blocks/impact_numbers_block.js";

$(document).foundation();

console.log(
  "😃 If you see this message, the JS watch and build steps are working properly! 😃",
);

document.addEventListener("DOMContentLoaded", () => {
  initImpactStatAnimationsOnScroll();
});
