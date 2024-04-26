import Accordion from "../accordion/accordion";

class NavDesktopDropdown extends Accordion {
  static selector() {
    return "[data-desktop-dropdown]";
  }

  constructor(node) {
    super(node);
    this.isDropdownWayfindingActive = this.accordion.dataset.isWayfindingActive;
    if (this.isDropdownWayfindingActive === "true") {
      this.addBaseWayfindingStyles();
    }
  }

  /*
  The three wayfinding state handlers here do the same thing:
   - remove the transparent border colour and add a black one
  This is because the behaviour of the active wayfinder state on desktop is simply to
  always keep a black border on the bottom of the dropdown's title.

  The three methods are kept separate for clarity and to allow for eventual independent changes.
  */

  addBaseWayfindingStyles() {
    this.titleText.classList.remove("large:tw-border-transparent");
    this.titleText.classList.add("large:tw-border-black");
  }

  handleWayfindingOpenStyles() {
    this.titleText.classList.remove("large:tw-border-transparent");
    this.titleText.classList.add("large:tw-border-black");
  }

  handleWayfindingClosedStyles() {
    this.titleText.classList.remove("large:tw-border-transparent");
    this.titleText.classList.add("large:tw-border-black");
  }

  getSiblings() {
    let siblings = document.querySelectorAll(NavDesktopDropdown.selector());
    return Array.from(siblings).filter((sibling) => sibling !== this.accordion);
  }

  bindEvents() {
    this.accordion.addEventListener("focus", () => {
      this.open();
    });
    this.accordion.addEventListener("pointerenter", () => {
      this.open();
    });
    this.accordion.addEventListener("blur", () => {
      this.close();
    });
    this.accordion.addEventListener("pointerleave", () => {
      this.close();
    });
  }

  open() {
    super.open();
    this.titleText.classList.add("large:tw-text-black");
    this.titleText.classList.add("large:tw-border-black");
    this.titleText.classList.remove("large:tw-border-transparent");
    this.accordion.setAttribute("aria-selected", "true");
    this.content.classList.remove("large:tw-opacity-0", "large:tw-invisible");
    this.content.classList.add("large:tw-opacity-100", "large:tw-visible");

    if (this.isDropdownWayfindingActive === "true") {
      this.handleWayfindingOpenStyles();
    }
    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const titleText = sibling.querySelector("[data-accordion-title] h5");
      titleText.classList.remove("large:tw-text-black");
      titleText.classList.add("large:tw-text-gray-40");
      const isSiblingDropdownWayfindingActive =
        sibling.dataset.isWayfindingActive;
      if (isSiblingDropdownWayfindingActive === "true") {
        titleText.classList.remove(
          "large:tw-border-transparent",
          "large:tw-border-black"
        );
        titleText.classList.add("large:tw-border-gray-40");
      }
    });
  }

  close() {
    super.close();
    this.titleText.classList.remove("large:tw-text-black");
    this.titleText.classList.remove("large:tw-border-black");
    this.titleText.classList.add("large:tw-border-transparent");
    this.accordion.setAttribute("aria-selected", "false");
    this.content.classList.remove("large:tw-opacity-100", "large:tw-visible");
    this.content.classList.add("large:tw-opacity-0", "large:tw-invisible");
    if (this.isDropdownWayfindingActive === "true") {
      this.handleWayfindingClosedStyles();
    }
    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const titleText = sibling.querySelector("[data-accordion-title] h5");
      titleText.classList.add("large:tw-text-black");
      titleText.classList.remove("large:tw-text-gray-40");
      const isSiblingDropdownWayfindingActive =
        sibling.dataset.isWayfindingActive;
      if (isSiblingDropdownWayfindingActive === "true") {
        titleText.classList.remove(
          "large:tw-border-transparent",
          "large:tw-border-gray-40"
        );
        titleText.classList.add("large:tw-border-black");
      }
    });
  }
}

export default NavDesktopDropdown;
