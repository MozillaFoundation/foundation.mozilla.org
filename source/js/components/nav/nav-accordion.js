import Accordion from "../accordion/accordion";

class NavAccordion extends Accordion {
  static selector() {
    return "[data-nav-accordion]";
  }

  constructor(node) {
    super(node);
  }

  // getSiblings() {
  //   let siblings = document.querySelectorAll(NavAccordion.selector());
  //   return Array.from(siblings).filter((sibling) => sibling !== this.node);
  // }

  // isDesktop() {
  //   return window.matchMedia("(min-width: 992px)").matches;
  // }

  // bindEvents() {
  //   if (this.isDesktop()) {
  //     // Opens the accordion when the user interacts with the title
  //     this.title.addEventListener("focus", () => {
  //       this.open();
  //     });
  //     this.title.addEventListener("pointerenter", () => {
  //       this.open();
  //     });
  //     // But only closes when you leave the content so that it stays open
  //     // when you're interacting with it
  //     this.content.addEventListener("blur", () => {
  //       this.close();
  //     });
  //     this.content.addEventListener("pointerleave", () => {
  //       this.close();
  //     });
  //     // Also close when you enter any of the siblings
  //     this.siblings = this.getSiblings();
  //     this.siblings.forEach((sibling) => {
  //       sibling.addEventListener("pointerenter", () => {
  //         this.close();
  //       });
  //       sibling.addEventListener("focus", () => {
  //         this.close();
  //       });
  //     });
  //   }
  // }

  // open() {
  //   super.open();
  //   this.titleText.classList.add("large:tw-text-black");
  //   this.titleText.classList.add("large:tw-border-black");
  //   this.titleText.classList.remove("large:tw-border-transparent");
  //   this.title.setAttribute("aria-selected", "true");
  //   this.content.classList.add("large:tw-inline");
  // }

  // close() {
  //   super.close();
  //   this.titleText.classList.remove("large:tw-text-black");
  //   this.titleText.classList.remove("large:tw-border-black");
  //   this.titleText.classList.add("large:tw-border-transparent");
  //   this.title.setAttribute("aria-selected", "false");
  //   this.content.classList.remove("large:tw-inline");
  // }
}

export default NavAccordion;
