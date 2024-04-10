import Accordion from "../accordion/accordion";

class NavAccordion extends Accordion {
  static selector() {
    return "[data-nav-accordion]";
  }

  constructor(node) {
    super(node);
    this.siblings = this.getSiblings();
  }

  closeAccordion(accordion) {
    const content = accordion.querySelector("[data-accordion-content]");
    const chevron = accordion.querySelector("img");
    const title = accordion.querySelector("[data-accordion-title]");
    const titleText = title.querySelector("h5");
    titleText.classList.remove("large:tw-border-b-4");
    content.classList.add("tw-hidden");
    chevron.classList.remove("tw-rotate-180");
    title.setAttribute("aria-expanded", "false");
    content.setAttribute("aria-hidden", "true");
  }

  getSiblings() {
    let siblings = document.querySelectorAll("[data-nav-accordion]");
    return Array.from(siblings).filter((sibling) => sibling !== this.node);
  }

  closeSiblings() {
    this.siblings.forEach((sibling) => {
      this.closeAccordion(sibling);
    });
  }

  open() {
    const isDesktop = window.matchMedia("(min-width: 768px)").matches;
    if (isDesktop) {
      this.closeSiblings();
    }
    super.open();
    this.titleText.classList.add("large:tw-border-b-4");
  }

  close() {
    super.close();
    this.titleText.classList.remove("large:tw-border-b-4");
  }
}

export default NavAccordion;
