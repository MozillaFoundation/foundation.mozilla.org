/**
 * Css selectors for primary navigation elements.
 */
export const SELECTORS = {
  primaryNav: ".primary-nav-ns",
  primaryNavGrid: ".primary-nav-ns__grid",
  hamburger: ".primary-nav-ns .hamburger",
  wordmark: ".primary-nav-ns__wordmark",
  menuItem: ".primary-nav-ns__menu-item",
  dropdown: ".primary-nav-ns__dropdown",
  toggle: ".primary-nav-ns__dropdown-toggle",
  kineticTypeWordmark: ".kinetic-type-wordmark",
  searchToggle: ".primary-nav-ns__search-icon .search-toggle",
  searchInputContainer: ".search-input-container",
  searchInput: ".search-input-container input",
};

/**
 * Class names used for toggling state.
 */
export const CLASSNAMES = {
  navOpen: "primary-nav-ns-open",
  hidden: "hidden",
  hiddenWordmark: "hidden-wordmark",
  searchOpen: "search-open",
  searchOpenBackdrop: "search-open-backdrop",
  open: "open",
  active: "active",
};

/**
 * Configuration constants for behavior.
 */
export const TRANSITION_DURATION = 300;
export const DROPDOWN_DELAY = 200;
export const DESKTOP_BREAKPOINT = 1024;

/**
 * Cross-module coordination.
 *
 * Using explicit custom events keeps search/nav decoupled while still allowing
 * each feature to react to the other opening.
 */
export const EVENTS = {
  primaryNavWillOpen: "primaryNav:willOpen",
  searchWillOpen: "primaryNav:searchWillOpen",
};
