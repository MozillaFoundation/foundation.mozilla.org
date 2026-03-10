import {
  SELECTORS,
  DATA_MANAGED_TABINDEX,
  DATA_ORIGINAL_TABINDEX,
  NO_TABINDEX,
  FOCUS_REFRESH_THROTTLE_MS,
} from "./config.js";

/**
 * Restrict keyboard focus to cards currently visible in the viewport.
 * @param {boolean} [force=false]
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
  const wrappers = this.track.querySelectorAll(SELECTORS.cardWrapper);

  wrappers.forEach((wrapper) => {
    const isVisible = this.isElementHorizontallyVisible(wrapper, containerRect);
    this.updateWrapperFocusability(wrapper, isVisible);
  });
}

/**
 * Restore all card links/controls to their original focusability.
 */
export function resetCardFocusability() {
  if (!this.track) return;

  const wrappers = this.track.querySelectorAll(SELECTORS.cardWrapper);
  wrappers.forEach((wrapper) => this.updateWrapperFocusability(wrapper, true));
}

/**
 * Toggle a wrapper subtree as keyboard-focusable and screen-reader-visible.
 * @param {Element} wrapper
 * @param {boolean} isVisible
 */
export function updateWrapperFocusability(wrapper, isVisible) {
  wrapper.setAttribute("aria-hidden", String(!isVisible));

  const focusables = wrapper.querySelectorAll(SELECTORS.focusable);

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
  if (element.getAttribute(DATA_MANAGED_TABINDEX) !== "true") {
    const existingTabIndex = element.getAttribute("tabindex");
    element.setAttribute(
      DATA_ORIGINAL_TABINDEX,
      existingTabIndex == null ? NO_TABINDEX : existingTabIndex,
    );
    element.setAttribute(DATA_MANAGED_TABINDEX, "true");
  }

  element.setAttribute("tabindex", "-1");
}

/**
 * Restore tab index state previously saved by `makeTemporarilyUntabbable`.
 * @param {Element} element
 */
export function restoreOriginalTabIndex(element) {
  if (element.getAttribute(DATA_MANAGED_TABINDEX) !== "true") return;

  const original = element.getAttribute(DATA_ORIGINAL_TABINDEX);

  if (original && original !== NO_TABINDEX) {
    element.setAttribute("tabindex", original);
  } else {
    element.removeAttribute("tabindex");
  }

  element.removeAttribute(DATA_ORIGINAL_TABINDEX);
  element.removeAttribute(DATA_MANAGED_TABINDEX);
}
