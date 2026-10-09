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
export const DISMISS_COOKIE = "donate_pencil_banner_dismissed";
export const DISMISSED_CLASS = "donate-pencil-banner-dismissed";
const HEIGHT_PROPERTY = "--donate-pencil-banner-height";
const COLLAPSING_CLASS = "donate-pencil-banner--collapsing";
// Fallback in case transitionend never fires (e.g. reduced motion).
const COLLAPSE_TIMEOUT_MS = 300;

/**
 * Remembers the dismissal for the browser session only, so the banner returns on the next visit.
 */
function setDismissCookie(key) {
  const secure = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie = `${DISMISS_COOKIE}=${key}; path=/; SameSite=Lax${secure}`;
}

/**
 * Publishes the banner height as a CSS variable so the sticky nav sits below it.
 */
function trackHeight(banner) {
  const root = document.documentElement;
  const update = () =>
    root.style.setProperty(HEIGHT_PROPERTY, `${banner.offsetHeight}px`);

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

  banner.style.height = `${banner.offsetHeight}px`;
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
      setDismissCookie(banner.dataset.dismissKey);
      // The close button is about to be removed, so keep focus in the page.
      firstFocusableOutside(banner)?.focus({ preventScroll: true });
      collapse(banner, () => {
        heightObserver.disconnect();
        root.style.removeProperty(HEIGHT_PROPERTY);
        banner.remove();
      });
    },
    { once: true },
  );
}
