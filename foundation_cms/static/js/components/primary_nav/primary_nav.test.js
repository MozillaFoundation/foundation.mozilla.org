import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./primary_nav.js";
import {
  CLASSNAMES,
  DESKTOP_BREAKPOINT,
  DROPDOWN_DELAY,
  EVENTS,
} from "./config.js";

let eventListenerCleanups;

/**
 * Tracks listeners added to shared event targets so tests can remove them.
 *
 * @param {EventTarget[]} targets
 */
function trackEventListeners(targets) {
  targets.forEach((target) => {
    const addEventListener = target.addEventListener.bind(target);
    vi.spyOn(target, "addEventListener").mockImplementation(
      (type, listener, options) => {
        addEventListener(type, listener, options);
        eventListenerCleanups.push(() =>
          target.removeEventListener(type, listener, options),
        );
      },
    );
  });
}

function buildPrimaryNavMarkup() {
  document.body.innerHTML = `
    <nav class="primary-nav-ns">
      <button class="hamburger" type="button"></button>
      <div class="primary-nav-ns__grid">
        <div class="primary-nav-ns__wordmark"></div>
      </div>
      <ul>
        <li class="primary-nav-ns__menu-item">
          <a href="/topics">Topics</a>
          <div class="primary-nav-ns__dropdown">
            <a href="/topic-one">Topic one</a>
          </div>
        </li>
      </ul>
    </nav>
  `;
}

describe("initPrimaryNav", () => {
  beforeEach(() => {
    document.body.replaceWith(document.createElement("body"));
    document.documentElement.style.removeProperty("--primary-nav-search-top");
    eventListenerCleanups = [];
    trackEventListeners([document, document.body]);
    vi.useFakeTimers();
  });

  afterEach(() => {
    eventListenerCleanups.reverse().forEach((cleanup) => cleanup());
    document.documentElement.style.removeProperty("--primary-nav-search-top");
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it("does nothing when required nav elements are missing", () => {
    document.body.innerHTML = `<nav class="primary-nav-ns"></nav>`;

    expect(() => initPrimaryNav()).not.toThrow();
    expect(document.querySelector(".hamburger")).toBeNull();
  });

  it("toggles the mobile nav drawer when the hamburger is clicked", () => {
    buildPrimaryNavMarkup();
    const nav = document.querySelector(".primary-nav-ns");
    const hamburger = document.querySelector(".hamburger");

    initPrimaryNav();

    hamburger.click();
    expect(nav.classList.contains(CLASSNAMES.open)).toBe(true);
    expect(hamburger.classList.contains(CLASSNAMES.active)).toBe(true);
    expect(document.body.classList.contains(CLASSNAMES.navOpen)).toBe(true);

    hamburger.click();
    expect(nav.classList.contains(CLASSNAMES.open)).toBe(false);
    expect(hamburger.classList.contains(CLASSNAMES.active)).toBe(false);

    vi.advanceTimersByTime(300);
    expect(document.body.classList.contains(CLASSNAMES.navOpen)).toBe(false);
  });

  it("closes the mobile nav drawer when search is about to open", () => {
    buildPrimaryNavMarkup();
    const nav = document.querySelector(".primary-nav-ns");
    const hamburger = document.querySelector(".hamburger");

    initPrimaryNav();
    hamburger.click();
    expect(nav.classList.contains(CLASSNAMES.open)).toBe(true);

    document.dispatchEvent(new CustomEvent(EVENTS.searchWillOpen));

    expect(nav.classList.contains(CLASSNAMES.open)).toBe(false);
    vi.advanceTimersByTime(300);
    expect(document.body.classList.contains(CLASSNAMES.navOpen)).toBe(false);
  });

  it("creates a mobile dropdown toggle and opens it on click", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");
    const dropdown = document.querySelector(".primary-nav-ns__dropdown");

    initPrimaryNav();

    const toggle = menu.querySelector(".primary-nav-ns__dropdown-toggle");
    expect(toggle).not.toBeNull();
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(dropdown.getAttribute("aria-hidden")).toBe("true");
    expect(dropdown.hasAttribute("inert")).toBe(true);

    toggle.click();

    expect(menu.classList.contains(CLASSNAMES.open)).toBe(true);
    expect(dropdown.style.maxHeight).toBe(`${dropdown.scrollHeight}px`);
    expect(dropdown.getAttribute("aria-hidden")).toBe("false");
    expect(dropdown.hasAttribute("inert")).toBe(false);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
  });

  it("toggles dropdowns with Enter and Space keyboard events", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");

    initPrimaryNav();

    const toggle = menu.querySelector(".primary-nav-ns__dropdown-toggle");

    toggle.dispatchEvent(
      new KeyboardEvent("keydown", { key: "Enter", bubbles: true }),
    );
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(true);

    toggle.dispatchEvent(
      new KeyboardEvent("keydown", { key: " ", bubbles: true }),
    );
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(false);
  });

  it("opens dropdowns on desktop hover after the configured delay", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");
    vi.spyOn(window, "innerWidth", "get").mockReturnValue(1200);

    initPrimaryNav();

    menu.dispatchEvent(new MouseEvent("mouseenter", { bubbles: true }));
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(false);

    vi.advanceTimersByTime(DROPDOWN_DELAY);
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(true);
  });

  it("closes an open dropdown on desktop mouseleave", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");
    vi.spyOn(window, "innerWidth", "get").mockReturnValue(1200);

    initPrimaryNav();

    menu.dispatchEvent(new MouseEvent("mouseenter"));
    vi.advanceTimersByTime(DROPDOWN_DELAY);
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(true);

    menu.dispatchEvent(new MouseEvent("mouseleave"));
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(true);

    vi.advanceTimersByTime(DROPDOWN_DELAY);
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(false);
  });

  it("cancels a pending desktop hover opening on mouseleave", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");
    vi.spyOn(window, "innerWidth", "get").mockReturnValue(1200);

    initPrimaryNav();

    menu.dispatchEvent(new MouseEvent("mouseenter"));
    expect(vi.getTimerCount()).toBe(1);

    menu.dispatchEvent(new MouseEvent("mouseleave"));
    vi.advanceTimersByTime(DROPDOWN_DELAY);

    expect(menu.classList.contains(CLASSNAMES.open)).toBe(false);
  });

  it("ignores hover events below the desktop breakpoint", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");
    vi.spyOn(window, "innerWidth", "get").mockReturnValue(
      DESKTOP_BREAKPOINT - 1,
    );

    initPrimaryNav();
    const timerCountBeforeHover = vi.getTimerCount();

    menu.dispatchEvent(new MouseEvent("mouseenter"));
    menu.dispatchEvent(new MouseEvent("mouseleave"));

    expect(vi.getTimerCount()).toBe(timerCountBeforeHover);
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(false);
    expect(
      menu
        .querySelector(".primary-nav-ns__dropdown-toggle")
        .getAttribute("aria-expanded"),
    ).toBe("false");
  });

  it("closes open dropdowns when Escape is pressed", () => {
    buildPrimaryNavMarkup();
    const menu = document.querySelector(".primary-nav-ns__menu-item");

    initPrimaryNav();
    menu.querySelector(".primary-nav-ns__dropdown-toggle").click();
    expect(menu.classList.contains(CLASSNAMES.open)).toBe(true);

    document.dispatchEvent(
      new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
    );

    expect(menu.classList.contains(CLASSNAMES.open)).toBe(false);
  });
});

