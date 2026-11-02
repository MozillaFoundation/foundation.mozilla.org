import { CLASSNAMES, MOTION, SELECTORS } from "./config.js";
import {
  animateGridRows,
  prefersReducedMotion,
  readMotion,
  reflow,
} from "./motion.js";

/**
 * Animates the drawer's section rows open and closed. The rows are native
 * <details> sharing a `name`, so they open from the keyboard and stay
 * exclusive without script; this only adds LP's fold, and closes an open row
 * with that fold before the next one opens.
 *
 * @param {HTMLElement} scopeEl
 */
export function initDisclosures(scopeEl) {
  const disclosureEls = [...scopeEl.querySelectorAll(SELECTORS.disclosure)];

  disclosureEls.forEach((detailsEl) => {
    const summaryEl = detailsEl.querySelector(SELECTORS.disclosureSummary);
    if (!summaryEl) return;

    summaryEl.addEventListener("click", (event) => {
      if (prefersReducedMotion()) return;
      event.preventDefault();

      if (detailsEl.open) {
        closeDisclosure(detailsEl);
        return;
      }

      const openEls = disclosureEls.filter((el) => el !== detailsEl && el.open);
      let pending = openEls.length;
      if (!pending) {
        openDisclosure(detailsEl);
        return;
      }

      openEls.forEach((el) =>
        closeDisclosure(el, () => {
          pending -= 1;
          if (pending === 0) openDisclosure(detailsEl);
        }),
      );
    });
  });
}

/**
 * @param {HTMLDetailsElement} detailsEl
 */
function openDisclosure(detailsEl) {
  const revealEl = detailsEl.querySelector(SELECTORS.disclosureReveal);
  if (!revealEl) {
    detailsEl.open = true;
    return;
  }

  // Hold the reveal shut while [open] lands, or the first open paints at full
  // height before it animates.
  revealEl.style.gridTemplateRows = "0fr";
  revealEl.style.transition = "none";
  reflow(revealEl);
  detailsEl.open = true;

  animateGridRows(
    revealEl,
    {
      from: "0fr",
      to: "1fr",
      duration: readMotion(detailsEl, MOTION.disclosureExpandDuration),
      easing: readMotion(detailsEl, MOTION.disclosureExpandEase),
    },
    () => {},
  );
}

/**
 * Fades the row's content, folds it, and then removes [open].
 *
 * @param {HTMLDetailsElement} detailsEl
 * @param {() => void} [done]
 */
function closeDisclosure(detailsEl, done = () => {}) {
  if (
    !detailsEl.open ||
    detailsEl.classList.contains(CLASSNAMES.disclosureClosing)
  ) {
    done();
    return;
  }

  const closeDuration = Math.max(
    readMotion(detailsEl, MOTION.disclosureContentOutDuration),
    readMotion(detailsEl, MOTION.disclosureCollapseStartDelay) +
      readMotion(detailsEl, MOTION.disclosureCollapseDuration),
  );

  detailsEl.classList.add(CLASSNAMES.disclosureClosing);
  setTimeout(() => {
    detailsEl.open = false;
    detailsEl.classList.remove(CLASSNAMES.disclosureClosing);
    done();
  }, closeDuration + 32);
}
