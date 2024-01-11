import Swiper, {
  A11y,
  Autoplay,
  Pagination,
  Navigation,
  Keyboard,
} from "swiper";

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
      slidesPerView: this.node.dataset.slidesPerView || 1,
      autoHeight: false,
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
          slidesPerView: this.node.dataset.desktopSlidesPerView || 2,
          spaceBetween: this.node.dataset.desktopSpaceBetween || 30,
        },
      },
    });
    this.slideTotal = this.node.dataset.slidetotal;
  }
}

const MozfestCarousels = {
  init: function () {
    document
      .querySelectorAll(`[data-carousel]`)
      .forEach((e) => new Carousel(e));
  },
};

export default MozfestCarousels;
