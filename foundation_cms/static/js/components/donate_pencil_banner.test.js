import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  DISMISS_STORAGE_KEY,
  DISMISSED_CLASS,
  initDonatePencilBanner,
} from "./donate_pencil_banner.js";

const DISMISS_KEY = "9f1c2d3e-0000-4000-8000-000000000000";

function buildBannerMarkup() {
  document.body.innerHTML = `
    <div class="donate-pencil-banner" data-dismiss-key="${DISMISS_KEY}">
      <a data-donate-banner-cta-button href="?form=donate">Donate</a>
      <button data-donate-pencil-banner-close type="button">Close</button>
    </div>
    <nav class="primary-nav-ns">
      <button class="hamburger" type="button">Menu</button>
      <div class="primary-nav-ns__wordmark"><a href="/">Mozilla Foundation</a></div>
    </nav>
  `;
  const banner = document.querySelector(".donate-pencil-banner");
  Object.defineProperty(banner, "offsetHeight", {
    configurable: true,
    value: 30,
  });
  return banner;
}

const heightVar = () =>
  document.documentElement.style.getPropertyValue(
    "--donate-pencil-banner-height",
  );

describe("initDonatePencilBanner", () => {
  const originalGetClientRects = Element.prototype.getClientRects;

  beforeEach(() => {
    vi.useFakeTimers();
    // jsdom has no layout, so treat every element as rendered unless a test says otherwise.
    Element.prototype.getClientRects = () => [{}];
    window.ResizeObserver = class {
      observe() {}
      disconnect() {}
    };
    delete window.wagtailAbTesting;
  });

  afterEach(() => {
    vi.useRealTimers();
    Element.prototype.getClientRects = originalGetClientRects;
    document.documentElement.className = "";
    document.documentElement.removeAttribute("style");
    localStorage.clear();
  });

  it("does nothing when there is no pencil banner", () => {
    document.body.innerHTML = "";

    expect(() => initDonatePencilBanner()).not.toThrow();
    expect(heightVar()).toBe("");
  });

  it("removes the banner when it was dismissed earlier in the session", () => {
    buildBannerMarkup();
    document.documentElement.classList.add(DISMISSED_CLASS);

    initDonatePencilBanner();

    expect(document.querySelector(".donate-pencil-banner")).toBeNull();
    expect(heightVar()).toBe("");
  });

  it("publishes the banner height for the sticky nav offset", () => {
    buildBannerMarkup();

    initDonatePencilBanner();

    expect(heightVar()).toBe("30px");
  });

  it("remembers the dismissal for today, moves focus to the first focusable element and collapses when closed", () => {
    const banner = buildBannerMarkup();
    initDonatePencilBanner();

    banner.querySelector("[data-donate-pencil-banner-close]").click();

    expect(localStorage.getItem(DISMISS_STORAGE_KEY)).toBe(
      `${DISMISS_KEY}|${new Date().toDateString()}`,
    );
    expect(document.activeElement).toBe(document.querySelector(".hamburger"));
    expect(banner.style.height).toBe("0px");

    vi.runAllTimers();

    expect(document.querySelector(".donate-pencil-banner")).toBeNull();
    expect(heightVar()).toBe("");
  });

  it("only finishes the collapse on the banner's own height transition", () => {
    const banner = buildBannerMarkup();
    initDonatePencilBanner();
    const transitionEnd = (target, propertyName) => {
      const event = new Event("transitionend", { bubbles: true });
      Object.defineProperty(event, "propertyName", { value: propertyName });
      target.dispatchEvent(event);
    };

    banner.querySelector("[data-donate-pencil-banner-close]").click();
    transitionEnd(
      banner.querySelector("[data-donate-banner-cta-button]"),
      "transform",
    );
    expect(document.querySelector(".donate-pencil-banner")).not.toBeNull();

    transitionEnd(banner, "height");
    expect(document.querySelector(".donate-pencil-banner")).toBeNull();
  });

  it("skips elements that are not rendered when moving focus", () => {
    const banner = buildBannerMarkup();
    const hamburger = document.querySelector(".hamburger");
    hamburger.getClientRects = () => [];
    initDonatePencilBanner();

    banner.querySelector("[data-donate-pencil-banner-close]").click();

    expect(document.activeElement).toBe(
      document.querySelector(".primary-nav-ns__wordmark a"),
    );
  });

  it("still dismisses when storage is blocked", () => {
    const setItem = vi
      .spyOn(Storage.prototype, "setItem")
      .mockImplementation(() => {
        throw new DOMException("blocked", "SecurityError");
      });
    const banner = buildBannerMarkup();
    initDonatePencilBanner();

    banner.querySelector("[data-donate-pencil-banner-close]").click();
    vi.runAllTimers();

    expect(document.querySelector(".donate-pencil-banner")).toBeNull();
    setItem.mockRestore();
  });

  it("tracks CTA clicks for A/B testing", () => {
    window.wagtailAbTesting = { triggerEvent: vi.fn() };
    const banner = buildBannerMarkup();
    initDonatePencilBanner();

    banner.querySelector("[data-donate-banner-cta-button]").click();

    expect(window.wagtailAbTesting.triggerEvent).toHaveBeenCalledWith(
      "donate-banner-link-click",
    );
  });
});
