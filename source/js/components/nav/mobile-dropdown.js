import Accordion from "../accordion/accordion";

class NavMobileDropdown extends Accordion {
  static selector() {
    return "[data-mobile-dropdown]";
  }

  constructor(node) {
    super(node);
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
}

export default NavMobileDropdown;
