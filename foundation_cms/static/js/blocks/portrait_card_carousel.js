import { SlidingCarousel } from "./util/sliding_carousel.js";

const NUM_CARD_DESIGNS = 4;

export function initPortraitCardSetCarousels() {
  const carousels = document.querySelectorAll(".portrait-card-set");
  carousels.forEach((carousel) => new PortraitCardSetCarousels(carousel));
}

class PortraitCardSetCarousels extends SlidingCarousel {
  constructor(rootEl) {
    super(rootEl, {
      viewport: ".portrait-card-set__card-container",
      track: ".carousel-track",
      item: ".portrait-card",
    });
    this.init();
  }

  init() {
    this.applyCardColorDataAttrs(this.originalItems);
    super.init();
  }

  // Portrait cards use marginRight on the card itself rather than columnGap on the track.
  getItemSpacing(item) {
    return parseFloat(window.getComputedStyle(item).marginRight);
  }

  applyCardColorDataAttrs(items) {
    items.forEach((item, i) => {
      item.setAttribute("data-card-design", i % NUM_CARD_DESIGNS);
    });
  }
}
