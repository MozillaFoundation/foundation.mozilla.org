import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  GALLERY_HUB_SCROLL_COOLDOWN as COOLDOWN_MS,
  GALLERY_HUB_SCROLL_LOCK_CLASS as LOCK_CLASS,
} from "./config";

const BANNER_HEIGHT = 600;

let listeners = [];
let prefersReducedMotion = true;

/**
 * Render a Gallery Hub with an optional donate banner above the navigation.
 *
 * @param {Object} options
 * @param {?string} options.bannerStyle - Banner variant, or null for none.
 * @param {string} options.bannerPosition - Computed CSS position of the banner.
 */
function renderPage({ bannerStyle = "pushdown", bannerPosition = "sticky" }) {
  const banner = bannerStyle
    ? `<div class="donate-banner" data-banner-style="${bannerStyle}"
            style="position: ${bannerPosition}">
         <button data-donate-banner-close-button type="button">Close</button>
       </div>`
    : "";

  document.body.removeAttribute("style");
  document.body.className = "";
  document.documentElement.className = "";
  document.body.innerHTML = `
    ${banner}
    <nav class="primary-nav-ns"></nav>
    <div class="main-content-wrapper">
      <main class="gallery-hub gallery-hub--intro" data-gallery-hub>
        <button type="button" data-gallery-hub-enter>Explore</button>
        <article data-gallery-hub-project data-project-id="1"></article>
        <article data-gallery-hub-project data-project-id="2"></article>
      </main>
    </div>
  `;

  const bannerElement = document.querySelector(".donate-banner");

  if (bannerElement) {
    bannerElement.getBoundingClientRect = () => ({ height: BANNER_HEIGHT });
  }

  document.querySelector("[data-gallery-hub]").getBoundingClientRect = () => ({
    top: 80,
    bottom: 900,
  });
  // jsdom has no layout; the footer release nudge is capped by this height.
  Object.defineProperty(
    document.querySelector("[data-gallery-hub]"),
    "offsetHeight",
    { configurable: true, value: 820 },
  );
}

/**
 * Load fresh module instances so module-level scroll lock state starts clean.
 */
async function initCarousel() {
  vi.resetModules();
  const { initGalleryHubProjectCarousel } =
    await import("./project_carousel.js");

  initGalleryHubProjectCarousel();
}

function setScrollY(top) {
  window.scrollY = top;
}

function scrollPageTo(top) {
  setScrollY(top);
  window.dispatchEvent(new Event("scroll"));
}

function wheel(deltaY) {
  const event = new WheelEvent("wheel", { deltaY, cancelable: true });

  window.dispatchEvent(event);

  return event;
}

function isLocked() {
  return document.documentElement.classList.contains(LOCK_CLASS);
}

function getRoot() {
  return document.querySelector("[data-gallery-hub]");
}

