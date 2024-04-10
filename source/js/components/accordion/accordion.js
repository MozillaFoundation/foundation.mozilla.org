class Accordion {
  static selector() {
    return "[data-accordion]";
  }

  constructor(node) {
    this.accordion = node;
    this.title = this.accordion.querySelector("[data-accordion-title]");
    this.content = this.accordion.querySelector("[data-accordion-content]");
    this.chevron = this.title.querySelector("img");
    this.titleText = this.title.querySelector("h5");
    this.close();
    this.bindEvents();
  }

  bindEvents() {
    this.title.addEventListener("click", (e) => {
      e.preventDefault();
      let open = !this.content.classList.contains("tw-hidden");

      if (open) {
        this.close();
        open = false;
      } else {
        this.open();
        open = true;
      }
    });

    this.title.addEventListener("focus", () => {
      this.title.setAttribute("aria-selected", "true");
    });

    this.title.addEventListener("blur", () => {
      this.title.setAttribute("aria-selected", "false");
    });
  }

  open() {
    this.content.classList.remove("tw-hidden");
    this.chevron.classList.add("tw-rotate-180");
    this.title.setAttribute("aria-expanded", "true");
    this.content.setAttribute("aria-hidden", "false");
  }

  close() {
    this.content.classList.add("tw-hidden");
    this.chevron.classList.remove("tw-rotate-180");
    this.title.setAttribute("aria-expanded", "false");
    this.content.setAttribute("aria-hidden", "true");
  }
}

export default Accordion;
