import { CLASSNAMES, EVENTS, SELECTORS } from "./config.js";

const SEARCH_TOP_CUSTOM_PROPERTY = "--primary-nav-search-top";

/**
 * Controls the open/close state for the primary-nav search drawer.
 */
class PrimaryNavSearchDrawerController {
  /**
   * @param {{ searchToggleEls: HTMLElement[], searchInputContainerEl: HTMLElement, searchInputEl: HTMLInputElement, primaryNavEl?: HTMLElement | null }} options
   */
  constructor({
    searchToggleEls,
    searchInputContainerEl,
    searchInputEl,
    primaryNavEl = null,
  }) {
    this.searchToggleEls = searchToggleEls;
    this.searchInputContainerEl = searchInputContainerEl;
    this.searchInputEl = searchInputEl;
    this.primaryNavEl = primaryNavEl;
    this.openerEl = null;
    this.backdropEl = this.ensureBackdrop();
    this.handleViewportChange = this.handleViewportChange.bind(this);
  }

  isOpen() {
    return this.searchInputContainerEl.classList.contains(
      CLASSNAMES.searchOpen,
    );
  }

  /**
   * @param {HTMLElement | null} openerEl - The control that opened search,
   *   which takes focus back when search closes.
   */
  open(openerEl = null) {
    if (this.isOpen()) return;

    // Let other modules close themselves first (ex: mobile nav).
    document.dispatchEvent(new CustomEvent(EVENTS.searchWillOpen));

    this.openerEl = openerEl;
    this.updateSearchTop();
    this.setTogglesOpen(true);
    this.searchInputContainerEl.classList.add(CLASSNAMES.searchOpen);
    this.updateDrawerHeight();
    this.searchInputContainerEl.setAttribute("aria-expanded", "true");
    this.searchInputContainerEl.setAttribute("aria-hidden", "false");
    this.searchInputContainerEl.removeAttribute("inert");
    this.addViewportListeners();
    this.searchInputEl.focus({ preventScroll: true });

    // Re-measure after open classes/listeners settle so pushdown layout is reflected.
    requestAnimationFrame(() => {
      if (!this.isOpen()) return;

      this.updateSearchTop();
      this.updateDrawerHeight();
    });
  }

  close() {
    if (!this.isOpen()) return;
    this.removeViewportListeners();
    this.setTogglesOpen(false);
    this.searchInputContainerEl.classList.remove(CLASSNAMES.searchOpen);
    this.searchInputContainerEl.style.maxHeight = null;
    this.searchInputContainerEl.setAttribute("aria-expanded", "false");
    this.searchInputContainerEl.setAttribute("aria-hidden", "true");
    this.searchInputContainerEl.setAttribute("inert", "");
  }

  /**
   * @param {HTMLElement | null} openerEl
   */
  toggle(openerEl = null) {
    if (this.isOpen()) {
      this.close();
      return;
    }
    this.open(openerEl);
  }

  setTogglesOpen(isOpen) {
    this.searchToggleEls.forEach((toggleEl) => {
      toggleEl.classList.toggle(CLASSNAMES.searchOpen, isOpen);
      toggleEl.setAttribute("aria-expanded", String(isOpen));
    });
  }

  /**
   * Returns focus to the control that opened search. The drawer's Search row
   * is gone once the drawer closes, so focus falls back to the first search
   * toggle still shown, then to the menu button.
   */
  restoreFocus() {
    const isShown = (el) =>
      el?.isConnected &&
      !el.closest("[hidden]") &&
      getComputedStyle(el).display !== "none";
    const menuButtonEl = this.primaryNavEl?.querySelector(SELECTORS.menuButton);
    const focusEl = [this.openerEl, ...this.searchToggleEls, menuButtonEl].find(
      isShown,
    );

    focusEl?.focus({ preventScroll: true });
  }

  /**
   * Ensures a backdrop element exists adjacent to the search drawer.
   *
   * @returns {HTMLElement | null}
   */
  ensureBackdrop() {
    const parentEl = this.searchInputContainerEl.parentNode;
    if (!parentEl) return null;

    const existingBackdrop = parentEl.querySelector(
      `.${CLASSNAMES.searchOpenBackdrop}`,
    );
    if (existingBackdrop) return existingBackdrop;

    const backdropEl = document.createElement("div");
    backdropEl.classList.add(CLASSNAMES.searchOpenBackdrop);
    parentEl.insertBefore(backdropEl, this.searchInputContainerEl);
    return backdropEl;
  }

  updateDrawerHeight() {
    this.searchInputContainerEl.style.maxHeight =
      this.searchInputContainerEl.scrollHeight + "px";
  }

  updateSearchTop() {
    if (!this.primaryNavEl) return;

    const navBottom = this.primaryNavEl.getBoundingClientRect().bottom;
    const searchTop = Math.max(0, Math.round(navBottom));

    document.documentElement.style.setProperty(
      SEARCH_TOP_CUSTOM_PROPERTY,
      `${searchTop}px`,
    );
  }

  handleViewportChange() {
    if (!this.isOpen()) return;

    this.updateSearchTop();
    this.updateDrawerHeight();
  }

  addViewportListeners() {
    window.addEventListener("resize", this.handleViewportChange);
    window.addEventListener("scroll", this.handleViewportChange, {
      passive: true,
    });
  }

  removeViewportListeners() {
    window.removeEventListener("resize", this.handleViewportChange);
    window.removeEventListener("scroll", this.handleViewportChange);
  }
}

/**
 * Initializes the search input toggle functionality, toggling visibility from
 * the nav's search controls: the desktop search button and the drawer's
 * Search row.
 */
export function initSearchToggle() {
  const searchToggleEls = [
    ...document.querySelectorAll(SELECTORS.searchToggle),
  ];
  const searchInputContainerEl = document.querySelector(
    SELECTORS.searchInputContainer,
  );
  const searchInputEl = document.querySelector(SELECTORS.searchInput);
  const primaryNavEl = document.querySelector(SELECTORS.primaryNav);

  if (!searchToggleEls.length || !searchInputContainerEl || !searchInputEl) {
    return;
  }

  const searchDrawer = new PrimaryNavSearchDrawerController({
    searchToggleEls,
    searchInputContainerEl,
    searchInputEl,
    primaryNavEl,
  });

  const closeAndRestoreFocus = () => {
    searchDrawer.close();
    searchDrawer.restoreFocus();
  };

  // If a nav menu is about to open, close search first.
  document.addEventListener(EVENTS.primaryNavWillOpen, () => {
    searchDrawer.close();
  });

  searchToggleEls.forEach((searchToggleEl) => {
    searchToggleEl.addEventListener("click", (e) => {
      e.preventDefault();
      searchDrawer.toggle(searchToggleEl);
    });
  });

  searchInputEl.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    e.preventDefault();
    closeAndRestoreFocus();
  });

  if (searchDrawer.backdropEl) {
    searchDrawer.backdropEl.addEventListener("click", closeAndRestoreFocus);
  }

  document.body.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (!searchDrawer.isOpen()) return;
    e.preventDefault();
    closeAndRestoreFocus();
  });
}
