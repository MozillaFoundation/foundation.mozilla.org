// import Glide from "@glidejs/glide";
// import ArrowDisabler from "./carousel-arrow-disabler";
//
// class HeroCarousel {
//   static selector() {
//     return "[data-hero-carousel]";
//   }
//
//   constructor(node) {
//     this.node = node;
//     this.createSlideshow();
//     this.slideTotal = this.node.dataset.slidetotal;
//     this.slideshow.mount({ ArrowDisabler });
//     this.bindEvents();
//     this.setLiveRegion();
//   }
//
//   bindEvents() {
//     this.updateAriaRoles();
//
//     // Rerun after each slide move
//     this.slideshow.on("run.after", () => {
//       this.updateAriaRoles();
//       this.updateLiveRegion();
//     });
//   }
//
//   createSlideshow() {
//     this.slideshow = new Glide(this.node, {
//       type: "slider",
//       startAt: 0,
//       gap: 0,
//       keyboard: true,
//       perTouch: 1,
//       touchRatio: 0.5,
//       perView: 1,
//       rewind: true,
//       autoplay: false,
//
//       // Swipe animation on mobile but
//       // fade animation on desktop.
//       // They require different animation durations
//       animationDuration: window.innerWidth > 992 ? 0 : 300,
//     });
//   }
//
//   updateAriaRoles() {
//     for (const slide of this.node.querySelectorAll(
//       ".glide__slide:not(.glide__slide--active)"
//     )) {
//       const inactiveSlideAnchors = slide.querySelectorAll("a");
//       slide.setAttribute("aria-hidden", "true");
//       inactiveSlideAnchors.forEach(function inactiveAnchor(el) {
//         el.setAttribute("tabindex", -1);
//       });
//     }
//     const activeSlide = this.node.querySelector(".glide__slide--active");
//     const activeSlideAnchors = activeSlide.querySelectorAll("a");
//     activeSlide.removeAttribute("aria-hidden");
//     activeSlideAnchors.forEach(function activeAnchor(el) {
//       el.removeAttribute("tabindex");
//     });
//   }
//
//   // Sets a live region. This will announce which slide is showing to screen readers when previous / next buttons clicked
//   setLiveRegion() {
//     const liveRegion = this.node.querySelector("[data-liveregion]");
//     const inner = document.createElement("div");
//     inner.setAttribute("aria-live", "polite");
//     inner.setAttribute("aria-atomic", "true");
//     inner.setAttribute("data-liveregion", true);
//     liveRegion.appendChild(inner);
//   }
//
//   // Update the live region that announces the next slide.
//   updateLiveRegion() {
//     this.node.querySelector(
//       "[data-liveregion]"
//     ).innerHTML = `<span class="carousel-hero__count-first">${
//       this.slideshow.index + 1
//     } </span><span class="carousel-hero__count-second">/ ${
//       this.slideTotal
//     }</span>`;
//   }
// }
//
// export const initYoutubeRegretsHeroCarousel = () => {
//   const carousels = [...document.querySelectorAll("#yt-hero-carousel")];
//   carousels.map((carousel) => new HeroCarousel(carousel));
// };
//
// export default HeroCarousel;
