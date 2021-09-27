import Swiper, {A11y, Autoplay, Pagination, Navigation} from 'swiper';

Swiper.use([A11y, Autoplay, Pagination, Navigation]);

class MozfestHeroCarousel {
  static selector() {
    return "[data-mozfest-hero-carousel]";
  }

  constructor(node) {
    this.node = node;
    this.backgroundImages = this.node.querySelector(
      "[data-background-images-carousel]"
    );

    // This slideshow autoplays in the background and cannot be manipulated
    this.backGroundImagesSwiper = new Swiper(this.backgroundImages, {
      // allowTouchMove: false,
      disableOnInteraction: false,
      loop: true,
      autoplay: {
        delay: 5000,
      },
    });

    // this.swiper = new Swiper(this.node, {
    //   spaceBetween: 20,
    //   watchOverflow: true,
    //   // autoHeight: true,
    //   centeredSlides: false,
    //   simulateTouch: true,
    //   slidesPerView: 1,
    //   keyboard: {
    //     enabled: true,
    //   },
    //   pagination: {
    //     el: ".swiper-navigation",
    //     clickable: true,
    //   },
    //   navigation: {
    //     nextEl: ".swiper-button-next",
    //     prevEl: ".swiper-button-prev",
    //   },
    //   // Responsive breakpoints
    //   breakpoints: {
    //     768: {
    //       slidesPerView: 2,
    //       spaceBetween: 25,
    //     },
    //   },
    // });

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
