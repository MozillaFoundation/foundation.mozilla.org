import Accordion from "../accordion/accordion";

class NavDesktopDropdown extends Accordion {
  static selector() {
    return "[data-desktop-dropdown]";
  }

  constructor(node) {
    super(node);
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
    this.accordion.classList.add("large:tw-border-black");
    this.accordion.classList.remove("large:tw-border-transparent");
    this.accordion.setAttribute("aria-selected", "true");
    this.content.classList.add("large:tw-grid");
    this.content.classList.remove("large:tw-hidden");
    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const titleText = sibling.querySelector("[data-accordion-title] h5");
      titleText.classList.remove("large:tw-text-black");
      titleText.classList.add("large:tw-text-gray-40");
    });
  }

  close() {
    super.close();
    this.titleText.classList.remove("large:tw-text-black");
    this.accordion.classList.remove("large:tw-border-black");
    this.accordion.classList.add("large:tw-border-transparent");
    this.accordion.setAttribute("aria-selected", "false");
    this.content.classList.remove("large:tw-grid");
    this.content.classList.add("large:tw-hidden");
    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const titleText = sibling.querySelector("[data-accordion-title] h5");
      titleText.classList.add("large:tw-text-black");
      titleText.classList.remove("large:tw-text-gray-40");
    });
  }
}

export default NavDesktopDropdown;
