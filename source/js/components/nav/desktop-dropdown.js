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
    // titleButton event handlers
    this.titleButton.addEventListener("keydown", (event) => {
      const isEnterKey = event.key === "Enter" || event.keyCode === 13;
      const isSpaceKey = event.key === " " || event.keyCode === 32;

      if (isEnterKey || isSpaceKey) {
        if (this.titleButton.getAttribute("aria-expanded") === "true") {
          this.close();
        } else {
          this.closeSiblings();
          this.open();
        }
      }
    });

    this.titleButton.addEventListener("blur", (event) => {
      const accordionExpanded =
        this.titleButton.getAttribute("aria-expanded") === "true";
      const newFocusInNav = document
        .querySelector(".wide-screen-menu")
        .contains(event.relatedTarget);

      if (accordionExpanded && !newFocusInNav) {
        this.close();
      }
    });

    // accordion event handlers

    this.accordion.addEventListener("pointerenter", () => {
      this.open();
    });

    this.accordion.addEventListener("pointerleave", () => {
      this.close();
    });
  }

  open() {
    super.open();

    let topOffset = document
      .querySelector(".wide-screen-menu-container")
      .getBoundingClientRect().bottom;

    this.accordion.setAttribute("aria-selected", "true");
    this.accordion.classList.remove("tw-grayed-out");

    this.content.style.top = `${topOffset}px`;
    this.content.classList.add("xlarge:tw-flex");
    this.content.classList.remove("xlarge:tw-hidden");

    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const isSiblingDropdownWayfindingActive =
        sibling.dataset.shouldWayfindingBeActive;

      sibling.classList.add("tw-grayed-out");
      if (isSiblingDropdownWayfindingActive === "true") {
        sibling.classList.remove("tw-highlighted");
      }
    });
  }

  closeSiblings() {
    if (!this.siblings) {
      this.siblings = this.getSiblings();
    }
    this.siblings.forEach((sibling) => {
      const titleButton = sibling.querySelector("[data-accordion-button]");

      sibling.classList.remove("tw-grayed-out");

      this.closeAccordion(
        sibling,
        titleButton,
        sibling.querySelector("[data-accordion-content]")
      );
    });
  }

  closeAccordion(accordion, titleButton, content) {
    titleButton.setAttribute("aria-expanded", "false");
    accordion.setAttribute("aria-selected", "false");
    content.classList.remove("xlarge:tw-flex");
    content.classList.add("xlarge:tw-hidden");
  }

  close() {
    if (this.shouldWayfindingBeActive === undefined) {
      this.shouldWayfindingBeActive =
        this.accordion.dataset.shouldWayfindingBeActive;
    }

    super.close();

    this.closeAccordion(this.accordion, this.titleButton, this.content);
    this.closeSiblings();
  }
}

export default NavDesktopDropdown;
