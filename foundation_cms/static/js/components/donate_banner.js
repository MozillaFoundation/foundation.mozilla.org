/**
 * CSS selectors for donate banner and elements.
 */
const SELECTORS = {
  donateBanner: ".donate-banner",
  ctaButton: "[data-data-donate-banner-cta-button]",
  closeButton: "[data-donate-banner-close-button]",
  skipButton: "[data-donate-banner-skip-button]",
  skipTarget: "nav.primary-nav-ns",
};

/**
 * Initializes the donate banner component.
 */
export function initDonateBanner() {
  const banner = document.querySelector(SELECTORS.donateBanner);
  if (!banner) return;

  const ctaButton = banner.querySelector(SELECTORS.ctaButton);
  const closeButtons = banner.querySelectorAll(SELECTORS.closeButton);
  const skipButton = banner.querySelector(SELECTORS.skipButton);

  if (window.wagtailAbTesting) {
    ctaButton?.addEventListener(`click`, (e) => {
      wagtailAbTesting.triggerEvent("donate-banner-link-click");
    });
  }

  closeButtons.forEach((btn) => {
    btn.addEventListener(
      "click",
      (e) => {
        e.preventDefault();
        banner.remove();
      },
      { once: true },
    );
  });

  skipButton?.addEventListener("click", (e) => {
    e.preventDefault();
    const target = document.querySelector(SELECTORS.skipTarget);
    target?.scrollIntoView({ behavior: "smooth" });
  });
}
