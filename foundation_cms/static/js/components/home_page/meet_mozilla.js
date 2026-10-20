// Scroll behavior for Meet Mozilla, based on LP's script
// (components/blocks/sections/meet-mozilla/index.html in
// MozillaFoundation/mofo-lp-design-system, commit 0db3629dcf), which only changes the
// background. We add, per TP1-4382: the heading and statements light up word by word,
// and on desktop each statement pins beside the intro while it fills.
//
// Without this script, nothing pins and all text stays fully inked. With reduced
// motion it does nothing, and our styles show each step as a static color band.

/**
 * Elements the script reads. Steps without a state attribute are passed over.
 * @constant {Object}
 */
const SELECTORS = {
  root: "[data-mzf-meet-mozilla]",
  item: "[data-mzf-meet-mozilla-state]",
  step: ".mzf-c-meet-mozilla__item",
  content: ".mzf-c-biglabel-h2",
  label: ".mzf-c-big-label",
  statement: ".mzf-c-meet-mozilla__statement",
  heading: ".mzf-c-text-group--h1 .mzf-c-text-group__heading",
  aside: ".mzf-c-meet-mozilla__aside",
  introHeading: ".mzf-c-meet-mozilla__aside .mzf-c-text-group__heading",
};

/**
 * LP's four states, in reading order. "00" is the section before the first step.
 * @constant {string[]}
 */
const STATES = ["00", "01", "02", "03"];

const STATE_CLASS_PREFIX = "mzf-c-meet-mozilla--state-";

/**
 * Turns on the pinned layout in our styles (meet_mozilla_block.scss).
 * @constant {string}
 */
const PINNED_CLASS = "mzf-c-meet-mozilla--pinned";

/**
 * LP's class for the half-strength ink of words the reader hasn't reached yet.
 * @constant {string}
 */
const UNREAD_CLASS = "mzf-c-meet-mozilla__unread";

/**
 * Where the first step's color arrives, as a share of the viewport height: LP's 80%
 * when pinned, the middle when stacked.
 * @constant {Object}
 */
const COLOR_LINE = { pinned: 0.8, stacked: 0.5 };

/**
 * How far the page scrolls while a statement fills, as a share of the viewport
 * height. On desktop the statement stays pinned for this plus HOLD_DISTANCE.
 * @constant {number}
 */
const FILL_DISTANCE = 0.35;

/**
 * How far the page scrolls with a pinned statement fully lit before the next color
 * comes in and the statement moves on, as a share of the viewport height.
 * @constant {number}
 */
const HOLD_DISTANCE = 0.1;

/**
 * Where the section heading's bottom edge is when it is fully lit, as a share of the
 * viewport height, so the reader sees it finish before it scrolls away.
 * @constant {number}
 */
const HEADING_FILL_END = 0.5;

/**
 * Whether the steps should pin: only while the intro is sticky (desktop).
 * @param {Element} root - The Meet Mozilla section
 * @returns {boolean}
 */
export function shouldPin(root) {
  const aside = root.querySelector(SELECTORS.aside);
  return Boolean(aside) && getComputedStyle(aside).position === "sticky";
}

/**
 * Where step content sticks so its statement sits level with the intro heading, in
 * pixels from the viewport top.
 * @param {Element} root - The Meet Mozilla section
 * @param {Element} content - A step's content (big label and statement)
 * @returns {number} The sticky offset in pixels
 */
export function getPinTop(root, content) {
  const aside = root.querySelector(SELECTORS.aside);
  const heading = root.querySelector(SELECTORS.introHeading);
  const statement = content.querySelector(SELECTORS.statement);

  if (!aside || !heading || !statement) {
    return 0;
  }

  const headingOffset =
    heading.getBoundingClientRect().top - aside.getBoundingClientRect().top;
  const statementOffset =
    statement.getBoundingClientRect().top - content.getBoundingClientRect().top;

  return headingOffset - statementOffset;
}

