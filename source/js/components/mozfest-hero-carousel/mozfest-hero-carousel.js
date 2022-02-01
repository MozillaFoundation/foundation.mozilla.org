import Swiper, {
  A11y,
  Autoplay,
  Pagination,
  Navigation,
  Keyboard,
  EffectFade,
} from "swiper";

/**
 * Image Carousel on Mozfest Homepage Hero Section.
 * Uses Swiper library to provide functionality to move between slides.
 */

Swiper.use([A11y, Autoplay, Pagination, Navigation, Keyboard, EffectFade]);

class MozfestHeroCarousel {
  constructor(node) {
    this.node = node;
    this.delay = 10000;

    // Initialize Carousels
    this.initBackgroundImageCarousel();
    this.initMobileTexCarousel();

    // Link transitions
    this.linkSlideChanges();
  }

  initBackgroundImageCarousel() {
    this.backGroundImagesSwiper = new Swiper(".swiper-hero-carousel", {
      loop: true,
      watchSlidesProgress: true,
      autoplay: {
        delay: this.delay,
        disableOnInteraction: false,
      },
      paginationClickable: false,
      keyboard: {
        enabled: true,
      },
      pagination: {
        el: ".swiper-hero-pagination",
        clickable: true,
      },
      effect: "fade",
      fadeEffect: {
        crossFade: false,
      },
    });
  }

  initMobileTexCarousel() {
    this.heroTextMobile = new Swiper(".swiper-hero-mobile", {
      allowTouchMove: true,
      loop: true,
      keyboard: {
        enabled: true,
      },
      autoplay: {
        delay: this.delay,
        disableOnInteraction: false,
      },
      slidesPerView: 1,
      centeredSlides: true,
      spaceBetween: 30,
    });
  }

  // Ensure that the background image slider stays in sync with the mobile one
  linkSlideChanges() {
    this.heroTextMobile.on("slideChange", (event) => {
      if (event.swipeDirection === "next") {
        this.backGroundImagesSwiper.slideNext();
      }
      if (event.swipeDirection === "prev") {
        this.backGroundImagesSwiper.slidePrev();
      }
    });
  }
}

const MozfestHeroCarousels = {
  init: function () {
    document
      .querySelectorAll(`[data-mozfest-hero-carousel]`)
      .forEach((e) => new MozfestHeroCarousel(e));
  },
};

export default MozfestHeroCarousels;
