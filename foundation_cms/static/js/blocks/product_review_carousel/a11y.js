const CARD_WRAPPER_SELECTOR = ".product-review-carousel__card-wrapper";
const FOCUSABLE_SELECTOR =
  "a[href], button, input, select, textarea, [tabindex]";
const DATA_MANAGED = "data-carousel-managed-tabindex";
const DATA_ORIGINAL = "data-carousel-original-tabindex";
const NO_TABINDEX = "__none__";
const FOCUS_REFRESH_THROTTLE_MS = 100;

/**
 * Restrict keyboard focus to cards currently visible in the viewport.
 * @param {boolean} [force=false]
 * @this {import("./carousel.js").default}
 */
export function refreshVisibleCardFocus(force = false) {
  if (!this.container || !this.track) return;

  const now = performance.now();
  const shouldThrottle =
    !force &&
    this._lastFocusRefreshTs != null &&
    now - this._lastFocusRefreshTs < FOCUS_REFRESH_THROTTLE_MS;

  if (shouldThrottle) return;
  this._lastFocusRefreshTs = now;

  if (!this.enabled) {
    this.resetCardFocusability();
    return;
  }

  const containerRect = this.container.getBoundingClientRect();
  const wrappers = this.track.querySelectorAll(CARD_WRAPPER_SELECTOR);

  wrappers.forEach((wrapper) => {
    const isVisible = this.isElementHorizontallyVisible(wrapper, containerRect);
    this.updateWrapperFocusability(wrapper, isVisible);
  });
}

/**
 * Restore all card links/controls to their original focusability.
 * @this {import("./carousel.js").default}
 */
export function resetCardFocusability() {
  if (!this.track) return;

  const wrappers = this.track.querySelectorAll(CARD_WRAPPER_SELECTOR);
  wrappers.forEach((wrapper) => this.updateWrapperFocusability(wrapper, true));
}

/**
 * Toggle a wrapper subtree as keyboard-focusable and screen-reader-visible.
 * @param {Element} wrapper
 * @param {boolean} isVisible
 * @this {import("./carousel.js").default}
 */
export function updateWrapperFocusability(wrapper, isVisible) {
  wrapper.setAttribute("aria-hidden", String(!isVisible));

  const focusables = wrapper.querySelectorAll(FOCUSABLE_SELECTOR);

  focusables.forEach((el) => {
    if (isVisible) {
      this.restoreOriginalTabIndex(el);
    } else {
      this.makeTemporarilyUntabbable(el);
    }
  });
}

/**
 * Check horizontal overlap between a card wrapper and the viewport container.
 * @param {Element} element
 * @param {DOMRect} containerRect
 * @returns {boolean}
 * @this {import("./carousel.js").default}
 */
export function isElementHorizontallyVisible(element, containerRect) {
  const rect = element.getBoundingClientRect();
  const overlapPx =
    Math.min(rect.right, containerRect.right) -
    Math.max(rect.left, containerRect.left);

  return overlapPx > 1;
}

/**
 * Save existing tab index state and remove from tab order for now.
 * @param {Element} element
 */
export function makeTemporarilyUntabbable(element) {
  if (element.getAttribute(DATA_MANAGED) !== "true") {
    const existingTabIndex = element.getAttribute("tabindex");
    element.setAttribute(
      DATA_ORIGINAL,
      existingTabIndex == null ? NO_TABINDEX : existingTabIndex,
    );
    element.setAttribute(DATA_MANAGED, "true");
  }

  element.setAttribute("tabindex", "-1");
}

/**
 * Restore tab index state previously saved by `makeTemporarilyUntabbable`.
 * @param {Element} element
 */
export function restoreOriginalTabIndex(element) {
  if (element.getAttribute(DATA_MANAGED) !== "true") return;

  const original = element.getAttribute(DATA_ORIGINAL);

  if (original && original !== NO_TABINDEX) {
    element.setAttribute("tabindex", original);
  } else {
    element.removeAttribute("tabindex");
  }

  element.removeAttribute(DATA_ORIGINAL);
  element.removeAttribute(DATA_MANAGED);
}
