/**
 * Initializes count-up animation when an ImpactNumberBlock's stat number enters the viewport.
 */

const SELECTORS = {
  statContainer: ".impact-stat__number",
  countUpValue: "[data-impact-stat-count-up]",
};

const COUNT_UP_DURATION_MS = 1200;

function parseStatNumber(value) {
  const match = value.trim().match(/^([^0-9-]*)(-?\d[\d,]*(?:\.\d+)?)(.*)$/);

  if (!match) {
    return null;
  }

  const [, prefix, numericValue, suffix] = match;
  const decimalPlaces = numericValue.includes(".")
    ? numericValue.split(".")[1].length
    : 0;
  const targetValue = Number(numericValue.replace(/,/g, ""));

  if (!Number.isFinite(targetValue)) {
    return null;
  }

  return {
    prefix,
    suffix,
    decimalPlaces,
    useGrouping: numericValue.includes(","),
    targetValue,
  };
}

function formatStatNumber(value, numberParts) {
  const formatterOptions = {
    minimumFractionDigits: numberParts.decimalPlaces,
    maximumFractionDigits: numberParts.decimalPlaces,
    useGrouping: numberParts.useGrouping,
  };

  return `${numberParts.prefix}${value.toLocaleString(
    "en-US",
    formatterOptions,
  )}${numberParts.suffix}`;
}

function easeOutCubic(progress) {
  return 1 - (1 - progress) ** 3;
}

function animateCountUp(valueElement, numberParts) {
  const startTime = window.performance.now();

  const updateValue = (timestamp) => {
    const elapsed = timestamp - startTime;
    const progress = Math.min(elapsed / COUNT_UP_DURATION_MS, 1);
    const easedProgress = easeOutCubic(progress);
    const currentValue =
      numberParts.targetValue * easedProgress < 1 &&
      numberParts.decimalPlaces === 0
        ? 0
        : numberParts.targetValue * easedProgress;
    const roundedValue =
      numberParts.decimalPlaces === 0
        ? Math.round(currentValue)
        : Number(currentValue.toFixed(numberParts.decimalPlaces));

    valueElement.textContent = formatStatNumber(roundedValue, numberParts);

    if (progress < 1) {
      window.requestAnimationFrame(updateValue);
      return;
    }

    valueElement.textContent = formatStatNumber(
      numberParts.targetValue,
      numberParts,
    );
  };

  window.requestAnimationFrame(updateValue);
}

export function initImpactNumberStatAnimationsOnScroll() {
  const impactStatNumberContainers = document.querySelectorAll(
    SELECTORS.statContainer,
  );

  const handleImpactNumberStatInView = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const statContainer = entry.target;
        const valueElement = statContainer.querySelector(
          SELECTORS.countUpValue,
        );

        if (!valueElement || valueElement.dataset.animationComplete) {
          observer.unobserve(statContainer);
          return;
        }

        const finalValue =
          valueElement.dataset.finalValue || valueElement.textContent;
        const numberParts = parseStatNumber(finalValue);

        if (!numberParts) {
          observer.unobserve(statContainer);
          return;
        }

        valueElement.dataset.animationComplete = "true";

        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
          valueElement.textContent = formatStatNumber(
            numberParts.targetValue,
            numberParts,
          );
        } else {
          animateCountUp(valueElement, numberParts);
        }

        observer.unobserve(statContainer);
      }
    });
  };

  const observerOptions = {
    threshold: 0.4,
  };

  const observer = new IntersectionObserver(
    handleImpactNumberStatInView,
    observerOptions,
  );

  impactStatNumberContainers.forEach((container) => {
    const valueElement = container.querySelector(SELECTORS.countUpValue);
    const finalValue = valueElement?.dataset.finalValue || "";
    const numberParts = parseStatNumber(finalValue);

    if (!valueElement || !numberParts) {
      return;
    }

    valueElement.textContent = formatStatNumber(0, numberParts);

    observer.observe(container);
  });
}
