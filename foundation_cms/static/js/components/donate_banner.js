/**
 * Css selectors for donate banner and elements.
 */
const SELECTORS = {
  donateBanner: ".donate-banner",
  ctaButton: "#banner-cta-button",
};
/**

/**
* Initializes the donate banner component.
 */
export function initDonateBanner() {
  const donateBanner = document.querySelector(SELECTORS.donateBanner);
  const ctaButton = document.querySelector(SELECTORS.ctaButton);

  if (!donateBanner) return;

  if (window.wagtailAbTesting) {
    ctaButton?.addEventListener(`click`, (e) => {
      wagtailAbTesting.triggerEvent("donate-banner-link-click");
    });
  }
}
