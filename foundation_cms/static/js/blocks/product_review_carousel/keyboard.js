import { CLASSNAMES, SELECTORS } from "./config.js";

/**
 * Button handler: toggle the user-controlled pause state.
 * @this {import("./carousel.js").default}
 */
export function onPauseToggle() {
  this.userPaused = !this.userPaused;
  this.updatePaused();
  this.updateButtonUI();
}

/**
 * Recompute the effective paused state and start/stop the RAF loop accordingly.
 * @this {import("./carousel.js").default}
 */
export function updatePaused() {
  const newPaused =
    this.userPaused ||
    this.hovered ||
    this.focusWithin ||
    document.hidden ||
    this._offscreen;

  if (newPaused === this.paused) return;

  this.paused = newPaused;
  this.lastTs = null;

  this.track.style.willChange = this.paused ? "auto" : "transform";

  if (this.paused && this.rafId != null) {
    cancelAnimationFrame(this.rafId);
    this.rafId = null;
  } else if (!this.paused && this.enabled && this.rafId == null) {
    this.rafId = requestAnimationFrame(this.boundTick);
  }
}

/**
 * Reflect pause state in the UI control (pressed state + accessible name).
 * @this {import("./carousel.js").default}
 */
export function updateButtonUI() {
  if (!this.pauseBtn) return;

  const isPaused = this.userPaused;

  this.pauseBtn.setAttribute("aria-pressed", String(isPaused));
  this.pauseBtn.setAttribute(
    "aria-label",
    isPaused ? gettext("Play carousel") : gettext("Pause carousel"),
  );

  this.pauseBtn.classList.toggle(CLASSNAMES.paused, isPaused);
}

/**
 * Pause when the pointer is over any card (ignores container whitespace).
 * @param {MouseEvent} e
 * @this {import("./carousel.js").default}
 */
export function onMouseOver(e) {
  if (e.target && e.target.closest(SELECTORS.productCard) && !this.hovered) {
    this.hovered = true;
    this.updatePaused();
  }
}

/**
 * Resume when the pointer leaves the cards entirely (not card-to-card moves).
 * @param {MouseEvent} e
 * @this {import("./carousel.js").default}
 */
export function onMouseOut(e) {
  const fromCard = e.target && e.target.closest(SELECTORS.productCard);
  if (!fromCard) return;

  const to = e.relatedTarget;
  const stillInCard =
    to && this.container.contains(to) && to.closest(SELECTORS.productCard);

  if (!stillInCard && this.hovered) {
    this.hovered = false;
    this.updatePaused();
  }
}

/**
 * Document visibility handler (hidden/visible): update pause state.
 * @this {import("./carousel.js").default}
 */
export function onVisibilityChange() {
  this.updatePaused();
}

/**
 * Keep autoplay paused while focus is inside the carousel.
 * @this {import("./carousel.js").default}
 */
export function onFocusIn() {
  if (!this.focusWithin) {
    this.focusWithin = true;
    this.refreshVisibleCardFocus(true);
    this.updatePaused();
  }
}

/**
 * Resume autoplay once focus leaves the carousel root entirely.
 * @param {FocusEvent} e
 * @this {import("./carousel.js").default}
 */
export function onFocusOut(e) {
  const to = e.relatedTarget;
  const stillWithin = to && this.root.contains(to);

  if (!stillWithin && this.focusWithin) {
    this.focusWithin = false;
    this.resetCardFocusability();
    this.updatePaused();
  }
}

/**
 * Keep visible-card focusability in sync as the user tabs within the carousel.
 * This handler is intentionally non-obtrusive: it does not prevent default.
 * @param {KeyboardEvent} e
 * @this {import("./carousel.js").default}
 */
export function onKeyDown(e) {
  if (e.key === "Tab" && this.focusWithin) {
    this.refreshVisibleCardFocus(true);
  }
}