describe("initGalleryHubProjectCarousel with a donate banner", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    listeners = [];

    for (const target of [window, document]) {
      const add = target.addEventListener.bind(target);

      vi.spyOn(target, "addEventListener").mockImplementation((...args) => {
        listeners.push([target, args]);
        add(...args);
      });
    }

    Object.defineProperty(window, "scrollY", {
      configurable: true,
      writable: true,
      value: 0,
    });
    window.scrollTo = vi.fn(({ top }) => setScrollY(top));
    window.scrollBy = vi.fn();
    window.requestAnimationFrame = vi.fn((callback) => callback());
    // Reduced motion also skips the intro collage animation gate.
    prefersReducedMotion = true;
    window.matchMedia = vi.fn((query) => ({
      matches: query.includes("prefers-reduced-motion") && prefersReducedMotion,
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();

    for (const [target, args] of listeners) {
      target.removeEventListener(...args);
    }

    vi.useRealTimers();
  });

  it("leaves a pushdown banner to native scrolling on load", async () => {
    renderPage({ bannerStyle: "pushdown" });

    await initCarousel();
    const event = wheel(120);

    expect(isLocked()).toBe(false);
    expect(document.body.style.position).toBe("");
    expect(event.defaultPrevented).toBe(false);
    expect(getRoot().classList.contains("gallery-hub--intro")).toBe(true);
  });

  it("pins the gallery below the banner once scrolling reaches it", async () => {
    renderPage({ bannerStyle: "pushdown" });

    await initCarousel();
    scrollPageTo(BANNER_HEIGHT);

    expect(isLocked()).toBe(true);
    expect(document.body.style.top).toBe(`-${BANNER_HEIGHT}px`);

    // The gesture that reached the gallery must not also move into projects.
    expect(wheel(120).defaultPrevented).toBe(true);
    expect(getRoot().classList.contains("gallery-hub--intro")).toBe(true);

    vi.advanceTimersByTime(COOLDOWN_MS);
    wheel(120);

    expect(getRoot().classList.contains("gallery-hub--project-view")).toBe(
      true,
    );
  });

  it("pins below the banner when the intro is entered while it is in view", async () => {
    renderPage({ bannerStyle: "pushdown" });

    await initCarousel();
    document
      .querySelector("[data-gallery-hub-enter]")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(isLocked()).toBe(true);
    expect(window.scrollTo).toHaveBeenLastCalledWith({
      top: BANNER_HEIGHT,
      left: 0,
      behavior: "instant",
    });
    expect(getRoot().classList.contains("gallery-hub--project-view")).toBe(
      true,
    );
  });

  it("returns to the banner when scrolling up from the intro", async () => {
    renderPage({ bannerStyle: "pushdown" });

    await initCarousel();
    scrollPageTo(BANNER_HEIGHT);
    vi.advanceTimersByTime(COOLDOWN_MS);
    const event = wheel(-120);

    expect(event.defaultPrevented).toBe(true);
    expect(isLocked()).toBe(false);
    expect(window.scrollY).toBe(BANNER_HEIGHT);
    // Reduced motion: the nudge back to the banner must not animate.
    expect(window.scrollBy).toHaveBeenCalledWith(
      expect.objectContaining({ left: 0, behavior: "instant" }),
    );
    expect(window.scrollBy.mock.calls[0][0].top).toBeLessThan(0);

    // The release restores the pin position; that alone must not re-pin.
    window.dispatchEvent(new Event("scroll"));
    expect(isLocked()).toBe(false);

    scrollPageTo(200);
    expect(isLocked()).toBe(false);

    scrollPageTo(BANNER_HEIGHT);
    expect(isLocked()).toBe(true);
  });

  it("animates the release nudges when motion is allowed", async () => {
    prefersReducedMotion = false;
    renderPage({ bannerStyle: "pushdown" });

    await initCarousel();
    vi.advanceTimersByTime(1200);
    scrollPageTo(BANNER_HEIGHT);
    vi.advanceTimersByTime(COOLDOWN_MS);
    wheel(-120);

    expect(isLocked()).toBe(false);
    expect(window.scrollBy).toHaveBeenLastCalledWith(
      expect.objectContaining({ left: 0, behavior: "smooth" }),
    );
    expect(window.scrollBy.mock.lastCall[0].top).toBeLessThan(0);

    scrollPageTo(200);
    scrollPageTo(BANNER_HEIGHT);

    for (let step = 0; step < 3; step += 1) {
      vi.advanceTimersByTime(COOLDOWN_MS);
      wheel(120);
    }

    expect(isLocked()).toBe(false);
    expect(window.scrollBy).toHaveBeenLastCalledWith(
      expect.objectContaining({ left: 0, behavior: "smooth" }),
    );
    expect(window.scrollBy.mock.lastCall[0].top).toBeGreaterThan(0);
  });

  it("re-pins below the banner, not at the page top, coming back from the footer", async () => {
    renderPage({ bannerStyle: "pushdown" });

    await initCarousel();
    scrollPageTo(BANNER_HEIGHT);

    for (let step = 0; step < 3; step += 1) {
      vi.advanceTimersByTime(COOLDOWN_MS);
      wheel(120);
    }

    expect(isLocked()).toBe(false);
    expect(window.scrollY).toBe(BANNER_HEIGHT);
    expect(window.scrollBy).toHaveBeenCalledWith(
      expect.objectContaining({ left: 0, behavior: "instant" }),
    );
    expect(window.scrollBy.mock.calls[0][0].top).toBeGreaterThan(0);

    window.dispatchEvent(new Event("scroll"));
    expect(isLocked()).toBe(false);

    scrollPageTo(BANNER_HEIGHT + 400);
    expect(isLocked()).toBe(false);

    scrollPageTo(BANNER_HEIGHT);
    expect(isLocked()).toBe(true);
    expect(document.body.style.top).toBe(`-${BANNER_HEIGHT}px`);
  });

  it("moves the pinned gallery up when a pinned banner is dismissed", async () => {
    renderPage({ bannerStyle: "legacy", bannerPosition: "relative" });

    await initCarousel();
    scrollPageTo(BANNER_HEIGHT);
    expect(document.body.style.top).toBe(`-${BANNER_HEIGHT}px`);

    document.querySelector(".donate-banner").remove();
    document.dispatchEvent(new CustomEvent("donateBanner:dismiss"));

    expect(isLocked()).toBe(true);
    expect(document.body.style.top).toBe("0px");
  });

  it("pins the gallery at the top when the banner in view is dismissed", async () => {
    renderPage({ bannerStyle: "legacy", bannerPosition: "relative" });

    await initCarousel();
    expect(isLocked()).toBe(false);

    document.querySelector(".donate-banner").remove();
    document.dispatchEvent(new CustomEvent("donateBanner:dismiss"));

    expect(isLocked()).toBe(true);
    expect(document.body.style.top).toBe("0px");
  });

  it("ignores overlay banners that take no space above the navigation", async () => {
    renderPage({ bannerStyle: "lightbox", bannerPosition: "fixed" });

    await initCarousel();

    expect(isLocked()).toBe(true);
    expect(document.body.style.top).toBe("0px");
  });

  it("keeps the gallery pinned at the top without a banner", async () => {
    renderPage({ bannerStyle: null });

    await initCarousel();
    const event = wheel(-120);

    expect(isLocked()).toBe(true);
    expect(document.body.style.top).toBe("0px");
    expect(event.defaultPrevented).toBe(true);
    expect(window.scrollBy).not.toHaveBeenCalled();
  });
});
