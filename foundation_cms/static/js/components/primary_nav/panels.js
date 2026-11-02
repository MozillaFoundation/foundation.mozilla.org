import { CLASSNAMES, EVENTS, MOTION, SELECTORS } from "./config.js";
import {
  animateGridRows,
  prefersReducedMotion,
  readMotion,
  reflow,
} from "./motion.js";

/**
 * Controls the desktop panel shell: one shell holds every section's mega
 * menu. It opens on the first section, crossfades between sections while it
 * stays open, and folds away after its content fades on close.
 */
export class NavPanelsController {
  /**
   * @param {HTMLElement} navEl
   */
  constructor(navEl) {
    this.navEl = navEl;
    this.panelEl = navEl.querySelector(SELECTORS.panel);
    this.revealEl = navEl.querySelector(SELECTORS.panelReveal);
    this.innerEl = navEl.querySelector(SELECTORS.panelInner);
    this.stageEl = navEl.querySelector(SELECTORS.panelStage);
    this.triggerEls = [...navEl.querySelectorAll(SELECTORS.panelTrigger)];
    this.contentEls = [...navEl.querySelectorAll(SELECTORS.panelContent)];
    this.openKey = null;
    this.closeTimer = null;
    this.finishSwitch = null;
  }

  isOpen() {
    return this.openKey !== null;
  }

  isClosing() {
    return this.closeTimer !== null;
  }

  triggerFor(key) {
    return this.triggerEls.find((el) => el.dataset.navPanel === key) ?? null;
  }

  contentFor(key) {
    return (
      this.contentEls.find((el) => el.dataset.navPanelContent === key) ?? null
    );
  }

  setExpanded(key) {
    this.triggerEls.forEach((el) => {
      el.setAttribute("aria-expanded", String(el.dataset.navPanel === key));
    });
  }

  /**
   * Opens a section, switches to it, or closes it when it is already open.
   *
   * @param {string} key
   */
  toggle(key) {
    if (!this.panelEl || this.isClosing() || this.finishSwitch) return;

    const contentEl = this.contentFor(key);
    if (!contentEl) return;

    if (this.openKey === key) {
      this.close();
    } else if (this.isOpen()) {
      this.switchTo(key, contentEl);
    } else {
      this.open(key, contentEl);
    }
  }

  open(key, contentEl) {
    document.dispatchEvent(new CustomEvent(EVENTS.primaryNavWillOpen));

    this.contentEls.forEach((el) => {
      if (el !== contentEl) resetContent(el);
    });
    contentEl.hidden = false;
    contentEl.classList.add(CLASSNAMES.contentActive);
    this.panelEl.classList.remove(CLASSNAMES.panelOpen);
    this.panelEl.hidden = false;
    this.openKey = key;
    this.setExpanded(key);

    if (prefersReducedMotion()) {
      this.panelEl.classList.add(CLASSNAMES.panelOpen);
      return;
    }

    // Paint the closed shell once so the open state transitions from it.
    reflow(this.panelEl);
    requestAnimationFrame(() => {
      if (this.openKey !== key) return;
      this.panelEl.classList.add(CLASSNAMES.panelOpen);
    });
  }

