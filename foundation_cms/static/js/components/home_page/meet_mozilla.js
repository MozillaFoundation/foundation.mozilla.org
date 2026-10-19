// Changes the Meet Mozilla background as each step reaches the intro text. Based on
// the scroll script in components/blocks/sections/meet-mozilla/index.html in
// MozillaFoundation/mofo-lp-design-system, commit 0db3629dcf. Unlike LP's script,
// which switches at a fixed line 80% down the viewport, the line is the intro text's
// position (the middle of the viewport on mobile), as TP1-4382 asks.
//
// Without this script the section stays on its first state, --state-00.

/**
 * Elements the script reads. Steps without a state attribute are passed over.
 * @constant {Object}
 */
const SELECTORS = {
  root: "[data-mzf-meet-mozilla]",
  item: "[data-mzf-meet-mozilla-state]",
  label: ".mzf-c-big-label",
  aside: ".mzf-c-meet-mozilla__aside",
  intro: ".mzf-c-meet-mozilla__aside .mzf-c-text-group",
};

/**
 * LP's four states, in reading order. "00" is the section before the first step.
 * @constant {string[]}
 */
const STATES = ["00", "01", "02", "03"];

const STATE_CLASS_PREFIX = "mzf-c-meet-mozilla--state-";

/**
 * Where the line sits when the intro isn't sticky, as a share of the viewport height.
 * @constant {number}
 */
const STACKED_READING_LINE = 0.5;

/**
 * Finds the line a step has to reach to hand over its color: the top of the intro
 * text while it is sticky, otherwise the middle of the viewport.
 * @param {Element} root - The Meet Mozilla section
 * @param {number} viewportHeight - The viewport height in pixels
 * @returns {number} The line's distance from the top of the viewport, in pixels
 */
export function getReadingLine(root, viewportHeight) {
  const aside = root.querySelector(SELECTORS.aside);
  const intro = root.querySelector(SELECTORS.intro);

  if (aside && intro && getComputedStyle(aside).position === "sticky") {
    return intro.getBoundingClientRect().top;
  }

  return viewportHeight * STACKED_READING_LINE;
}

/**
 * Finds the state of the last step whose number and label have reached the line.
 * @param {Element[]} items - The steps that carry a state, in reading order
 * @param {number} line - The line's distance from the top of the viewport, in pixels
 * @returns {string} The state to show, "00" when no step has reached the line
 */
export function getCurrentState(items, line) {
  let current = STATES[0];

  items.forEach((item) => {
    const label = item.querySelector(SELECTORS.label) || item;
    if (label.getBoundingClientRect().top <= line) {
      current = item.dataset.mzfMeetMozillaState;
    }
  });

  return current;
}

/**
 * Puts the section on one state class and takes it off the others.
 * @param {Element} root - The Meet Mozilla section
 * @param {string} state - One of STATES
 */
export function setState(root, state) {
  STATES.forEach((value) => {
    root.classList.toggle(`${STATE_CLASS_PREFIX}${value}`, value === state);
  });
}

/**
 * Keeps one section's state in step with the scroll position. The line moves with
 * the intro, so the state is worked out on scroll rather than by an observer with a
 * fixed margin. Scroll and resize are only listened to while the section is on
 * screen, and updates are batched to one per animation frame.
 * @param {Element} root - The Meet Mozilla section
 * @returns {IntersectionObserver|null} The observer watching the section, or null
 *   when there is nothing to update
 */
export function initMeetMozilla(root) {
  const items = [...root.querySelectorAll(SELECTORS.item)];

  if (!items.length || typeof IntersectionObserver !== "function") {
    return null;
  }

  let frame = null;

  const update = () => {
    frame = null;
    const line = getReadingLine(root, window.innerHeight);
    setState(root, getCurrentState(items, line));
  };

  const scheduleUpdate = () => {
    if (frame === null) {
      frame = requestAnimationFrame(update);
    }
  };

  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      window.addEventListener("scroll", scheduleUpdate, { passive: true });
      window.addEventListener("resize", scheduleUpdate);
    } else {
      window.removeEventListener("scroll", scheduleUpdate);
      window.removeEventListener("resize", scheduleUpdate);
    }
    // Also settle the state on the way in and out, in case a fast scroll skipped
    // past the steps between two frames.
    scheduleUpdate();
  });

  observer.observe(root);
  return observer;
}

/**
 * Starts every Meet Mozilla section on the page.
 */
export function initAllMeetMozilla() {
  document.querySelectorAll(SELECTORS.root).forEach(initMeetMozilla);
}
