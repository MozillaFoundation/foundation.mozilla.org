import {
  CLASSNAMES,
  DESKTOP_BREAKPOINT,
  DROPDOWN_DELAY,
  EVENTS,
  SELECTORS,
  TRANSITION_DURATION,
} from "./config.js";

const dropdownControllers = new WeakMap();

/**
 * Gets a cached dropdown controller for a menu, creating it if needed.
 *
 * @param {{ menuEl: HTMLElement, dropdownEl: HTMLElement, toggleEl: HTMLElement }} options
 * @returns {PrimaryNavDropdownController}
 */
function getDropdownController({ menuEl, dropdownEl, toggleEl }) {
  const existing = dropdownControllers.get(menuEl);
  if (existing) return existing;

  const controller = new PrimaryNavDropdownController({
    menuEl,
    dropdownEl,
    toggleEl,
  });
  dropdownControllers.set(menuEl, controller);
  return controller;
}

function closeDropdownMenu(menuEl) {
  const existing = dropdownControllers.get(menuEl);
  if (existing) {
    existing.close();
    return;
  }

  const dropdownEl = menuEl.querySelector(SELECTORS.dropdown);
  const toggleEl = menuEl.querySelector(SELECTORS.toggle);
  if (!dropdownEl || !toggleEl) return;
  new PrimaryNavDropdownController({ menuEl, dropdownEl, toggleEl }).close();
}

/**
 * Controls the open/close state of the mobile primary nav drawer.
 */
class PrimaryNavDrawerController {
  /**
   * @param {{ navEl: HTMLElement, hamburgerEl: HTMLElement }} options
   */
  constructor({ navEl, hamburgerEl }) {
    this.navEl = navEl;
    this.hamburgerEl = hamburgerEl;
  }

  isOpen() {
    return this.navEl.classList.contains(CLASSNAMES.open);
  }

  open() {
    if (this.isOpen()) return;
    this.navEl.classList.add(CLASSNAMES.open);
    this.hamburgerEl.classList.add(CLASSNAMES.active);
    document.body.classList.add(CLASSNAMES.navOpen);
  }

  close() {
    if (!this.isOpen()) return;
    this.navEl.classList.remove(CLASSNAMES.open);
    this.hamburgerEl.classList.remove(CLASSNAMES.active);
    setTimeout(() => {
      document.body.classList.remove(CLASSNAMES.navOpen);
    }, TRANSITION_DURATION);
  }

  toggle() {
    if (this.isOpen()) {
      this.close();
      return;
    }

    document.dispatchEvent(new CustomEvent(EVENTS.primaryNavWillOpen));
    this.open();
  }
}

/**
 * Controls the open/close state of a single primary-nav dropdown.
 */
class PrimaryNavDropdownController {
  /**
   * @param {{ menuEl: HTMLElement, dropdownEl: HTMLElement, toggleEl: HTMLElement }} options
   */
  constructor({ menuEl, dropdownEl, toggleEl }) {
    this.menuEl = menuEl;
    this.dropdownEl = dropdownEl;
    this.toggleEl = toggleEl;
  }

  isOpen() {
    return this.menuEl.classList.contains(CLASSNAMES.open);
  }

  open() {
    if (this.isOpen()) return;
    this.menuEl.classList.add(CLASSNAMES.open);
    this.dropdownEl.style.maxHeight = this.dropdownEl.scrollHeight + "px";
    this.dropdownEl.setAttribute("aria-hidden", "false");
    this.dropdownEl.removeAttribute("inert");
    this.toggleEl.setAttribute("aria-expanded", "true");
  }

  close() {
    if (!this.isOpen()) return;
    this.menuEl.classList.remove(CLASSNAMES.open);
    this.dropdownEl.style.maxHeight = null;
    this.dropdownEl.setAttribute("aria-hidden", "true");
    this.dropdownEl.setAttribute("inert", "");
    this.toggleEl.setAttribute("aria-expanded", "false");
  }
}

/**
 * Closes all currently-open dropdown menus, except (optionally) a specific menu.
 *
 * @param {HTMLElement | null} currentMenuEl
 */
function closeAllOpenDropdownsExcept(currentMenuEl) {
  document
    .querySelectorAll(`${SELECTORS.menuItem}.${CLASSNAMES.open}`)
    .forEach((openMenuEl) => {
      if (currentMenuEl && openMenuEl === currentMenuEl) return;
      closeDropdownMenu(openMenuEl);
    });
}

/**
 * Initializes a single primary-nav dropdown menu.
 * Adds mobile toggle behavior plus desktop hover behavior.
 *
 * @param {Element} dropdownEl
 */
