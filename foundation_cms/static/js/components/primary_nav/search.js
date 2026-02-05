import { CLASSNAMES, EVENTS, SELECTORS } from "./config.js";

/**
 * Controls the open/close state for the primary-nav search drawer.
 */
class PrimaryNavSearchDrawerController {
  /**
   * @param {{ searchToggleEl: HTMLElement, searchInputContainerEl: HTMLElement, searchInputEl: HTMLInputElement }} options
   */
  constructor({ searchToggleEl, searchInputContainerEl, searchInputEl }) {
    this.searchToggleEl = searchToggleEl;
    this.searchInputContainerEl = searchInputContainerEl;
    this.searchInputEl = searchInputEl;
    this.backdropEl = this.ensureBackdrop();
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

    this.searchToggleEl.classList.add(CLASSNAMES.searchOpen);
    this.searchInputContainerEl.classList.add(CLASSNAMES.searchOpen);
    this.searchInputContainerEl.style.maxHeight =
      this.searchInputContainerEl.scrollHeight + "px";
    this.searchInputContainerEl.setAttribute("aria-expanded", "true");
    this.searchInputEl.focus({ preventScroll: true });
  }

  close() {
    if (!this.isOpen()) return;
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

  if (!searchToggleEl || !searchInputContainerEl || !searchInputEl) return;

  const searchDrawer = new PrimaryNavSearchDrawerController({
    searchToggleEl,
    searchInputContainerEl,
    searchInputEl,
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
