class Accordion {
  static selector() {
    return "[data-accordion]";
  }

  constructor(node) {
    this.accordion = node;
    this.titleButton = this.accordion.querySelector("[data-accordion-button]");
    this.content = this.accordion.querySelector("[data-accordion-content]");
    this.chevron = this.titleButton.querySelector("img");
    this.titleText = this.titleButton.querySelector("span");
    this.shouldWayfindingBeActive =
      this.accordion.dataset.shouldWayfindingBeActive;

    if (this.shouldWayfindingBeActive === "true") {
      this.addBaseWayfindingStyles();
    }

    this.close();
    this.bindEvents();
  }

  addBaseWayfindingStyles() {
    this.accordion.classList.add("tw-highlighted");
  }

  bindEvents() {
    this.titleButton.addEventListener("click", (e) => {
      e.preventDefault();
      let open = this.titleButton.getAttribute("aria-expanded") === "true";

      if (open) {
        this.close();
        open = false;
      } else {
        this.open();
        open = true;
      }
    });

    this.titleButton.addEventListener("focus", () => {
      this.titleButton.setAttribute("aria-selected", "true");
    });

    this.titleButton.addEventListener("blur", () => {
      this.titleButton.setAttribute("aria-selected", "false");
    });
  }

  open() {
    this.chevron.classList.remove("tw-rotate-180");
    this.titleButton.setAttribute("aria-expanded", "true");
    this.content.setAttribute("aria-hidden", "false");
    this.content.style.visibility = "visible";
  }

  close() {
    this.chevron.classList.add("tw-rotate-180");
    this.titleButton.setAttribute("aria-expanded", "false");
    this.content.setAttribute("aria-hidden", "true");
    this.content.style.visibility = "hidden";
  }
}

export default Accordion;
