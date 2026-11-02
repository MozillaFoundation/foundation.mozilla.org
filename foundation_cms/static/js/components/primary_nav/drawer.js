import { CLASSNAMES, EVENTS, MOTION, SELECTORS } from "./config.js";
import {
  animateGridRows,
  prefersReducedMotion,
  readMotion,
  reflow,
} from "./motion.js";

/**
 * Controls the phone drawer opened by the menu button below LP's mobile
 * boundary. It folds open and closed with the same motion as the desktop
 * panel shell.
 */
export class NavDrawerController {
  /**
   * @param {HTMLElement} navEl
   */
  constructor(navEl) {
    this.navEl = navEl;
    this.drawerEl = navEl.querySelector(SELECTORS.drawer);
    this.revealEl = navEl.querySelector(SELECTORS.drawerReveal);
    this.innerEl = navEl.querySelector(SELECTORS.drawerInner);
    this.menuButtonEl = navEl.querySelector(SELECTORS.menuButton);
    this.closeTimer = null;
  }

  isOpen() {
    return this.navEl.classList.contains(CLASSNAMES.drawerOpen);
  }

  isClosing() {
    return this.closeTimer !== null;
  }

  toggle() {
    if (this.isOpen()) {
      this.close();
      return;
    }
    this.open();
  }

  open() {
    if (!this.drawerEl || this.isOpen() || this.isClosing()) return;

    document.dispatchEvent(new CustomEvent(EVENTS.primaryNavWillOpen));
    this.drawerEl.classList.remove(CLASSNAMES.drawerClosing);
    this.drawerEl.hidden = false;
    this.setMenuButtonExpanded(true);

    if (prefersReducedMotion()) {
      this.navEl.classList.add(CLASSNAMES.drawerOpen);
      return;
    }

    // Paint the closed drawer once so the open state transitions from it.
    reflow(this.drawerEl);
    requestAnimationFrame(() => {
      this.navEl.classList.add(CLASSNAMES.drawerOpen);
    });
  }

  /**
   * @param {{ returnFocus?: boolean, immediate?: boolean }} options -
   *   `returnFocus` moves focus back to the menu button, for keyboard
   *   dismissal. `immediate` skips the fold, for when the header's height
   *   must settle at once, such as before the search drawer measures it.
   */
  close({ returnFocus = false, immediate = false } = {}) {
    if (!this.drawerEl || this.drawerEl.hidden) return;
    if (this.isClosing() && !immediate) return;

    clearTimeout(this.closeTimer);
    this.setMenuButtonExpanded(false);

    const finish = () => {
      this.closeTimer = null;
      this.navEl.classList.remove(CLASSNAMES.drawerOpen);
      this.drawerEl.classList.remove(CLASSNAMES.drawerClosing);
      this.revealEl?.style.removeProperty("grid-template-rows");
      this.revealEl?.style.removeProperty("transition");
      this.drawerEl.hidden = true;
      if (returnFocus) this.menuButtonEl?.focus();
    };

    const startHeight = this.innerEl?.scrollHeight ?? 0;
    if (
      immediate ||
      prefersReducedMotion() ||
      !this.revealEl ||
      startHeight <= 0
    ) {
      finish();
      return;
    }

    // The rows fade out first, then the drawer folds after a short delay.
    this.drawerEl.classList.add(CLASSNAMES.drawerClosing);
    this.closeTimer = setTimeout(
      () => {
        this.revealEl.style.gridTemplateRows = `${startHeight}px`;
        this.revealEl.style.transition = "none";
        this.navEl.classList.remove(CLASSNAMES.drawerOpen);
        animateGridRows(
          this.revealEl,
          {
            from: `${startHeight}px`,
            to: "0px",
            duration: readMotion(this.navEl, MOTION.collapseDuration),
            easing: readMotion(this.navEl, MOTION.collapseEase),
          },
          () => {
            // An immediate close may have finished the drawer already.
            if (this.closeTimer !== null) finish();
          },
        );
      },
      readMotion(this.navEl, MOTION.collapseStartDelay),
    );
  }

  setMenuButtonExpanded(expanded) {
    if (!this.menuButtonEl) return;

    const { labelOpen, labelClose } = this.menuButtonEl.dataset;
    this.menuButtonEl.setAttribute("aria-expanded", String(expanded));
    const label = expanded ? labelClose : labelOpen;
    if (label) this.menuButtonEl.setAttribute("aria-label", label);
  }
}
