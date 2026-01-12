import {
  CLASSNAMES,
  DESKTOP_BREAKPOINT,
  DROPDOWN_DELAY,
  EVENTS,
  SELECTORS,
  TRANSITION_DURATION,
} from "./config.js";

export { initSearchToggle } from "./search.js";

class PrimaryNavDrawerController {
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

class PrimaryNavDropdownController {
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

function closeAllOpenDropdownsExcept(currentMenuEl) {
  document
    .querySelectorAll(`${SELECTORS.menuItem}.${CLASSNAMES.open}`)
    .forEach((openMenuEl) => {
      if (currentMenuEl && openMenuEl === currentMenuEl) return;
      const dropdownEl = openMenuEl.querySelector(SELECTORS.dropdown);
      const toggleEl = openMenuEl.querySelector(SELECTORS.toggle);
      if (!dropdownEl || !toggleEl) return;
      new PrimaryNavDropdownController({
        menuEl: openMenuEl,
        dropdownEl,
        toggleEl,
      }).close();
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
  dropdowns.forEach((dropdown) => {
    const toggle = document.createElement("div");
    const menu = dropdown.parentElement;
    const anchor = menu.querySelector("a");

    // Assign a pseudo random id to the dropdown in order to link it with the toggle via aria-controls.
    const dropdownId =
      dropdown.id || `dropdown-${Math.random().toString(36).slice(2, 8)}`;
    dropdown.id = dropdownId;

    // Mobile toggle
    toggle.classList.add(SELECTORS.toggle.replace(".", ""));

    toggle.setAttribute("role", "button");
    toggle.setAttribute("tabindex", "0");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", dropdownId);
    dropdown.setAttribute("aria-hidden", "true");
    dropdown.setAttribute("inert", "");

    anchor.insertAdjacentElement("afterend", toggle);

    toggle.addEventListener("click", () => {
      const dropdownController = new PrimaryNavDropdownController({
        menuEl: menu,
        dropdownEl: dropdown,
        toggleEl: toggle,
      });

      if (dropdownController.isOpen()) {
        dropdownController.close();
        return;
      }

      closeAllOpenDropdownsExcept(menu);
      dropdownController.open();
    });

    toggle.addEventListener("keydown", (e) => {
      if (e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault();

      const dropdownController = new PrimaryNavDropdownController({
        menuEl: menu,
        dropdownEl: dropdown,
        toggleEl: toggle,
      });

      if (dropdownController.isOpen()) {
        dropdownController.close();
        return;
      }

      closeAllOpenDropdownsExcept(menu);
      dropdownController.open();
    });

    // Desktop nav mouse enter/leave events with debounce
    let showTimeout, hideTimeout;

    menu.addEventListener("mouseenter", () => {
      if (window.innerWidth < DESKTOP_BREAKPOINT) return;
      clearTimeout(hideTimeout);
      showTimeout = setTimeout(() => {
        new PrimaryNavDropdownController({
          menuEl: menu,
          dropdownEl: dropdown,
          toggleEl: toggle,
        }).open();
      }, DROPDOWN_DELAY);
    });

    menu.addEventListener("mouseleave", () => {
      if (window.innerWidth < DESKTOP_BREAKPOINT) return;
      clearTimeout(showTimeout);
      hideTimeout = setTimeout(() => {
        new PrimaryNavDropdownController({
          menuEl: menu,
          dropdownEl: dropdown,
          toggleEl: toggle,
        }).close();
      }, DROPDOWN_DELAY);
    });
  });

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
