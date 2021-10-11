import Swiper, {A11y, Autoplay, Pagination, Navigation, Keyboard, EffectFade} from 'swiper';

Swiper.use([A11y, Autoplay, Pagination, Navigation, Keyboard, EffectFade]);

class MozfestHeroCarousel {
  static selector() {
    return "[data-mozfest-hero-carousel]";
  }

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
      },
      paginationClickable: false,
      keyboard: {
        enabled: true,
      },
      pagination: {
        el: ".swiper-hero-pagination",
        clickable: false,
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
    })
  }
}

const MozfestHeroCarousels = {
  init: function () {
    for (const carousel of document.querySelectorAll(
      MozfestHeroCarousel.selector()
    )) {
      new MozfestHeroCarousel(carousel);
    }
  },
};

export default MozfestHeroCarousels;
