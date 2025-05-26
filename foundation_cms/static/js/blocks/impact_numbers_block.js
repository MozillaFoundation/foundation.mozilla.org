/**
 * Create a span element to display a digit or character.
 * @param {string} char - The character to display (digit, comma, period, etc.).
 * @returns {HTMLSpanElement}
 */
function createDigitElement(char) {
  const digitSpanElement = document.createElement("span");
  digitSpanElement.textContent = char;
  return digitSpanElement;
}

/**
 * Return a random digit string between 0–9.
 * @returns {string}
 */
function randomDigit() {
  return Math.floor(Math.random() * 10).toString();
}

/**
 * Handles the rolling digit animation for one impact stat block.
 */
export class AnimatedImpactNumber {
  /**
   * @param {HTMLElement} impactStatValueWrapper - The element with data-number and .impact-stat__animated-value span.
   */
  constructor(impactStatValueWrapper) {
    this.impactStatValueWrapper = impactStatValueWrapper;
    this.numberString = impactStatValueWrapper.dataset.number || "";
    this.numberValueSpan = impactStatValueWrapper.querySelector(
      ".impact-stat__animated-value",
    );
    this.animationDuration = 1500;
    this.frameRate = 30;
    this.frameInterval = 1000 / this.frameRate;
    this.digitElements = [];
  }

  /**
   * Builds and inserts digit <span> elements into the DOM with randomized starting characters.
   */
  initDigits() {
    this.numberValueSpan.innerHTML = "";

    for (const char of this.numberString) {
      // Check if the character is a numerical digit
      const isDigit = /\d/.test(char);
      // If it's a digit, start with a random digit; otherwise, use the character itself
      const initialChar = isDigit ? randomDigit() : char;
      // Create a span element for the digit or character.
      const digitSpan = createDigitElement(initialChar);
      this.numberValueSpan.appendChild(digitSpan);
      // Store the span and its final character for later use.
      this.digitElements.push({ el: digitSpan, final: char });
    }
  }

  /**
   * Starts the digit animation loop and updates DOM until complete.
   */
  animate() {
    this.initDigits();
    const startTime = performance.now();

    const updateFrame = (currentTime) => {
      const timeElapsed = currentTime - startTime;

      // If the animation is still in progress, keep updating digits
      if (timeElapsed < this.animationDuration) {
        for (const digit of this.digitElements) {
          const isDigit = /\d/.test(digit.final);

          // Randomize the digit if it's a number
          if (isDigit) {
            digit.el.textContent = randomDigit();
          } else {
            // Keep non-numeric characters static (e.g., commas, periods)
            digit.el.textContent = digit.final;
          }
        }

        // Schedule the next update frame
        setTimeout(
          () => requestAnimationFrame(updateFrame),
          this.frameInterval,
        );
      } else {
        // Final frame — replace all characters with their actual values
        for (const digit of this.digitElements) {
          digit.el.textContent = digit.final;
        }
      }
    };

    // Begin the animation by requesting the first frame
    requestAnimationFrame(updateFrame);
  }
}

/**
 * Initializes all impact stat animations when scrolled into view.
 */
export function initAllAnimatedImpactNumbers() {
  const impactStatValueWrappers = document.querySelectorAll(
    ".impact-stat__value-wrapper",
  );

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const impactStatValueWrapper = entry.target;
          const hasNumber = impactStatValueWrapper.dataset.number;

          if (!impactStatValueWrapper.dataset.animated && hasNumber) {
            new AnimatedImpactNumber(impactStatValueWrapper).animate();
            impactStatValueWrapper.dataset.animated = "true";
          }

          obs.unobserve(impactStatValueWrapper);
        }
      });
    },
    { threshold: 0.4 },
  );

  impactStatValueWrappers.forEach((impactStatValueWrapper) => {
    observer.observe(impactStatValueWrapper);
  });
}
