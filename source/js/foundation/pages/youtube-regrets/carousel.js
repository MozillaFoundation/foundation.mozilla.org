import Glide from "@glidejs/glide";
import ArrowDisabler from "./carousel-arrow-disabler";

class Carousel {
  static selector() {
    return "[data-carousel]";
  }

  constructor(node) {
    this.node = node;
    this.createSlideshow();
    this.slideTotal = this.node.dataset.slidetotal;
    this.slideshow.mount({ ArrowDisabler });
    this.bindEvents();
    this.setLiveRegion();
    this.throttled = false;
  }

  bindEvents() {
    this.updateAriaRoles();

    // Rerun after each slide move
    this.slideshow.on("run.after", () => {
      this.updateAriaRoles();
      this.updateLiveRegion();
    });

  }

  createSlideshow() {
    this.slideshow = new Glide(this.node, {
      type: "slider",
      startAt: 0,
      gap: 0,
      keyboard: true,
      perTouch: 1,
      touchRatio: 0.5,
      perView: 1,
      rewind: true,
      autoplay: false,
      autoHeight: true,
      // Swipe animation on mobile but
      // fade animation on desktop.
      // They require different animation durations
      animationDuration: window.innerWidth > 992 ? 0 : 300,
    });
  }

  updateAriaRoles() {
    for (const slide of this.node.querySelectorAll(
      ".glide__slide:not(.glide__slide--active)"
    )) {
      const inactiveSlideAnchors = slide.querySelectorAll("a");
      slide.setAttribute("aria-hidden", "true");
      inactiveSlideAnchors.forEach(function inactiveAnchor(el) {
        el.setAttribute("tabindex", -1);
      });
    }
    const activeSlide = this.node.querySelector(".glide__slide--active");
    const activeSlideAnchors = activeSlide.querySelectorAll("a");
    activeSlide.removeAttribute("aria-hidden");
    activeSlideAnchors.forEach(function activeAnchor(el) {
      el.removeAttribute("tabindex");
    });
  }

  // Sets a live region. This will announce which slide is showing to screen readers when previous / next buttons clicked
  setLiveRegion() {
    const liveRegion = this.node.querySelector("[data-liveregion]");
    const inner = document.createElement("div");
    inner.setAttribute("aria-live", "polite");
    inner.setAttribute("aria-atomic", "true");
    inner.setAttribute("data-liveregion", true);
    liveRegion.appendChild(inner);
  }

  // resizeSlider() {
  //   const activeSlide = this.node.querySelector(".glide__slide--active");
  //   const activeSlideHeight = activeSlide ? activeSlide.offsetHeight : 0;
  //
  //   const glideTrack = this.node.querySelector(".glide__track");
  //   // const glideTrackHeight = glideTrack ? glideTrack.offsetHeight : 0;
  //
  //   glideTrack.style.height = `${activeSlideHeight}px`;
  // }

  // Update the live region that announces the next slide.
  updateLiveRegion() {
    this.node.querySelector(
      "[data-liveregion]"
    ).innerHTML = `<span class="carousel__count-first">0${
      this.slideshow.index + 1
    }</span> <span class="carousel__count-second">/0${this.slideTotal}</span>`;
  }
}

export const initYoutubeRegretsCarousel = () => {
  const carousels = [...document.querySelectorAll("#yt-regrets-carousel")];
  carousels.map((carousel) => new Carousel(carousel));
};

export default Carousel;
