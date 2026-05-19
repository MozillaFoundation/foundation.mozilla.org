/**
 * Shared selectors, class names, and tuning values for the Gallery Hub UI.
 *
 * Keeping these symbols centralized lets the template, SCSS, and JS stay in
 * sync as the landing, project carousel, modal overlays, and media slideshow
 * continue to evolve across tickets.
 *
 * @module galleryHubConfig
 */

/**
 * DOM selectors for the page-level Gallery Hub controller.
 *
 * @type {Object<string, string>}
 */
export const GALLERY_HUB_SELECTORS = {
  root: "[data-gallery-hub]",
  enter: "[data-gallery-hub-enter]",
  project: "[data-gallery-hub-project]",
  previous: "[data-gallery-hub-previous]",
  next: "[data-gallery-hub-next]",
  projectMarker: "[data-gallery-hub-project-marker]",
  modalLayer: "[data-gallery-hub-modal-layer]",
  modal: "[data-gallery-hub-modal]",
  modalScrollable: "[data-gallery-hub-modal-scrollable]",
  modalToggle: "[data-gallery-hub-modal-toggle]",
  modalClose: "[data-gallery-hub-modal-close]",
  projectListItem: "[data-gallery-hub-project-list-item]",
  projectListItemShell: "[data-gallery-hub-project-list-item-shell]",
  projectListSlot: "[data-gallery-hub-project-list-slot]",
  filterSlot: "[data-gallery-hub-filter-slot]",
};

/**
 * State classes applied by the Gallery Hub JS modules.
 *
 * @type {Object<string, string>}
 */
export const GALLERY_HUB_CLASSES = {
  intro: "gallery-hub--intro",
  introEntering: "gallery-hub--intro-entering",
  mobileCompact: "gallery-hub--mobile-compact",
  mobileShort: "gallery-hub--mobile-short",
  modalClosing: "gallery-hub-modal--closing",
  modalOpen: "gallery-hub--modal-open",
  projectActive: "gallery-hub-project--active",
  projectMarkerActive: "gallery-hub__project-marker--active",
  projectView: "gallery-hub--project-view",
};

/**
 * DOM selectors for each project's media slideshow.
 *
 * @type {Object<string, string>}
 */
export const GALLERY_HUB_SLIDESHOW_SELECTORS = {
  root: "[data-gallery-hub-slideshow]",
  slide: "[data-gallery-hub-slide]",
  previous: "[data-gallery-hub-slide-previous]",
  next: "[data-gallery-hub-slide-next]",
};

/**
 * State classes applied to slideshow slides and dots.
 *
 * @type {Object<string, string>}
 */
export const GALLERY_HUB_SLIDESHOW_CLASSES = {
  active: "is-active",
  afterActive: "is-after-active",
  beforeActive: "is-before-active",
};

/**
 * Gallery Hub view modes.
 *
 * @type {{intro: string, project: string}}
 */
export const GALLERY_HUB_VIEW_MODES = {
  intro: "intro",
  project: "project",
};

/**
 * CSS custom property updated with the available viewport height.
 *
 * @type {string}
 */
export const GALLERY_HUB_VIEWPORT_PROPERTY = "--gallery-hub-viewport-height";

/**
 * CSS custom property updated with the Gallery Hub offset from the real viewport.
 *
 * The gallery stage starts below the page header; CSS uses this value to center
 * intro artwork against the actual viewport rather than the reduced stage box.
 *
 * @type {string}
 */
export const GALLERY_HUB_VIEWPORT_OFFSET_PROPERTY =
  "--gallery-hub-viewport-offset";

/**
 * Duration for the first-load intro collage animation.
 *
 * JS removes the entering class after this timeout so the animation only plays
 * on initial page load, not when users navigate back to the intro state.
 *
 * @type {number}
 */
export const GALLERY_HUB_INTRO_ENTERING_DURATION = 1200;

/**
 * Duration for modal exit animations before hidden state is applied.
 *
 * @type {number}
 */
export const GALLERY_HUB_MODAL_CLOSE_DURATION = 220;

/**
 * Legacy deep link stripped on load so the JS-controlled experience starts at
 * the top of the Gallery Hub.
 *
 * @type {string}
 */
export const GALLERY_HUB_LEGACY_PROJECTS_HASH = "#gallery-hub-projects";

/**
 * Class used to lock page scrolling while the Gallery Hub owns navigation.
 *
 * @type {string}
 */
export const GALLERY_HUB_SCROLL_LOCK_CLASS = "gallery-hub-scroll-locked";

/**
 * Minimum wheel/touch delta before treating the gesture as project navigation.
 *
 * @type {number}
 */
export const GALLERY_HUB_SCROLL_THRESHOLD = 28;

/**
 * Minimum delay between project-carousel scroll transitions.
 *
 * @type {number}
 */
export const GALLERY_HUB_SCROLL_COOLDOWN = 650;

/**
 * Keyboard keys that map to vertical project navigation.
 *
 * @type {Set<string>}
 */
export const GALLERY_HUB_SCROLL_KEYS = new Set([
  "ArrowDown",
  "ArrowUp",
  "PageDown",
  "PageUp",
]);
