/**
 * Css selectors for primary navigation elements.
 */
export const SELECTORS = {
  primaryNav: "[data-primary-nav]",
  panelTrigger: "[data-nav-panel]",
  panel: ".mzf-c-nav__panel",
  panelReveal: ".mzf-c-nav__panel-reveal",
  panelInner: ".mzf-c-nav__panel-inner",
  panelStage: ".mzf-c-nav__panel-stage",
  panelContent: "[data-nav-panel-content]",
  menuButton: ".mzf-c-nav__menu",
  drawer: ".mzf-c-nav__drawer",
  drawerReveal: ".mzf-c-nav__drawer-reveal",
  drawerInner: ".mzf-c-nav__drawer-inner",
  disclosure: ".mzf-c-mega-menu__disclosure",
  disclosureSummary: ".mzf-c-mega-menu__summary",
  disclosureReveal: ".mzf-c-mega-menu__reveal",
  kineticTypeWordmark: ".kinetic-type-wordmark",
  searchToggle: "[data-primary-nav-search-toggle]",
  searchInputContainer: ".search-input-container",
  searchInput: ".search-input-container input",
};

/**
 * Class names used for toggling state. The `mzf-c-` names are LP's Nav and
 * Mega menu modifiers (cosmos/blocks/sections/_nav.scss, _mega-menu.scss).
 */
export const CLASSNAMES = {
  panelOpen: "mzf-c-nav__panel--open",
  panelClosing: "mzf-c-nav__panel--closing",
  contentActive: "mzf-c-nav__panel-content--active",
  contentSwapOut: "mzf-c-nav__panel-content--swap-out",
  contentSwapIn: "mzf-c-nav__panel-content--swap-in",
  switching: "mzf-c-nav--switching",
  swapActive: "mzf-c-nav--swap-active",
  drawerOpen: "mzf-c-nav--drawer-open",
  drawerClosing: "mzf-c-nav__drawer--closing",
  disclosureClosing: "mzf-c-mega-menu__disclosure--closing",
  logoHidden: "primary-nav-ns--logo-hidden",
  searchOpen: "search-open",
  searchOpenBackdrop: "search-open-backdrop",
};

/**
 * LP's mobile boundary, `size.breakpoint.mobile` (48rem). The CSS swaps the
 * desktop panels for the drawer here; the script closes both when crossing it.
 */
export const MOBILE_MEDIA_QUERY = "(max-width: 48rem)";

/**
 * Motion custom properties the script reads, with LP's defaults as fallbacks.
 */
export const MOTION = {
  collapseDuration: ["--mzf-motion-duration-index-cards-collapse", 400],
  collapseStartDelay: ["--mzf-nav-panel-collapse-start-delay", 55],
  swapDuration: ["--mzf-nav-panel-swap-duration", 250],
  collapseEase: [
    "--mzf-nav-panel-collapse-ease",
    "cubic-bezier(0.16, 1, 0.3, 1)",
  ],
  disclosureExpandDuration: ["--mzf-mega-menu-disclosure-expand-duration", 500],
  disclosureCollapseDuration: [
    "--mzf-mega-menu-disclosure-collapse-duration",
    400,
  ],
  disclosureContentOutDuration: [
    "--mzf-mega-menu-disclosure-content-out-duration",
    200,
  ],
  disclosureCollapseStartDelay: [
    "--mzf-mega-menu-disclosure-collapse-start-delay",
    55,
  ],
  disclosureExpandEase: [
    "--mzf-mega-menu-disclosure-expand-ease",
    "cubic-bezier(0.16, 1, 0.3, 1)",
  ],
};

/**
 * Cross-module coordination.
 *
 * Using explicit custom events keeps search/nav decoupled while still allowing
 * each feature to react to the other opening.
 */
export const EVENTS = {
  primaryNavWillOpen: "primaryNav:willOpen",
  searchWillOpen: "primaryNav:searchWillOpen",
  closeMenus: "primaryNav:closeMenus",
};