function initPrimaryNavDropdown(dropdownEl) {
  if (!(dropdownEl instanceof HTMLElement)) return;

  const toggle = document.createElement("div");
  const menu = dropdownEl.parentElement;
  const anchor = menu?.querySelector("a");

  if (!menu || !anchor) return;

  // Assign a pseudo random id to the dropdown in order to link it with the toggle via aria-controls.
  const dropdownId =
    dropdownEl.id || `dropdown-${Math.random().toString(36).slice(2, 8)}`;
  dropdownEl.id = dropdownId;

  // Mobile toggle
  toggle.classList.add(SELECTORS.toggle.replace(".", ""));

  toggle.setAttribute("role", "button");
  toggle.setAttribute("tabindex", "0");
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", dropdownId);
  dropdownEl.setAttribute("aria-hidden", "true");
  dropdownEl.setAttribute("inert", "");

  anchor.insertAdjacentElement("afterend", toggle);

  const dropdownController = getDropdownController({
    menuEl: menu,
    dropdownEl: dropdownEl,
    toggleEl: toggle,
  });

  const toggleDropdown = () => {
    if (dropdownController.isOpen()) {
      dropdownController.close();
      return;
    }

    closeAllOpenDropdownsExcept(menu);
    dropdownController.open();
  };

  toggle.addEventListener("click", () => {
    toggleDropdown();
  });

  toggle.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" && e.key !== " ") return;
    e.preventDefault();

    toggleDropdown();
  });

  // Desktop nav mouse enter/leave events with debounce
  let showTimeout, hideTimeout;

  menu.addEventListener("mouseenter", () => {
    if (window.innerWidth < DESKTOP_BREAKPOINT) return;
    clearTimeout(hideTimeout);
    showTimeout = setTimeout(() => {
      dropdownController.open();
    }, DROPDOWN_DELAY);
  });

  menu.addEventListener("mouseleave", () => {
    if (window.innerWidth < DESKTOP_BREAKPOINT) return;
    clearTimeout(showTimeout);
    hideTimeout = setTimeout(() => {
      dropdownController.close();
    }, DROPDOWN_DELAY);
  });
}

/**
 * Initializes the primary navigation component.
 * Sets up mobile and desktop navigation behaviors, including dropdowns and hamburger menu.
 */
export function initPrimaryNav() {
  const hamburger = document.querySelector(SELECTORS.hamburger);
  const nav = document.querySelector(SELECTORS.primaryNav);
  const dropdowns = document.querySelectorAll(SELECTORS.dropdown);

  if (!nav || !hamburger) return;

  const navDrawer = new PrimaryNavDrawerController({
    navEl: nav,
    hamburgerEl: hamburger,
  });

  // If search intends to open, close mobile nav first.
  document.addEventListener(EVENTS.searchWillOpen, () => {
    navDrawer.close();
  });

  // Mobile nav
  hamburger.addEventListener("click", () => {
    navDrawer.toggle();
  });

  // Menu dropdowns
  dropdowns.forEach(initPrimaryNavDropdown);

  // Esc key closes all menus
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeAllOpenDropdownsExcept(null);
    }
  });
}

/**
 * Initializes the visibility of the wordmark based on scroll position.
 * Hides the navigation wordmark when the kinetic type wordmark is visible in the viewport.
 */
export function initWordmarkVisibilityOnScroll() {
  const nav = document.querySelector(SELECTORS.primaryNav);
  const grid = document.querySelector(SELECTORS.primaryNavGrid);
  const wordmark = document.querySelector(SELECTORS.wordmark);
  const kineticTypeWordmark = document.querySelector(
    SELECTORS.kineticTypeWordmark,
  );

  if (!nav || !grid || !wordmark) return;

  // If kineticTypeWordmark is not present, always show the wordmark
  if (!kineticTypeWordmark) {
    wordmark.classList.remove(CLASSNAMES.hidden);
    grid.classList.remove(CLASSNAMES.hiddenWordmark);
    return;
  }

  const navHeight = nav.offsetHeight;

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        wordmark.classList.add(CLASSNAMES.hidden);
        grid.classList.add(CLASSNAMES.hiddenWordmark);
      } else {
        wordmark.classList.remove(CLASSNAMES.hidden);
        grid.classList.remove(CLASSNAMES.hiddenWordmark);
      }
    },
    {
      root: null, // viewport
      rootMargin: `-${navHeight}px  0px 0px 0px`,
      threshold: 0.01, // as soon as even 1% is visible/invisible
    },
  );

  observer.observe(kineticTypeWordmark);
}
