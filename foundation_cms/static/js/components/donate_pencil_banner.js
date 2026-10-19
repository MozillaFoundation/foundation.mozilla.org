import { EVENTS } from "./primary_nav/config.js";

const SELECTORS = {
  banner: ".donate-pencil-banner",
  closeButton: "[data-donate-pencil-banner-close]",
  ctaButton: "[data-donate-banner-cta-button]",
  focusable: [
    "a[href]",
    "button:not([disabled])",
    'input:not([disabled]):not([type="hidden"])',
    "select:not([disabled])",
    "textarea:not([disabled])",
    '[tabindex]:not([tabindex="-1"])',
  ].join(", "),
};

// Also read by _pencil_banner_head.html to hide the banner before first paint.
export const DISMISS_STORAGE_KEY = "donate pencil banner dismiss day";
export const DISMISSED_CLASS = "donate-pencil-banner-dismissed";
const HEIGHT_PROPERTY = "--donate-pencil-banner-height";
const COLLAPSING_CLASS = "donate-pencil-banner--collapsing";
// Fallback in case transitionend never fires (e.g. reduced motion).
const COLLAPSE_TIMEOUT_MS = 300;

/**
 * Hides this banner for the rest of the local day, matching the legacy banner.
 */
function storeDismissal(key) {
  try {
    localStorage.setItem(
      DISMISS_STORAGE_KEY,
      `${key}|${new Date().toDateString()}`,
    );
  } catch {
    // Storage can be blocked; the banner then just returns on the next page load.
  }
}

/**
 * Lets things positioned off the nav, like the open search drawer, re-measure.
 */
function announceHeightChange() {
  document.dispatchEvent(new CustomEvent(EVENTS.pencilBannerHeightChange));
}

/**
 * Publishes the banner height as a CSS variable so the sticky nav sits below it.
 */
function trackHeight(banner) {
  const root = document.documentElement;
  // offsetHeight rounds, which leaves a sub-pixel gap above the nav at fractional heights.
  const update = () => {
    root.style.setProperty(
      HEIGHT_PROPERTY,
      `${banner.getBoundingClientRect().height}px`,
    );
    announceHeightChange();
  };

  update();
  const observer = new ResizeObserver(update);
  observer.observe(banner);
  return observer;
}

/**
 * Returns the first element a keyboard user would reach if the banner weren't on the page.
 */
function firstFocusableOutside(banner) {
  return [...document.querySelectorAll(SELECTORS.focusable)].find(
    (el) =>
      !banner.contains(el) &&
      el.getClientRects().length > 0 &&
      getComputedStyle(el).visibility !== "hidden",
  );
}

function collapse(banner, onDone) {
  let done = false;
  const finish = () => {
    if (done) return;
    done = true;
    onDone();
  };

  banner.style.height = `${banner.getBoundingClientRect().height}px`;
  banner.classList.add(COLLAPSING_CLASS);
  // Flush the starting height so the change to 0 transitions.
  void banner.offsetHeight;
  banner.style.height = "0px";
  // Ignore transitions bubbling up from children, like the CTA arrow's hover slide.
  banner.addEventListener("transitionend", (event) => {
    if (event.target === banner && event.propertyName === "height") finish();
  });
  setTimeout(finish, COLLAPSE_TIMEOUT_MS);
}

/**
 * Initializes the pencil-style donate banner.
 */
export function initDonatePencilBanner() {
  const banner = document.querySelector(SELECTORS.banner);
  if (!banner) return;

  const root = document.documentElement;
  if (root.classList.contains(DISMISSED_CLASS)) {
    banner.remove();
    return;
  }

  const heightObserver = trackHeight(banner);

  if (window.wagtailAbTesting) {
    banner.querySelector(SELECTORS.ctaButton)?.addEventListener("click", () => {
      wagtailAbTesting.triggerEvent("donate-banner-link-click");
    });
  }

  banner.querySelector(SELECTORS.closeButton)?.addEventListener(
    "click",
    () => {
      storeDismissal(banner.dataset.dismissKey);
      // The close button is about to be removed, so keep focus in the page.
      firstFocusableOutside(banner)?.focus({ preventScroll: true });
      collapse(banner, () => {
        heightObserver.disconnect();
        root.style.removeProperty(HEIGHT_PROPERTY);
        announceHeightChange();
        banner.remove();
      });
    },
    { once: true },
  );
}
