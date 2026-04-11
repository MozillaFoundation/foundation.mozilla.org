import { SlidingCarousel } from "./util/sliding_carousel.js";

export function initImageCarousels() {
  const carousels = document.querySelectorAll(".image-carousel");
  carousels.forEach((carousel) => new ImageCarousel(carousel));
}

class ImageCarousel extends SlidingCarousel {
  constructor(rootEl) {
    super(rootEl, {
      viewport: ".image-carousel__card-container",
      track: ".image-carousel__track",
      item: ".image-carousel__slide",
    });
    this.init();
  }
}
