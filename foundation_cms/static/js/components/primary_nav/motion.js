/**
 * Motion helpers shared by the nav's panel shell, drawer and drawer rows.
 */

/**
 * @returns {boolean} Whether the reader asked for reduced motion.
 */
export function prefersReducedMotion() {
  return (
    window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false
  );
}

/**
 * Reads a motion custom property, falling back when it is unset.
 *
 * @param {Element} el
 * @param {[string, number | string]} token - Property name and fallback.
 * @returns {number | string} Milliseconds for a numeric fallback, else the raw value.
 */
export function readMotion(el, [property, fallback]) {
  const value = getComputedStyle(el).getPropertyValue(property).trim();
  if (typeof fallback !== "number") return value || fallback;

  const ms = parseFloat(value);
  return Number.isFinite(ms) ? ms : fallback;
}

/**
 * Forces a style flush so the next change transitions from the current state.
 *
 * @param {HTMLElement} el
 */
export function reflow(el) {
  void el.offsetHeight;
}

/**
 * Animates a grid reveal's rows between two sizes, then clears inline styles.
 *
 * @param {HTMLElement} revealEl
 * @param {{ from: string, to: string, duration: number, easing: string }} options
 * @param {() => void} done
 */
export function animateGridRows(
  revealEl,
  { from, to, duration, easing },
  done,
) {
  revealEl.style.gridTemplateRows = from;
  revealEl.style.transition = "none";
  reflow(revealEl);
  revealEl.style.transition = `grid-template-rows ${duration}ms ${easing}`;
  revealEl.style.gridTemplateRows = to;

  let finished = false;
  const finish = () => {
    if (finished) return;
    finished = true;
    revealEl.removeEventListener("transitionend", onEnd);
    clearTimeout(fallback);
    revealEl.style.removeProperty("grid-template-rows");
    revealEl.style.removeProperty("transition");
    done();
  };
  const onEnd = (event) => {
    if (event.target !== revealEl) return;
    if (event.propertyName !== "grid-template-rows") return;
    finish();
  };

  revealEl.addEventListener("transitionend", onEnd);
  // transitionend never fires if the transition is interrupted or skipped.
  const fallback = setTimeout(finish, duration + 32);
}
