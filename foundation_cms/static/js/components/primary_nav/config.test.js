import { describe, expect, it } from "vitest";
import {
  CLASSNAMES,
  DESKTOP_BREAKPOINT,
  DROPDOWN_DELAY,
  EVENTS,
  SELECTORS,
  TRANSITION_DURATION,
} from "./config.js";

describe("primary nav config", () => {
  it("exports stable selectors for nav elements", () => {
    expect(SELECTORS.primaryNav).toBe(".primary-nav-ns");
    expect(SELECTORS.hamburger).toBe(".primary-nav-ns .hamburger");
    expect(SELECTORS.dropdown).toBe(".primary-nav-ns__dropdown");
    expect(SELECTORS.searchToggle).toBe(
      ".primary-nav-ns__search-icon .search-toggle",
    );
  });

  it("exports class names and timing constants used by nav behavior", () => {
    expect(CLASSNAMES.open).toBe("open");
    expect(CLASSNAMES.searchOpen).toBe("search-open");
    expect(CLASSNAMES.navOpen).toBe("primary-nav-ns-open");
    expect(TRANSITION_DURATION).toBe(300);
    expect(DROPDOWN_DELAY).toBe(200);
    expect(DESKTOP_BREAKPOINT).toBe(1024);
  });

  it("exports cross-module coordination events", () => {
    expect(EVENTS.primaryNavWillOpen).toBe("primaryNav:willOpen");
    expect(EVENTS.searchWillOpen).toBe("primaryNav:searchWillOpen");
  });
});
