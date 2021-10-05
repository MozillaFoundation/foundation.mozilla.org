import Swiper, {A11y, Autoplay, Pagination, Navigation, Keyboard} from 'swiper';

Swiper.use([A11y, Autoplay, Pagination, Navigation, Keyboard]);

class Carousel {
  static selector() {
    return "[data-carousel]";
  }

  constructor(node) {
    this.node = node;
    this.swiper = new Swiper(this.node, {
      spaceBetween: 20,
      watchOverflow: true,
      centeredSlides: false,
      simulateTouch: true,
      slidesPerView: 1,
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
        768: {
          slidesPerView: 1.75,
          spaceBetween: 30,
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
