import { CLASSNAMES, EVENTS, SELECTORS } from "./config.js";

const SEARCH_TOP_CUSTOM_PROPERTY = "--primary-nav-search-top";

/**
 * Controls the open/close state for the primary-nav search drawer.
 */
class PrimaryNavSearchDrawerController {
  /**
   * @param {{ searchToggleEl: HTMLElement, searchInputContainerEl: HTMLElement, searchInputEl: HTMLInputElement, primaryNavEl?: HTMLElement | null }} options
   */
  constructor({
    searchToggleEl,
    searchInputContainerEl,
    searchInputEl,
    primaryNavEl = null,
  }) {
    this.searchToggleEl = searchToggleEl;
    this.searchInputContainerEl = searchInputContainerEl;
    this.searchInputEl = searchInputEl;
    this.primaryNavEl = primaryNavEl;
    this.backdropEl = this.ensureBackdrop();
    this.handleViewportChange = this.handleViewportChange.bind(this);
  }

  isOpen() {
    return this.searchInputContainerEl.classList.contains(
      CLASSNAMES.searchOpen,
    );
  }

  open() {
    if (this.isOpen()) return;

    // Let other modules close themselves first (ex: mobile nav).
    document.dispatchEvent(new CustomEvent(EVENTS.searchWillOpen));

    this.updateSearchTop();
    this.searchToggleEl.classList.add(CLASSNAMES.searchOpen);
    this.searchInputContainerEl.classList.add(CLASSNAMES.searchOpen);
    this.updateDrawerHeight();
    this.searchInputContainerEl.setAttribute("aria-expanded", "true");
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
    this.searchToggleEl.classList.remove(CLASSNAMES.searchOpen);
    this.searchInputContainerEl.classList.remove(CLASSNAMES.searchOpen);
    this.searchInputContainerEl.style.maxHeight = null;
    this.searchInputContainerEl.setAttribute("aria-expanded", "false");
  }

  toggle() {
    if (this.isOpen()) {
      this.close();
      return;
    }
    this.open();
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
 * Initializes the search input toggle functionality, toggling visibility on search icon click.
 */
export function initSearchToggle() {
  const searchToggleEl = document.querySelector(SELECTORS.searchToggle);
  const searchInputContainerEl = document.querySelector(
    SELECTORS.searchInputContainer,
  );
  const searchInputEl = document.querySelector(SELECTORS.searchInput);
  const primaryNavEl = document.querySelector(SELECTORS.primaryNav);

  if (!searchToggleEl || !searchInputContainerEl || !searchInputEl) return;

  const searchDrawer = new PrimaryNavSearchDrawerController({
    searchToggleEl,
    searchInputContainerEl,
    searchInputEl,
    primaryNavEl,
  });

  // If the mobile nav is about to open, close search first.
  document.addEventListener(EVENTS.primaryNavWillOpen, () => {
    searchDrawer.close();
  });

  searchToggleEl.addEventListener("click", (e) => {
    e.preventDefault();
    searchDrawer.toggle();
  });

  searchInputEl.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    e.preventDefault();
    searchDrawer.close();
    searchToggleEl.focus({ preventScroll: true });
  });

  if (searchDrawer.backdropEl) {
    searchDrawer.backdropEl.addEventListener("click", () => {
      searchDrawer.close();
      searchToggleEl.focus({ preventScroll: true });
    });
  }

  document.body.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (!searchDrawer.isOpen()) return;
    e.preventDefault();
    searchDrawer.close();
    searchToggleEl.focus({ preventScroll: true });
  });
}
