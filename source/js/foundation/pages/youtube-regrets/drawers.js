import {gsap} from "gsap";
import {ScrollToPlugin} from "gsap/all";

gsap.registerPlugin(ScrollToPlugin);

class Drawers {
  constructor(node) {
    this.accordion = node;
    this.drawerElements = [
      ...this.accordion.querySelectorAll("[data-accordion-drawer]"),
    ];

    this.bindEvents();
  }

  bindEvents() {
    this.drawerElements.forEach((drawer, index) => {
      const mask = drawer.querySelector("[data-expand-mask]");
      const content = drawer.querySelector("[data-accordion-content]");
      const button = drawer.querySelector("[data-accordion-button]");
      const closeButton = drawer.querySelector("[data-accordion-close-button]");

      //Set Z index descending
      drawer.style.zIndex = this.drawerElements.length - index;

      button.addEventListener("click", (e) => {
        if (!drawer.classList.contains('is-open')) {
          this.closeDrawers();
        }
        drawer.classList.add('is-open')
        closeButton.classList.remove('d-none')

        gsap.to(content, 0.2, {maxHeight: "100%"});
        gsap.to(button, 0.2, {opacity: 0});
        gsap.to(button, 0.2, {display: "none"});
        gsap.to(window, 0.2, {
          delay: 0.4,
          ease: "Power0.easeNone",
          scrollTo: {
            y: window.pageYOffset + mask.getBoundingClientRect().top - 80,
          },
        });
      });

      closeButton.addEventListener("click", () => {
        this.closeDrawers();
        gsap.to(window, 0.2, {
          delay: 0.4,
          ease: "Power0.easeNone",
          scrollTo: {
            y: window.pageYOffset + button.getBoundingClientRect().top - 80,
          },
        });
      });

      drawer.addEventListener("mouseenter", (e) => {
        gsap.to(mask, 0.2, {y: 10});
      });
      drawer.addEventListener("mouseleave", (e) => {
        gsap.to(mask, 0.2, {y: 0});
      });
    });
  }

  closeDrawers() {
    this.drawerElements.forEach((drawer) => {
      if (drawer.classList.contains("is-open")) {
        const content = drawer.querySelector("[data-accordion-content]");
        const button = drawer.querySelector("[data-accordion-button]");
        const closeButton = drawer.querySelector("[data-accordion-close-button]");
        closeButton.classList.add('d-none')

        gsap.to(content, 0.2, {maxHeight: "0px"});
        drawer.classList.remove('is-open')
        gsap.to(button, 0.2, {opacity: 1});
        gsap.to(button, 0.2, {display: "block"});
      }
    })
  }
}

export const initYoutubeRegretsDrawers = () => {
  const accordions = [...document.querySelectorAll("#yt-regrets-accordion")];
  accordions.map((accordion) => new Drawers(accordion));
};

export default Drawers;
