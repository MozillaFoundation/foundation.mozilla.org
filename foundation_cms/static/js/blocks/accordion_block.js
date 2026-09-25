const SELECTORS = {
  root: ".accordion-block__items",
  item: ".accordion-item",
  trigger: ".accordion-item__button",
  panel: ".accordion-item__panel",
};

// Used when the Cosmos motion tokens aren't loaded on the page.
const FALLBACK_MOTION = { duration: 300, easing: "ease-in-out" };

/**
 * Reads the height transition for opening ("expand") or closing ("collapse")
 * from LP's index-cards motion tokens, so the panel moves in step with the
 * row's background and icon transitions in accordion_block.scss.
 * Reduced motion gets a duration of 0.
 */
function getPanelMotion(panel, phase) {
  if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) {
    return { duration: 0, easing: FALLBACK_MOTION.easing };
  }

  const styles = getComputedStyle(panel);
  const duration = parseFloat(
    styles.getPropertyValue(`--mzf-motion-duration-index-cards-${phase}`),
  );
  const easing = styles
    .getPropertyValue(`--mzf-motion-easing-index-cards-${phase}`)
    .trim();

  return {
    duration: Number.isFinite(duration) ? duration : FALLBACK_MOTION.duration,
    easing: easing || FALLBACK_MOTION.easing,
  };
}

export class AccordionBlock {
  constructor(root) {
    this.root = root;
    this.triggers = root.querySelectorAll(SELECTORS.trigger);
  }

  init() {
    this.triggers.forEach((trigger) => {
      const panel = this.getPanelForTrigger(trigger);
      if (!panel) return;

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

    const { duration, easing } = getPanelMotion(panel, "expand");
    panel.style.transition = `height ${duration}ms ${easing}`;

    // No transition means no transitionend, so finish immediately
    if (duration === 0) {
      panel.style.height = "auto";
      return;
    }

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

    const { duration, easing } = getPanelMotion(panel, "collapse");
    panel.style.transition = `height ${duration}ms ${easing}`;

    // No transition means no transitionend, so finish immediately
    if (duration === 0) {
      panel.style.height = "0px";
      panel.hidden = true;
      return;
    }

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