  switchTo(key, toEl) {
    const fromEl = this.contentFor(this.openKey);
    this.openKey = key;
    this.setExpanded(key);

    if (!fromEl || prefersReducedMotion()) {
      if (fromEl) resetContent(fromEl);
      toEl.hidden = false;
      toEl.classList.add(CLASSNAMES.contentActive);
      return;
    }

    // Pin the stage at its current height, then ease it to the new section's
    // height while the two sections crossfade.
    const startHeight = this.stageEl.offsetHeight;
    const targetHeight = measureHidden(toEl);
    this.stageEl.style.transition = "none";
    this.stageEl.style.blockSize = `${startHeight}px`;
    reflow(this.stageEl);

    this.navEl.classList.add(CLASSNAMES.switching);
    toEl.hidden = false;
    fromEl.classList.add(CLASSNAMES.contentSwapOut);
    toEl.classList.add(CLASSNAMES.contentSwapIn);
    reflow(this.stageEl);

    this.stageEl.style.removeProperty("transition");
    if (targetHeight > 0) this.stageEl.style.blockSize = `${targetHeight}px`;
    reflow(this.stageEl);
    this.navEl.classList.add(CLASSNAMES.swapActive);

    const timer = setTimeout(
      () => this.finishSwitch?.(),
      readMotion(this.navEl, MOTION.swapDuration) + 16,
    );
    this.finishSwitch = () => {
      clearTimeout(timer);
      this.finishSwitch = null;
      resetContent(fromEl);
      toEl.classList.remove(CLASSNAMES.contentSwapIn);
      toEl.classList.add(CLASSNAMES.contentActive);
      this.clearSwitching();
    };
  }

  clearSwitching() {
    this.navEl.classList.remove(CLASSNAMES.switching, CLASSNAMES.swapActive);
    this.stageEl?.style.removeProperty("block-size");
    this.stageEl?.style.removeProperty("transition");
  }

  /**
   * @param {{ returnFocus?: boolean }} options - Return focus to the section's
   *   trigger, for keyboard dismissal.
   */
  close({ returnFocus = false } = {}) {
    if (!this.isOpen() || this.isClosing()) return;

    const triggerEl = this.triggerFor(this.openKey);
    this.finishSwitch?.();
    this.openKey = null;
    this.setExpanded(null);

    const finish = () => {
      this.closeTimer = null;
      this.panelEl.classList.remove(
        CLASSNAMES.panelOpen,
        CLASSNAMES.panelClosing,
      );
      this.panelEl.hidden = true;
      this.contentEls.forEach(resetContent);
      if (returnFocus) triggerEl?.focus();
    };

    const startHeight = this.innerEl?.scrollHeight ?? 0;
    if (prefersReducedMotion() || !this.revealEl || startHeight <= 0) {
      finish();
      return;
    }

    // Like LP's index cards: the content fades out first, then the shell
    // folds away after a short delay, so the two overlap.
    this.panelEl.classList.add(CLASSNAMES.panelClosing);
    this.closeTimer = setTimeout(
      () => {
        this.revealEl.style.gridTemplateRows = `${startHeight}px`;
        this.revealEl.style.transition = "none";
        this.panelEl.classList.remove(CLASSNAMES.panelOpen);
        animateGridRows(
          this.revealEl,
          {
            from: `${startHeight}px`,
            to: "0px",
            duration: readMotion(this.navEl, MOTION.collapseDuration),
            easing: readMotion(this.navEl, MOTION.collapseEase),
          },
          finish,
        );
      },
      readMotion(this.navEl, MOTION.collapseStartDelay),
    );
  }
}

/**
 * @param {HTMLElement} contentEl
 */
function resetContent(contentEl) {
  contentEl.classList.remove(
    CLASSNAMES.contentActive,
    CLASSNAMES.contentSwapOut,
    CLASSNAMES.contentSwapIn,
  );
  contentEl.hidden = true;
}

/**
 * Measures a hidden section's height without showing it.
 *
 * @param {HTMLElement} contentEl
 * @returns {number}
 */
function measureHidden(contentEl) {
  const measuringStyles = {
    visibility: "hidden",
    position: "absolute",
    insetInlineStart: "0",
    insetBlockStart: "0",
    inlineSize: "100%",
  };
  const wasHidden = contentEl.hidden;
  contentEl.hidden = false;
  Object.assign(contentEl.style, measuringStyles);
  const height = contentEl.offsetHeight;
  Object.keys(measuringStyles).forEach((property) => {
    contentEl.style[property] = "";
  });
  contentEl.hidden = wasHidden;
  return height;
}