/**
 * Finds the state of the last step whose label has reached the line.
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
 * Finds the state while the steps pin: the first step's color arrives when its label
 * reaches the line, and each later step's once the step before it is done (fully lit
 * and held).
 * @param {{label: Element, state: ?string, done: boolean}[]} steps - Every step in
 *   reading order, with its state (null when it carries none) and whether it is done
 * @param {number} line - The first step's line, in pixels from the top of the viewport
 * @returns {string} The state to show, "00" before the first step arrives
 */
export function getPinnedState(steps, line) {
  let current = STATES[0];

  steps.forEach(({ label, state }, index) => {
    const arrived =
      index === 0
        ? label.getBoundingClientRect().top <= line
        : steps[index - 1].done;
    if (arrived && state) {
      current = state;
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
 * Wraps each word of an element's text in a span, keeping the spaces between them as
 * plain text, so the sentence still reads as one string.
 * @param {Element} element - An element holding plain text, such as a statement
 * @returns {HTMLSpanElement[]} The word spans, in reading order
 */
export function splitIntoWords(element) {
  const parts = element.textContent.split(/(\s+)/).filter(Boolean);
  const words = [];

  element.textContent = "";
  parts.forEach((part) => {
    if (/^\s+$/.test(part)) {
      element.append(part);
      return;
    }
    const word = document.createElement("span");
    word.textContent = part;
    element.append(word);
    words.push(word);
  });

  return words;
}

/**
 * Turns the distance scrolled since a fill began into the share of words to light.
 * @param {number} travelled - Pixels scrolled since the fill began; negative before it
 * @param {number} distance - Pixels it takes to light every word
 * @returns {number} The share of words to light, from 0 to 1
 */
export function getFillProgress(travelled, distance) {
  if (distance <= 0) {
    return travelled >= 0 ? 1 : 0;
  }

  return Math.min(1, Math.max(0, travelled / distance));
}

/**
 * Works out how much of the section heading is lit: none until it is fully on screen,
 * all of it once its bottom edge reaches the middle of the viewport, and always all
 * of it once the first step's color has arrived.
 * @param {number} headingBottom - The heading's bottom edge, in pixels from the top
 *   of the viewport
 * @param {number} firstLabelTop - The first step's label, in pixels from the top of
 *   the viewport
 * @param {number} line - Where the first step's color arrives, in pixels from the top
 *   of the viewport
 * @param {number} viewportHeight - The viewport height in pixels
 * @returns {number} The share of words to light, from 0 to 1
 */
export function getHeadingProgress(
  headingBottom,
  firstLabelTop,
  line,
  viewportHeight,
) {
  if (firstLabelTop <= line) {
    return 1;
  }

  return getFillProgress(
    viewportHeight - headingBottom,
    viewportHeight * (1 - HEADING_FILL_END),
  );
}

/**
 * Lights the first share of a statement's words and dims the rest.
 * @param {HTMLSpanElement[]} words - The statement's word spans
 * @param {number} progress - The share of words to light, from 0 to 1
 */
export function setFill(words, progress) {
  const lit = Math.round(progress * words.length);

  words.forEach((word, index) => {
    word.classList.toggle(UNREAD_CLASS, index >= lit);
  });
}

/**
 * Sets or clears (null) a length custom property, skipping unchanged values since this
 * runs every scroll frame.
 * @param {HTMLElement} root - The Meet Mozilla section
 * @param {string} name - The custom property's name
 * @param {number|null} value - The length in pixels, or null to clear it
 */
export function setLength(root, name, value) {
  const next = value === null ? "" : `${value}px`;

  if (root.style.getPropertyValue(name) === next) {
    return;
  }
  if (next) {
    root.style.setProperty(name, next);
  } else {
    root.style.removeProperty(name);
  }
}

/**
 * Drives one section's state, pinning and fills from the scroll position. Listens only
 * while the section is on screen, one update per frame.
 * @param {Element} root - The Meet Mozilla section
 * @returns {IntersectionObserver|null} The observer watching the section, or null
 *   when there is nothing to update
 */
export function initMeetMozilla(root) {
  const reduceMotion = window.matchMedia?.(
    "(prefers-reduced-motion: reduce)",
  )?.matches;

  if (reduceMotion || typeof IntersectionObserver !== "function") {
    return null;
  }

  const items = [...root.querySelectorAll(SELECTORS.item)];
  const firstLabel = root.querySelector(`${SELECTORS.step} ${SELECTORS.label}`);
  const fills = [...root.querySelectorAll(SELECTORS.step)]
    .map((step) => {
      const statement = step.querySelector(SELECTORS.statement);
      return {
        step,
        content: step.querySelector(SELECTORS.content) || step,
        label: step.querySelector(SELECTORS.label) || step,
        // Read once: the step's top padding doesn't change while scrolling.
        paddingTop: parseFloat(getComputedStyle(step).paddingTop) || 0,
        words: statement ? splitIntoWords(statement) : [],
      };
    })
    .filter((fill) => fill.words.length);
  const heading = root.querySelector(SELECTORS.heading);
  const headingWords = heading && firstLabel ? splitIntoWords(heading) : [];

  if (!items.length && !fills.length && !headingWords.length) {
    return null;
  }

  let frame = null;

  const update = () => {
    frame = null;
    const viewportHeight = window.innerHeight;
    const distance = viewportHeight * FILL_DISTANCE;
    const hold = viewportHeight * HOLD_DISTANCE;

    // Layout first (writes skipped when unchanged).
    const pinned = fills.length > 0 && shouldPin(root);
    const pinTop = pinned ? getPinTop(root, fills[0].content) : null;
    root.classList.toggle(PINNED_CLASS, pinned);
    setLength(root, "--mzf-meet-mozilla-pin-top", pinTop);
    setLength(
      root,
      "--mzf-meet-mozilla-pin-distance",
      pinned ? distance + hold : null,
    );
    const colorLine =
      viewportHeight * (pinned ? COLOR_LINE.pinned : COLOR_LINE.stacked);

    // Then read every position, before any class changes.
    const headingProgress = headingWords.length
      ? getHeadingProgress(
          heading.getBoundingClientRect().bottom,
          firstLabel.getBoundingClientRect().top,
          colorLine,
          viewportHeight,
        )
      : 0;
    let state = null;
    let progresses;

    if (pinned) {
      const steps = fills.map(({ step, label, paddingTop }) => {
        // Where the content would be if it weren't pinned: the top of the step's
        // content box. The fill begins when that reaches the pin.
        const naturalTop = step.getBoundingClientRect().top + paddingTop;
        const travelled = pinTop - naturalTop;
        return {
          label,
          state: step.dataset.mzfMeetMozillaState || null,
          travelled,
          done: travelled >= distance + hold,
        };
      });
      state = getPinnedState(steps, colorLine);
      progresses = steps.map(({ travelled }) =>
        getFillProgress(travelled, distance),
      );
    } else {
      if (items.length) {
        state = getCurrentState(items, colorLine);
      }
      progresses = fills.map(({ label }) =>
        getFillProgress(
          colorLine - label.getBoundingClientRect().top,
          distance,
        ),
      );
    }

    // Last, apply the classes.
    if (headingWords.length) {
      setFill(headingWords, headingProgress);
    }
    fills.forEach(({ words }, index) => setFill(words, progresses[index]));
    if (state) {
      setState(root, state);
    }
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
    // Also settle everything on the way in and out, in case a fast scroll skipped
    // past the steps between two frames.
    scheduleUpdate();
  });

  // Set the layout up straight away, so adding the pin room never shifts the page
  // after the reader has started scrolling.
  update();
  observer.observe(root);
  return observer;
}

/**
 * Starts every Meet Mozilla section on the page.
 */
export function initAllMeetMozilla() {
  document.querySelectorAll(SELECTORS.root).forEach(initMeetMozilla);
}
