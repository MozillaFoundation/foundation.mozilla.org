export const SWIPE_THRESHOLD = 50;
export const RESIZE_DEBOUNCE_MS = 200;

/**
 * Returns the 0-based logical index within the original card set.
 * Handles negative indices correctly for backwards navigation.
 * @param {number} index - The current (possibly cloned) track index
 * @param {number} total - The total number of original cards
 * @returns {number} A value in the range [0, total - 1]
 */
export function getLogicalIndex(index, total) {
  return ((index % total) + total) % total;
}

/**
 * Builds a DocumentFragment with a tripled set of cards for infinite scroll.
 * The order is: [clones] [originals] [clones]
 *
 * Having clones before and after the originals allows the carousel to silently
 * jump back to the middle set when the user scrolls past either end,
 * making the loop appear seamless.
 *
 * @param {HTMLElement[]} originalCards - The original set of card elements
 * @returns {DocumentFragment}
 */
export function tripleCards(originalCards) {
  const fragment = document.createDocumentFragment();

  originalCards.forEach((card) => fragment.appendChild(card.cloneNode(true)));
  originalCards.forEach((card) => fragment.appendChild(card));
  originalCards.forEach((card) => fragment.appendChild(card.cloneNode(true)));

  return fragment;
}

/**
 * Returns a debounced version of the given function.
 * @param {Function} fn - The function to debounce
 * @param {number} ms - Delay in milliseconds
 * @returns {Function}
 */
export function debounce(fn, ms) {
  let timer;

  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}
