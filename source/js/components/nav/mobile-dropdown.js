import Accordion from "../accordion/accordion";

class NavMobileDropdown extends Accordion {
  static selector() {
    return "[data-mobile-dropdown]";
  }

  constructor(node) {
    super(node);
  }

  getSiblings() {
    let siblings = document.querySelectorAll(NavMobileDropdown.selector());
    return Array.from(siblings).filter((sibling) => sibling !== this.accordion);
  }

  bindEvents() {
    super.bindEvents();
    this.accordion.addEventListener("focus", () => {
      this.addHoverEffects();
    });
    this.accordion.addEventListener("pointerenter", () => {
      this.addHoverEffects();
    });
    this.accordion.addEventListener("blur", () => {
      this.removeHoverEffects();
    });
    this.accordion.addEventListener("pointerleave", () => {
      this.removeHoverEffects();
    });
  }

  addHoverEffects() {
    this.accordion.classList.add("tw-bg-blue-03");
    this.titleText.classList.add("tw-underline");
  }

  removeHoverEffects() {
    this.accordion.classList.remove("tw-bg-blue-03");
    this.titleText.classList.remove("tw-underline");
  }

  open() {
    super.open();
    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const title = sibling.querySelector("[data-accordion-title]");
      const chevron = sibling.querySelector("[data-accordion-title] img");
      const content = sibling.querySelector("[data-accordion-content]");
      title.setAttribute("aria-expanded", "false");
      content.setAttribute("aria-hidden", "true");
      content.classList.add("tw-hidden");
      chevron.classList.add("tw-rotate-180");
    });
    this.title.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

export default NavMobileDropdown;
