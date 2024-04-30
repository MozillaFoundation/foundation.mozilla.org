import Accordion from "../accordion/accordion";

class NavMobileDropdown extends Accordion {
  static selector() {
    return "[data-mobile-dropdown]";
  }

  constructor(node) {
    super(node);
    this.isDropdownWayfindingActive = this.accordion.dataset.isWayfindingActive;
    if (this.isDropdownWayfindingActive === "true") {
      this.addBaseWayfindingStyles();
    }
  }

  addBaseWayfindingStyles() {
    this.title.classList.add("tw-border-s-4", "tw-border-gray-60");
  }

  handleWayfindingOpenStyles() {
    this.titleText.classList.add("tw-border-b-4", "tw-border-gray-60");
    this.title.classList.remove("tw-border-s-4");
  }

  handleWayfindingClosedStyles() {
    this.titleText.classList.remove("tw-border-b-4", "tw-border-gray-60");
    this.title.classList.add("tw-border-s-4");
  }

  getOpenSibling() {
    return document
      .querySelector(`${NavMobileDropdown.selector()} [aria-expanded="true"]`)
      ?.closest(NavMobileDropdown.selector());
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
    // Only add the underline effect if the dropdown wayfinding is not active
    // Otherwise, border styles will clash
    if (this.isDropdownWayfindingActive === "false") {
      this.titleText.classList.add("tw-underline");
    }
  }

  removeHoverEffects() {
    this.accordion.classList.remove("tw-bg-blue-03");
    this.titleText.classList.remove("tw-underline");
  }

  open() {
    if (this.isDropdownWayfindingActive === "true") {
      this.handleWayfindingOpenStyles();
    }

    let openAccordion = this.getOpenSibling();
    if (openAccordion) {
      const title = openAccordion.querySelector("[data-accordion-title]");
      const chevron = openAccordion.querySelector("[data-accordion-title] img");
      const content = openAccordion.querySelector("[data-accordion-content]");
      title.setAttribute("aria-expanded", "false");
      content.setAttribute("aria-hidden", "true");
      chevron.classList.add("tw-rotate-180");
      content.style.height = "0";
    }

    super.open();
    let transitionEndHandler = () => {
      this.title.scrollIntoView({ behavior: "smooth", block: "start" });
      this.content.removeEventListener("transitionend", transitionEndHandler);
    };

    this.content.addEventListener("transitionend", transitionEndHandler);
    this.content.style.height = `${this.content.scrollHeight}px`;
  }

  close() {
    super.close();
    if (this.isDropdownWayfindingActive === "true") {
      this.handleWayfindingClosedStyles();
    }
    this.content.style.height = "0";
  }
}

export default NavMobileDropdown;
