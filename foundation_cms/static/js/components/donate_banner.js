/**
 * CSS selectors for donate banner and elements.
 */
const SELECTORS = {
  donateBanner: ".donate-banner",
  ctaButton: "[data-donate-banner-cta-button]",
  closeButton: "[data-donate-banner-close-button]",
  skipButton: "[data-donate-banner-skip-button]",
  skipTarget: "nav.primary-nav-ns",
};

const LEGACY_SELECTORS = {
  ctaButton: ".donate-banner__cta-button",
  skipTarget: "main",
};

/**
 * Initializes the donate banner component.
 */
export function initDonateBanner() {
  const banner = document.querySelector(SELECTORS.donateBanner);
  if (!banner) return;

  const bannerStyle = banner.dataset.bannerStyle;
  const closeButtons = banner.querySelectorAll(SELECTORS.closeButton);
  const skipButton = banner.querySelector(SELECTORS.skipButton);
  const isLegacyPage = document
    .querySelector("body")
    .classList.contains("legacy");

  let ctaButton = banner.querySelector(SELECTORS.ctaButton);
  let skipTargetSelector = SELECTORS.skipTarget;

  if (isLegacyPage) {
    ctaButton = banner.querySelector(LEGACY_SELECTORS.ctaButton);
    skipTargetSelector = LEGACY_SELECTORS.skipTarget;
  }

  if (window.wagtailAbTesting) {
    ctaButton?.addEventListener("click", (e) => {
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

  if (bannerStyle == "pushdown") {
    skipButton?.addEventListener("click", (e) => {
      e.preventDefault();

      const target = document.querySelector(skipTargetSelector);
      target?.scrollIntoView({ behavior: "smooth" });
    });
  }
}
