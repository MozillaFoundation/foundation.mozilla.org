import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initSearchToggle } from "./search.js";
import { CLASSNAMES, EVENTS } from "./config.js";

function buildSearchMarkup() {
  document.body.innerHTML = `
    <nav class="primary-nav-ns"></nav>
    <div class="primary-nav-ns__search-icon">
      <button class="search-toggle" type="button">Search</button>
    </div>
    <div class="search-input-container" aria-hidden="true" inert>
      <input type="search" />
    </div>
  `;
}

describe("initSearchToggle", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    vi.spyOn(window, "requestAnimationFrame").mockImplementation((callback) => {
      callback(0);
      return 1;
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("does nothing when required search elements are missing", () => {
    document.body.innerHTML = `<button class="search-toggle"></button>`;

    expect(() => initSearchToggle()).not.toThrow();
  });

  it("opens and closes the search drawer when the toggle is clicked", () => {
    buildSearchMarkup();
    const searchToggle = document.querySelector(".search-toggle");
    const searchInputContainer = document.querySelector(
      ".search-input-container",
    );
    const searchInput = document.querySelector(".search-input-container input");
    const focusSpy = vi.spyOn(searchInput, "focus");

    initSearchToggle();

    searchToggle.click();

    expect(searchToggle.classList.contains(CLASSNAMES.searchOpen)).toBe(true);
    expect(searchInputContainer.classList.contains(CLASSNAMES.searchOpen)).toBe(
      true,
    );
    expect(searchInputContainer.getAttribute("aria-expanded")).toBe("true");
    expect(searchInputContainer.getAttribute("aria-hidden")).toBe("false");
    expect(searchInputContainer.hasAttribute("inert")).toBe(false);
    expect(searchToggle.getAttribute("aria-expanded")).toBe("true");
    expect(focusSpy).toHaveBeenCalledWith({ preventScroll: true });
    expect(
      document.querySelector(`.${CLASSNAMES.searchOpenBackdrop}`),
    ).not.toBeNull();

    searchToggle.click();

    expect(searchToggle.classList.contains(CLASSNAMES.searchOpen)).toBe(false);
    expect(searchInputContainer.classList.contains(CLASSNAMES.searchOpen)).toBe(
      false,
    );
    expect(searchInputContainer.getAttribute("aria-expanded")).toBe("false");
    expect(searchInputContainer.getAttribute("aria-hidden")).toBe("true");
    expect(searchInputContainer.hasAttribute("inert")).toBe(true);
  });

  it("dispatches searchWillOpen before opening the drawer", () => {
    buildSearchMarkup();
    const searchToggle = document.querySelector(".search-toggle");
    const listener = vi.fn();

    document.addEventListener(EVENTS.searchWillOpen, listener);
    initSearchToggle();
    searchToggle.click();

    expect(listener).toHaveBeenCalledTimes(1);
  });

  it("closes the search drawer when the primary nav is about to open", () => {
    buildSearchMarkup();
    const searchToggle = document.querySelector(".search-toggle");
    const searchInputContainer = document.querySelector(
      ".search-input-container",
    );

    initSearchToggle();
    searchToggle.click();
    expect(searchInputContainer.classList.contains(CLASSNAMES.searchOpen)).toBe(
      true,
    );

    document.dispatchEvent(new CustomEvent(EVENTS.primaryNavWillOpen));

    expect(searchInputContainer.classList.contains(CLASSNAMES.searchOpen)).toBe(
      false,
    );
  });

  it("positions the search drawer below the primary nav", () => {
    buildSearchMarkup();
    const primaryNav = document.querySelector(".primary-nav-ns");
    const searchToggle = document.querySelector(".search-toggle");

    vi.spyOn(primaryNav, "getBoundingClientRect").mockReturnValue({
      bottom: 88.4,
    });

    initSearchToggle();
    searchToggle.click();

    expect(
      document.documentElement.style.getPropertyValue(
        "--primary-nav-search-top",
      ),
    ).toBe("88px");
  });

  it("closes the search drawer when Escape is pressed in the input", () => {
    buildSearchMarkup();
    const searchToggle = document.querySelector(".search-toggle");
    const searchInput = document.querySelector(".search-input-container input");
    const searchInputContainer = document.querySelector(
      ".search-input-container",
    );
    const focusSpy = vi.spyOn(searchToggle, "focus");

    initSearchToggle();
    searchToggle.click();

    searchInput.dispatchEvent(
      new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
    );

    expect(searchInputContainer.classList.contains(CLASSNAMES.searchOpen)).toBe(
      false,
    );
    expect(focusSpy).toHaveBeenCalledWith({ preventScroll: true });
  });

  it("closes the search drawer when the backdrop is clicked", () => {
    buildSearchMarkup();
    const searchToggle = document.querySelector(".search-toggle");
    const searchInputContainer = document.querySelector(
      ".search-input-container",
    );
    const focusSpy = vi.spyOn(searchToggle, "focus");

    initSearchToggle();
    searchToggle.click();

    document
      .querySelector(`.${CLASSNAMES.searchOpenBackdrop}`)
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(searchInputContainer.classList.contains(CLASSNAMES.searchOpen)).toBe(
      false,
    );
    expect(focusSpy).toHaveBeenCalledWith({ preventScroll: true });
  });
});
