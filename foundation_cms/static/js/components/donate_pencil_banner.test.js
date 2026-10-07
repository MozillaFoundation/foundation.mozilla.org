import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  DISMISS_COOKIE,
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
  beforeEach(() => {
    vi.useFakeTimers();
    window.ResizeObserver = class {
      observe() {}
      disconnect() {}
    };
    delete window.wagtailAbTesting;
  });

  afterEach(() => {
    vi.useRealTimers();
    document.documentElement.className = "";
    document.documentElement.removeAttribute("style");
    document.cookie = `${DISMISS_COOKIE}=; path=/; max-age=0`;
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

  it("sets a session cookie, moves focus to the nav logo and collapses when closed", () => {
    const banner = buildBannerMarkup();
    initDonatePencilBanner();

    banner.querySelector("[data-donate-pencil-banner-close]").click();

    expect(document.cookie).toContain(`${DISMISS_COOKIE}=${DISMISS_KEY}`);
    expect(document.activeElement).toBe(
      document.querySelector(".primary-nav-ns__wordmark a"),
    );
    expect(banner.style.height).toBe("0px");

    vi.runAllTimers();

    expect(document.querySelector(".donate-pencil-banner")).toBeNull();
    expect(heightVar()).toBe("");
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