describe("initWordmarkVisibilityOnScroll", () => {
  let observerCallback;

  beforeEach(() => {
    document.body.replaceWith(document.createElement("body"));
    document.documentElement.style.removeProperty("--primary-nav-search-top");
    observerCallback = null;
    vi.stubGlobal(
      "IntersectionObserver",
      vi.fn((callback) => {
        observerCallback = callback;
        return {
          observe: vi.fn(),
          disconnect: vi.fn(),
        };
      }),
    );
  });

  afterEach(() => {
    document.documentElement.style.removeProperty("--primary-nav-search-top");
    vi.unstubAllGlobals();
  });

  it("shows the wordmark when the kinetic type wordmark is absent", () => {
    document.body.innerHTML = `
      <nav class="primary-nav-ns">
        <div class="primary-nav-ns__grid"></div>
        <div class="primary-nav-ns__wordmark hidden"></div>
      </nav>
    `;
    const wordmark = document.querySelector(".primary-nav-ns__wordmark");
    const grid = document.querySelector(".primary-nav-ns__grid");

    initWordmarkVisibilityOnScroll();

    expect(wordmark.classList.contains(CLASSNAMES.hidden)).toBe(false);
    expect(grid.classList.contains(CLASSNAMES.hiddenWordmark)).toBe(false);
    expect(IntersectionObserver).not.toHaveBeenCalled();
  });

  it("hides the nav wordmark when the kinetic type wordmark intersects", () => {
    document.body.innerHTML = `
      <nav class="primary-nav-ns">
        <div class="primary-nav-ns__grid"></div>
        <div class="primary-nav-ns__wordmark"></div>
      </nav>
      <div class="kinetic-type-wordmark"></div>
    `;
    const wordmark = document.querySelector(".primary-nav-ns__wordmark");
    const grid = document.querySelector(".primary-nav-ns__grid");

    initWordmarkVisibilityOnScroll();

    expect(IntersectionObserver).toHaveBeenCalledTimes(1);
    observerCallback([{ isIntersecting: true }]);
    expect(wordmark.classList.contains(CLASSNAMES.hidden)).toBe(true);
    expect(grid.classList.contains(CLASSNAMES.hiddenWordmark)).toBe(true);

    observerCallback([{ isIntersecting: false }]);
    expect(wordmark.classList.contains(CLASSNAMES.hidden)).toBe(false);
    expect(grid.classList.contains(CLASSNAMES.hiddenWordmark)).toBe(false);
  });
});
