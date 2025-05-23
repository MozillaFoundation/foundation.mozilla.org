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
  root: ".kinetic-type-brand-line",
  phraseList: ".kinetic-type-brand-line__phrase-list",
  phraseWrapper: ".kinetic-type-brand-line__phrase-wrapper",
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
      `CSS variable ${varName} is missing or invalid. Using fallback: ${fallback}`,
    );
    return fallback;
  }
  return value;
};

/**
 * Animates a vertically rolling sequence of short phrases,
 * using CSS transforms and dynamic resizing to fit the text.
 */
export class KineticTypeBrandLine {
  /**
   * @param {HTMLElement} root - The root element of the rolling phrase component.
   */
  constructor(root) {
    this.root = root;
    this.phraseList = root.querySelector(SELECTORS.phraseList);
    this.index = 0;
    this.timer = null;
    this.initialized = false;
  }

  /**
   * Initializes the component, sets up phrases, clones, and starts the loop.
   */
  init() {
    if (
      !this.root ||
      !this.phraseList ||
      this.phraseList.dataset.initialized === "true"
    )
      return;
    this.phraseList.dataset.initialized = "true";

    this.phrases = Array.from(this.phraseList.children).filter(
      (el) => el.nodeType === Node.ELEMENT_NODE,
    );
    if (!this.phrases.length) return;

    this.lineHeightMultiplier = getCssVarFloat(
      this.root,
      CSS_VARS.lineHeightMultiplier,
      FALLBACKS.lineHeight,
    );

    this.transitionDurationMs = getCssVarFloat(
      this.root,
      CSS_VARS.animationDuration,
      FALLBACKS.animationDurationMs,
    );

    this.pauseDurationMs = FALLBACKS.pauseDurationMs;

    // Duplicate phrases for looping
    this.phrases.forEach((phrase) => {
      const clone = phrase.cloneNode(true);
      this.phraseList.appendChild(clone);
    });

    this.total = this.phrases.length;

    // Respect user motion preferences
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      this.timer = setTimeout(() => this.rollLoop(), this.pauseDurationMs);
    }
  }

  /**
   * Core animation loop that scrolls through phrases and triggers width updates.
   */
  rollLoop() {
    this.index += 1;

    this.phraseList.style.transition = `transform ${this.transitionDurationMs}ms ease-in-out`;
    this.phraseList.style.transform = `translateY(-${this.index * this.lineHeightMultiplier}em)`;

    setTimeout(() => {
      if (this.index >= this.total) {
        this.phraseList.style.transition = "none";
        this.phraseList.style.transform = "translateY(0)";
        this.index = 0;
      }

      this.timer = setTimeout(() => this.rollLoop(), this.pauseDurationMs);
    }, this.transitionDurationMs + 100);
  }

  /**
   * Cleans up animation loop and state.
   */
  destroy() {
    clearTimeout(this.timer);
    if (this.phraseList) {
      this.phraseList.dataset.initialized = "false";
    }
  }
}

/**
 * Initializes all rolling phrase components on the page.
 */
export function initAllRollingPhrases() {
  document
    .querySelectorAll(SELECTORS.root)
    .forEach((el) => new RollingPhrases(el).init());
}
