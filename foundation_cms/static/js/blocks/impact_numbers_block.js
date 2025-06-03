/**
 * Initializes counting animation when an ImpactNumberBlock's "stat number" enters the viewport.
 */
export function initImpactNumberStatAnimationsOnScroll() {
  // Select all elements that contain animated number digits
  const impactStatNumberContainers = document.querySelectorAll(
    ".impact-stat__number",
  );

  const handleImpactNumberStatInView = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const statContainer = entry.target;

        // Find all animated digits inside this stat number
        const digitElements = statContainer.querySelectorAll(
          ".impact-stat__digit",
        );

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
