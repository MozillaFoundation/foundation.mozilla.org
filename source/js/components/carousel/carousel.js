import Swiper, {A11y, Autoplay, Pagination, Navigation, Keyboard} from 'swiper';

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
        el: '.swiper-pagination',
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
        },
      },
    });
    this.slideTotal = this.node.dataset.slidetotal;
  }
}

const MozfestCarousels = {
  init: function () {
    for (const carousel of document.querySelectorAll("[data-carousel]")) {
      new Carousel(carousel);
    }
  },
};

export default MozfestCarousels;
