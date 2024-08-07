import Swiper from "swiper";
import {
  A11y,
  Autoplay,
  Pagination,
  Navigation,
  Keyboard,
} from "swiper/modules";

/**
 * Image Carousel on Mozfest Homepage Hero Section.
 * Uses Swiper library to provide functionality to move between slides.
 */

Swiper.use([A11y, Autoplay, Pagination, Navigation, Keyboard]);

class Carousel {
  constructor(node) {
    this.node = node;
    this.swiper = new Swiper(this.node, {
      spaceBetween: 20,
      watchOverflow: true,
      centeredSlides: false,
      simulateTouch: true,
      slidesPerView: 1,
      autoHeight: true,
      keyboard: {
        enabled: true,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      // Responsive breakpoints
      breakpoints: {
        992: {
          slidesPerView: 2,
          spaceBetween: 30,
          pagination: {
            el: ".swiper-fraction",
            type: "fraction",
          },
        },
      },
    });
    this.slideTotal = this.node.dataset.slidetotal;
  }
}

const FoundationCarousels = {
  init: function () {
    document
      .querySelectorAll(`[data-foundation-carousel]`)
      .forEach((e) => new Carousel(e));
  },
};

export default FoundationCarousels;
