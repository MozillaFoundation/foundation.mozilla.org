/**
 * Initializes counting animation when a Impact Number Block enters the viewport.
 */
export function initImpactStatAnimationsOnScroll() {
    // Select all elements that contain animated number digits
    const impactStatNumberContainers = document.querySelectorAll(".impact-stat__number");
  

    const handleImpactNumberStatInView = (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const statContainer = entry.target;
  
          // Find all animated digits inside this ImpactNumberStat block
          const digitElements = statContainer.querySelectorAll(".numbers__window__digit");
  
          // Trigger the CSS animation by adding the `.animate` class
          digitElements.forEach((digitEl) => digitEl.classList.add("animate"));
  

          observer.unobserve(statContainer);
        }
      });
    };
  
    // When the animation should trigger ( when 60% of element is visible)
    const observerOptions = {
      threshold: 0.6
    };
  
    // Create the observer
    const observer = new IntersectionObserver(handleImpactNumberStatInView, observerOptions);
  
    // Observe each impact stat number container
    impactStatNumberContainers.forEach((container) => {
      observer.observe(container);
    });

  }