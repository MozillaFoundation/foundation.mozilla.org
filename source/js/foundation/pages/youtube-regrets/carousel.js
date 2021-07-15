import Swiper from 'swiper/bundle';

class Carousel {
  static selector() {
    return "[data-carousel-swiper]";
  }

  constructor(node) {
    this.node = node;
    this.createSlideshow();
    this.bindEvents();
  }

  bindEvents() {
  }

  createSlideshow() {
    this.slideshow = new Swiper(this.node, {
      effect: "fade",
      fadeEffect: {crossFade: true},
      autoHeight: true,
      centeredSlides: true,
      initialSlide: 0,
      loop: false,
      slidesPerView: "auto",
      hideOnClick: true,
      speed: 400,
      keyboard: {
        enabled: true,
        onlyInViewport: false,
      },

      // Navigation arrows
      navigation: {
        nextEl: ".carousel__button--next",
        prevEl: ".carousel__button--prev",
      },

      pagination: {
        el: ".carousel__count-inner",
        type: "fraction",
      },
    });
  }

  // updateAriaRoles() {
  //   for (const slide of this.node.querySelectorAll(
  //     ".glide__slide:not(.glide__slide--active)"
  //   )) {
  //     const inactiveSlideAnchors = slide.querySelectorAll("a");
  //     slide.setAttribute("aria-hidden", "true");
  //     inactiveSlideAnchors.forEach(function inactiveAnchor(el) {
  //       el.setAttribute("tabindex", -1);
  //     });
  //   }
  //   const activeSlide = this.node.querySelector(".glide__slide--active");
  //   const activeSlideAnchors = activeSlide.querySelectorAll("a");
  //   activeSlide.removeAttribute("aria-hidden");
  //   activeSlideAnchors.forEach(function activeAnchor(el) {
  //     el.removeAttribute("tabindex");
  //   });
  // }
}

export const initYoutubeRegretsCarousel = () => {
  const carousels = [...document.querySelectorAll("#yt-regrets-carousel")];
  carousels.map((carousel) => new Carousel(carousel));
};

export default Carousel;
