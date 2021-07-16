import Swiper from 'swiper/bundle';

class Carousel {
  // Note: ensure your parent element has a unique id and data-carousel attr
  constructor() {
    this.slideshows = document.querySelectorAll('[data-carousel]');
    this.createSlideshows();
  }

  createSlideshows() {
    let swipers = [];
    this.slideshows.forEach((slideshow, index) => {
      let slideshowId = slideshow.id;
      swipers[index] = new Swiper(`#${slideshowId}`, {
        effect: "fade",
        fadeEffect: {crossFade: true},
        autoHeight: true,
        centeredSlides: true,
        initialSlide: 0,
        loop: false,
        slidesPerView: "auto",
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
    });
  }
}

export const initYoutubeRegretsCarousel = () => {
  // const carousels = [...document.querySelectorAll("[data-carousel]")];
  // carousels.map((carousel) => new Carousel(carousel));
  new Carousel();
};

export default Carousel;
