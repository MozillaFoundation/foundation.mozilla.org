import { gsap } from "gsap";
import { ScrollToPlugin } from "gsap/all";

gsap.registerPlugin(ScrollToPlugin);

class Accordion {
  constructor(node) {
    this.accordion = node;
    this.accordionElements = [
      ...this.accordion.querySelectorAll("[data-accordion-item]"),
    ];
    this.animateSpeed = 0.1;

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
        if (!drawer.classList.contains("is-open")) {
          this.closeDrawers();
        }
        drawer.classList.add("is-open");
        closeButton.classList.remove("d-none");
        closeButton.classList.add("d-flex");
        button.setAttribute("aria-expanded", true);

        // Animate height, hide original button and scroll to the top of the content area
        let timeline = gsap.timeline({
          onComplete: this.scrollToY,
          onCompleteParams: [drawer, 0.1, 80],
        });
        timeline
          .to(button, { duration: this.animateSpeed, opacity: 0 })
          .to(content, {
            duration: this.animateSpeed,
            height: "auto",
            onComplete: () => {
              const event = document.createEvent("Event");
              event.initEvent("openDrawer", true, true);
              document.dispatchEvent(event);
            },
          });
      });

      closeButton.addEventListener("click", () => {
        this.scrollToY(drawer, 0.1, 80);
        this.closeDrawers(this.animateSpeed);
      });

      drawer.addEventListener("mouseenter", () => {
        gsap.to(mask, { duration: this.animateSpeed, ease: "none", y: 10 });
      });

      drawer.addEventListener("mouseleave", () => {
        gsap.to(mask, { duration: this.animateSpeed, ease: "none", y: 0 });
      });
    });
  }

  closeDrawers(speed = 0.1) {
    this.accordionElements.forEach((drawer) => {
      if (drawer.classList.contains("is-open")) {
        const content = drawer.querySelector("[data-accordion-content]");
        const button = drawer.querySelector("[data-accordion-button]");
        const closeButton = drawer.querySelector(
          "[data-accordion-close-button]"
        );
        closeButton.classList.add("d-none");
        closeButton.classList.remove("d-flex");
        drawer.classList.remove("is-open");
        button.setAttribute("aria-expanded", false);

        // Animate height down and show original button
        let timeline = gsap.timeline();
        timeline
          .to(button, { duration: speed, opacity: 1 })
          .to(content, { duration: speed, height: "0px" });
      }
    });
  }

  scrollToY(element, speed = 0.1, offset, callback) {
    const distance = window.scrollY + element.getBoundingClientRect().top;
    const extraOffset = offset ? offset : 0;
    gsap.to(window, {
      duration: speed,
      scrollTo: { y: distance - extraOffset },
    });
  }
}

export const initYoutubeRegretsAccordions = () => {
  const accordions = [...document.querySelectorAll("#yt-regrets-accordion")];
  accordions.map((accordion) => new Accordion(accordion));
};

export default Accordion;
