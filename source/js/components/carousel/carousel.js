import Swiper, {A11y, Autoplay, Pagination, Navigation} from 'swiper';

Swiper.use([A11y, Autoplay, Pagination, Navigation]);

class Carousel {
  static selector() {
    return "[data-carousel]";
  }

  constructor(node) {
    this.node = node;
    this.swiper = new Swiper(this.node, {
      spaceBetween: 20,
      watchOverflow: true,
      // autoHeight: true,
      centeredSlides: false,
      simulateTouch: true,
      slidesPerView: 1,
      keyboard: {
        enabled: true,
      },
      pagination: {
        el: ".swiper-navigation",
        clickable: true,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      // Responsive breakpoints
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 25,
        },
      },
    });
    this.slideTotal = this.node.dataset.slidetotal;
  }
}

export const initCarousel = () => {
  const carousels = [...document.querySelectorAll("[data-carousel]")];
  carousels.map((carousel) => new Carousel(carousel));
};

export default Carousel;
