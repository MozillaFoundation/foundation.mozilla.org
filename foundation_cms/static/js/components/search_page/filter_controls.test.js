import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initSearchPageFilters } from "./filter_controls.js";

describe("initSearchPageFilters drawer position", () => {
  let navBarHeight;

  beforeEach(() => {
    document.body.replaceWith(document.createElement("body"));
    document.body.innerHTML = `
      <header data-primary-nav><div class="mzf-c-nav__bar"></div></header>
      <div data-search-results-page>
        <button type="button" data-search-drawer-open>Filter &amp; Sort</button>
        <div class="search-filter-drawer" data-search-drawer hidden>
          <button type="button" data-search-drawer-close>Close</button>
        </div>
      </div>
    `;
    navBarHeight = 120;
    vi.spyOn(
      document.querySelector(".mzf-c-nav__bar"),
      "getBoundingClientRect",
    ).mockImplementation(() => ({ height: navBarHeight }));
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: false, addEventListener: vi.fn() })),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("sits under the header bar's actual height while open", () => {
    initSearchPageFilters();
    const drawer = document.querySelector("[data-search-drawer]");
    const topOf = () =>
      drawer.style.getPropertyValue("--search-filter-drawer-top");

    // Long section labels wrap the bar to two rows.
    document.querySelector("[data-search-drawer-open]").click();
    expect(topOf()).toBe("120px");

    navBarHeight = 80;
    window.dispatchEvent(new Event("resize"));
    expect(topOf()).toBe("80px");

    // Once closed, resizing no longer moves it.
    drawer.querySelector("[data-search-drawer-close]").click();
    navBarHeight = 200;
    window.dispatchEvent(new Event("resize"));
    expect(topOf()).toBe("80px");
  });
});
