/**
 * Initializes counting animation when an ImpactNumberBlock's "stat number" enters the viewport.
 */

const SELECTORS = {
  statContainer: ".impact-stat__number",
  digit: ".impact-stat__digit",
};

export function initImpactNumberStatAnimationsOnScroll() {
  // Select all elements that contain animated number digits
  const impactStatNumberContainers = document.querySelectorAll(
    SELECTORS.statContainer,
  );

  const handleImpactNumberStatInView = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const statContainer = entry.target;

        // Find all animated digits inside this stat number
        const digitElements = statContainer.querySelectorAll(SELECTORS.digit);

        // Trigger the CSS animation by adding the `.animate` class
        digitElements.forEach((digitEl) => {
          digitEl.classList.add("animate");
        });

        observer.unobserve(statContainer);
      }
    });
  };

  // Trigger animation when 40% of the element is visible
  const observerOptions = {
    threshold: 0.4,
  };

  // Create the observer
  const observer = new IntersectionObserver(
    handleImpactNumberStatInView,
    observerOptions,
  );

  // Observe each impact stat number container
  impactStatNumberContainers.forEach((container) => {
    observer.observe(container);
  });
}
