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

const PNI_SELECTORS = {
  ctaButton: ".donate-banner__cta-button",
  skipTarget: ".primary-nav-container-wrapper",
};

/**
 * Legacy-style dismiss helpers
 */
const DISMISS_KEY = "donate banner dismiss day";

function getDismissDate() {
  return localStorage.getItem(DISMISS_KEY);
}

function setDismissDate() {
  const today = new Date();
  localStorage.setItem(DISMISS_KEY, today.toDateString());
}

function shouldHideBanner() {
  const today = new Date();
  return getDismissDate() === today.toDateString();
}

/**
 * Initializes the donate banner component.
 */
export function initDonateBanner() {
  const banner = document.querySelector(SELECTORS.donateBanner);
  if (!banner) return;

  const bannerStyle = banner.dataset.bannerStyle;
  const closeButtons = banner.querySelectorAll(SELECTORS.closeButton);
  const skipButton = banner.querySelector(SELECTORS.skipButton);
  const siteType = document.querySelector("body").dataset.siteType;

  let ctaButton = banner.querySelector(SELECTORS.ctaButton);
  let skipTargetSelector = SELECTORS.skipTarget;

  if (siteType === "legacy") {
    ctaButton = banner.querySelector(LEGACY_SELECTORS.ctaButton);
    skipTargetSelector = LEGACY_SELECTORS.skipTarget;
  } else if (siteType === "pni") {
    ctaButton = banner.querySelector(PNI_SELECTORS.ctaButton);
    skipTargetSelector = PNI_SELECTORS.skipTarget;
  }

  // Handle legacy banner visibility based on dismissal date.
  if (bannerStyle === "legacy") {
    const hideBanner = shouldHideBanner();
    if (hideBanner) {
      // If we should hide the banner, remove it from the DOM to prevent it
      // from creating unexpected behavior due to its absolute positioning.
      banner.remove();
      return;
    }

    // if not dismissed today, ensure it's visible
    banner.classList.add("donate-banner--visible");
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

        // Only the legacy banner is dismissible for the day.
        if (bannerStyle === "legacy") {
          setDismissDate();
        }

        banner.remove();
      },
      { once: true },
    );
  });

  if (bannerStyle === "pushdown") {
    skipButton?.addEventListener("click", (e) => {
      e.preventDefault();

      const target = document.querySelector(skipTargetSelector);
      target?.scrollIntoView({ behavior: "smooth" });
    });
  }
}
