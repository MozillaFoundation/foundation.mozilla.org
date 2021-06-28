import {gsap} from "gsap";
import {ScrollToPlugin} from "gsap/all";

gsap.registerPlugin(ScrollToPlugin);

class Accordion {
  constructor(node) {
    this.accordion = node;
    this.accordionElements = [
      ...this.accordion.querySelectorAll("[data-accordion-item]"),
    ];
    this.animateSpeed = 0.2;

    this.bindEvents();
  }

  bindEvents() {
    this.accordionElements.forEach((drawer, index) => {
      const mask = drawer.querySelector("[data-expand-mask]");
      const content = drawer.querySelector("[data-accordion-content]");
      const button = drawer.querySelector("[data-accordion-button]");
      const closeButton = drawer.querySelector("[data-accordion-close-button]");

      //Set Z index descending so tabs will overlap
      drawer.style.zIndex = this.accordionElements.length - index;

      button.addEventListener("click", (e) => {
        if (!drawer.classList.contains('is-open')) {
          this.closeDrawers();
        }
        drawer.classList.add('is-open');
        closeButton.classList.remove("d-none");
        button.setAttribute("aria-expanded", true);

        // Animate height, hide original button and scroll to the top of the content area
        gsap.to(content, this.animateSpeed, {height: "auto"});
        gsap.to(button, this.animateSpeed, {opacity: 0});
        gsap.to(button, this.animateSpeed, {display: "none"});
        gsap.to(window, this.animateSpeed, {
          ease: "Power0.easeNone",
          scrollTo: {
            y: window.pageYOffset + mask.getBoundingClientRect().top - 80,
          },
        });
      });

      closeButton.addEventListener("click", () => {
        this.closeDrawers(this.animateSpeed);
        gsap.to(window, this.animateSpeed, {
          ease: "Power0.easeNone",
          scrollTo: {
            y: window.pageYOffset + button.getBoundingClientRect().top - 80,
          },
        });
      });

      drawer.addEventListener("mouseenter", (e) => {
        gsap.to(mask, this.animateSpeed, {y: 10});
      });
      drawer.addEventListener("mouseleave", (e) => {
        gsap.to(mask, this.animateSpeed, {y: 0});
      });
    });
  }

  closeDrawers(speed = 0.2) {
    this.accordionElements.forEach((drawer) => {
      if (drawer.classList.contains("is-open")) {
        const content = drawer.querySelector("[data-accordion-content]");
        const button = drawer.querySelector("[data-accordion-button]");
        const closeButton = drawer.querySelector(
          "[data-accordion-close-button]"
        );
        closeButton.classList.add("d-none");
        drawer.classList.remove("is-open");
        button.setAttribute("aria-expanded", false);

        // Animate height down and show original button
        gsap.to(content, speed, {height: "0px"});
        gsap.to(button, speed, {opacity: 1, delay: 0.2});
        gsap.to(button, speed, {display: "block", delay: 0.2});
      }
    });
  }
}

export const initYoutubeRegretsAccordions = () => {
  const accordions = [...document.querySelectorAll("#yt-regrets-accordion")];
  accordions.map((accordion) => new Accordion(accordion));
};

export default Accordion;
