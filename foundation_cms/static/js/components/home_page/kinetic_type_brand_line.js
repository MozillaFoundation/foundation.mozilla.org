/**
 * CSS variable names used to control animation and layout behavior.
 */
const CSS_VARS = {
  lineHeightMultiplier: "--line-height-multiplier",
  animationDuration: "--animation-duration-in-ms",
};

/**
 * Fallback values used if CSS variables are missing or invalid.
 */
const FALLBACKS = {
  lineHeight: 1,
  animationDurationMs: 1000,
  pauseDurationMs: 3000,
};

/**
 * CSS selectors used to locate key DOM elements in the component.
 */
const SELECTORS = {
  phraseList: ".kinetic-brand-line__phrase-list",
  phraseWrapper: ".kinetic-brand-line__phrase-wrapper",
  root: ".kinetic-brand-line",
};

/**
 * Safely retrieves a float value from a CSS variable.
 * Logs a warning and returns a fallback if the variable is missing or invalid.
 *
 * @param {Element} element - The element to read the variable from.
 * @param {string} varName - The CSS variable name (e.g., "--line-height-multiplier").
 * @param {number} fallback - Fallback value if variable is not found or invalid.
 * @returns {number}
 */
const getCssVarFloat = (element, varName, fallback) => {
  const value = parseFloat(getComputedStyle(element).getPropertyValue(varName));
  if (isNaN(value)) {
    console.warn(
      `CSS variable ${varName} is missing or invalid. Using fallback: ${fallback}`
    );
    return fallback;
  }
  return value;
};

/**
 * Initializes a single rolling phrase list component.
 * Duplicates phrases for looping, applies transforms, and handles animation.
 *
 * @param {HTMLElement} phraseList - The element containing the list of phrases.
 */
export function initRollingPhrases(phraseList) {
  if (phraseList.dataset.initialized === "true") return;
  phraseList.dataset.initialized = "true";

  const phrases = Array.from(phraseList.children).filter(
    (el) => el.nodeType === Node.ELEMENT_NODE
  );
  if (!phrases.length) return;

  const root = phraseList.closest(SELECTORS.root);
  if (!root) return;

  const lineHeightMultiplier = getCssVarFloat(
    root,
    CSS_VARS.lineHeightMultiplier,
    FALLBACKS.lineHeight
  );

  const transitionDurationMs = getCssVarFloat(
    root,
    CSS_VARS.animationDuration,
    FALLBACKS.animationDurationMs
  );

  const pauseDurationMs = FALLBACKS.pauseDurationMs;

  phrases.forEach((phrase) => {
    const clone = phrase.cloneNode(true);
    phraseList.appendChild(clone);
  });

  const total = phrases.length;
  let index = 0;

  /**
   * Dynamically adjusts the wrapper width to match the current phrase.
   * Prevents layout shifts by locking the width after measurement.
   *
   * @param {HTMLElement} phrase - The currently visible phrase.
   */
  function updateWrapperWidth(phrase) {
    const phraseWrapper = phrase.closest(SELECTORS.phraseWrapper);
    if (!phraseWrapper) return;

    // Use requestAnimationFrame to safely read and write layout in the same frame.
    // Step-by-step:
    // 1. Temporarily reset the wrapper width to "auto" so we can measure the natural width of the current phrase.
    // 2. Measure the actual width of the phrase using offsetWidth (a layout read).
    // 3. Set the wrapper’s width explicitly to that measured value (a layout write).
    // This avoids layout thrashing by ensuring the read and write operations are batched
    // together at the start of the next animation frame, keeping animations smooth and performant.
    requestAnimationFrame(() => {
      phraseWrapper.style.width = "auto";
      const width = phrase.offsetWidth;
      phraseWrapper.style.width = `${width}px`;
    });
  }

  /**
   * Core animation loop that scrolls through phrases and triggers width updates.
   */
  function rollLoop() {
    index += 1;

    phraseList.style.transition = `transform ${transitionDurationMs}ms ease-in-out`;
    phraseList.style.transform = `translateY(-${index * lineHeightMultiplier}em)`;

    if (root.dataset.styleType === "3") {
      const visiblePhraseIndex = index % phrases.length;
      updateWrapperWidth(phrases[visiblePhraseIndex]);
    }

    setTimeout(() => {
      if (index >= total) {
        phraseList.style.transition = "none";
        phraseList.style.transform = "translateY(0)";
        index = 0;
      }

      setTimeout(rollLoop, pauseDurationMs);
    }, transitionDurationMs + 100);
  }

  // Respect user motion preferences
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setTimeout(rollLoop, pauseDurationMs);
  }
}

/**
 * Initializes all rolling phrase components on the page.
 */
export function initAllRollingPhrases() {
  document
    .querySelectorAll(`${SELECTORS.root} ${SELECTORS.phraseList}`)
    .forEach(initRollingPhrases);
}
