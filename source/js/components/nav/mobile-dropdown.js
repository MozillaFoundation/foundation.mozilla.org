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
    this.titleButton.classList.add("tw-border-s-4", "tw-border-gray-60");
  }

  handleWayfindingOpenStyles() {
    this.titleText.classList.add("tw-border-b-4", "tw-border-gray-60");
    this.titleButton.classList.remove("tw-border-s-4");
  }

  handleWayfindingClosedStyles() {
    this.titleText.classList.remove("tw-border-b-4", "tw-border-gray-60");
    this.titleButton.classList.add("tw-border-s-4");
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

    super.open();
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
