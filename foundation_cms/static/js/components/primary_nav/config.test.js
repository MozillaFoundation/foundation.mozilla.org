import { describe, expect, it } from "vitest";
import { CLASSNAMES, EVENTS, MOBILE_MEDIA_QUERY, SELECTORS } from "./config.js";

describe("primary nav config", () => {
  it("exports stable selectors for nav elements", () => {
    expect(SELECTORS.primaryNav).toBe("[data-primary-nav]");
    expect(SELECTORS.panelTrigger).toBe("[data-nav-panel]");
    expect(SELECTORS.menuButton).toBe(".mzf-c-nav__menu");
    expect(SELECTORS.searchToggle).toBe("[data-primary-nav-search-toggle]");
  });

  it("exports LP's state classes and mobile boundary", () => {
    expect(CLASSNAMES.panelOpen).toBe("mzf-c-nav__panel--open");
    expect(CLASSNAMES.drawerOpen).toBe("mzf-c-nav--drawer-open");
    expect(CLASSNAMES.searchOpen).toBe("search-open");
    expect(MOBILE_MEDIA_QUERY).toBe("(max-width: 48rem)");
  });

  it("exports cross-module coordination events", () => {
    expect(EVENTS.primaryNavWillOpen).toBe("primaryNav:willOpen");
    expect(EVENTS.searchWillOpen).toBe("primaryNav:searchWillOpen");
    expect(EVENTS.closeMenus).toBe("primaryNav:closeMenus");
  });
});
