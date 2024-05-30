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
  }

  open() {
    super.open();
    this.content.style.height = `${this.content.scrollHeight}px`;

    if (this.shouldWayfindingBeActive === "true") {
      this.accordion.classList.add("tw-border-s-0");
    }
  }

  close() {
    super.close();
    this.content.style.height = "0";

    if (this.shouldWayfindingBeActive === "true") {
      this.accordion.classList.remove("tw-border-s-0");
    }
  }
}

export default NavMobileDropdown;
