import Swiper, {A11y, Autoplay, Pagination, Navigation, Keyboard} from 'swiper';

Swiper.use([A11y, Autoplay, Pagination, Navigation, Keyboard]);

class MozfestHeroCarousel {
  static selector() {
    return "[data-mozfest-hero-carousel]";
  }

  constructor(node) {
    this.node = node;
    this.delay = 10000;

    // This slideshow autoplays in the background and cannot be manipulated
    this.backGroundImagesSwiper = new Swiper(".swiper-hero-carousel", {
      loop: true,
      watchSlidesProgress: true,
      autoplay: {
        delay: this.delay,
      },
      paginationClickable: true,
      keyboard: {
        enabled: true,
      },
      pagination: {
        el: ".swiper-hero-pagination",
        clickable: true,
      },
    });

    this.heroTextMobile = new Swiper(".swiper-hero-mobile", {
      allowTouchMove: false,
      loop: true,
      keyboard: {
        enabled: true,
      },
      autoplay: {
        delay: this.delay,
      },
      slidesPerView: 1,
      centeredSlides: true,
      spaceBetween: 30,
    });

    this.slideTotal = this.node.dataset.slidetotal;
  }
}

export const initMozfestHeroCarousel = () => {
  const carousels = [
    ...document.querySelectorAll("[data-mozfest-hero-carousel]"),
  ];
  carousels.map((carousel) => new MozfestHeroCarousel(carousel));
};

export default MozfestHeroCarousel;
