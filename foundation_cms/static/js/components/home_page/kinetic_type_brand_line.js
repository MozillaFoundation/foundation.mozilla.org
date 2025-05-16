const CSS_VARS = {
  lineHeightMultiplier: "--line-height-multiplier",
  animationDuration: "--animation-duration-in-ms",
};

const FALLBACKS = {
  lineHeight: 1,
  animationDurationMs: 1000,
  pauseDurationMs: 3000,
};

const SELECTORS = {
  phraseList: ".kinetic-brand-line__phrase-list",
  phraseWrapper: ".kinetic-brand-line__phrase-wrapper",
  root: ".kinetic-brand-line",
};

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

export function initRollingPhrases(phraseList) {
  if (phraseList.dataset.initialized === "true") return;
  phraseList.dataset.initialized = "true";

  const phrases = Array.from(phraseList.children).filter(
    (el) => el.nodeType === Node.ELEMENT_NODE,
  );
  if (!phrases.length) return;

  const root = phraseList.closest(SELECTORS.root);
  if (!root) return;

  const lineHeightMultiplier = getCssVarFloat(
    root,
    CSS_VARS.lineHeightMultiplier,
    FALLBACKS.lineHeight,
  );

  const transitionDurationMs = getCssVarFloat(
    root,
    CSS_VARS.animationDuration,
    FALLBACKS.animationDurationMs,
  );

  const pauseDurationMs = FALLBACKS.pauseDurationMs;

  phrases.forEach((phrase) => {
    const clone = phrase.cloneNode(true);
    phraseList.appendChild(clone);
  });

  const total = phrases.length;
  let index = 0;

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

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setTimeout(rollLoop, pauseDurationMs);
  }
}

export function initAllRollingPhrases() {
  document
    .querySelectorAll(`${SELECTORS.root} ${SELECTORS.phraseList}`)
    .forEach(initRollingPhrases);
}
