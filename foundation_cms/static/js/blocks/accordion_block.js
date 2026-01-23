const SELECTORS = {
  root: ".accordion-block__items",
  item: ".accordion-item",
  trigger: ".accordion-item__button",
  panel: ".accordion-item__panel",
};

const TRANSITION_MS = 300;
export class AccordionBlock {
  constructor(root) {
    this.root = root;
    this.triggers = root.querySelectorAll(SELECTORS.trigger);
  }

  init() {
    this.triggers.forEach((trigger) => {
      const panel = this.getPanelForTrigger(trigger);
      if (!panel) return;

      // set transition
      panel.style.transition = `height ${TRANSITION_MS}ms ease-in-out`;

      trigger.addEventListener("click", () => this.toggle(trigger, panel));
    });
  }

  getPanelForTrigger(trigger) {
    const panelId = trigger.getAttribute("aria-controls");
    return panelId
      ? this.root.querySelector(`#${CSS.escape(panelId)}`)
      : trigger.closest(SELECTORS.item)?.querySelector(SELECTORS.panel);
  }

  toggle(trigger, panel) {
    const isOpen = trigger.getAttribute("aria-expanded") === "true";
    if (isOpen) {
      this.closeAccordion(trigger, panel);
    } else {
      this.closeAccordionAllExcept(trigger);
      this.openAccordion(trigger, panel);
    }
  }

  openAccordion(trigger, panel) {
    if (trigger.getAttribute("aria-expanded") === "true") return;

    trigger.setAttribute("aria-expanded", "true");

    // If it was hidden, unhide it before measuring
    panel.hidden = false;

    // Start from 0 for a clean animation
    panel.style.height = "0px";

    // Wait a frame so the browser applies the 0px height
    requestAnimationFrame(() => {
      // Measure target height
      const target = panel.scrollHeight;
      panel.style.height = `${target}px`;

      // After animation, set to auto so dynamic content won't clip
      this.onTransitionEnd(panel, () => {
        // Only finalize if still open
        if (trigger.getAttribute("aria-expanded") === "true") {
          panel.style.height = "auto";
        }
      });
    });
  }

  closeAccordion(trigger, panel) {
    if (trigger.getAttribute("aria-expanded") === "false") return;

    trigger.setAttribute("aria-expanded", "false");

    // If height is auto, lock it to a pixel value so we can animate to 0
    const currentHeight =
      panel.style.height === "auto" ? panel.scrollHeight : panel.offsetHeight;

    panel.style.height = `${currentHeight}px`;

    // Force reflow so the browser acknowledges the start height
    // (this is intentional; it makes the transition reliable)

    panel.offsetHeight;

    // Animate to closed
    panel.style.height = "0px";

    this.onTransitionEnd(panel, () => {
      // Only finalize if still closed
      if (trigger.getAttribute("aria-expanded") === "false") {
        panel.hidden = true;
      }
    });
  }

  closeAccordionAllExcept(activeTrigger) {
    this.triggers.forEach((trigger) => {
      if (trigger === activeTrigger) return;

      const panel = this.getPanelForTrigger(trigger);
      if (!panel) return;

      if (trigger.getAttribute("aria-expanded") === "true") {
        this.closeAccordion(trigger, panel);
      }
    });
  }

  onTransitionEnd(el, callback) {
    const handler = (e) => {
      if (e.target !== el || e.propertyName !== "height") return;
      el.removeEventListener("transitionend", handler);
      callback();
    };
    el.addEventListener("transitionend", handler);
  }
}

export function initAllAccordionBlocks() {
  document.querySelectorAll(SELECTORS.root).forEach((el) => {
    new AccordionBlock(el).init();
  });
}
