import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initDonateBanner } from "./donate_banner.js";

const DISMISS_KEY = "donate banner dismiss day";

function buildBannerMarkup({
  bannerStyle = "pushdown",
  siteType = "redesign",
} = {}) {
  document.body.innerHTML = `
    <nav class="primary-nav-ns"></nav>
    <main></main>
    <div class="primary-nav-container-wrapper"></div>
    <div class="donate-banner" data-banner-style="${bannerStyle}">
      <button data-donate-banner-close-button type="button">Close</button>
      <button data-donate-banner-skip-button type="button">Skip</button>
      <a data-donate-banner-cta-button href="#">Donate</a>
      <a class="donate-banner__cta-button" href="#">Legacy donate</a>
    </div>
  `;
  document.body.dataset.siteType = siteType;
}

describe("initDonateBanner", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    vi.stubGlobal("localStorage", {
      getItem: vi.fn(),
      setItem: vi.fn(),
    });
    delete window.wagtailAbTesting;
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("does nothing when the donate banner is missing", () => {
    document.body.innerHTML = "";
    document.body.dataset.siteType = "redesign";

    expect(() => initDonateBanner()).not.toThrow();
  });

  it("removes a legacy banner that was dismissed today", () => {
    buildBannerMarkup({ bannerStyle: "legacy" });
    const today = new Date().toDateString();
    localStorage.getItem.mockReturnValue(today);

    initDonateBanner();

    expect(document.querySelector(".donate-banner")).toBeNull();
  });

  it("shows a legacy banner that has not been dismissed today", () => {
    buildBannerMarkup({ bannerStyle: "legacy" });
    localStorage.getItem.mockReturnValue(null);
    const banner = document.querySelector(".donate-banner");

    initDonateBanner();

    expect(banner.classList.contains("donate-banner--visible")).toBe(true);
  });

  it("persists dismissal and removes a legacy banner when closed", () => {
    buildBannerMarkup({ bannerStyle: "legacy" });
    localStorage.getItem.mockReturnValue(null);
    const banner = document.querySelector(".donate-banner");
    const closeButton = banner.querySelector(
      "[data-donate-banner-close-button]",
    );

    initDonateBanner();
    closeButton.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(localStorage.setItem).toHaveBeenCalledWith(
      DISMISS_KEY,
      new Date().toDateString(),
    );
    expect(document.querySelector(".donate-banner")).toBeNull();
  });

  it("removes non-legacy banners without persisting dismissal", () => {
    buildBannerMarkup({ bannerStyle: "pushdown" });
    const banner = document.querySelector(".donate-banner");
    const closeButton = banner.querySelector(
      "[data-donate-banner-close-button]",
    );

    initDonateBanner();
    closeButton.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(localStorage.setItem).not.toHaveBeenCalled();
    expect(document.querySelector(".donate-banner")).toBeNull();
  });

  it("scrolls to the redesign skip target for pushdown banners", () => {
    buildBannerMarkup({ bannerStyle: "pushdown", siteType: "redesign" });
    const skipTarget = document.querySelector("nav.primary-nav-ns");
    skipTarget.scrollIntoView = vi.fn();

    initDonateBanner();
    document
      .querySelector("[data-donate-banner-skip-button]")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(skipTarget.scrollIntoView).toHaveBeenCalledWith({
      behavior: "smooth",
    });
  });

  it("uses legacy selectors when the site type is legacy", () => {
    buildBannerMarkup({ bannerStyle: "pushdown", siteType: "legacy" });
    const skipTarget = document.querySelector("main");
    skipTarget.scrollIntoView = vi.fn();

    initDonateBanner();
    document
      .querySelector("[data-donate-banner-skip-button]")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(skipTarget.scrollIntoView).toHaveBeenCalledWith({
      behavior: "smooth",
    });
  });

  it("tracks donate CTA clicks when wagtail A/B testing is enabled", () => {
    buildBannerMarkup();
    window.wagtailAbTesting = {
      triggerEvent: vi.fn(),
    };
    const ctaButton = document.querySelector("[data-donate-banner-cta-button]");

    initDonateBanner();
    ctaButton.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(window.wagtailAbTesting.triggerEvent).toHaveBeenCalledWith(
      "donate-banner-link-click",
    );
  });
});
