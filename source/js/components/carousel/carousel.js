import Swiper, {A11y, Autoplay, Pagination, Navigation} from '../../node_modules/swiper/swiper-bundle.min.js';

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
        el: '[data-carousel-pagination]',
        clickable: true,
        bulletActiveClass: 'carousel__bullet--active',
        bulletClass: 'carousel__bullet',
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      // Responsive breakpoints
      breakpoints: {
        640: {
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
